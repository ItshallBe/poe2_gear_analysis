from utils import util

def filter_amulet_by_price(data, type, rarity, interval):
    price_obj = {}
    price_array = util.get_price_array(interval)
    util.init_price_obj(price_array, price_obj)
    print("process amulet...")
    for item_type in data:
        items_arry = data[item_type]
        for item in items_arry:
            name = item_type
            price_idx = util.cal_price_idx(item, interval)
            # 价格要在统计区间内
            if price_idx in price_obj:
                # 增加指定价格区间物品数目
                util.inc_price_obj(price_obj, price_idx, name)
                mods = item["item"]["extended"]["mods"]
                if 'explicit' in mods:
                    explicit_mods = mods['explicit']
                    mods_arry = []
                    # 同类合并后的词缀，如点伤，抗性
                    union_mods = {}
                    for mod in explicit_mods:
                        magnitudes = mod['magnitudes']
                        avg_value = util.affix_value(magnitudes)
                        mod_id = magnitudes[0]["hash"]
                        # 处理后的词缀，分为others和其他有用词缀如attacks、mana等
                        # util.inc_price_obj_one_affix(mod_id, price_obj, price_idx, name)
                        util.proc_affix(union_mods, item, mod_id, rarity, avg_value, type)
                    # 合并后单词缀处理
                    mods_arry = util.merge_affix(union_mods, item, rarity, price_obj, price_idx, name, type)
                    # 合并后组合词缀处理
                    mods_arry.sort()
                    key = ','.join(mods_arry)
                    util.inc_price_obj_pair_affix(key, price_obj, price_idx, name)
    return price_obj