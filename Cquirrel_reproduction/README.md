# Cquirrel Reproduction

Cquirrel 项目的复现实现 - 一个将 SQL 查询转换为 Apache Flink 流处理程序的系统，专门针对 TPC-H 基准测试优化。

## 项目概述

本项目是对香港科技大学数据库实验室开发的 Cquirrel 系统的复现，使用 Java 和 Flink 实现核心功能。原项目的核心代码以 JAR 包形式提供，本复现项目重新实现了整体框架和关键组件。

### 核心功能

- **SQL/JSON 解析**: 将 SQL 查询或 JSON 配置解析为内部查询计划
- **流式处理**: 支持 TPC-H 数据的流式插入和删除操作
- **增量计算**: 使用 Flink KeyedProcessFunction 实现增量连接和聚合
- **控制台输出**: 查询结果直接输出到控制台（无 Web 界面）

### 技术栈

- **Java**: 1.8
- **Scala**: 2.12.13
- **Apache Flink**: 1.11.2
- **Maven**: 3.6.3
- **Alibaba Druid**: SQL 解析
- **Picocli**: 命令行参数解析

## 项目结构

```
Cquirrel_reproduction/
├── pom.xml                                 # Maven 项目配置
├── README.md                               # 项目文档
└── src/
    ├── main/
    │   ├── java/
    │   │   └── org/hkust/
    │   │       ├── CquirrelMain.java                    # 主入口 [已实现框架]
    │   │       ├── schema/                              # TPC-H 模式定义
    │   │       │   ├── Attribute.java                   # 属性（列）定义 [需完善]
    │   │       │   ├── Relation.java                    # 关系（表）定义 [需完善]
    │   │       │   └── RelationSchema.java              # 完整 TPC-H 模式 [需完善]
    │   │       ├── objects/                             # 领域对象模型
    │   │       │   ├── Node.java                        # 查询计划根对象 [需完善]
    │   │       │   ├── RelationProcessFunction.java     # 关系处理函数定义 [需完善]
    │   │       │   ├── AggregateProcessFunction.java    # 聚合处理函数定义 [需完善]
    │   │       │   ├── SelectCondition.java             # WHERE 条件 [需完善]
    │   │       │   ├── Value.java                       # 值接口 [需完善]
    │   │       │   └── AggregateValue.java              # 聚合值定义 [需完善]
    │   │       ├── parser/                              # 解析器
    │   │       │   ├── SQLParser.java                   # SQL 解析器 [待实现]
    │   │       │   └── JSONParser.java                  # JSON 配置解析器 [待实现]
    │   │       ├── codegenerator/                       # 代码生成器
    │   │       │   └── CodeGenerator.java               # Flink 代码生成 [待实现]
    │   │       ├── utils/                               # 工具类
    │   │       │   ├── TPCHDataParser.java              # TPC-H 数据解析 [待实现]
    │   │       │   └── FlinkJobBuilder.java             # Flink 作业构建 [待实现]
    │   │       └── flink/                               # Flink 处理函数
    │   │           ├── RelationKeyedProcessFunction.java    # 关系处理 [待实现]
    │   │           └── AggregateKeyedProcessFunction.java   # 聚合处理 [待实现]
    │   └── resources/
    │       └── log4j.properties                         # 日志配置
    └── test/
        ├── java/                                        # 测试代码
        └── resources/                                   # 测试资源（JSON 配置等）
```

## 待实现的核心模块

### 1. Schema 模块 (schema/)

**文件**: `Attribute.java`, `Relation.java`, `RelationSchema.java`

**功能**: 定义完整的 TPC-H 模式，包括 8 个表的所有字段和类型。

**需要实现**:
- `RelationSchema.initializeSchema()`: 定义所有 TPC-H 表
  - **lineitem** (16 个字段): l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment
  - **orders** (9 个字段): o_orderkey, o_custkey, o_orderstatus, o_totalprice, o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment
  - **customer** (8 个字段): c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, c_mktsegment, c_comment
  - **part** (9 个字段): p_partkey, p_name, p_mfgr, p_brand, p_type, p_size, p_container, p_retailprice, p_comment
  - **partsupp** (5 个字段): ps_partkey, ps_suppkey, ps_availqty, ps_supplycost, ps_comment
  - **supplier** (7 个字段): s_suppkey, s_name, s_address, s_nationkey, s_phone, s_acctbal, s_comment
  - **nation** (4 个字段): n_nationkey, n_name, n_regionkey, n_comment
  - **region** (3 个字段): r_regionkey, r_name, r_comment

