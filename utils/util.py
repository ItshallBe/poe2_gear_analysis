import json
from priceConfig import common_price

def merge_dicts(d1, d2):
    """递归合并两个嵌套字典，数值类型相加，字典类型递归合并"""
    merged = {}
    # 获取所有唯一键
    all_keys = set(d1.keys()) | set(d2.keys())
    print("唯一键", all_keys)
    for key in all_keys:
        v1 = d1.get(key, {})
        v2 = d2.get(key, {})
        print("v1, v2", v1, v2)

        # 处理数值类型
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)):
            merged[key] = v1 + v2

        # 处理字典类型
        elif isinstance(v1, dict) and isinstance(v2, dict):
            merged[key] = merge_dicts(v1, v2)

        # 处理一方不存在的情况
        else:
            merged[key] = v1 if v2 == {} else v2

    return merged

def load_json(path):
    with open(path, encoding='UTF-8') as f:
        return json.load(f)

def cal_price_idx(item, interval):
    price = item["listing"]["price"]["amount"]
    price_idx = str((((price - 1) // interval) * interval) + 1)
    return price_idx

def inc_price_obj(price_obj, price_idx, name):
    if name not in price_obj[price_idx]:
        price_obj[price_idx][name] = {
            "ones": {},
            "pairs": {},
            "count": 1
        }
    else:
        price_obj[price_idx][name]["count"] += 1

def inc_price_obj_one_affix(mod_desc, price_obj, price_idx, name):
    if mod_desc not in price_obj[price_idx][name]["ones"]:
        price_obj[price_idx][name]["ones"][mod_desc] = {"count": 1}
    else:
        price_obj[price_idx][name]["ones"][mod_desc]["count"] += 1

def inc_price_obj_pair_affix(key, price_obj, price_idx, name):
    if key in price_obj[price_idx][name]["pairs"]:
        price_obj[price_idx][name]["pairs"][key]["count"] += 1
    else:
        price_obj[price_idx][name]["pairs"][key] = {"count": 1}

def affix_name(item, mod_id, rarity, type):
    affix_item = affix_obj(item, mod_id, rarity, type)
    return affix_item['desc']

def affix_obj(item, mod_id, rarity, type):
    file_name = ''
    if rarity == 'unique':
        file_name = item["item"]["name"]
    else:
        file_name = item["item"]["baseType"]
    file = './affix/' + type + '/' + file_name + '.json'
    affix_config = load_json(file)
    return affix_config[mod_id]

def init_price_obj(price_array, price_obj):
    for arr in price_array:
        min_price = str(arr[0])
        price_obj[min_price] = {}

def affix_value(magnitudes):
    min_value = magnitudes[0]["min"]
    max_value = magnitudes[0]["max"]
    if len(magnitudes) > 1:
        max_value = magnitudes[1]["max"]
    avg_value = round((float(min_value) + float(max_value)) / 2)
    return avg_value

# union_mods: 合并后的词缀
# item: 当前物品
# mod: 当前词缀id
# rarity: 物品稀有度，稀有和传奇物品取affix下的文件时，规则不同
# avg_value: 当前词缀的均值
# 物品: 基底

def proc_affix(union_mods, item, mod_id, rarity, avg_value, type):
    mod_item = affix_obj(item, mod_id, rarity, type)
    mod_type = mod_item["type"]
    # 合并同类词缀，如点伤、抗性
    mod_type_obj = affix_obj(item, mod_type, rarity, type)
    if mod_type != 'others':
        final_value = mod_type_obj[mod_id]["weight"] * avg_value
        if mod_type not in union_mods:
            union_mods[mod_type] = {"value": final_value}
        else:
            union_mods[mod_type]["value"] += final_value
    else:
        if 'others' not in union_mods:
            union_mods['others'] = {"count": 1}
        else:
            union_mods['others']["count"] += 1

def merge_affix(union_mods, item, rarity, price_obj, price_idx, name, type):
    mods_arry = []
    for key in union_mods:
        mod_type_obj = affix_obj(item, key, rarity, type)
        desc = mod_type_obj['desc']
        if key == 'others':
            # 废词缀处理
            count = union_mods[key]['count']
            cur_mod = str(count) + desc
            mods_arry.append(cur_mod)
        else:
            tiers = mod_type_obj['tiers']
            value = union_mods[key]['value']
            t = 1
            for tier in tiers:
                if tier < value:
                    t += 1
            cur_mod = 't' + str(t) + desc
            inc_price_obj_one_affix(cur_mod, price_obj, price_idx, name)
            mods_arry.append(cur_mod)
    return mods_arry

def get_price_array(interval):
    # interval = 5, [1, 5], [6, 10]...
    # interval = 10, [1, 10], [11, 20]...
    if interval == 5:
        return common_price.price1
    else:
        return common_price.price2