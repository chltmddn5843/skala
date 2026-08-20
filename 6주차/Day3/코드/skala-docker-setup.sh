#!/usr/bin/env bash

# ==================================================================
# Docker Desktop 사전 설치 스크립트 (Apple Silicon / macOS)  — v2
#
# 과정 시작 전, 수강생 노트북에서 미리 실행하여
# Docker Desktop 설치를 완료해 두기 위한 스크립트입니다.
#
# v1 대비 추가된 사전 점검 항목:
#   - macOS 최소 버전 확인
#   - Rosetta로 실행된 터미널인지 확인 (아키텍처 오탐지 방지)
#   - 디스크 여유 공간 확인
#   - Homebrew 표준 경로 외 위치에 설치된 경우 안내
#   - brew update 수행 (오래된 cask 정의로 인한 실패 방지)
#   - Docker.app이 brew 관리 밖에서 이미 설치된 경우 감지 및 안내
#   - 설치 후 PATH 미반영 상황 안내
#
# 실행 방법:
#   chmod +x skala-docker-setup-v2.sh
#   ./skala-docker-setup-v2.sh
# ==================================================================

set -uo pipefail
# 주의: -e 는 의도적으로 사용하지 않습니다.
# 아래 각 단계는 실패 시 자체적으로 안내 메시지를 출력하고
# exit 여부를 명시적으로 판단하도록 작성되어 있습니다.

TOTAL_STEPS=8
STEP=0

step_header() {
  STEP=$((STEP + 1))
  echo ""
  echo "[$STEP/$TOTAL_STEPS] $1"
}

echo "=================================================="
echo " Docker Desktop 사전 설치 스크립트 (v2)"
echo "=================================================="
echo "이 스크립트는 과정 시작 전 미리 실행해 두는 것을 권장합니다."
echo "총 $TOTAL_STEPS 단계로 진행됩니다."
echo "=================================================="

# --------------------------------------------------
# [1/8] macOS 버전 확인
#   - Docker Desktop은 최신 macOS 일부 버전만 지원합니다.
#   - 너무 오래된 macOS에서는 brew install 자체는 성공해도
#     앱 실행이 되지 않는 경우가 있어 사전에 안내합니다.
# --------------------------------------------------
step_header "macOS 버전 확인"

MACOS_VERSION="$(sw_vers -productVersion 2>/dev/null || echo "unknown")"
echo "  - 감지된 macOS 버전: $MACOS_VERSION"

MACOS_MAJOR="$(echo "$MACOS_VERSION" | cut -d. -f1)"

if [[ "$MACOS_MAJOR" =~ ^[0-9]+$ ]] && [[ "$MACOS_MAJOR" -lt 12 ]]; then
  echo "  ⚠️  macOS 12(Monterey) 미만입니다. 최신 Docker Desktop은"
  echo "     이 버전에서 정상 동작하지 않을 수 있습니다."
  echo "     계속 진행할 수는 있지만, 문제가 발생하면 강사에게 문의해 주세요."
else
  echo "  ✅ macOS 버전 확인 완료."
fi

# --------------------------------------------------
# [2/8] 시스템 아키텍처 확인 (Rosetta 오탐지 방지)
#   - 터미널이 "Rosetta로 열기"로 설정되어 있으면
#     Apple Silicon Mac에서도 uname -m 이 x86_64로 나옵니다.
#   - sysctl.proc_translated 값으로 실제 Rosetta 여부를 다시 확인합니다.
# --------------------------------------------------
step_header "시스템 아키텍처 확인"

ARCH="$(uname -m)"
echo "  - uname -m 결과: $ARCH"

IS_TRANSLATED="$(sysctl -n sysctl.proc_translated 2>/dev/null || echo "0")"

if [[ "$ARCH" == "x86_64" && "$IS_TRANSLATED" == "1" ]]; then
  echo "  ⚠️  이 터미널은 Rosetta로 실행되고 있습니다."
  echo "     실제로는 Apple Silicon Mac일 가능성이 높습니다."
  echo "     (터미널 앱 정보 → '로제타를 사용하여 열기' 체크 해제 후 재실행 권장)"
  echo "  ℹ️  일단 실제 하드웨어 기준(arm64)으로 진행합니다."
  ARCH="arm64"
fi

if [[ "$ARCH" == "arm64" ]]; then
  echo "  ✅ Apple Silicon Mac으로 확인되었습니다."
  BREW_PREFIX="/opt/homebrew"
else
  echo "  ℹ️  Intel(x86_64) Mac으로 확인되었습니다."
  BREW_PREFIX="/usr/local"
fi
echo "  - Homebrew 예상 설치 경로: $BREW_PREFIX"

