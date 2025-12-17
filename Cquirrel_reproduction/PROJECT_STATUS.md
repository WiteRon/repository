# Cquirrel Reproduction - 项目状态报告

**最后更新**: 2025-12-17 15:00
**当前阶段**: 框架完成，编译通过 ✅

---

## ✅ 已完成的工作

### 1. 项目结构搭建 (100%)
```
Cquirrel_reproduction/
├── pom.xml                          ✅ Maven配置（已优化）
├── README.md                        ✅ 完整文档
├── QUICKSTART.md                    ✅ 快速开始指南
├── PROJECT_STATUS.md                ✅ 本文件
├── run.sh                           ✅ Flink运行脚本
├── build.sh                         ✅ 构建脚本
├── .gitignore                       ✅ Git配置
└── src/main/java/org/hkust/
    ├── CquirrelMain.java            ✅ 主入口（框架完成）
    ├── schema/                      ⏸️ 占位符（需填充）
    ├── objects/                     ⏸️ 占位符（需填充）
    ├── parser/                      ⏸️ 占位符（需填充）
    ├── utils/                       ⏸️ 占位符（需填充）
    ├── flink/                       ⏸️ 占位符（需填充）
    └── codegenerator/               ⏸️ 占位符（可选）
```

### 2. 依赖配置优化 (100%)

**最终依赖清单**（最小化，无冗余）：
```xml
✅ Flink 1.11.2 (scope=provided, 使用本地 /usr/local/share/flink-1.11.2)
✅ Druid 1.2.5 (SQL解析器)
✅ Gson 2.8.6 (JSON处理)
✅ Picocli 4.6.1 (命令行参数)
✅ SLF4J + Log4j (日志)
```

**已移除的依赖**（不需要）：
```
❌ Kafka (数据源改为CSV文件)
❌ Guava (用Java标准库替代)
❌ JGraphT (直接执行，不生成代码)
❌ Picocog (不需要代码生成)
```

### 3. Maven配置优化 (100%)
- ✅ 配置阿里云镜像 (~/.m2/settings.xml)
- ✅ Flink设为provided依赖
- ✅ 编译成功
- ✅ 打包成功 (4.6 MB JAR)

### 4. 代码框架 (100%)

**已创建17个Java类**，全部编译通过：

| 模块 | 文件 | 状态 | 说明 |
|------|------|------|------|
| **入口** | CquirrelMain.java | ✅ 框架完成 | 命令行参数解析完整 |
| **Schema** | Attribute.java | ⏸️ 占位符 | 需定义属性类型和验证 |
| | Relation.java | ⏸️ 占位符 | 需定义表结构 |
| | RelationSchema.java | ⏸️ 占位符 | **需定义8个TPC-H表** |
| **Objects** | Node.java | ⏸️ 占位符 | 需完善查询计划结构 |
| | RelationProcessFunction.java | ⏸️ 占位符 | 需定义关系处理逻辑 |
| | AggregateProcessFunction.java | ⏸️ 占位符 | 需定义聚合逻辑 |
| | SelectCondition.java | ⏸️ 占位符 | 需定义WHERE条件 |
| | Value.java | ⏸️ 占位符 | 需实现3种Value类型 |
| | AggregateValue.java | ⏸️ 占位符 | 需定义聚合值 |
| **Parser** | SQLParser.java | ⏸️ 占位符 | **需用Druid解析SQL** |
| | JSONParser.java | ⏸️ 占位符 | **需解析JSON配置** |
| **Utils** | TPCHDataParser.java | ⏸️ 占位符 | **需解析数据格式** |
| | FlinkJobBuilder.java | ⏸️ 占位符 | **需构建DataStream** |
| **Flink** | RelationKeyedProcessFunction.java | ⏸️ 占位符 | **核心：增量join** |
| | AggregateKeyedProcessFunction.java | ⏸️ 占位符 | **核心：增量聚合** |
| **CodeGen** | CodeGenerator.java | ⏸️ 占位符 | 可选，暂不实现 |

---

## 🎯 下一步工作：补全核心算法

### 实现优先级（推荐顺序）

#### 第一阶段：基础设施 (必需)

**1. Schema模块** - 定义TPC-H数据模型
```
文件: src/main/java/org/hkust/schema/RelationSchema.java
任务:
  - 定义8个TPC-H表：lineitem, orders, customer, part, partsupp, supplier, nation, region
  - 每个表的所有字段及类型（参考原项目或TPC-H规范）
  - 表前缀映射：LI->lineitem, OR->orders, CU->customer 等

参考:
  - 原项目: /Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/codegen/src/main/java/org/hkust/schema/
  - TPC-H数据: /Users/ron/Documents/Code/self/IP/cquirrel/TPC-H V3.0.1/
```

