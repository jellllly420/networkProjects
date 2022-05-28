#!/bin/bash

# build ffmpeg 4.x.x for the installation of PyAV
wget https://ffmpeg.org/releases/ffmpeg-4.4.2.tar.gz
tar -xzf ffmpeg-4.4.2.tar.gz
cd ~/ffmpeg-4.4.2
sudo apt-get install yasm libmp3lame-dev  # mp3 decoders needed by video2text.py
./configure --disable-x86asm --enable-shared  --enable-libmp3lame # static lib NOT supported by PyAV
make -j 16
make install
sudo echo "/usr/local/ffmpeg/lib/" >> /etc/ld.conf  # set env vars
sudo ldconfig

# prepare for video2text.py and editor.py
pip3 install requests # upgrade to >=2.20.0 
pip3 install sympy textrank4zh
pip3 install av --no-binary av
pip3 install auto-editor  # there may be other dependencies
                          # just follow the hints