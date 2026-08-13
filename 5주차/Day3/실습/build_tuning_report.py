from pathlib import Path
from html import escape


OUT = Path(__file__).with_name("SQL_쿼리_튜닝_테스트_보고서.html")


sections = [
    {
        "no": 2,
        "title": "인덱스 없는 함수 조건 쿼리 튜닝",
        "goal": "lower(email) 및 lower(status) 조건이 일반 B-tree 인덱스를 사용하지 못하는 사유를 확인하고, 표현식 인덱스와 쿼리 재작성을 비교한다.",
        "before": [
            ("2-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM hr.employees
WHERE lower(email) = 'user1234@corp.com';""", """Seq Scan on employees (actual time=4.816..4.818 rows=0)
  Filter: lower(email) = 'user1234@corp.com'
  Rows Removed by Filter: 50000
  Buffers: shared hit=786
Planning Time: 0.065 ms
Execution Time: 4.834 ms"""),
            ("2-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM hr.employees
WHERE lower(status) = 'inactive';""", """Seq Scan on employees (actual time=0.002..4.017 rows=2522)
  Filter: lower(status) = 'inactive'
  Rows Removed by Filter: 47478
  Buffers: shared hit=786
Planning Time: 0.011 ms
Execution Time: 4.059 ms"""),
        ],
        "ddl": """CREATE INDEX idx_employees_lower_email
ON hr.employees (lower(email));

CREATE INDEX idx_employees_status
ON hr.employees (status);

ANALYZE hr.employees;""",
        "after": [
            ("2-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM hr.employees
WHERE lower(email) = 'user1234@corp.com';""", """Index Scan using idx_employees_lower_email (actual time=0.010..0.010 rows=0)
  Index Cond: lower(email) = 'user1234@corp.com'
  Buffers: shared read=3
Planning Time: 0.066 ms
Execution Time: 0.016 ms"""),
            ("2-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM hr.employees
WHERE status = 'INACTIVE';""", """Index Scan using idx_employees_status (actual time=0.010..0.387 rows=2522)
  Index Cond: status = 'INACTIVE'
  Buffers: shared hit=757 read=4
Planning Time: 0.009 ms
Execution Time: 0.430 ms"""),
        ],
        "comparison": [("2-1 lower(email)", "Seq Scan", "4.834 ms", "Index Scan", "0.016 ms", "99.7%"), ("2-2 status", "Seq Scan", "4.059 ms", "Index Scan", "0.430 ms", "89.4%")],
        "discussion": "email은 대소문자 무시 검색이 필요하므로 lower(email) 표현식 인덱스가 적합하다. status는 값이 이미 대문자로 정규화되어 있어 컬럼에서 lower()를 제거하는 편이 낫다. ACTIVE는 95%라 인덱스 이점이 적고, 5%인 INACTIVE 조회로 비교해야 효과가 명확하다.",
        "best": "이메일은 lower(email) 표현식 인덱스, status는 입력값을 정규화하고 status = 'INACTIVE'로 직접 비교한다.",
    },
    {
        "no": 3,
        "title": "LIKE 접미사 검색 쿼리 튜닝",
        "goal": "'%@gmail.com'처럼 선행 와일드카드가 기존 email B-tree 인덱스를 사용하지 못하는 문제를 역문자열 표현식 인덱스로 개선한다.",
        "before": [
            ("3-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE email LIKE '%@gmail.com';""", """Seq Scan on employees (actual time=0.004..2.062 rows=1438)
  Filter: email LIKE '%@gmail.com'
  Rows Removed by Filter: 48562
  Buffers: shared hit=786
Planning Time: 0.052 ms
Execution Time: 2.087 ms"""),
            ("3-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT employee_id, email FROM hr.employees
WHERE email LIKE '%@outlook.com';""", """Seq Scan on employees (actual time=0.002..1.961 rows=5953)
  Filter: email LIKE '%@outlook.com'
  Rows Removed by Filter: 44047
  Buffers: shared hit=786
Planning Time: 0.012 ms
Execution Time: 2.053 ms"""),
        ],
        "ddl": """CREATE INDEX idx_employees_reverse_email
ON hr.employees (reverse(email) text_pattern_ops);

ANALYZE hr.employees;""",
        "after": [
            ("3-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE reverse(email) LIKE reverse('@gmail.com') || '%';""", """Bitmap Heap Scan on employees (actual time=0.139..0.463 rows=1438)
  Heap Blocks: exact=655
  -> Bitmap Index Scan on idx_employees_reverse_email
     (actual time=0.108 rows=1438)
  Buffers: shared hit=655 read=10
Planning Time: 2.153 ms
Execution Time: 0.492 ms"""),
            ("3-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT employee_id, email FROM hr.employees
WHERE reverse(email) LIKE reverse('@outlook.com') || '%';""", """Bitmap Heap Scan on employees (actual time=0.219..1.034 rows=5953)
  -> Bitmap Index Scan on idx_employees_reverse_email
     (actual time=0.184 rows=5953)
  Buffers: shared hit=787 read=30
Planning Time: 0.019 ms
Execution Time: 1.128 ms"""),
        ],
        "comparison": [("3-1 gmail", "Seq Scan", "2.087 ms", "Bitmap Index", "0.492 ms", "76.4%"), ("3-2 outlook", "Seq Scan", "2.053 ms", "Bitmap Index", "1.128 ms", "45.1%")],
        "discussion": "접미사 검색은 문자열을 뒤집으면 접두사 검색으로 바뀐다. gmail은 2.9%로 선택도가 높아 효과가 크고, outlook은 11.9%를 반환해 테이블 방문 비용이 커서 개선폭이 작다. 특정 도메인 하나만을 위한 partial index보다 여러 도메인에 재사용 가능한 역문자열 인덱스를 선택했다.",
        "best": "reverse(email) text_pattern_ops 인덱스를 생성하고 reverse(email) LIKE reverse('접미사') || '%'로 재작성한다.",
    },
    {
        "no": 4,
        "title": "ORDER BY와 필터 결합 쿼리 튜닝",
        "goal": "최근 365일 이내에 입사한 ACTIVE 직원을 연봉 내림차순으로 100명만 반환할 때 전체 스캔과 top-N 정렬을 제거한다.",
        "before": [
            ("4-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE hire_date >= CURRENT_DATE - INTERVAL '365 days'
  AND status = 'ACTIVE'
ORDER BY salary DESC LIMIT 100;""", """Limit (actual time=4.496..4.501 rows=100)
  -> Sort: salary DESC; top-N heapsort, Memory: 47kB
     -> Seq Scan on employees (actual time=0.002..4.188 rows=9412)
        Rows Removed by Filter: 40588
        Buffers: shared hit=786
Planning Time: 0.255 ms
Execution Time: 4.506 ms"""),
            ("4-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT employee_id, email, hire_date, salary
FROM hr.employees
WHERE status = 'ACTIVE'
  AND hire_date >= CURRENT_DATE - INTERVAL '365 days'
ORDER BY salary DESC LIMIT 100;""", """Limit (actual time=4.670..4.675 rows=100)
  -> Sort: salary DESC; top-N heapsort, Memory: 36kB
     -> Seq Scan on employees (actual time=0.002..4.216 rows=9412)
        Rows Removed by Filter: 40588
        Buffers: shared hit=786
Planning Time: 0.018 ms
Execution Time: 4.678 ms"""),
        ],
        "ddl": """CREATE INDEX idx_employees_active_salary
ON hr.employees (salary DESC)
WHERE status = 'ACTIVE';

ANALYZE hr.employees;""",
        "after": [
            ("4-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE hire_date >= CURRENT_DATE - INTERVAL '365 days'
  AND status = 'ACTIVE'
ORDER BY salary DESC LIMIT 100;""", """Limit (actual time=0.007..0.147 rows=100)
  -> Index Scan using idx_employees_active_salary
     Filter: hire_date >= CURRENT_DATE - '365 days'
     Rows Removed by Filter: 383
     Buffers: shared hit=481 read=2
Planning Time: 0.067 ms
Execution Time: 0.151 ms"""),
            ("4-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT employee_id, email, hire_date, salary
FROM hr.employees
WHERE status = 'ACTIVE'
  AND hire_date >= CURRENT_DATE - INTERVAL '365 days'
ORDER BY salary DESC LIMIT 100;""", """Limit (actual time=0.002..0.073 rows=100)
  -> Index Scan using idx_employees_active_salary
     Filter: hire_date >= CURRENT_DATE - '365 days'
     Rows Removed by Filter: 383
     Buffers: shared hit=483
Planning Time: 0.013 ms
Execution Time: 0.076 ms"""),
        ],
        "comparison": [("4-1 SELECT *", "Seq Scan + Sort", "4.506 ms", "Partial Index", "0.151 ms", "96.6%"), ("4-2 선택 컬럼", "Seq Scan + Sort", "4.678 ms", "Partial Index", "0.076 ms", "98.4%")],
        "discussion": "hire_date는 범위 조건이므로 (status, hire_date, salary) 순서로는 salary 정렬을 완전히 제거하기 어렵다. ACTIVE만 포함한 salary DESC partial index를 이용하면 연봉 순으로 읽으며 hire_date를 확인해 100건에서 바로 멈춘다. 실제로 후보 9,412건 정렬이 사라지고 483건만 확인했다.",
        "best": "ORDER BY salary DESC + LIMIT 100을 먼저 지원하는 ACTIVE partial index로 정렬을 제거한다. 최근 입사자 비율이 크게 바뀌면 인덱스 설계를 재측정한다.",
    },
    {
        "no": 5,
        "title": "OR 조건 쿼리 튜닝",
        "goal": "department_id = 10 OR job_id IN (3,4,5) 조건의 전체 스캔을 각 조건의 인덱스와 BitmapOr로 변환하고 UNION 재작성과 비교한다.",
        "before": [
            ("5-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE department_id = 10
   OR job_id IN (3,4,5);""", """Seq Scan on employees (actual time=0.002..2.183 rows=4085)
  Filter: department_id = 10 OR job_id = ANY('{3,4,5}')
  Rows Removed by Filter: 45915
  Buffers: shared hit=786
Planning Time: 0.012 ms
Execution Time: 2.243 ms"""),
            ("5-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*) FROM hr.employees
WHERE department_id = 10
   OR job_id IN (3,4,5);""", """Aggregate (actual time=2.100 rows=1)
  -> Seq Scan on employees (actual time=0.001..2.021 rows=4085)
     Rows Removed by Filter: 45915
     Buffers: shared hit=786
Planning Time: 0.016 ms
Execution Time: 2.103 ms"""),
        ],
        "ddl": """CREATE INDEX idx_employees_department_id
ON hr.employees (department_id);

CREATE INDEX idx_employees_job_id
ON hr.employees (job_id);

ANALYZE hr.employees;""",
        "after": [
            ("5-1", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees
WHERE department_id = 10
   OR job_id IN (3,4,5);""", """Bitmap Heap Scan on employees (actual time=0.112..0.432 rows=4085)
  Recheck Cond: department_id = 10 OR job_id = ANY('{3,4,5}')
  -> BitmapOr
     -> Bitmap Index Scan on idx_employees_department_id (rows=251)
     -> Bitmap Index Scan on idx_employees_job_id (rows=3855)
  Buffers: shared hit=783 read=7
Execution Time: 0.500 ms"""),
            ("5-2", """EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM hr.employees WHERE department_id = 10
UNION
SELECT * FROM hr.employees WHERE job_id IN (3,4,5);""", """HashAggregate (actual time=1.216..1.500 rows=4085)
  Group Key: employees columns (duplicate removal)
  Memory Usage: 985kB
  -> Append (actual time=0.014..0.448 rows=4106)
     -> Bitmap Index Scan: department_id (rows=251)
     -> Bitmap Index Scan: job_id (rows=3855)
Planning Time: 0.074 ms
Execution Time: 1.578 ms"""),
        ],
        "comparison": [("5-1 OR", "Seq Scan", "2.243 ms", "BitmapOr", "0.500 ms", "77.7%"), ("5-2 UNION", "Seq Scan(비교기준 5-1)", "2.243 ms", "UNION + Index", "1.578 ms", "29.6%")],
        "discussion": "OR의 양쪽 컬럼에 각각 인덱스가 있으면 PostgreSQL이 BitmapOr로 결합한다. UNION은 각 분기에서 인덱스를 사용하지만, 중복 21건을 제거하는 HashAggregate 비용으로 직접 OR보다 느렸다. UNION ALL은 중복 행으로 결과가 바뀌므로 대체하지 않았다.",
        "best": "department_id와 job_id에 각각 단일 인덱스를 생성하고 원본 OR 쿼리를 유지한다. 현재 분포에서 BitmapOr가 UNION보다 빠르고 의미도 명확하다.",
    },
]


