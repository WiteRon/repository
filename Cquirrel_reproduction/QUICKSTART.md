# Cquirrel Reproduction - 快速开始

## ✅ 项目已完成构建

```
JAR文件: target/cquirrel-reproduction-1.0-SNAPSHOT.jar (4.6 MB)
构建时间: 2025-12-17
状态: 编译成功 ✓
```

## 🎯 当前状态

### 已完成
- ✅ Maven项目结构
- ✅ 17个Java类框架（带详细TODO）
- ✅ pom.xml优化（使用本地Flink，最小化依赖）
- ✅ 编译打包成功
- ✅ 运行脚本就绪

### 待实现（核心业务逻辑）
- ⏸️ TPC-H Schema定义（8个表）
- ⏸️ 数据解析器（TPCHDataParser）
- ⏸️ SQL/JSON解析器
- ⏸️ Flink流处理逻辑

## 📦 依赖配置

### 使用的依赖
```xml
核心依赖（已优化，无冗余）：
✓ Flink 1.11.2 (provided - 使用本地安装)
✓ Druid 1.2.5 (SQL解析)
✓ Gson 2.8.6 (JSON处理)
✓ Picocli 4.6.1 (命令行参数)
✓ SLF4J + Log4j (日志)

已移除：
✗ Kafka (不需要)
✗ Guava (用Java标准库替代)
✗ JGraphT (不生成代码，不需要)
```

### Flink位置
```bash
本地Flink: /usr/local/share/flink-1.11.2
```

### Maven镜像
已配置阿里云镜像（~/.m2/settings.xml）

## 🚀 运行方式

### 方法1：使用运行脚本（推荐）

```bash
# 使用本地Flink提交作业
./run.sh --input /path/to/input_data_all.csv --output /path/to/output.txt

# 使用JSON配置
./run.sh --json /path/to/query.json --input /path/to/data.csv
```

### 方法2：直接使用flink命令

```bash
/usr/local/share/flink-1.11.2/bin/flink run \
  -c org.hkust.CquirrelMain \
  target/cquirrel-reproduction-1.0-SNAPSHOT.jar \
  --input /path/to/data.csv
```

### 查看帮助

```bash
/usr/local/share/flink-1.11.2/bin/flink run \
  -c org.hkust.CquirrelMain \
  target/cquirrel-reproduction-1.0-SNAPSHOT.jar \
  --help
```

## 📝 重新构建

```bash
# 完整构建
./build.sh

# 或手动构建
mvn clean package -DskipTests
```

## 🔧 开发流程

### 1. 实现核心模块

按推荐顺序：

```bash
1. Schema模块 (最基础)
   src/main/java/org/hkust/schema/RelationSchema.java
   → 定义TPC-H 8个表的schema

2. 数据解析 (读取输入)
   src/main/java/org/hkust/utils/TPCHDataParser.java
   → 解析 +LI|field1|field2|... 格式

3. JSON解析 (推荐先实现)
   src/main/java/org/hkust/parser/JSONParser.java
   → 解析query.json配置文件

4. Flink处理函数 (核心逻辑)
   src/main/java/org/hkust/flink/RelationKeyedProcessFunction.java
   src/main/java/org/hkust/flink/AggregateKeyedProcessFunction.java
   → 实现增量join和聚合

5. 作业构建 (整合)
   src/main/java/org/hkust/utils/FlinkJobBuilder.java
   → 构建完整的DataStream pipeline
```

### 2. 测试开发

```bash
# 编辑代码
vi src/main/java/org/hkust/schema/RelationSchema.java

# 编译
mvn compile

# 打包
mvn package -DskipTests

# 运行
./run.sh --input test_data.csv
```

## 📚 参考资源

### 原项目参考

```bash
# 原项目位置
/Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/

# 关键参考文件
- codegen/src/test/resources/q3/Q3.json        # JSON格式示例
- codegen/src/test/resources/q3/Job.scala      # 生成的代码示例
- codegen/src/main/java/org/hkust/schema/     # Schema定义
- gui/cquirrel_flask/config.py                 # 配置参考
```

### TPC-H数据

```bash
# 数据位置（已生成1GB）
/Users/ron/Documents/Code/self/IP/cquirrel/TPC-H V3.0.1/

# 数据格式示例
+LI1|155190|7706|1|17|21168.23|0.04|0.02|N|O|1996-03-13|...
-OR1|36901|O|173665.47|1996-01-02|5-LOW|...
+CU36901|Customer#000036901|...|BUILDING|...
```

## 💡 实现提示

### TPCHDataParser示例

```java
// 需要解析的格式
String line = "+LI1|155190|7706|1|17|21168.23|0.04|0.02|...";

// 步骤
1. 提取操作符: line.charAt(0) // '+' or '-'
2. 提取表前缀: line.substring(1, 3) // "LI"
3. 分割字段: line.substring(3).split("\\|")
4. 类型转换: fields[0].toLong(), fields[4].toDouble()
5. 返回TPCHTuple对象
```

### RelationSchema示例

```java
// 参考原项目
Relation lineitem = new Relation("lineitem");
lineitem.addAttribute(new Attribute("l_orderkey", "INTEGER", "lineitem"));
lineitem.addAttribute(new Attribute("l_partkey", "INTEGER", "lineitem"));
// ... 共16个字段
```

### Flink数据读取（参考原项目Q6）

```java
// 原项目使用
env.readTextFile(inputPath)
   .process(new ParseFunction())  // 解析每行
   .getSideOutput(lineitemTag)     // 路由到不同表
   .keyBy(tuple -> tuple._3)       // 按key分组
   .process(new RelationProcessFunction())
```

## ❓ 常见问题

### Q: 编译时提示找不到Flink类？
A: 正常的，Flink是`provided`依赖。运行时会用本地的Flink。

### Q: 如何测试单个模块？
A: 在`src/test/java`下写单元测试，运行`mvn test`

### Q: 可以直接`java -jar`运行吗？
A: 不行，必须用`flink run`提交，因为Flink依赖是`provided`的。

### Q: 如何调试？
A:
1. 添加日志：`System.out.println()` 或使用 SLF4J
2. 本地测试：用小数据集
3. Flink Web UI：http://localhost:8081（需启动Flink集群）

## 📖 详细文档

- **完整README**: `README.md`（包含所有待实现模块的详细说明）
- **项目状态**: `PROJECT_STATUS.md`（开发进度和下一步）
- **运行脚本**: `run.sh`（Flink提交脚本）
- **构建脚本**: `build.sh`（一键编译打包）

---

**当前版本**: 1.0-SNAPSHOT
**最后更新**: 2025-12-17
**构建状态**: ✅ 编译成功，框架就绪，等待实现核心逻辑