**2. TPCHDataParser** - 解析输入数据
```
文件: src/main/java/org/hkust/utils/TPCHDataParser.java
任务:
  - 解析格式: [+/-][TablePrefix]field1|field2|field3|...
  - 识别操作类型: + (插入) / - (删除)
  - 识别表名: LI, OR, CU, PA, PS, SU, NA, RI
  - 按|分隔字段
  - 类型转换: String -> Integer/Double/Date
  - 返回TPCHTuple对象

示例输入:
  +LI1|155190|7706|1|17|21168.23|0.04|0.02|N|O|1996-03-13|...
  -OR1|36901|O|173665.47|1996-01-02|5-LOW|...

参考:
  - 原项目: Cquirrel-release/codegen/src/test/resources/q6/Job.scala (29-60行)
```

**3. Objects模块** - 完善领域对象
```
文件: src/main/java/org/hkust/objects/*.java
任务:
  - Node.java: 添加RelationProcessFunction和AggregateProcessFunction列表管理
  - RelationProcessFunction.java: 添加thisKey, nextKey, SelectCondition列表等
  - AggregateProcessFunction.java: 添加thisKey, AggregateValue列表等
  - Value.java: 实现ConstantValue, AttributeValue, Expression三个子类
  - SelectCondition.java: 实现条件评估逻辑

参考:
  - 原项目: Cquirrel-release/codegen/src/main/java/org/hkust/objects/
```

#### 第二阶段：解析器 (必需)

**4. JSONParser** - 解析JSON配置（推荐先实现）
```
文件: src/main/java/org/hkust/parser/JSONParser.java
任务:
  - 读取JSON文件
  - 解析join_structure
  - 解析RelationProcessFunction数组
  - 解析AggregateProcessFunction数组
  - 构建Node对象

JSON格式:
  {
    "join_structure": {...},
    "RelationProcessFunction": [...],
    "AggregateProcessFunction": [...]
  }

参考:
  - 原项目: Cquirrel-release/codegen/src/test/resources/q3/Q3.json
  - 解析器: Cquirrel-release/codegen/src/main/java/org/hkust/jsonutils/JsonParser.java
```

**5. SQLParser** - SQL解析（可选，建议后实现）
```
文件: src/main/java/org/hkust/parser/SQLParser.java
任务:
  - 使用Alibaba Druid解析SQL
  - 提取SELECT, FROM, WHERE, JOIN, GROUP BY, HAVING
  - 构建Node对象

参考:
  - 原项目: Cquirrel-release/codegen/src/main/java/org/hkust/parser/Parser.java
```

#### 第三阶段：核心处理逻辑 (最关键)

**6. RelationKeyedProcessFunction** - 关系处理和增量Join
```
文件: src/main/java/org/hkust/flink/RelationKeyedProcessFunction.java
任务:
  - 使用MapState存储当前表的元组
  - 实现processElement方法:
    a. 解析输入（插入/删除）
    b. 应用WHERE条件过滤
    c. 插入操作:
       - 添加到状态
       - 与父/子表join
       - 输出join结果
    d. 删除操作:
       - 从状态移除
       - 找到受影响的join结果
       - 传播删除

这是最核心的部分！

参考:
  - 原项目生成的代码: Cquirrel-release/codegen/src/test/resources/q3/
  - Flink KeyedProcessFunction文档
```

**7. AggregateKeyedProcessFunction** - 增量聚合
```
文件: src/main/java/org/hkust/flink/AggregateKeyedProcessFunction.java
任务:
  - 为每个聚合维护MapState (SUM, COUNT, AVG, MIN, MAX)
  - 实现processElement方法:
    a. 提取grouping key
    b. 插入: 更新聚合（SUM累加，COUNT递增）
    c. 删除: 回退聚合（SUM减少，COUNT递减）
    d. 应用HAVING条件
    e. 输出聚合结果

参考:
  - 原项目: Cquirrel-release/codegen/src/test/resources/q6/Q6AggregateProcessFunction.scala
```

**8. FlinkJobBuilder** - 构建Flink作业
```
文件: src/main/java/org/hkust/utils/FlinkJobBuilder.java
任务:
  - 创建StreamExecutionEnvironment
  - 读取CSV文件: env.readTextFile()
  - 使用TPCHDataParser解析每行
  - 按表名路由（可用SideOutput）
  - 连接RelationProcessFunction（按join顺序）
  - 连接AggregateProcessFunction
  - 输出到console或文件

参考:
  - 原项目: Cquirrel-release/codegen/src/test/resources/q6/Job.scala
```

