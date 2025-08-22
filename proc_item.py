from network import network
from filter import filter

# item: 物品base，如Ring
# item_sub：具体物品，如Prismatic Ring
# start_date：统计起始日期
# end_date：统计结束日期
# interval：统计价位间隔，支持5或10。传入5，统计[1, 5]、[6,10]...
#                               传入10，统计[1, 10]、[11, 20]...
# history：是否查询历史记录
# unit: 查询单位记录
def process_item(item, item_sub, start_date, end_date, interval, history, unit):
    price_obj = {}
    if item == 'rings':
        price_obj = rings(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'amulets':
        price_obj = amulets(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'body_armour':
        price_obj = body_armour(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'spears':
        price_obj = spears(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'boots':
        price_obj = boots(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'bows':
        price_obj = bows(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'helmets':
        price_obj = helmets(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'jewels':
        price_obj = jewels(start_date, end_date, item_sub, interval, history, unit)
    elif item == 'gloves':
        price_obj = gloves(start_date, end_date, item_sub, interval, history, unit)
    return price_obj

def rings(start_date, end_date, ring_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "Ring", ring_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Ring", ring_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Ring")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'ring', 'rare', interval)
    return price_obj

def amulets(start_date, end_date, amulet_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "Amulet", amulet_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Amulet", amulet_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Amulet")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'amulet', 'rare', interval)
    return price_obj

def body_armour(start_date, end_date, armour_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "BodyArmour", armour_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Body Armour", armour_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Body Armour")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'armour', 'rare', interval)
    return price_obj

def spears(start_date, end_date, spear_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "[Spear]", spear_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "[Spear]", spear_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "[Spear]")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'spear', 'rare', interval)
    return price_obj

def boots(start_date, end_date, boot_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "Boots", boot_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Boots", boot_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Boots")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'boot', 'rare', interval)
    return price_obj

def bows(start_date, end_date, bow_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "[Bow]", bow_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "[Bow]", bow_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "[Bow]")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'bow', 'rare', interval)
    return price_obj

def helmets(start_date, end_date, helmet_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "Helmet", helmet_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Helmet", helmet_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Helmet")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'helmet', 'rare', interval)
    return price_obj

def jewels(start_date, end_date, jewel_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "[Jewel]", jewel_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "[Jewel]", jewel_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "[Jewel]")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'jewel', 'rare', interval)
    return price_obj

def gloves(start_date, end_date, glove_name, interval, history, unit):
    src_data = {}
    if history == 1:
        src_data = network.history_req_item(start_date, end_date, "Gloves", glove_name, interval, unit)
    else:
        src_data = network.req_item(start_date, end_date, "Gloves", glove_name, interval, unit)
    filterd_type = filter.filter_by_type(src_data, "Gloves")
    [rare_items, magic_items, unique_items] = filter.filter_by_rarity(filterd_type)
    price_obj = filter.filter_by_price(rare_items, 'glove', 'rare', interval)
    return price_obj