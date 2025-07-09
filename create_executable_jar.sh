#!/bin/bash
echo "================================================================"
echo "  Creating Executable JAR - Waveshare CAN Tool"
echo "================================================================"

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build_final
rm -rf dist_final
rm -f WaveshareCANTool-executable.jar

# Create directories
mkdir -p build_final
mkdir -p dist_final

echo "Compiling Java source code..."
javac -cp "lib/jSerialComm-2.10.4.jar" -d build_final src/main/java/com/waveshare/cantool/WaveshareCANTool.java

if [ $? -ne 0 ]; then
    echo "❌ Compilation failed!"
    exit 1
fi

echo "Extracting serial library..."
cd build_final
jar -xf ../lib/jSerialComm-2.10.4.jar
cd ..

echo "Creating executable JAR..."
jar cfm dist_final/WaveshareCANTool-executable.jar src/main/resources/META-INF/MANIFEST.MF -C build_final .

if [ $? -ne 0 ]; then
    echo "❌ JAR creation failed!"
    exit 1
fi

# Copy to main directory for easy access
cp dist_final/WaveshareCANTool-executable.jar ./WaveshareCANTool-executable.jar

echo "================================================================"
echo "  ✅ Executable JAR created successfully!"
echo "================================================================"
echo "File: WaveshareCANTool-executable.jar"
echo "Size: $(ls -lh WaveshareCANTool-executable.jar | awk '{print $5}')"
echo ""
echo "To run:"
echo "  java -jar WaveshareCANTool-executable.jar"
echo ""
echo "Or use the platform-specific launchers:"
echo "  Windows: WaveshareCANTool.bat"
echo "  Linux/macOS: ./WaveshareCANTool.sh"
echo ""