---

## 📊 关键参考资料

### 原项目位置
```bash
基础目录: /Users/ron/Documents/Code/self/IP/cquirrel/Cquirrel-release/

重要文件:
1. Schema定义:
   codegen/src/main/java/org/hkust/schema/

2. 生成的Scala代码示例（理解处理逻辑）:
   codegen/src/test/resources/q3/Job.scala
   codegen/src/test/resources/q6/Q6LineitemProcessFunction.scala
   codegen/src/test/resources/q6/Q6AggregateProcessFunction.scala

3. JSON配置示例:
   codegen/src/test/resources/q3/Q3.json
   codegen/src/test/resources/q6/Q6.json

4. 原始代码（可参考但已编译成JAR）:
   codegen/src/main/java/org/hkust/
```

### TPC-H数据位置
```bash
数据目录: /Users/ron/Documents/Code/self/IP/cquirrel/TPC-H V3.0.1/
规格: 1GB数据（Scale Factor = 1）
```

### 数据格式示例
```
+LI1|155190|7706|1|17|21168.23|0.04|0.02|N|O|1996-03-13|1996-02-12|1996-03-22|DELIVER IN PERSON|TRUCK|...
+OR1|36901|O|173665.47|1996-01-02|5-LOW|Clerk#000000951|0|nstructions sleep furiously among
-CU36901|Customer#000036901|IVhzIApeRb ot,c,E|15|25-989-741-2988|711.56|BUILDING|...

格式说明:
  [+/-]    : 操作类型（插入/删除）
  [XX]     : 表前缀（LI/OR/CU/PA/PS/SU/NA/RI）
  field1|field2|... : 按|分隔的字段值
```

---

## 🔧 开发建议

### 1. 从简单到复杂
- 先支持单表查询（SELECT + WHERE）
- 再添加JOIN
- 最后实现聚合

### 2. 可以先不支持删除操作
- 只处理`+`开头的数据
- 简化状态管理
- 后续再添加删除逻辑

### 3. 使用小数据集测试
- 手动创建10-20行测试数据
- 验证解析和处理逻辑正确
- 再用完整1GB数据测试

### 4. 参考原项目生成的代码
- 查看Job.scala理解整体流程
- 查看ProcessFunction理解状态管理
- 理解增量计算的思路

---

## 📝 TODO清单（供新Agent参考）

### 立即开始（按顺序）
- [ ] 1. 实现RelationSchema - 定义8个TPC-H表的完整schema
- [ ] 2. 实现TPCHDataParser - 解析输入数据格式
- [ ] 3. 完善Objects模块 - 添加必要的属性和方法
- [ ] 4. 实现JSONParser - 解析JSON查询配置
- [ ] 5. 实现RelationKeyedProcessFunction - 核心join逻辑
- [ ] 6. 实现AggregateKeyedProcessFunction - 核心聚合逻辑
- [ ] 7. 实现FlinkJobBuilder - 构建完整DataStream
- [ ] 8. 测试完整流程 - 使用Q3或Q6测试

### 可选（后续）
- [ ] 实现SQLParser - SQL到Node转换
- [ ] 实现CodeGenerator - 生成代码功能
- [ ] 优化性能 - 状态管理和并行度
- [ ] 添加单元测试

---

## 💡 重要提示

1. **每个类都有详细TODO注释**
   - 打开任意Java文件，查看`// TODO: Implement...`注释
   - 每个注释都说明了需要实现什么

2. **README.md包含完整实现指南**
   - 查看"待实现的核心模块"章节
   - 每个模块都有详细的实现说明

3. **编译和运行**
   ```bash
   # 编译
   mvn compile

   # 打包
   mvn package -DskipTests

   # 运行
   ./run.sh --input /path/to/data.csv
   ```

4. **Flink本地调试**
   - 启动Flink集群: `/usr/local/share/flink-1.11.2/bin/start-cluster.sh`
   - Web UI: http://localhost:8081
   - 查看日志: `/usr/local/share/flink-1.11.2/log/`

---

## 🎯 当前状态总结

**✅ 已完成**: 项目框架、依赖配置、编译打包
**⏸️ 待完成**: 核心业务逻辑实现
**🚀 下一步**: 按优先级顺序实现上述8个核心模块

**项目可以编译通过，但所有业务逻辑都是占位符，需要逐个填充实现。**

---

**创建时间**: 2025-12-17
**框架完成**: 2025-12-17 15:00
**编译状态**: ✅ 成功
**JAR大小**: 4.6 MB
**准备就绪**: ✅ 可以开始实现核心算法
