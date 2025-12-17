#!/bin/bash

# Cquirrel Reproduction 构建脚本

set -e  # 遇到错误立即退出

echo "=== Cquirrel Reproduction 构建脚本 ==="
echo ""

# 检查 Maven
if ! command -v mvn &> /dev/null; then
    echo "错误: 未找到 Maven，请先安装 Maven"
    exit 1
fi

echo "Maven 版本:"
mvn -version
echo ""

# 步骤 1: 清理
echo "步骤 1/3: 清理旧的构建..."
mvn clean

# 步骤 2: 下载依赖
echo ""
echo "步骤 2/3: 下载依赖..."
echo "提示: 如果下载慢，请配置 ~/.m2/settings.xml 使用阿里云镜像"
mvn dependency:resolve -DskipTests

# 步骤 3: 编译和打包
echo ""
echo "步骤 3/3: 编译和打包..."
mvn package -DskipTests

# 检查结果
if [ -f "target/cquirrel-reproduction-1.0-SNAPSHOT.jar" ]; then
    echo ""
    echo "=== 构建成功! ==="
    echo "生成的 JAR: target/cquirrel-reproduction-1.0-SNAPSHOT.jar"
    echo ""
    echo "运行示例:"
    echo "  ./run.sh --input /path/to/input_data_all.csv --output /path/to/output.txt"
    echo ""
else
    echo ""
    echo "=== 构建失败 ==="
    exit 1
fi
