#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo
echo "================================================================"
echo "  🚀 Waveshare CAN Tool - Professional Configuration Suite"
echo "================================================================"
echo -e "  ${GREEN}✅ Real serial communication with hardware validation${NC}"
echo -e "  ${GREEN}✅ Advanced CAN configuration with all parameters${NC}"
echo -e "  ${GREEN}✅ JSON parameter management (save/load/apply)${NC}"
echo -e "  ${GREEN}✅ Transparent mode handling with smart fallback${NC}"
echo -e "  ${GREEN}✅ Multi-protocol support (OBD-II, J1939, ISO-TP, UDS)${NC}"
echo -e "  ${GREEN}✅ Cross-platform compatibility (Windows/Linux/macOS)${NC}"
echo "================================================================"
echo

# Check if Java is available
if ! command -v java &> /dev/null; then
    echo -e "${RED}❌ Java not found! Please install Java 8 or later.${NC}"
    echo
    echo "To install Java:"
    echo "  Ubuntu/Debian: sudo apt-get install default-jdk"
    echo "  CentOS/RHEL:   sudo yum install java-1.8.0-openjdk"
    echo "  macOS:         brew install openjdk"
    echo "  Or download from: https://www.java.com/download/"
    echo
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
echo -e "${BLUE}ℹ Java version: $JAVA_VERSION${NC}"

# Check if JAR file exists
if [ ! -f "WaveshareCANTool-executable.jar" ]; then
    echo -e "${RED}❌ WaveshareCANTool-executable.jar not found!${NC}"
    echo
    echo "Please ensure the JAR file is in the same directory as this script."
    echo "Current directory: $(pwd)"
    echo
    exit 1
fi

# Check file permissions
if [ ! -r "WaveshareCANTool-executable.jar" ]; then
    echo -e "${YELLOW}⚠ JAR file is not readable. Attempting to fix permissions...${NC}"
    chmod +r WaveshareCANTool-executable.jar
fi

echo -e "${GREEN}✅ Java found - launching application...${NC}"
echo

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JAR_FILE="$SCRIPT_DIR/WaveshareCANTool-executable.jar"

# Launch the application
java -jar "$JAR_FILE" "$@"

# Check exit code
EXIT_CODE=$?
echo

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Application closed successfully.${NC}"
else
    echo -e "${RED}❌ Application exited with error code: $EXIT_CODE${NC}"
    echo
    echo "Possible solutions:"
    echo "1. Check if you have permission to access serial ports:"
    echo "   sudo usermod -a -G dialout \$USER"
    echo "2. Verify Java installation: java -version"
    echo "3. Check if JAR file is corrupted: java -jar WaveshareCANTool-executable.jar --help"
    echo "4. Try running with more verbose output: java -jar WaveshareCANTool-executable.jar -verbose"
    echo
    exit $EXIT_CODE
fi