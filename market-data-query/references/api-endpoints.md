# API接口详细说明

## 目录
- [股票模块接口](#股票模块接口)
- [接口参数说明](#接口参数说明)
- [返回数据格式](#返回数据格式)
- [扩展指南](#扩展指南)

## 股票模块接口

### 1. 财务数据 (cwsj)
- **接口标识**: `cwsj`
- **功能描述**: 获取股票A股的公司2021年来对应报告期的财务数据
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 营收、利润、资产负债等财务指标

### 2. 大事提醒 (dstx)
- **接口标识**: `dstx`
- **功能描述**: 获取股票A股的大事内容
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 重大事件、公告、新闻等

### 3. 概念解读 (gnjd)
- **接口标识**: `gnjd`
- **功能描述**: 获取股票A股的公司所属的概念题材和入选理由
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 概念分类、题材关联、入选逻辑

### 4. 公司高管 (gsgg)
- **接口标识**: `gsgg`
- **功能描述**: 获取股票A股的公司高管信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 董事、监事、高管人员信息

### 5. 公司资料 (gszl)
- **接口标识**: `gszl`
- **功能描述**: 获取股票A股的公司资料基本信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 公司简介、行业分类、主营业务等

### 6. 股本结构 (gbjg)
- **接口标识**: `gbjg`
- **功能描述**: 获取股票A股的公司股本结构
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 总股本、流通股、股东分布等

### 7. 经营分析 (jyfx)
- **接口标识**: `jyfx`
- **功能描述**: 获取股票A股的公司的经营信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 经营数据、业务分析、发展动态

### 8. 十大股东 (sdgd)
- **接口标识**: `sdgd`
- **功能描述**: 获取股票A股的十大股东信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 前十大股东持股情况、变化趋势

### 9. 同行比较 (thbj)
- **接口标识**: `thbj`
- **功能描述**: 获取股票A股的同行公司的对比信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 同行业公司对比、排名、指标比较

### 10. 投资评级明细 (tzpjmx)
- **接口标识**: `tzpjmx`
- **功能描述**: 获取股票A股的投资明细信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **数据内容**: 机构评级、目标价、评级变化

### 11. 投资评级统计 (tzpjtj)
- **接口标识**: `tzpjtj`
- **功能描述**: 获取股票A股的投资评级统计信息
- **请求方式**: POST
- **必需参数**: `stockCode`（股票代码）
- **可选参数**: `period`（周期）
- **数据内容**: 评级统计、买入/卖出/持有分布

## 接口参数说明

### 通用参数
| 参数名 | 类型 | 必需 | 说明 | 示例 |
|--------|------|------|------|------|
| stockCode | string | 是 | 股票代码（6位数字） | 000001 |

### 特殊参数
| 参数名 | 类型 | 必需 | 适用接口 | 说明 | 示例 |
|--------|------|------|----------|------|------|
| period | string | 否 | tzpjtj | 统计周期 | 1 |

## 返回数据格式

所有接口返回JSON格式数据，结构如下：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    // 具体数据内容，根据接口不同而变化
  }
}
```

- `code`: 状态码（0表示成功）
- `message`: 响应消息
- `data`: 具体数据内容

## 扩展指南

### 添加新模块

在 `api_config.json` 中添加新模块配置：

```json
{
  "fund": {
    "base_url": "https://api.example.com/fund-api/fund",
    "endpoints": {
      "net_value": {
        "name": "基金净值",
        "description": "获取基金净值数据"
      },
      "position": {
        "name": "基金持仓",
        "description": "获取基金持仓明细",
        "extra_params": ["report_type"]
      }
    }
  },
  "index": {
    "base_url": "https://api.example.com/index-api/index",
    "endpoints": {
      "components": {
        "name": "成分股",
        "description": "获取指数成分股列表"
      }
    }
  }
}
```

### 添加新接口

在现有模块的 `endpoints` 中添加新接口：

```json
{
  "stock": {
    "base_url": "http://glink.genius.com.cn/stockf10-api/stockf10",
    "endpoints": {
      "new_endpoint": {
        "name": "新接口名称",
        "description": "接口功能描述",
        "extra_params": ["param1", "param2"]  // 如有额外参数
      }
    }
  }
}
```

### 调用新接口

```bash
# 基金净值查询
python scripts/query_market_data.py \
  --module fund \
  --endpoint net_value \
  --fundCode 000001

# 带额外参数的查询
python scripts/query_market_data.py \
  --module fund \
  --endpoint position \
  --fundCode 000001 \
  --report_type Q3
```