def code_block(text):
    return f'<pre>{escape(text)}</pre>'


def test_cards(items, phase):
    blocks = []
    for label, query, result in items:
        blocks.append(f'<h3>{phase} 테스트 {label} - 쿼리</h3>{code_block(query)}')
        blocks.append(f'<h3>{phase} 테스트 {label} - 실행 결과</h3><div class="terminal"><div class="terminal-title">psql | skala_db | EXPLAIN ANALYZE</div>{code_block(result)}</div>')
    return "".join(blocks)


def comparison_table(rows):
    body = "".join(
        f"<tr><td>{escape(a)}</td><td>{escape(b)}</td><td class='num'>{escape(c)}</td><td>{escape(d)}</td><td class='num'>{escape(e)}</td><td class='num good'>{escape(f)}</td></tr>"
        for a, b, c, d, e, f in rows
    )
    return f"""<table><thead><tr><th>테스트</th><th>튜닝 전</th><th>전 시간</th><th>튜닝 후</th><th>후 시간</th><th>개선율</th></tr></thead><tbody>{body}</tbody></table>"""


parts = ["""<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>
@page { size: Letter; margin: 22mm 20mm 20mm 20mm; }
body { font-family: Apple SD Gothic Neo, Malgun Gothic, Arial, sans-serif; color:#172033; font-size:10.5pt; line-height:1.45; }
h1 { color:#153b64; font-size:22pt; margin:0 0 8pt; }
h2 { color:#1d5d8f; font-size:16pt; margin:18pt 0 7pt; border-bottom:1px solid #b9c9d8; padding-bottom:4pt; }
h3 { color:#274c69; font-size:11.5pt; margin:12pt 0 5pt; }
p { margin:0 0 7pt; }
.cover { text-align:center; padding-top:135pt; page-break-after:always; }
.cover .kicker { color:#2878b5; font-weight:bold; letter-spacing:1.5pt; }
.cover .subtitle { color:#536579; font-size:12pt; margin-top:10pt; }
.meta { margin-top:55pt; color:#68788a; }
.lead { background:#eef5fb; border-left:4px solid #2878b5; padding:10pt 12pt; margin:10pt 0 14pt; }
.section { page-break-before:always; }
pre { white-space:pre-wrap; font-family:Menlo, Consolas, monospace; font-size:8.4pt; line-height:1.38; background:#f4f6f8; border:1px solid #d9e0e6; padding:9pt; margin:4pt 0 9pt; }
.terminal { background:#eef3f7; color:#172033; border:1px solid #b9c9d8; margin-bottom:12pt; padding-bottom:1pt; }
.terminal pre { background:#eef3f7; color:#172033; border:0; margin:0; }
.terminal-title { background:#d9e6f0; color:#173f61; font-size:8pt; padding:5pt 9pt; font-weight:bold; }
table { width:100%; border-collapse:collapse; margin:7pt 0 13pt; font-size:9pt; }
th { background:#e8eef5; color:#173f61; text-align:left; padding:6pt; border:1px solid #cbd5df; }
td { padding:6pt; border:1px solid #d6dee6; vertical-align:middle; }
.num { text-align:right; white-space:nowrap; }.good { color:#08783e; font-weight:bold; }
.callout { background:#f4f8ec; border-left:4px solid #6d9637; padding:9pt 11pt; margin:8pt 0; }
.note { color:#5d6875; font-size:9pt; }
.evidence { color:#2878b5; font-weight:bold; }
ul { margin-top:4pt; }
</style></head><body>
<div class="cover"><div class="kicker">POSTGRESQL PERFORMANCE LAB</div><h1>SQL 쿼리 튜닝 테스트 보고서</h1><div class="subtitle">함수 조건·LIKE 접미사·ORDER BY·OR 조건 튜닝</div><div class="meta">Database: skala_db / Schema: hr<br>PostgreSQL 17.10 / 측정일: 2026-08-13<br>작성자: ____________________ &nbsp;&nbsp; 반: ________</div></div>
<h1>실험 개요</h1>
<div class="lead"><b>목적</b><br>1번 '사번 100 검색'은 제외하고, 2~5번 문항에 대해 튜닝 전·후 실행 계획과 실측값을 비교했다.</div>
<h2>실행 환경과 방법</h2>
<ul><li>employees: 50,000건, ACTIVE 47,478건, INACTIVE 2,522건</li><li>모든 측정: <code>EXPLAIN (ANALYZE, BUFFERS)</code></li><li>튜닝 전에 해당 실험용 인덱스를 제거하고, 튜닝 후 인덱스 생성 및 <code>ANALYZE hr.employees</code> 실행</li><li>테이블 데이터는 변경하지 않음</li></ul>
<h2>제출 형식 충족</h2><p>각 문항은 <span class="evidence">튜닝 전 쿼리 2개 + 결과 2개 + 튜닝 후 쿼리 2개 + 결과 2개</span>로, 총 8개의 증빙을 포함한다. 4개 문항 합계 32개이다.</p>
<p class="note">주의: 실행 시간은 캐시, 동시 부하, 장비에 따라 달라질 수 있다. 본 보고서는 동일 환경의 실측값과 스캔 방식 변화를 함께 판단했다.</p>"""]

