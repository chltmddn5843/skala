const DATA_FILES={facilities:'facilities.csv',failures:'failures.csv',passengers:'passengers.csv',workers:'workers.csv',emergency:'emergency.csv',special:'special.csv',self:'self.csv',staffing:'staffing.csv'};
const state={data:{},schedules:[],edits:JSON.parse(localStorage.getItem('stepguard-edits')||'{}')};

function parseCSV(text){
  text=text.replace(/^\uFEFF/,'');const rows=[];let row=[],cell='',quoted=false;
  for(let i=0;i<text.length;i++){const c=text[i],next=text[i+1];if(c==='"'&&quoted&&next==='"'){cell+='"';i++;}else if(c==='"'){quoted=!quoted;}else if(c===','&&!quoted){row.push(cell);cell='';}else if((c==='\n'||c==='\r')&&!quoted){if(c==='\r'&&next==='\n')i++;row.push(cell);if(row.some(v=>v!==''))rows.push(row);row=[];cell='';}else cell+=c;}
  if(cell||row.length){row.push(cell);rows.push(row);}const headers=rows.shift()||[];
  return rows.map(values=>Object.fromEntries(headers.map((h,i)=>[h.trim(),(values[i]||'').trim()])));
}
async function loadData(){
  const entries=await Promise.all(Object.entries(DATA_FILES).map(async([key,file])=>{const response=await fetch(`./data/${file}`);if(!response.ok)throw new Error(`${file} 로드 실패`);return[key,parseCSV(await response.text())];}));
  state.data=Object.fromEntries(entries);state.schedules=[...tag(state.data.emergency,'긴급점검'),...tag(state.data.special,'수시특별점검'),...tag(state.data.self,'자체점검')];applyEdits();render();
}
const tag=(rows,type)=>rows.map((row,index)=>({...row,_type:type,_key:`${type}-${row.시설ID}-${index}`}));
const esc=value=>String(value??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function applyEdits(){state.schedules.forEach(row=>Object.assign(row,state.edits[row._key]||{}));}
function persist(row,field,value){row[field]=value;state.edits[row._key]={...(state.edits[row._key]||{}),[field]:value};localStorage.setItem('stepguard-edits',JSON.stringify(state.edits));renderSchedule();toast('변경사항을 브라우저에 저장했습니다.');}

function render(){
  document.querySelector('#facilityCount').textContent=state.data.facilities.length;
  document.querySelector('#emergencyCount').textContent=state.data.emergency.length;
  document.querySelector('#scheduleCount').textContent=state.schedules.length;
  document.querySelector('#workerCount').textContent=state.data.workers.length;
  fillStations();renderMix();renderSchedule();renderShifts();renderFacilities();
}
function fillStations(){const select=document.querySelector('#stationFilter');const current=select.value;const stations=[...new Set(state.schedules.map(r=>r.역명))].sort();select.innerHTML='<option value="all">전체 역</option>'+stations.map(s=>`<option value="${esc(s)}">${esc(s)}</option>`).join('');select.value=stations.includes(current)?current:'all';}
function renderMix(){const total=Math.max(state.schedules.length,1);const groups=[['긴급점검','emergency'],['수시특별점검','special'],['자체점검','self']];document.querySelector('#inspectionMix').innerHTML=groups.map(([name,cls])=>{const count=state.schedules.filter(r=>r._type===name).length;return `<div class="mix-row"><b>${name}</b><div class="bar ${cls}"><i style="width:${count/total*100}%"></i></div><span>${count}</span></div>`}).join('');}
function filteredSchedules(){const month=document.querySelector('#monthFilter').value,type=document.querySelector('#typeFilter').value,station=document.querySelector('#stationFilter').value;return state.schedules.filter(r=>(!month||r.점검일.startsWith(month))&&(type==='all'||r._type===type)&&(station==='all'||r.역명===station)).sort((a,b)=>a.점검일.localeCompare(b.점검일)||Number(a.우선순위)-Number(b.우선순위));}
function renderSchedule(){const rows=filteredSchedules();document.querySelector('#scheduleBody').innerHTML=rows.length?rows.map(row=>{const cls=row._type==='긴급점검'?'emergency':row._type==='수시특별점검'?'special':'self';return `<tr><td><span class="type-pill ${cls}">${row._type}</span></td><td><input type="date" value="${esc(row.점검일)}" data-key="${esc(row._key)}" data-field="점검일"></td><td>${esc(row.시간)}</td><td><b>${esc(row.시설ID)}</b> · ${esc(row.역명)}</td><td>${esc(row.담당조)}</td><td>${esc(row.중점점검항목)}</td><td><select data-key="${esc(row._key)}" data-field="승인상태"><option ${row.승인상태==='담당자 확인 필요'?'selected':''}>담당자 확인 필요</option><option ${row.승인상태==='승인 완료'?'selected':''}>승인 완료</option><option ${row.승인상태==='보류'?'selected':''}>보류</option></select></td></tr>`}).join(''):'<tr><td colspan="7">조건에 맞는 일정이 없습니다.</td></tr>';document.querySelectorAll('[data-key]').forEach(el=>el.addEventListener('change',()=>{const row=state.schedules.find(r=>r._key===el.dataset.key);if(row)persist(row,el.dataset.field,el.value);}));}
function renderShifts(){const meta={주간:'06:00–14:00',석간:'14:00–22:00',야간:'22:00–06:00'},fallback={주간:'D06',석간:'E06',야간:'N05'};document.querySelector('#shiftCards').innerHTML=Object.entries(meta).map(([shift,time])=>{const workers=state.data.workers.filter(w=>w.교대===shift),teams=new Set(workers.map(w=>w.소속조)).size,available=workers.filter(w=>w.현재상태==='배정가능').length;const reserves=[...new Set(state.data.staffing.filter(r=>r.교대===shift).map(r=>r.긴급대기조))].filter(Boolean).join(', ')||fallback[shift];return `<article class="shift-card"><header><h3>${shift}</h3><span class="time">${time}</span></header><div class="shift-stats"><div><span>운영 조</span><b>${teams}개</b></div><div><span>배정 가능</span><b>${available}명</b></div><div><span>대기조</span><b>${esc(reserves)}</b></div><div><span>고피로</span><b>${workers.filter(w=>w.현재피로도==='높음').length}명</b></div></div></article>`}).join('');}
function renderFacilities(){document.querySelector('#facilityCards').innerHTML=state.data.facilities.map(f=>{const failures=state.data.failures.filter(x=>x.시설ID===f.시설ID).length,alert=f.실시간이상여부==='Y'||f.현재상태!=='정상운행';return `<article class="facility-card"><header><h3>${esc(f.시설ID)} · ${esc(f.역명)}</h3><i class="state ${alert?'alert':''}"></i></header><p>${esc(f.위치)}<br>상태 ${esc(f.현재상태)} · 고장이력 ${failures}건<br>다음 자체점검 ${esc(f.다음자체점검예정일)}</p></article>`}).join('');}
function downloadCSV(){const rows=filteredSchedules();if(!rows.length)return toast('다운로드할 일정이 없습니다.');const headers=['점검종류','우선순위','점검일','시간','시설ID','역명','담당조','인원수','중점점검항목','승인상태'];const quote=v=>`"${String(v??'').replaceAll('"','""')}"`;const csv='\uFEFF'+[headers,...rows.map(r=>[r._type,...headers.slice(1).map(h=>r[h]??'')])].map(row=>row.map(quote).join(',')).join('\n');const blob=new Blob([csv],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`STEP_GUARD_${document.querySelector('#monthFilter').value}_일정.csv`;a.click();URL.revokeObjectURL(url);toast('현재 필터의 일정을 다운로드했습니다.');}
let toastTimer;function toast(message){const el=document.querySelector('#toast');el.textContent=message;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove('show'),2200);}
async function generateAIPlan(token=sessionStorage.getItem('stepguard-access-token')||'',skipConfirm=false){
  if(!skipConfirm&&!confirm('개인 OpenAI API 사용량이 발생합니다. AI 월간 일정을 생성할까요?'))return;
  const button=document.querySelector('#aiPlanBtn'),status=document.querySelector('#aiStatus');button.disabled=true;button.innerHTML='<span>✦</span> Agent 실행 중…';status.hidden=false;status.className='ai-status';status.textContent='기계 분석과 이용객 분석을 시작했습니다. 점검 분류와 일정 생성까지 잠시 기다려 주세요.';
  try{
    const response=await fetch('/api/plan',{method:'POST',headers:{'Content-Type':'application/json',...(token?{'x-dashboard-token':token}:{})},body:JSON.stringify({referenceDate:new Date().toISOString().slice(0,10),planMonth:document.querySelector('#monthFilter').value})});
    if(response.status===401&&!token){const entered=prompt('대시보드 접근 토큰을 입력하세요.');if(entered){sessionStorage.setItem('stepguard-access-token',entered);button.disabled=false;button.innerHTML='<span>✦</span> AI 일정 생성';return generateAIPlan(entered,true);}}
    const payload=await response.json();if(!response.ok)throw new Error(payload.error||'AI 일정 생성에 실패했습니다.');
    state.data.emergency=payload.data.emergency_schedule;state.data.special=payload.data.special_schedule;state.data.self=payload.data.self_schedule;state.data.staffing=payload.data.staffing_plan;
    state.schedules=[...tag(state.data.emergency,'긴급점검'),...tag(state.data.special,'수시특별점검'),...tag(state.data.self,'자체점검')];state.edits={};localStorage.removeItem('stepguard-edits');render();
    status.textContent=`AI 일정 생성 완료 · ${payload.meta.model} · 총 ${Number(payload.meta.totalTokens||0).toLocaleString()} tokens`;toast('새 AI 일정을 대시보드에 반영했습니다.');
  }catch(error){status.className='ai-status error';status.textContent=`AI 실행 오류: ${error.message}`;toast('AI 일정 생성에 실패했습니다.');}
  finally{button.disabled=false;button.innerHTML='<span>✦</span> AI 일정 생성';}
}
document.querySelector('#typeFilter').addEventListener('change',renderSchedule);document.querySelector('#stationFilter').addEventListener('change',renderSchedule);document.querySelector('#monthFilter').addEventListener('change',renderSchedule);document.querySelector('#downloadBtn').addEventListener('click',downloadCSV);document.querySelector('#aiPlanBtn').addEventListener('click',()=>generateAIPlan());
loadData().catch(error=>{console.error(error);document.querySelector('#scheduleBody').innerHTML=`<tr><td colspan="7">데이터를 불러오지 못했습니다: ${esc(error.message)}</td></tr>`;toast('데이터 로드에 실패했습니다. 로컬 서버로 실행해 주세요.');});
