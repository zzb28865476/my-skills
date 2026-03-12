---
name: market-data-query
description: 提供股票、基金、指数等金融市场数据的统一查询能力；当用户需要查询股票财务数据、公司资料、股东信息或需要获取市场投资分析数据时使用
---

# 市场数据查询

## 任务目标
- 本 Skill 用于: 提供统一的金融市场数据查询接口，支持股票、基金、指数等多模块数据获取
- 能力包含: 股票F10数据查询（财务、公司、股东、评级等）、灵活的多模块扩展架构
- 触发条件: 用户询问股票财务数据、公司信息、股东结构、投资评级或需要扩展其他金融市场数据查询功能

## 前置准备
- 依赖说明: scripts脚本所需的依赖包及版本
  ```
  python-docx>=0.8.11
  ```
- 凭证配置: 需要配置市场数据API的访问密钥（通过技能凭证系统配置）

## 操作步骤

### 标准流程

1. **识别查询需求**
   - 智能体理解用户想要查询的数据类型（财务数据、公司信息、股东信息等）
   - 确定股票代码或其他标识符

2. **调用API获取数据**
   - 执行 `scripts/query_market_data.py` 查询数据
   - 参数说明:
     - `--module`: 模块名称（当前支持: stock）
     - `--endpoint`: 接口标识（见下文接口列表）
     - `--stockCode`: 股票代码（如: 000001）
     - `--period`: 可选参数（部分接口需要，如投资评级统计）

3. **解析与呈现数据**
   - 智能体解析API返回的JSON数据
   - 以用户友好的方式呈现关键信息
   - 根据上下文提供投资分析建议

### 可选分支
- 当用户需要**财务数据**: 执行 `--endpoint cwsj`
- 当用户需要**大事提醒**: 执行 `--endpoint dstx`
- 当用户需要**概念解读**: 执行 `--endpoint gnjd`
- 当用户需要**公司高管**: 执行 `--endpoint gsgg`
- 当用户需要**公司资料**: 执行 `--endpoint gszl`
- 当用户需要**股本结构**: 执行 `--endpoint gbjg`
- 当用户需要**经营分析**: 执行 `--endpoint jyfx`
- 当用户需要**十大股东**: 执行 `--endpoint sdgd`
- 当用户需要**同行比较**: 执行 `--endpoint thbj`
- 当用户需要**投资评级明细**: 执行 `--endpoint tzpjmx`
- 当用户需要**投资评级统计**: 执行 `--endpoint tzpjtj --period 1`

## 资源索引

- 必要脚本: 
  - [scripts/query_market_data.py](scripts/query_market_data.py) - 通用API调用脚本
  - [scripts/api_config.json](scripts/api_config.json) - API配置文件（支持多模块扩展）
- 领域参考: [references/api-endpoints.md](references/api-endpoints.md) - 完整的API接口文档

## 注意事项
- 股票代码使用6位数字格式（如: 000001）
- 部分接口需要额外参数（如投资评级统计的period）
- 脚本支持多模块扩展，未来添加基金、指数接口时只需更新配置文件
- 所有API调用通过统一脚本处理，确保错误处理和数据格式的一致性

## 使用示例

### 示例1: 查询平安银行的财务数据
```bash
python scripts/query_market_data.py \
  --module stock \
  --endpoint cwsj \
  --stockCode 000001
```

### 示例2: 查询腾讯的十大股东信息
```bash
python scripts/query_market_data.py \
  --module stock \
  --endpoint sdgd \
  --stockCode 300750
```

### 示例3: 查询股票的投资评级统计（带周期参数）
```bash
python scripts/query_market_data.py \
  --module stock \
  --endpoint tzpjtj \
  --stockCode 000001 \
  --period 1
```

## 扩展指南

当需要添加新的数据模块（如基金、指数）时：

1. 在 `scripts/api_config.json` 中添加新的模块配置：
```json
{
  "fund": {
    "base_url": "https://api.example.com/fund",
    "endpoints": {
      "净值": {
        "name": "基金净值",
        "description": "获取基金净值数据"
      }
    }
  }
}
```

2. 使用相同脚本查询，指定新的模块和接口：
```bash
python scripts/query_market_data.py \
  --module fund \
  --endpoint 净值 \
  --fundCode 000001
```

无需修改脚本代码，只需更新配置文件即可实现扩展。
