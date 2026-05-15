"""
订阅合并脚本 v3：
- 自动从远程拉取原始订阅
- 合并 custom-rules.yaml 自定义分流规则
- 输出完整 Clash 配置
"""
import yaml
import os
import copy
import requests

SUBSCRIPTION_URL = 'https://www.gitlabip.xyz/Alvin9999/PAC/refs/heads/master/backup/img/1/2/ipp/clash.meta2/2/config.yaml'
RULES_FILE = 'custom-rules.yaml'
OUTPUT_FILE = os.path.join('docs', os.environ.get('OUTPUT_NAME', 'index.html'))
# 如果远程拉取失败，使用本地 base.yaml 兜底
LOCAL_BASE = 'base.yaml'

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fetch_subscription(url):
    """拉取远程订阅"""
    print(f"拉取订阅: {url}")
    r = requests.get(url, timeout=30, proxies={'http': None, 'https': None})
    r.raise_for_status()
    return yaml.safe_load(r.text)

def merge_config(base, custom_rules):
    config = copy.deepcopy(base)
    
    proxy_group_name = None
    if config.get('proxy-groups'):
        proxy_group_name = config['proxy-groups'][0]['name']
    
    final_rules = []
    for rule in custom_rules:
        if isinstance(rule, str):
            rule = rule.replace(',PROXY,', f',{proxy_group_name},')
            if rule.endswith(',PROXY'):
                rule = rule.replace(',PROXY', f',{proxy_group_name}')
            final_rules.append(rule)
        else:
            final_rules.append(rule)
    
    config['rules'] = final_rules
    return config

def main():
    print("=== Clash 订阅合并 ===")
    
    # 尝试远程拉取，失败用本地兜底
    try:
        base = fetch_subscription(SUBSCRIPTION_URL)
        print(f"  远程订阅成功")
    except Exception as e:
        print(f"  远程拉取失败: {e}")
        print(f"  使用本地兜底: {LOCAL_BASE}")
        base = load_yaml(LOCAL_BASE)
    
    print(f"  代理: {len(base.get('proxies', []))} 个")
    
    # 同时更新本地 base.yaml
    os.makedirs('.', exist_ok=True)
    with open(LOCAL_BASE, 'w', encoding='utf-8') as f:
        yaml.dump(base, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    # 加载自定义规则
    print(f"加载规则: {RULES_FILE}")
    rules_data = load_yaml(RULES_FILE)
    custom_rules = rules_data.get('rules', [])
    print(f"  自定义规则: {len(custom_rules)} 条")
    
    # 合并
    merged = merge_config(base, custom_rules)
    
    # 输出
    os.makedirs('docs', exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(merged, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    
    print(f"\n输出: {OUTPUT_FILE}")
    print(f"  代理: {len(merged.get('proxies', []))} 个")
    print(f"  规则: {len(merged.get('rules', []))} 条")
    print("完成!")

if __name__ == '__main__':
    main()
