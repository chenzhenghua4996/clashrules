# Clash 订阅规则

自动合并原始订阅 + 自定义分流规则的 Clash 配置。

## 订阅地址

```
https://你的用户名.github.io/clash-rules/clash.yaml
```

## 自定义规则

编辑 `custom-rules.yaml` 修改分流规则，push 后自动触发更新。

## 规则优先级

1. 爬虫数据源（9fzt/xueqiu/futunn/eastmoney等）→ 直连
2. 国内AI（deepseek/chatglm/doubao等）→ 直连  
3. 国内网站 → 直连
4. GeoIP中国 → 直连
5. moomoo → 代理
6. 境外网站（google/youtube/github等）→ 代理
7. 兜底 → 代理