- 每个字段的数据类型定义 (INTEGER, DOUBLE, VARCHAR, DATE)
- 主键和外键关系定义

**参考**: 原项目 `codegen/src/main/java/org/hkust/schema/`

### 2. Objects 模块 (objects/)

**文件**: `Node.java`, `RelationProcessFunction.java`, `AggregateProcessFunction.java`, `SelectCondition.java`, `Value.java`, `AggregateValue.java`

**功能**: 定义查询执行计划的对象模型。

**需要实现**:

#### Node.java
- 存储完整查询计划
- 包含 RelationProcessFunction 列表
- 包含 AggregateProcessFunction 列表
- 包含 join 结构映射（父子关系）

#### RelationProcessFunction.java
- 关系名称和关联的 Relation 对象
- thisKey 和 nextKey（用于 keying）
- 子节点数量
- isRoot 和 isLast 标志
- SelectCondition 列表（WHERE 条件）
- 属性重命名规则

#### AggregateProcessFunction.java
- 聚合函数名称
- thisKey 和 outputKey
- AggregateValue 列表（SUM, COUNT, AVG, MIN, MAX）
- HAVING 条件

#### SelectCondition.java
- 左值和右值（Value 对象）
- 比较操作符 (=, <, >, <=, >=, !=, LIKE)
- 逻辑操作符 (AND, OR)

#### Value 接口及其实现
- **ConstantValue**: 常量值（如 "BUILDING", 10, 3.14）
- **AttributeValue**: 列引用（如 c_mktsegment, l_quantity）
- **Expression**: 二元表达式（如 l_extendedprice * (1 - l_discount)）

**参考**: 原项目 `codegen/src/main/java/org/hkust/objects/`

### 3. Parser 模块 (parser/)

**文件**: `SQLParser.java`, `JSONParser.java`

**功能**: 将 SQL 查询或 JSON 配置解析为 Node 对象。

**需要实现**:

#### SQLParser.java
- 使用 Alibaba Druid 解析 SQL
- 提取 SELECT 子句（投影和聚合）
- 提取 FROM/JOIN 子句（关系和连接条件）
- 提取 WHERE 子句（选择条件）
- 提取 GROUP BY 子句
- 提取 HAVING 子句
- 构建 RelationProcessFunction 对象
- 构建 AggregateProcessFunction 对象
- 构建 join 结构映射

#### JSONParser.java
- 解析 JSON 配置文件
- JSON 格式包含三个主要部分:
  - `join_structure`: 父子关系映射
  - `RelationProcessFunction`: 关系处理函数数组
  - `AggregateProcessFunction`: 聚合处理函数数组
- 构建完整的 Node 对象

**JSON 格式示例**:
```json
{
  "join_structure": {
    "primary": "customer",
    "foreign": "orders"
  },
  "RelationProcessFunction": [
    {
      "name": "CustomerRPF",
      "relation": "customer",
      "this_key": "c_custkey",
      "next_key": "c_custkey",
      "child_nodes": 1,
      "is_Root": true,
      "is_Last": false,
      "select_conditions": {
        "operator": "&&",
        "values": [...]
      }
    }
  ],
  "AggregateProcessFunction": [...]
}
```

**参考**: 原项目 `codegen/src/main/java/org/hkust/parser/` 和 `codegen/src/test/resources/q3/Q3.json`

### 4. Utils 模块 (utils/)

**文件**: `TPCHDataParser.java`, `FlinkJobBuilder.java`

**功能**: 数据解析和 Flink 作业构建工具。

**需要实现**:

#### TPCHDataParser.java
- 解析 TPC-H 流式数据格式: `[+/-][TablePrefix]field1|field2|field3|...`
- 表前缀映射:
  - LI → lineitem
  - OR → orders
  - CU → customer
  - PA → part
  - PS → partsupp
  - SU → supplier
  - NA → nation
  - RI → region
- 提取操作类型（+ 插入，- 删除）
- 按 `|` 分隔字段
- 根据 schema 进行类型转换
- 返回 TPCHTuple 对象

#### FlinkJobBuilder.java
- 创建 StreamExecutionEnvironment
- 设置数据源（文件读取）
- 使用 TPCHDataParser 解析每一行
- 根据表名路由到不同的 RelationProcessFunction
- 按照 join 结构连接多个 ProcessFunction
- 连接 AggregateProcessFunction
- 设置输出 sink（控制台或文件）
- 配置 parallelism 和 checkpointing

