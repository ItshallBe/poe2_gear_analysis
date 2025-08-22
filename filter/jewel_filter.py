from utils import util

def filter_jewel_by_price(data, type, rarity, interval, en=False):
    # 戒指词缀没有等阶，所以要特殊处理
    price_obj = {}
    price_array = util.get_price_array(interval)
    util.init_price_obj(price_array, price_obj)
    print(f"process jewel")
    for item_type in data:
        items_arry = data[item_type]
        for item in items_arry:
            name = item_type
            if rarity == 'unique':
                name = name + ':' + item["item"]["name"]
            price_idx = util.cal_price_idx(item, interval)
            util.inc_price_obj(price_obj, price_idx, name)
            mods = item["item"]["extended"]["hashes"]
            key = ''
            mods_arry = []
            if "explicit" in mods:
                for explicit_mod_arry in mods["explicit"]:
                    mod_id = explicit_mod_arry[0]
                    # 单词缀数目统计
                    mod_desc = util.affix_name(item, mod_id, rarity, type, en)
                    util.inc_price_obj_one_affix(mod_desc, price_obj, price_idx, name)
                    mods_arry.append(mod_desc)
            else:
                print("当前物品没有词缀", item)
            mods_arry.sort()
            key = ','.join(mods_arry)
            util.inc_price_obj_pair_affix(key, price_obj, price_idx, name)
    return price_obj