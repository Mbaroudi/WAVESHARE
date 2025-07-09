#!/bin/bash
echo "================================================"
echo "  Compilation JAR Waveshare CAN Tool - Real Serial"
echo "================================================"

echo "Creation des repertoires..."
mkdir -p build
mkdir -p dist

echo "Compilation du code Java avec support serial..."
javac -d build -cp "lib/jSerialComm-2.10.4.jar" src/main/java/com/waveshare/cantool/WaveshareCANTool.java

if [ $? -ne 0 ]; then
    echo "Erreur de compilation!"
    exit 1
fi

echo "Creation du fichier JAR avec librairie serie..."
cd build
jar cfm ../dist/WaveshareCANTool.jar ../src/main/resources/META-INF/MANIFEST.MF com/waveshare/cantool/*.class
cd ..

# Extraction et integration de la librairie serie
echo "Integration de la librairie serie..."
mkdir -p temp_lib
cd temp_lib
jar -xf ../lib/jSerialComm-2.10.4.jar
cd ..
jar -uf dist/WaveshareCANTool.jar -C temp_lib .
rm -rf temp_lib

echo "================================================"
echo "  Compilation terminee avec succes!"
echo "================================================"
echo "Fichier JAR cree: dist/WaveshareCANTool.jar"
echo ""
echo "Pour executer:"
echo "java -jar dist/WaveshareCANTool.jar"
echo ""
echo "MAINTENANT AVEC SUPPORT SERIAL REEL!"
echo ""