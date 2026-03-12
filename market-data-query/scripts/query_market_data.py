#!/usr/bin/env python3
"""
市场数据查询通用API调用脚本

支持多模块（股票、基金、指数）的数据查询，通过配置文件动态管理API接口。

使用方式:
  python query_market_data.py --module stock --endpoint cwsj --stockCode 000001
  python query_market_data.py --module stock --endpoint tzpjtj --stockCode 000001 --period 1
"""

import os
import json
import sys
import argparse
import requests  # 替换为标准requests库


def load_config(config_path):
    """
    加载API配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        dict: 配置字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"配置文件格式错误: {e}")


def build_url(config, module, endpoint):
    """
    构建API请求URL
    
    Args:
        config: 配置字典
        module: 模块名称（stock/fund/index）
        endpoint: 接口标识
        
    Returns:
        str: 完整的API URL
    """
    if module not in config:
        raise ValueError(f"不支持的模块: {module}")
    
    module_config = config[module]
    base_url = module_config.get("base_url")
    
    if not base_url:
        raise ValueError(f"模块 {module} 未配置base_url")
    
    if endpoint not in module_config["endpoints"]:
        raise ValueError(f"模块 {module} 不支持的接口: {endpoint}")
    
    return f"{base_url}/{endpoint}"


def call_api(url, params):
    """
    调用API接口（移除API密钥相关逻辑）
    
    Args:
        url: API URL
        params: 请求参数
        
    Returns:
        dict: API响应数据
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=params, timeout=30)
        
        if response.status_code >= 400:
            raise Exception(f"HTTP请求失败: 状态码 {response.status_code}, 响应内容: {response.text}")
        
        data = response.json()
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API调用失败: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"响应数据解析失败: {e}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='市场数据查询API调用脚本')
    parser.add_argument('--config', type=str, default='api_config.json',
                       help='API配置文件路径（默认: api_config.json）')
    parser.add_argument('--module', type=str, required=True,
                       help='模块名称（stock/fund/index）')
    parser.add_argument('--endpoint', type=str, required=True,
                       help='接口标识')
    parser.add_argument('--stockCode', type=str,
                       help='股票代码（股票模块必需）')
    parser.add_argument('--fundCode', type=str,
                       help='基金代码（基金模块必需）')
    parser.add_argument('--indexCode', type=str,
                       help='指数代码（指数模块必需）')
    parser.add_argument('--period', type=str,
                       help='周期参数（部分接口需要）')
    
    args = parser.parse_args()
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), args.config)
    config = load_config(config_path)
    
    # 构建URL
    url = build_url(config, args.module, args.endpoint)
    
    # 构建请求参数
    params = {}
    
    # 根据模块添加必需参数
    if args.module == "stock":
        if not args.stockCode:
            raise ValueError("股票模块需要 --stockCode 参数")
        params["stockCode"] = args.stockCode
    elif args.module == "fund":
        if not args.fundCode:
            raise ValueError("基金模块需要 --fundCode 参数")
        params["fundCode"] = args.fundCode
    elif args.module == "index":
        if not args.indexCode:
            raise ValueError("指数模块需要 --indexCode 参数")
        params["indexCode"] = args.indexCode
    
    # 添加可选参数
    if args.period:
        params["period"] = args.period
    
    # 调用API（不再传入api_key）
    result = call_api(url, params)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)