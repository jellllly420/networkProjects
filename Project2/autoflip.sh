#!/bin/bash
cd ~/mediapipe

GLOG_logtostderr=1 bazel-bin/mediapipe/examples/desktop/autoflip/run_autoflip   --calculator_graph_config_file=mediapipe/examples/desktop/autoflip/autoflip_graph.pbtxt   --input_side_packets=input_video_path=$1,output_video_path=$2,aspect_ratio=$3

# Usage:
# ./autoflip.sh /home/username/input.mp4 /home/username/output.mp4 9:16

# If encountered with segmentation fault, you can change the Line 38 of ~/mediapipe/mediapipe/examples/desktop/autoflip/autoflip_graph.pbtxt from "period: 200000" to "period: 10000000"