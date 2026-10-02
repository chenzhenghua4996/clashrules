# Clash 订阅规则

自动合并原始订阅 + 自定义分流规则的 Clash 配置，每 6 小时自动更新节点。

## 订阅地址

```
https://chenzhenghua4996.github.io/clashrules/b6041168492a1af2.yaml
```

## 工作流程

1. GitHub Actions 每 6 小时（或 push `custom-rules.yaml` / `merge.py` / `base.yaml` 时）运行 `merge.py`
2. 从订阅源拉取最新节点（gitlab.com/free9999 主源，www.67867867.xyz 备用，base.yaml 兜底）
3. 合并 `custom-rules.yaml` 自定义分流规则
4. 发布到 gh-pages

## 自定义规则

编辑 `custom-rules.yaml` 修改分流规则，push 后自动触发更新。

## 规则优先级

1. 私有网络/本地 → 直连
2. 爬虫数据源（9fzt/xueqiu/futunn/eastmoney等）→ 直连
3. 国内AI（deepseek/chatglm/doubao等）→ 直连
4. 国内网站 → 直连
5. GeoIP中国 → 直连
6. Yahoo Finance / moomoo → 代理
7. 境外网站（google/youtube/github等）→ 代理
8. 兜底 → 代理
