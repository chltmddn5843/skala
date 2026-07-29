const fs=require('node:fs/promises');
const path=require('node:path');

const COMMON='제공된 데이터만 사용하고 없는 사실이나 수치를 만들지 않는다. 정보가 부족하면 추가 확인 필요라고 표시한다. 정확한 고장 날짜나 실제 고장확률을 주장하지 않는다. 결과는 한국어로 작성하고 최종 안전 판단과 일정 승인은 사람에게 남긴다.';
const FILES={facility:'facilities.csv',failure:'failures.csv',passenger:'passengers.csv',staff:'workers.csv',special:'special-rules.csv',rules:'work-rules.csv'};

function parseCSV(text){text=text.replace(/^\uFEFF/,'');const rows=[];let row=[],cell='',quoted=false;for(let i=0;i<text.length;i++){const c=text[i],n=text[i+1];if(c==='"'&&quoted&&n==='"'){cell+='"';i++;}else if(c==='"')quoted=!quoted;else if(c===','&&!quoted){row.push(cell);cell='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&n==='\n')i++;row.push(cell);if(row.some(v=>v!==''))rows.push(row);row=[];cell='';}else cell+=c;}if(cell||row.length){row.push(cell);rows.push(row);}const headers=rows.shift()||[];return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h.trim(),(values[i]||'').trim()])));}
function toCSV(rows,columns){const quote=v=>`"${String(v??'').replaceAll('"','""')}"`;return [columns,...rows.map(row=>columns.map(c=>row[c]))].map(row=>row.map(quote).join(',')).join('\n');}
function select(rows,columns){return rows.map(row=>Object.fromEntries(columns.map(c=>[c,row[c]])));}
async function readData(){const base=path.join(process.cwd(),'data');const entries=await Promise.all(Object.entries(FILES).map(async([key,file])=>[key,parseCSV(await fs.readFile(path.join(base,file),'utf8'))]));return Object.fromEntries(entries);}
function cleanModelName(value){return String(value||'gpt-4o-mini').replace(/^openai\//,'');}
function parseModelJSON(text){const cleaned=String(text||'').trim().replace(/^```(?:json)?\s*/i,'').replace(/\s*```$/,'');return JSON.parse(cleaned);}
async function callModel(system,user,{json=false}={}){
  const key=process.env.OPENAI_API_KEY;if(!key)throw new Error('OPENAI_API_KEY가 설정되지 않았습니다.');
  const body={model:cleanModelName(process.env.OPENAI_MODEL_NAME),temperature:0.1,messages:[{role:'system',content:system},{role:'user',content:user}]};
  if(json)body.response_format={type:'json_object'};
  const response=await fetch('https://api.openai.com/v1/chat/completions',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json'},body:JSON.stringify(body)});
  const payload=await response.json();if(!response.ok)throw new Error(payload?.error?.message||`OpenAI API 오류 (${response.status})`);
  return {text:payload.choices?.[0]?.message?.content||'',usage:payload.usage||{},requestId:response.headers.get('x-request-id')||''};
}
function monthRange(month){if(!/^\d{4}-\d{2}$/.test(month))throw new Error('계획월 형식은 YYYY-MM이어야 합니다.');const [year,m]=month.split('-').map(Number);const end=new Date(Date.UTC(year,m,0)).getUTCDate();return {start:`${month}-01`,end:`${month}-${String(end).padStart(2,'0')}`};}
function validatePlan(plan,month){const sections=['emergency_schedule','special_schedule','self_schedule','staffing_plan'];for(const key of sections)if(!Array.isArray(plan[key]))throw new Error(`AI 결과에 ${key} 목록이 없습니다.`);for(const key of sections.slice(0,3)){for(const row of plan[key])if(!String(row.점검일||'').startsWith(`${month}-`))throw new Error(`${key}에 계획월 밖의 날짜가 있습니다.`);}for(const row of plan.staffing_plan)if(row.계획월!==month||!String(row.운영일||'').startsWith(`${month}-`))throw new Error('인력운영안의 계획월 또는 운영일이 올바르지 않습니다.');return plan;}

module.exports=async function handler(req,res){
  if(req.method!=='POST')return res.status(405).json({error:'POST 요청만 허용됩니다.'});
  if(process.env.DASHBOARD_ACCESS_TOKEN&&req.headers['x-dashboard-token']!==process.env.DASHBOARD_ACCESS_TOKEN)return res.status(401).json({error:'대시보드 접근 토큰이 필요합니다.'});
  try{
    const referenceDate=String(req.body?.referenceDate||new Date().toISOString().slice(0,10));
    const planMonth=String(req.body?.planMonth||'2026-08');const range=monthRange(planMonth);const d=await readData();
    const machineFacility=toCSV(select(d.facility,['시설ID','설치연도','마지막점검일','현재상태','실시간이상여부','최근이상감지시각','실내외','최근환경']),['시설ID','설치연도','마지막점검일','현재상태','실시간이상여부','최근이상감지시각','실내외','최근환경']);
    const passengerFacility=toCSV(select(d.facility,['시설ID','역명','위치','대체이동수단']),['시설ID','역명','위치','대체이동수단']);
    const priorityFacility=toCSV(select(d.facility,['시설ID','역명','다음자체점검예정일','현재상태','실시간이상여부','최근이상감지시각','실내외','최근환경']),['시설ID','역명','다음자체점검예정일','현재상태','실시간이상여부','최근이상감지시각','실내외','최근환경']);
    const [machine,passenger]=await Promise.all([
      callModel(`당신은 기계 고장 분석 담당자다. 이용객 데이터는 판단하지 않는다. ${COMMON}`,`기준일 ${referenceDate}. 아래 두 CSV만 사용해 시설별 기계위험(높음/중간/낮음), 위험점수(0~100 상대비교), 반복고장, 중점점검항목, 근거, 신뢰도를 JSON 배열로 작성하라. 최근 90일 고장, 같은 고장 반복, 조치 후 재발, 운행중단, 현재 이상을 확인하고 환경은 원인으로 단정하지 말라.\n[시설정보]\n${machineFacility}\n[고장이력]\n${toCSV(d.failure,Object.keys(d.failure[0]||{}))}`,{json:true}),
      callModel(`당신은 지하철 이용객 패턴 분석 담당자다. 기계 고장과 매출은 판단하지 않는다. ${COMMON}`,`아래 CSV만 사용해 시설별 이용객영향, 혼잡시간, 점검 추천시간, 비추천시간과 근거를 JSON 배열로 작성하라.\n[시설정보]\n${passengerFacility}\n[이용객패턴]\n${toCSV(d.passenger,Object.keys(d.passenger[0]||{}))}`,{json:true})
    ]);
    const priority=await callModel(`당신은 점검 종류·우선순위 담당자다. 각 시설을 정확히 하나의 점검으로 분류한다. 우선순위는 긴급점검 > 수시특별점검 > 자체점검이다. ${COMMON}`,`계획월 ${planMonth}. 긴급점검은 실시간 이상 Y 또는 점검대기와 반복고장, 수시특별점검은 계획월·환경·특별기준 일치, 자체점검은 다음자체점검예정일과 소모품 관리로 판단하라. 시설별 점검종류, 우선순위, 완료기한, 중점점검항목, 점검주체, 분류근거, 추가확인사항을 JSON 배열로 작성하라.\n[분류용 시설정보]\n${priorityFacility}\n[특별점검기준]\n${toCSV(d.special,Object.keys(d.special[0]||{}))}\n[기계분석]\n${machine.text}\n[이용객분석]\n${passenger.text}`,{json:true});
    const schedule=await callModel(`당신은 현장 점검 일정 관리자다. 같은 소속조 2명, 3교대, 가능지역·가능일·근무시간·자격·피로도·이동시간을 지킨다. ${COMMON}`,`계획기간은 ${range.start}~${range.end}이다. 점검일과 운영일은 YYYY-MM-DD로 작성하라. 긴급·수시특별·자체 일정을 분리하고, 점검이 있는 각 날짜마다 staffing_plan에 주간·석간·야간 3개 행과 실제 긴급대기조를 작성하라. 같은 조를 점검과 대기에 동시에 배정하지 말라. 반드시 다음 최상위 키만 가진 JSON 객체로 반환하라: emergency_schedule, special_schedule, self_schedule, staffing_plan. 일정 행 필드: 우선순위,점검일,시간,시설ID,역명,담당조,인원수,중점점검항목,완료기한,점검주체,자격확인,이용객고려,선정이유,피로도확인,승인상태. 인력 행 필드: 계획월,운영일,교대,배정점검조수,긴급대기조,필요인원,판단근거,확인사항. 해당하지 않는 선택 필드는 빈 문자열로 써라.\n[점검분류]\n${priority.text}\n[이용객분석]\n${passenger.text}\n[작업자정보]\n${toCSV(d.staff,Object.keys(d.staff[0]||{}))}\n[운영규칙]\n${toCSV(d.rules,Object.keys(d.rules[0]||{}))}`,{json:true});
    const plan=validatePlan(parseModelJSON(schedule.text),planMonth);
    const usage=[machine,passenger,priority,schedule].reduce((sum,item)=>sum+(item.usage.total_tokens||0),0);
    return res.status(200).json({data:plan,meta:{referenceDate,planMonth,model:cleanModelName(process.env.OPENAI_MODEL_NAME),totalTokens:usage,requestIds:[machine.requestId,passenger.requestId,priority.requestId,schedule.requestId].filter(Boolean)}});
  }catch(error){console.error(error);return res.status(500).json({error:error.message||'AI 일정 생성 중 오류가 발생했습니다.'});}
};