# --------------------------------------------------
# [3/8] 디스크 여유 공간 확인
#   - Docker Desktop 설치 + 이미지 다운로드를 고려하면
#     최소 10GB 이상의 여유 공간을 권장합니다.
# --------------------------------------------------
step_header "디스크 여유 공간 확인"

AVAILABLE_GB="$(df -g / 2>/dev/null | tail -1 | awk '{print $4}')"

if [[ -n "${AVAILABLE_GB:-}" ]] && [[ "$AVAILABLE_GB" =~ ^[0-9]+$ ]]; then
  echo "  - 루트 디스크(/) 여유 공간: 약 ${AVAILABLE_GB}GB"
  if [[ "$AVAILABLE_GB" -lt 10 ]]; then
    echo "  ⚠️  여유 공간이 10GB 미만입니다. 설치 및 실습 도중"
    echo "     디스크 부족 문제가 발생할 수 있으니 미리 정리해 주세요."
  else
    echo "  ✅ 디스크 여유 공간이 충분합니다."
  fi
else
  echo "  ℹ️  디스크 여유 공간을 자동으로 확인하지 못했습니다. 수동으로 확인해 주세요."
fi

# --------------------------------------------------
# [4/8] Homebrew 설치 여부 확인
#   - 표준 경로(/opt/homebrew, /usr/local) 외에 PATH 상에
#     brew가 잡혀 있는 경우도 함께 확인합니다.
# --------------------------------------------------
step_header "Homebrew 설치 여부 확인"

if [[ -x "$BREW_PREFIX/bin/brew" ]]; then
  eval "$("$BREW_PREFIX/bin/brew" shellenv)"
fi

if ! command -v brew >/dev/null 2>&1; then
  # 표준 경로에 없다면, PATH 어딘가에 이미 설치되어 있는지 마지막으로 한 번 더 확인
  if command -v brew >/dev/null 2>&1; then
    echo "  ✅ PATH 상에서 brew를 찾았습니다: $(command -v brew)"
  else
    echo "  ❌ Homebrew가 설치되어 있지 않습니다."
    echo ""
    echo "  Docker Desktop은 Homebrew를 통해 설치하므로, 먼저 Homebrew를"
    echo "  설치한 뒤 이 스크립트를 다시 실행해 주세요."
    echo ""
    echo "  Homebrew 설치 명령 (터미널에 직접 붙여넣기):"
    echo '    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
  fi
else
  echo "  ✅ Homebrew가 이미 설치되어 있습니다. ($(command -v brew))"
  echo "  - 버전: $(brew --version | head -n 1)"
fi

# --------------------------------------------------
# [5/8] Homebrew 업데이트
#   - cask 정의가 오래되어 있으면 최신 Docker Desktop을
#     찾지 못하는 경우가 있어 설치 전 업데이트합니다.
# --------------------------------------------------
step_header "Homebrew 업데이트"

echo "  ⬇️  brew update 실행 중... (네트워크 상황에 따라 다소 시간이 걸릴 수 있습니다)"
if brew update >/dev/null 2>&1; then
  echo "  ✅ Homebrew 업데이트 완료"
else
  echo "  ⚠️  brew update 중 일부 경고가 발생했습니다. 설치는 계속 진행합니다."
fi

# --------------------------------------------------
# [6/8] Docker Desktop 설치 여부 확인
#   - brew로 관리 중인지 확인
#   - brew 관리 밖에서 이미 Docker.app이 설치되어 있는 경우
#     (예: 공식 홈페이지에서 dmg로 직접 설치한 경우)를 별도로 감지합니다.
#     이 상태에서 그대로 brew install을 실행하면 설치가 실패하므로
#     미리 안내하고 스크립트를 종료합니다.
# --------------------------------------------------
step_header "Docker Desktop 설치 여부 확인"

BREW_MANAGED=0
if brew list --cask docker >/dev/null 2>&1; then
  BREW_MANAGED=1
fi

APP_EXISTS=0
if [[ -d "/Applications/Docker.app" ]]; then
  APP_EXISTS=1
fi

if [[ "$BREW_MANAGED" -eq 1 ]]; then
  echo "  ⏭️  Docker Desktop이 이미 Homebrew로 설치되어 있습니다. 설치 단계를 건너뜁니다."
  DOCKER_ALREADY_INSTALLED=1
