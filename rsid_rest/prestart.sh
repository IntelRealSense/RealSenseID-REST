#! /usr/bin/env sh

set -eu

GREEN='\033[0;32m'
NC='\033[0m'
RED='\033[0;31m'
CYAN='\033[0;36m'
GRAY='\e[37m'

python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
app_version=$(python -c 'import app; print(".".join(map(str, app.__version_info__[:3])))')

echo ""
echo ""
printf "%b" "${GREEN}💫 Starting prestart.sh script${NC}"

echo "  Environment Summary:"
echo ""
echo "          APP VERSION: 🔑 ${app_version}"
echo "       PYTHON VERSION: 🐍 ${python_version}"
echo "                 USER: 🧑 $(whoami)"
echo "                  UID:    $(id -u)"
echo "           PYTHONPATH: 💡 ${PYTHONPATH}"
echo "    WORKING DIRECTORY: 📁 ${PWD}"
echo ""

# ❌❌❌ Loading env values will not work on Kubernetes ❌❌❌

echo ""
printf "%b" "${GREEN}✨ prestart.sh script completed${NC}"
echo ""
echo ""