for s in sections:
    parts.append(f'<div class="section"><h1>{s["no"]}. {escape(s["title"])}</h1><div class="lead"><b>테스트 목표</b><br>{escape(s["goal"])}</div>')
    parts.append('<h2>튜닝 전 테스트</h2>')
    parts.append(test_cards(s["before"], "튜닝 전"))
    parts.append('<h2>튜닝 작업 내역</h2>')
    parts.append(code_block(s["ddl"]))
    parts.append('<h2>튜닝 후 테스트</h2>')
    parts.append(test_cards(s["after"], "튜닝 후"))
    parts.append('<h2>성능 비교</h2>')
    parts.append(comparison_table(s["comparison"]))
    parts.append(f'<h2>조별 의견(논의 초안)</h2><p>{escape(s["discussion"])}</p>')
    parts.append(f'<div class="callout"><b>최적의 튜닝 Point</b><br>{escape(s["best"])}</div></div>')

parts.append("""<div class="section"><h1>종합 결론</h1>
<table><thead><tr><th>문항</th><th>병목</th><th>최적 튜닝 Point</th></tr></thead><tbody>
<tr><td>2</td><td>컬럼 함수로 인한 Seq Scan</td><td>표현식 인덱스 또는 정규화된 컬럼 직접 비교</td></tr>
<tr><td>3</td><td>선행 와일드카드</td><td>reverse(email) text_pattern_ops 표현식 인덱스</td></tr>
<tr><td>4</td><td>전체 스캔 + top-N 정렬</td><td>ACTIVE partial salary DESC 인덱스로 ORDER BY/LIMIT 조기 종료</td></tr>
<tr><td>5</td><td>OR 양쪽 컬럼 인덱스 부재</td><td>각 컬럼 단일 인덱스 + BitmapOr; 불필요한 UNION 제거</td></tr>
</tbody></table>
<h2>최종 의견</h2><p>인덱스는 무조건 추가하기보다 조건의 형태, 데이터 분포, 반환 행 수, 정렬과 LIMIT의 존재를 함께 보고 설계해야 한다. 이번 실험에서는 실행 시간뿐 아니라 Seq Scan, Sort, Rows Removed by Filter, Buffer 방문량이 줄었는지를 튜닝 성공 기준으로 삼았다.</p>
<h2>생성된 실험용 인덱스</h2><pre>idx_employees_lower_email
idx_employees_status
idx_employees_reverse_email
idx_employees_active_salary
idx_employees_department_id
idx_employees_job_id</pre>
<p class="note">제출 전 표지의 작성자와 반을 입력하고, 실제 조별 논의 내용에 맞게 '조별 의견(논의 초안)'을 보정한 후 PDF로 내보낸다.</p></div></body></html>""")

if __name__ == "__main__":
    OUT.write_text("".join(parts), encoding="utf-8")
    print(OUT)
