from analysis import  frequency
from proc_item import process_item
from datetime import datetime, timedelta

proc_item_list = [
    ["rings", "Prismatic_Ring", "全抗戒指"],
    ["spears", "Seaglass_Spear", "矛"],
    # ["amulets", "Solar Amulet", "精魂项链"],
    # ["body_armour", "Vile_Robe", "专家护盾衣服"],
    # ["body_armour", "Slipstrike Vest", "专家闪避衣服"],
    ["boots", "Sandsworn_Sandals", "专家羽毛便鞋"],
    ["bows", "Gemini_Bow", "专家双弦弓"],
    ["helmets", "Kamasan_Tiara", "专家头盔"],
    ["jewels", "Sapphire", "蓝玉珠宝"],
    ["jewels", "Emerald", "翠绿珠宝"]
    # ["gloves", "Vaal Gloves", "瓦尔手套"]
]

if __name__ == "__main__":
    # 取昨天数据处理
    start_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    for item_list in proc_item_list:
        # todo: 手套待施工
        # todo: 胸甲、鞋子、头盔、弓、蓝玉珠宝、翠绿珠宝待测试
        item = item_list[0]
        item_sub = item_list[1]
        desc = item_list[2]
        en = True # Eng diagrams
        interval = 5 # Price Range
        history = 0 # query history
        if en:
            desc = item_list[1]
        unit = "divine"
        price_obj = process_item(item, item_sub, start_date, end_date, interval, history, unit, en)
        print(price_obj)

        # # # 柱状图
        frequency.plot_price_tier_distribution(price_obj, desc=desc)
        # 单词缀热力图
        frequency.analyze_affix_popularity(price_obj)
        # 2，3，4词缀组合气泡图
        frequency.plot_3_affix_pairs_bubble_chart(price_obj)