from priceConfig.helmet import helmet_price
from utils import util

def filter_helmet_by_price(data, type, rarity, interval):
    price_obj = {}
    price_array = util.get_price_array(interval)
    util.init_price_obj(price_array, price_obj)
    print("processing helmet...")
    for item_type in data:
        items_arry = data[item_type]
        for item in items_arry:
            name = item_type
            price_idx = util.cal_price_idx(item, interval)
            # 价格要在统计区间内
            if price_idx in price_obj:
                # 增加指定价格区间物品数目
                util.inc_price_obj(price_obj, price_idx, name)
                prop = ''
                # todo: 完善盾、闪避等词缀处理
                if name == 'Kamasan Tiara':
                    prop = round(item["item"]["extended"]["es"])
                mods = item["item"]["extended"]["mods"]
                if 'explicit' in mods:
                    explicit_mods = mods['explicit']
                    mods_arry = []
                    union_mods = {}
                    for mod in explicit_mods:
                        magnitudes = mod['magnitudes']
                        mod_id = magnitudes[0]["hash"]
                        avg_value = util.affix_value(magnitudes)
                        # 测试获得装备词缀
                        # util.inc_price_obj_one_affix(mod_id, price_obj, price_idx, name)
                        util.proc_affix(union_mods, item, mod_id, rarity, avg_value, type)
                    if "defense" in mods:
                        union_mods['defense']["value"] = prop
                    else:
                        union_mods['defense'] = {"value": prop}
                    mods_arry = util.merge_affix(union_mods, item, rarity, price_obj, price_idx, name, type)
                    # 合并后组合词缀处理
                    mods_arry.sort()
                    key = ','.join(mods_arry)
                    util.inc_price_obj_pair_affix(key, price_obj, price_idx, name)
    return price_obj