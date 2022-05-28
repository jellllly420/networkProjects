#!/bin/bash

# For more details, please visit https://google.github.io/mediapipe/

cd ~
sudo apt-get update && sudo apt-get install -y build-essential git python zip adb openjdk-8-jdk python3 python3-pip
pip3 install numpy

# DO NOT install go with apt if you're not on Ubuntu 18.04 or you will not get the newest version.
wget https://golang.google.cn/dl/go1.18.2.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.18.2.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go install github.com/bazelbuild/bazelisk@latest

git clone https://github.com/google/mediapipe.git
cd mediapipe

# 1. DO NOT install opencv with apt if you're not on Ubuntu 18.04 or you will get opencv 4.x.x, which is not supported by autoflip.
# 2. (NOT ENSSENTIAL) You'd better REMOVE your ffmpeg before the command below for convenience
chmod +x setup_opencv.sh
./setup_opencv.sh

bazelisk build -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/autoflip:run_autoflip
# Uncomment the command below if lack of RAM
# bazel build --jobs=1 -c opt --define MEDIAPIPE_DISABLE_GPU=1 mediapipe/examples/desktop/autoflip:run_autoflip

