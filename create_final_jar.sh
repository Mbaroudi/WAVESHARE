#!/bin/bash
echo "Creating final JAR with real serial communication..."

# Create a proper JAR with class files and serial library
mkdir -p temp_jar
cp -r src/main/java/com/waveshare/cantool/*.class temp_jar/
mkdir -p temp_jar/com/waveshare/cantool/
mv temp_jar/*.class temp_jar/com/waveshare/cantool/

# Extract serial library
cd temp_jar
jar -xf ../lib/jSerialComm-2.10.4.jar
cd ..

# Create JAR with both our classes and serial library
jar cfm dist/WaveshareCANTool.jar src/main/resources/META-INF/MANIFEST.MF -C temp_jar .

# Clean up
rm -rf temp_jar

echo "JAR created successfully!"
ls -la dist/WaveshareCANTool.jar