elif [[ "$APP_EXISTS" -eq 1 ]]; then
  echo "  ⚠️  /Applications/Docker.app 이 이미 존재하지만, Homebrew가"
  echo "     이 설치를 관리하고 있지 않습니다 (예: 공식 홈페이지에서 dmg로 직접 설치)."
  echo ""
  echo "  이 상태에서는 'brew install --cask docker' 실행 시 충돌로 실패할 수 있습니다."
  echo "  아래 두 가지 방법 중 하나를 선택해 주세요."
  echo ""
  echo "   방법 A) 이미 설치된 Docker Desktop을 그대로 사용"
  echo "           → 이 스크립트를 종료하고, 터미널에서 'open -a Docker' 로 실행"
  echo ""
  echo "   방법 B) Homebrew 관리로 재설치하고 싶다면"
  echo "           → 기존 Docker.app을 휴지통으로 이동한 뒤 이 스크립트를 다시 실행"
  echo ""
  echo "  일단 이번 실행에서는 설치 단계를 건너뛰고 다음 단계로 진행합니다."
  DOCKER_ALREADY_INSTALLED=1
else
  echo "  ℹ️  Docker Desktop이 아직 설치되어 있지 않습니다. 설치를 진행합니다."
  DOCKER_ALREADY_INSTALLED=0
fi

# --------------------------------------------------
# [7/8] Docker Desktop 설치 진행
#   - GUI 앱 설치 과정에서 macOS 관리자 비밀번호 입력창이 뜰 수 있습니다.
#     (권한 상승이 필요한 네트워킹/파일시스템 헬퍼 설치, 최초 1회)
#   - 화면 공유/원격 환경에서는 이 창이 다른 창 뒤에 숨을 수 있으니
#     스크립트가 멈춘 것처럼 보이면 다른 창을 확인해 주세요.
# --------------------------------------------------
step_header "Docker Desktop 설치 진행"

if [[ "$DOCKER_ALREADY_INSTALLED" -eq 0 ]]; then
  echo "  ⬇️  brew install --cask docker 실행 중..."
  echo "     (다운로드 용량이 커서 몇 분 정도 걸릴 수 있습니다)"
  echo "  ℹ️  진행 중 macOS 관리자 비밀번호 입력창이 뜰 수 있습니다."
  echo "     (화면 공유 환경이라면 다른 창 뒤에 가려져 있을 수 있으니 확인해 주세요)"
  if brew install --cask docker; then
    echo "  ✅ Docker Desktop 설치 완료"
  else
    echo "  ❌ Docker Desktop 설치 실패"
    echo "     - 네트워크 상태를 확인한 뒤 스크립트를 다시 실행해 보세요."
    echo "     - 회사/학교 관리 Mac(MDM)인 경우 관리자 권한 문제일 수 있습니다."
    echo "     - 계속 실패한다면 'brew doctor' 로 Homebrew 상태를 점검해 보세요."
    exit 1
  fi
else
  echo "  ⏭️  이미 설치되어 있어 이번 단계는 건너뜁니다."
fi

# --------------------------------------------------
# [8/8] 설치 결과 확인 및 최초 실행 안내
# --------------------------------------------------
step_header "설치 결과 확인"

if [[ -d "/Applications/Docker.app" ]]; then
  echo "  ✅ /Applications/Docker.app 확인됨"
else
  echo "  ⚠️  /Applications/Docker.app 을 찾지 못했습니다. 설치 로그를 다시 확인해 주세요."
fi

if command -v docker >/dev/null 2>&1; then
  echo "  - docker CLI 위치: $(command -v docker)"
  docker --version 2>/dev/null || echo "  ℹ️  docker CLI는 있지만, Docker 데몬이 아직 실행되지 않은 것 같습니다."
else
  echo "  ℹ️  docker 명령을 아직 찾을 수 없습니다."
  echo "     새 터미널을 열거나, 아래 안내대로 앱을 먼저 실행한 뒤 다시 확인해 주세요."
fi

echo ""
echo "=================================================="
echo " 설치 스크립트 종료 — 마무리 안내"
echo "=================================================="
echo "1) Docker Desktop은 GUI 앱을 한 번 직접 실행해야 데몬(엔진)이 시작됩니다."
echo "   실행 명령:"
echo "     open -a Docker"
echo ""
echo "2) 앱 최초 실행 시 다음 절차가 나타날 수 있습니다."
echo "   - 라이선스 동의(License Agreement) 확인"
echo "   - 관리자 비밀번호 입력 (권한 상승이 필요한 네트워킹/파일시스템 헬퍼 설치)"
echo "   - 메뉴바에 고래 모양 아이콘이 뜨고, 아이콘이 안정적으로 표시되면 데몬 준비 완료"
echo ""
echo "3) 데몬이 켜진 뒤 아래 명령으로 정상 동작을 확인하세요."
echo "     docker --version"
echo "     docker compose version"
echo "     docker run hello-world"
echo ""
echo "4) 새 터미널에서 'docker' 명령을 찾지 못한다면 터미널을 재시작해 보세요."
echo "=================================================="