#!/bin/bash
echo "================================================"
echo "  Compilation JAR Waveshare CAN Tool"
echo "================================================"

echo "Creation des repertoires..."
mkdir -p build
mkdir -p dist

echo "Compilation du code Java..."
javac -d build -cp "lib/jSerialComm-2.10.4.jar" src/main/java/com/waveshare/cantool/*.java

if [ $? -ne 0 ]; then
    echo "Erreur de compilation!"
    exit 1
fi

echo "Creation du fichier JAR avec librairie serie..."
cd build
jar cfm ../dist/WaveshareCANTool.jar ../src/main/resources/META-INF/MANIFEST.MF com/waveshare/cantool/*.class
cd ..
# Ajout de la librairie serie dans le JAR
jar uf dist/WaveshareCANTool.jar -C lib jSerialComm-2.10.4.jar

if [ $? -ne 0 ]; then
    echo "Erreur de creation JAR!"
    cd ..
    exit 1
fi

cd ..
echo "================================================"
echo "  Compilation terminee avec succes!"
echo "================================================"
echo "Fichier JAR cree: dist/WaveshareCANTool.jar"
echo ""
echo "Pour executer:"
echo "java -jar dist/WaveshareCANTool.jar"
echo ""
echo "Ou double-cliquer sur le fichier JAR"
echo ""
