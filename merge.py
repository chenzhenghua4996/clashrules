"""
订阅合并脚本：拉取原始订阅 + 合并自定义分流规则 → 输出完整 Clash 配置
用于 GitHub Actions 自动构建
"""
import yaml
import requests
import sys
import os

# === 配置 ===
# 原始订阅URL（fanqiang）
SUBSCRIPTION_URL = os.environ.get('SUBSCRIPTION_URL', 'https://raw.githubusercontent.com/Alvin9999/pac/master/clash/config.yaml')
# 自定义规则文件
RULES_FILE = 'custom-rules.yaml'
# 输出文件
OUTPUT_FILE = 'docs/clash.yaml'

def fetch_subscription(url):
    """拉取原始订阅配置"""
    print(f"拉取订阅: {url}")
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return yaml.safe_load(r.text)

def load_custom_rules(filepath):
    """加载自定义规则"""
    print(f"加载规则: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('rules', [])

def merge_config(base_config, custom_rules):
    """合并配置：用自定义规则替换原始规则"""
    # 保留原始的 proxies 和 proxy-groups
    # 替换 rules
    # PROXY 占位符替换为第一个代理组名
    proxy_group_name = None
    if base_config.get('proxy-groups'):
        proxy_group_name = base_config['proxy-groups'][0]['name']
    
    # 替换 PROXY → 实际代理组名
    final_rules = []
    for rule in custom_rules:
        if isinstance(rule, str):
            # 替换 ,PROXY 或 ,PROXY,xxx 为实际代理组名
            rule = rule.replace(',PROXY,', f',{proxy_group_name},')
            if rule.endswith(',PROXY'):
                rule = rule.replace(',PROXY', f',{proxy_group_name}')
            final_rules.append(rule)
        else:
            final_rules.append(rule)
    
    base_config['rules'] = final_rules
    
    # 确保 dns 配置合理
    if 'dns' not in base_config:
        base_config['dns'] = {}
    base_config['dns']['enable'] = True
    base_config['dns']['enhanced-mode'] = 'fake-ip'
    base_config['dns']['nameserver'] = ['119.29.29.29', '223.5.5.5']
    
    return base_config

def main():
    # 拉取原始订阅
    try:
        base = fetch_subscription(SUBSCRIPTION_URL)
    except Exception as e:
        print(f"拉取订阅失败: {e}")
        sys.exit(1)
    
    print(f"原始配置: {len(base.get('proxies', []))} 个代理, {len(base.get('rules', []))} 条规则")
    
    # 加载自定义规则
    custom_rules = load_custom_rules(RULES_FILE)
    print(f"自定义规则: {len(custom_rules)} 条")
    
    # 合并
    merged = merge_config(base, custom_rules)
    
    # 确保输出目录存在
    os.makedirs('docs', exist_ok=True)
    
    # 写出
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(merged, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"输出: {OUTPUT_FILE}")
    print(f"最终: {len(merged.get('proxies', []))} 个代理, {len(merged.get('rules', []))} 条规则")

if __name__ == '__main__':
    main()
