from filter.amulet_filter import filter_amulet_by_price
from filter.armour_filter import filter_armour_by_price
from filter.boot_filter import filter_boot_by_price
from filter.bow_filter import filter_bow_by_price
from filter.glove_filter import filter_glove_by_price
from filter.helmet_filter import filter_helmet_by_price
from filter.jewel_filter import filter_jewel_by_price
from filter.ring_filter import filter_rings_by_price
from filter.spear_filter import filter_spear_by_price

item_catogries = {
    "[Jewel]": ["Sapphire", "Emerald", "Time-Lost Diamond"],
    "Ring": ["Breach Ring", "Lazuli Ring", "Iron Ring", "Topaz Ring",
             "Emerald Ring", "Sapphire Ring", "Prismatic Ring", "Amethyst Ring"],
    "[Bow]": ["Gemini Bow"],
    "Helmet": ["Kamasan Tiara"],
    "Boots": ["Sandsworn Sandals"],
    "Body Armour": ["Vile Robe", "Slipstrike Vest"],
    "Amulet": ["Solar Amulet"],
    "[Spear]": ["Spiked Spear", "Seaglass Spear"],
    "Gloves": ["Vaal Gloves"]
}

def filter_by_type(data, type):
    catogories = item_catogries[type]
    result = {}
    for item in data:
        item_class = item["item"]["baseType"]
        if item_class in catogories:
            if item_class not in result:
                result[item_class] = []
            result[item_class].append(item)   
    return result

def filter_by_rarity(data):
    rare_items = {}
    magic_items = {}
    unique_items = {}
    for item_class in data:
        rare_items[item_class] = []
        magic_items[item_class] = []
        unique_items[item_class] = []
    for item_class in data:
        items = data[item_class]
        for item in items:
            if item["item"]["rarity"] == 'Rare':
                rare_items[item_class].append(item)
            elif item["item"]["rarity"] == 'Magic':
                magic_items[item_class].append(item)
            elif item["item"]["rarity"] == "Unique":
                unique_items[item_class].append(item)
    return [rare_items, magic_items, unique_items]

def filter_by_corrupted(data):
    pass

def filter_by_price(data, type, rarity, interval):
    price_obj = {}
    if type == 'jewel':
        price_obj = filter_jewel_by_price(data, type, rarity, interval)
    elif type == 'ring':
        price_obj = filter_rings_by_price(data, type, rarity, interval)
    elif type == 'bow':
        price_obj = filter_bow_by_price(data, type, rarity, interval)
    elif type == 'helmet':
        price_obj = filter_helmet_by_price(data, type, rarity, interval)
    elif type == 'boot':
        price_obj = filter_boot_by_price(data, type, rarity, interval)
    elif type == 'armour':
        price_obj = filter_armour_by_price(data, type, rarity, interval)
    elif type == 'amulet':
        price_obj = filter_amulet_by_price(data, type, rarity, interval)
    elif type == 'spear':
        price_obj = filter_spear_by_price(data, type, rarity, interval)
    elif type == 'glove':
        price_obj = filter_glove_by_price(data, type, rarity, interval)
    return price_obj