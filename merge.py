"""
订阅合并脚本 v2：
- base.yaml 是原始订阅（含节点信息）
- custom-rules.yaml 是自定义分流规则
- 输出合并后的完整配置
"""
import yaml
import os
import copy

BASE_FILE = 'base.yaml'
RULES_FILE = 'custom-rules.yaml'
OUTPUT_FILE = 'docs/clash.yaml'

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def merge_config(base, custom_rules):
    config = copy.deepcopy(base)
    
    # 获取代理组名（第一个代理组）
    proxy_group_name = None
    if config.get('proxy-groups'):
        proxy_group_name = config['proxy-groups'][0]['name']
    
    # 替换 PROXY → 实际代理组名
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
    
    # 加载原始配置
    print(f"加载 base: {BASE_FILE}")
    base = load_yaml(BASE_FILE)
    print(f"  代理: {len(base.get('proxies', []))} 个")
    print(f"  原始规则: {len(base.get('rules', []))} 条")
    
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
