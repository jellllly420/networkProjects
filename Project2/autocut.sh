#!/bin/bash

python3 video2text.py src/$1
python3 editor.py src/$1