**数据格式示例**:
```
+LI1|155190|7706|1|17|21168.23|0.04|0.02|N|O|1996-03-13|1996-02-12|1996-03-22|DELIVER IN PERSON|TRUCK|egular courts above the
+OR1|36901|O|173665.47|1996-01-02|5-LOW|Clerk#000000951|0|nstructions sleep furiously among
-CU36901|Customer#000036901|IVhzIApeRb ot,c,E|15|25-989-741-2988|711.56|BUILDING|to beans. carefully final deposits detect slyly agai
```

**参考**: 原项目 `DemoTools/DataGenerator/DataGenerator.py` 和输出格式

### 5. Flink 模块 (flink/)

**文件**: `RelationKeyedProcessFunction.java`, `AggregateKeyedProcessFunction.java`

**功能**: Flink 流处理的核心逻辑。

**需要实现**:

#### RelationKeyedProcessFunction.java
- 继承 `KeyedProcessFunction<String, Object, Object>`
- 使用 `MapState` 存储当前关系的元组
- 使用 `MapState` 存储子关系的元组（用于 join）
- `processElement()` 方法:
  1. 解析输入元组
  2. 判断插入 (+) 或删除 (-)
  3. 应用 WHERE 条件过滤
  4. **插入操作**:
     - 添加到状态
     - 与现有的父/子元组进行 join
     - 输出 join 结果
  5. **删除操作**:
     - 从状态中移除
     - 找到受影响的 join 结果
     - 向下游传播删除操作

#### AggregateKeyedProcessFunction.java
- 继承 `KeyedProcessFunction<String, Object, Object>`
- 为每个聚合维护 `MapState`:
  - SUM: `MapState<String, Double>`
  - COUNT: `MapState<String, Long>`
  - AVG: SUM + COUNT
  - MIN/MAX: `MapState<String, Double>`
- `processElement()` 方法:
  1. 解析输入元组
  2. 提取 grouping key
  3. 判断插入 (+) 或删除 (-)
  4. **更新聚合**:
     - SUM: 加/减值
     - COUNT: 递增/递减
     - AVG: 更新 SUM 和 COUNT
     - MIN/MAX: 必要时重新计算
  5. 应用 HAVING 条件
  6. 输出聚合结果

**状态管理注意事项**:
- 使用 Flink 的 Keyed State
- 处理删除操作时正确更新状态
- MIN/MAX 删除时可能需要重新扫描（或使用特殊数据结构）

**参考**: 原项目生成的 Scala 代码，如 `codegen/src/test/resources/q3/Job.scala`

### 6. CodeGenerator 模块 (codegenerator/)

**文件**: `CodeGenerator.java`

**功能**: （可选）将 Node 对象转换为 Flink Java 代码。

**说明**:
- 这个模块是原项目的核心，用于生成 Scala/Java 代码
- 在本复现项目中，可以选择:
  1. **直接执行**: 不生成代码，直接在 `FlinkJobBuilder` 中构建 DataStream（推荐用于初期）
  2. **代码生成**: 使用 Picocog 生成完整的 Java 类文件（更接近原项目）

**如果实现代码生成**:
- 生成 RelationProcessFunction 的 Java 类
- 生成 AggregateProcessFunction 的 Java 类
- 生成主类（包含 main 方法和 DataStream 设置）
- 使用 Maven 编译生成的代码
- 打包成 JAR 并提交到 Flink

**参考**: 原项目 `codegen/src/main/java/org/hkust/codegenerator/`

## 构建和运行

### 前置条件

1. **Java 1.8**
```bash
java -version
# 应显示 1.8.x
```

2. **Maven 3.6+**
```bash
mvn -version
```

3. **Apache Flink 1.11.2** (可选，用于集群模式)
```bash
# 下载
wget https://archive.apache.org/dist/flink/flink-1.11.2/flink-1.11.2-bin-scala_2.12.tgz
tar -xzf flink-1.11.2-bin-scala_2.12.tgz

# 启动本地集群（可选）
cd flink-1.11.2
./bin/start-cluster.sh
```

### 构建项目

```bash
cd /Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel_reproduction

# 编译项目
mvn clean compile

# 打包（生成 fat JAR）
mvn clean package

# 生成的 JAR 位于
# target/cquirrel-reproduction-1.0-SNAPSHOT.jar
```

### 运行示例

假设你已经生成了 TPC-H 流式数据文件 `input_data_all.csv`。

