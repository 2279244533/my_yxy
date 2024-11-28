#!/bin/bash

# 要匹配的进程名称
process_names=("qqrobot.py" "go-cqhttp")

# 遍历每个进程名称，查找并杀死进程
for name in "${process_names[@]}"; do
  echo "查找并杀死进程: $name"

  # 查找进程ID
  pids=$(ps aux | grep "$name" | grep -v "grep" | awk '{print $2}')

  # 检查是否找到相关进程
  if [ -z "$pids" ]; then
    echo "未找到与 $name 匹配的进程"
  else
    # 杀死相关进程
    echo "$pids" | xargs -r kill -9
    echo "已杀死与 $name 匹配的进程: $pids"
  fi
done

# 启动 qqrobot.py
echo "启动 qqrobot.py"
nohup python3 ./qqrobot.py &

# 切换到 qqrobot 目录并启动 go-cqhttp
echo "切换到 qqrobot 目录并启动 go-cqhttp"
cd qqrobot || exit 1
nohup ./go-cqhttp &
