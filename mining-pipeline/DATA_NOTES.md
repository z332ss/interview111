# DATA_NOTES

## 数据来源
1. mining.com RSS feed（30条）
2. 中国稀土/澳洲DISR 政策公告（14条，模拟数据）
3. LME铜期货价格（yfinance，暂未获取成功）

## Schema
- source: 数据来源
- title: 标题
- link: 原文链接
- pub_date: 发布日期
- content: 正文内容

## 主键
- (source, title, pub_date) 组合去重

## 去重策略
- 按 title + source 去重，保留最新一条