#### 使用 SQL 查询

```bash
java -jar target/cquirrel-reproduction-1.0-SNAPSHOT.jar \
  --sql "SELECT c_custkey, c_name FROM customer WHERE c_mktsegment = 'BUILDING'" \
  --input /path/to/input_data_all.csv \
  --output results.txt
```

#### 使用 JSON 配置

```bash
java -jar target/cquirrel-reproduction-1.0-SNAPSHOT.jar \
  --json query.json \
  --input /path/to/input_data_all.csv \
  --parallelism 2
```

#### 查看帮助

```bash
java -jar target/cquirrel-reproduction-1.0-SNAPSHOT.jar --help
```

## 测试 TPC-H 查询

原项目支持的 TPC-H 查询示例可以在以下位置找到：
- `/Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/codegen/src/test/resources/`

包括:
- **Q3**: 运输优先级查询
- **Q4**: 订单优先级检查查询
- **Q6**: 预测收入变化查询
- **Q10**: 退货损失查询
- **Q18**: 大批量客户查询

你可以参考这些 JSON 配置文件来测试本复现项目。

## 开发指南

### 开发优先级

建议按以下顺序实现模块：

1. **Schema 模块** (最基础)
   - 先实现简化版本（只包含常用的几个表）
   - 再扩展到完整的 8 个表

2. **Objects 模块** (核心数据结构)
   - 实现基本的 getter/setter
   - 添加验证逻辑

3. **Utils 模块** (数据解析)
   - `TPCHDataParser` 是处理输入的关键
   - 先支持基本的 lineitem 和 orders

4. **Parser 模块** (输入处理)
   - 建议先实现 `JSONParser`（格式已定义）
   - 再实现 `SQLParser`（需要理解 Druid AST）

5. **Flink 模块** (核心处理逻辑)
   - 先实现简单的 `RelationKeyedProcessFunction`（只处理单表过滤）
   - 再添加 join 逻辑
   - 最后实现 `AggregateKeyedProcessFunction`

6. **FlinkJobBuilder** (集成)
   - 将所有模块整合到一起

7. **CodeGenerator** (可选)
   - 如果需要代码生成功能再实现

### 调试建议

1. 使用小数据集测试（如只有 10 行数据）
2. 先实现简单查询（单表 SELECT + WHERE）
3. 逐步添加 JOIN 和聚合
4. 使用 Flink Web UI 查看作业执行情况（http://localhost:8081）
5. 添加详细的日志输出

### 代码风格

- 遵循 Java 命名规范
- 每个 TODO 注释都应该包含具体的实现提示
- 关键逻辑添加注释说明

## 与原项目的差异

| 特性 | 原项目 | 本复现项目 |
|------|--------|-----------|
| 语言 | Java (codegen) + Scala (generated) | 纯 Java |
| 前端 | React + Flask Web 界面 | 无前端，命令行 |
| 输出 | Web 页面展示 + 文件 | 控制台 + 文件 |
| 代码生成 | 生成 Scala Flink 代码 | 可选（直接执行或生成 Java） |
| 核心库 | cquirrel-core.jar (闭源) | 需要重新实现 |

## 参考资料

- **原项目**: `/Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/`
- **原项目 README**: `/Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/README.md`
- **Codegen README**: `/Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/codegen/README.md`
- **TPC-H 数据**: `/Users/ron/Documents/Code/self/IP/cquirrel/TPC-H V3.0.1/`
- **Flink 文档**: https://nightlies.apache.org/flink/flink-docs-release-1.11/
- **Druid SQL Parser**: https://github.com/alibaba/druid/wiki/SQL-Parser

## 常见问题

### Q: 为什么选择 Java 而不是 Scala？
A: 为了简化实现和提高可读性，同时 Flink 对 Java 的支持同样完善。

### Q: 必须实现代码生成吗？
A: 不必须。可以直接在 `FlinkJobBuilder` 中动态构建 DataStream，这样更简单。

### Q: 如何验证实现的正确性？
A: 可以对比原项目和本复现项目在相同输入下的输出结果。

### Q: 状态管理很复杂，有简化方案吗？
A: 可以先实现不支持删除操作的版本（只处理 `+` 开头的数据），这样状态管理会简单很多。

## 许可证

本项目用于学习和研究目的。原 Cquirrel 项目遵循 GNU GPL v3 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**Last Updated**: 2025-12-17
**Author**: Reproduction Project
**Original Project**: https://github.com/hkustDB/Cquirrel-release
