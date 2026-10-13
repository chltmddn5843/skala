#!/usr/bin/env bash
# 템플릿의 __ID__ 를 본인 식별자로 바꿔 실제 파일을 만든다.
#
#   export ID=<본인 식별자>      # 소문자와 숫자만 (예: sk001)
#   ./render.sh
#
# 만들어지는 이름은 장표에 적힌 것과 같다: front.conf · ing-$ID.yaml 등
set -euo pipefail
: "${ID:?export ID=<본인 식별자> 를 먼저 설정한다}"
if ! printf '%s' "$ID" | grep -Eq '^[a-z][a-z0-9]{1,14}$'; then
  echo "ID 는 소문자로 시작하고 소문자와 숫자만 사용한다 (예: sk001). 지금 값: $ID" >&2
  exit 1
fi
cd "$(dirname "$0")"
sed "s/__ID__/${ID}/g" templates/front.conf > front.conf
echo "  front.conf"
for f in ing netpol pvc pod sts rbac; do
  sed "s/__ID__/${ID}/g" "templates/${f}.yaml" > "${f}-${ID}.yaml"
  echo "  ${f}-${ID}.yaml"
done
echo "완료. 장표의 명령은 이 폴더에서 실행한다."
