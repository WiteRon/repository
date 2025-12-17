#!/bin/bash

# Cquirrel Reproduction 运行脚本
# 使用本地 Flink 提交作业

# Flink 安装路径
FLINK_HOME="/usr/local/share/flink-1.11.2"

# 项目 JAR 路径
PROJECT_JAR="target/cquirrel-reproduction-1.0-SNAPSHOT.jar"

# 检查 JAR 是否存在
if [ ! -f "$PROJECT_JAR" ]; then
    echo "错误: 未找到 JAR 文件: $PROJECT_JAR"
    echo "请先运行: mvn clean package"
    exit 1
fi

# 检查 Flink 是否存在
if [ ! -d "$FLINK_HOME" ]; then
    echo "错误: 未找到 Flink 安装目录: $FLINK_HOME"
    exit 1
fi

# 提交 Flink 作业
echo "=== 使用本地 Flink 提交作业 ==="
echo "Flink Home: $FLINK_HOME"
echo "Project JAR: $PROJECT_JAR"
echo ""

# 使用 flink run 提交作业
# 参数会传递给 CquirrelMain
$FLINK_HOME/bin/flink run \
    -c org.hkust.CquirrelMain \
    "$PROJECT_JAR" \
    "$@"

# 参数示例：
# ./run.sh --input /path/to/input_data_all.csv --output /path/to/output.txt
# ./run.sh --json /path/to/query.json --input /path/to/data.csv
