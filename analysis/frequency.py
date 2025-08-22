import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
from mlxtend.frequent_patterns import apriori

x_label_name = "价位区间(d)"
def analyze_affix_popularity(equipment_data, top_n=21):
    print("生成词缀热力图...")
    price_tiers = {}
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 统计各价格区间的词缀出现次数
    for price, items in equipment_data.items():
        for item_name, item_data in items.items():
            if "ones" in item_data:
                for stat, stat_data in item_data["ones"].items():
                    if price not in price_tiers:
                        price_tiers[price] = {}
                    price_tiers[price][stat] = price_tiers[price].get(stat, 0) + stat_data["count"]

    # 处理数据，选取每个价格区间的 TOP N 词缀
    heatmap_data = {}
    for price, stats in price_tiers.items():
        sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)[:top_n]
        heatmap_data[price] = {stat: count for stat, count in sorted_stats}

    # 转换为 DataFrame
    df = pd.DataFrame(heatmap_data).fillna(0)

    # 画热力图
    plt.figure(figsize=(20, 12))
    sns.heatmap(df, annot=True, cmap="YlGnBu", fmt=".0f")
    plt.title(f"Top{top_n} 热门词缀频率",
                fontsize=20,
                color='#2C3E50',
                fontweight='bold',
                pad=25)
    plt.xlabel(x_label_name, fontsize=18, color='#2980B9', labelpad=15)
    plt.ylabel("词缀", fontsize=18, color='#2980B9', labelpad=15)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45)
    plt.savefig('heatmap.webp', format='webp', dpi=300)
    plt.show()

def plot_price_tier_distribution(equipment_data, desc="装备"):
    print("生成价位统计柱状图...")
    total_counts = {}
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # 统计每个价格区间的装备总量
    for price, items in equipment_data.items():
        total_counts[price] = sum(item_data.get("count", 0) for item_data in items.values())

    total_sum = sum(total_counts.values())
    # **绘制柱状图**
    plt.figure(figsize=(10, 6))
    price_labels = list(total_counts.keys())
    price_values = list(total_counts.values())

    ax = sns.barplot(x=price_labels, y=price_values, palette="OrRd")  # 更鲜艳的配色

    # **在每个柱子上方显示数值**
    for i, value in enumerate(price_values):
        ax.text(i, value + 0.5, str(value), ha='center', fontsize=12, fontweight='bold', color="black")

    plt.title(f"{desc}统计总数:{total_sum}", fontsize=14, fontweight='bold')
    plt.xlabel(x_label_name, fontsize=12)
    plt.ylabel("数量", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # 添加背景网格线提升可读性
    plt.savefig('histograms.webp', format='webp', dpi=300)
    plt.show()

def plot_affix_pairs_bubble_chart(equipment_data, top_n=3):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    print("生成词缀组合图...")
    # 统计每个价格区间内的词缀组合
    data = []

    # 遍历价格区间
    for price, items in equipment_data.items():
        for item_name, item_data in items.items():  # 遍历装备
            if "pairs" in item_data:  # 确保存在词缀组合
                sorted_pairs = sorted(item_data["pairs"].items(), key=lambda x: x[1]["count"], reverse=True)[:top_n]
                for pair, info in sorted_pairs:
                    data.append({"Price": str(price), "Pair": pair, "Count": info["count"]})  # 统一格式

    # 转换为 DataFrame
    df = pd.DataFrame(data)

    if df.empty:
        print("数据为空，无法绘制气泡图")
        return

    # print(df.head())  # ✅ 确保数据格式正确

    # 画气泡图
    plt.figure(figsize=(20, 12))
    sns.scatterplot(
        x=df["Price"], y=df["Pair"], size=df["Count"], hue=df["Price"],  # 显式传递 df 的列
        sizes=(20, 500), palette="coolwarm", edgecolor="black", alpha=0.7
    )

    plt.title(f"每价位Top {top_n} 词缀组合", fontsize=14)
    plt.xlabel("价位区间(d)", fontsize=12)
    plt.ylabel("词缀组合", fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title="Price Tier")
    plt.savefig('bubble.png', dpi=300)
    plt.show()

def extract_transactions_by_price(data):
    transactions_by_price = {}

    for price_range, item_data in data.items():
        transactions = []
        transaction_counts = []  # 记录每个组合的出现次数

        for item_name, item_info in item_data.items():
            pairs = item_info.get('pairs', {})
            for affix_combination, details in pairs.items():
                affix_list = tuple(affix_combination.split(","))
                count = details.get("count", 1)  # 记录该组合的出现次数

                transactions.append(affix_list)
                transaction_counts.append(count)

        transactions_by_price[price_range] = (transactions, transaction_counts)  # ✅ 返回二元组

    return transactions_by_price

def mine_frequent_itemsets(transactions, transaction_counts, min_support=0.1):
    if not transactions:
        return pd.DataFrame(), pd.DataFrame()  # 避免传入空列表导致错误

    # 获取所有唯一的词缀
    unique_affixes = sorted(set(affix for t in transactions for affix in t))

    # 构造DataFrame，并结合 transaction_counts 进行权重处理
    df = pd.DataFrame([{affix: (affix in transaction) for affix in unique_affixes} for transaction in transactions])

    # 将权重（出现次数）应用到 DataFrame
    df["support_weight"] = transaction_counts

    # 运行 apriori 算法，计算支持度
    frequent_itemsets = apriori(df.drop(columns=["support_weight"]),
                                min_support=min_support,
                                use_colnames=True)

    # 重新计算支持度，使其基于真实出现次数
    total_occurrences = sum(transaction_counts)  # 计算所有组合的总数
    frequent_itemsets["support"] = frequent_itemsets["itemsets"].apply(
        lambda itemset: sum(df["support_weight"][df[list(itemset)].all(axis=1)]) / total_occurrences
    )

    # 调试信息：检查频繁项集数据
    # print(f"挖掘到的频繁项集数量: {len(frequent_itemsets)}")
    # print(frequent_itemsets.head())  # 打印前几行，查看数据格式

    return frequent_itemsets, frequent_itemsets  # 返回两个DataFrame：频繁项集和筛选规则

def plot_bubble_chart(all_rules, affix_count, chart_title, top_n=5):
    """
    参数说明：
    - all_rules: 字典结构，格式为 {价格区间: (rules_df, total_combinations)}
    - affix_count: 词缀数量 (2/3/4)
    - chart_title: 图表主标题
    - top_n: 每个区间显示前N个组合
    """
    # 创建画布和坐标轴
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.set_facecolor("#FFF3E0")

    # 设置暖色系主题 (需seaborn>=0.11)
    sns.set_theme(style="whitegrid",
                  palette="autumn",  # 基础调色板
                  rc={
                      "axes.facecolor": "#FFF3E0",  # 浅米色背景
                      "grid.color": "#FFE0B2"  # 浅橙色网格线
                  })
    plt.rcParams['font.sans-serif'] = ['SimHei']

    # 可视化参数配置
    max_bubble_size = 1800  # 最大气泡尺寸基准
    cmap = cm.get_cmap("YlOrRd")  # 黄橙红渐变
    edge_color = '#B34700'  # 深橙色轮廓
    alpha_level = 0.85  # 透明度

    # 构建统一的Y轴坐标系
    all_combinations = set()
    for price_range, (rules, _) in all_rules.items():
        if not rules.empty:
            top_rules = rules.sort_values('support', ascending=False).head(top_n)
            all_combinations.update(top_rules['itemsets'].apply(lambda x: ", ".join(sorted(x))))

    # 处理空数据情况
    if not all_combinations:
        ax.text(0.5, 0.5, '无可用数据', ha='center', va='center', fontsize=16)
        plt.draw()
        return

    label_mapping = {label: idx for idx, label in enumerate(sorted(all_combinations))}

    # 主绘图循环
    for price_range, (rules, total_combinations) in all_rules.items():
        if rules.empty:
            continue

        # 筛选并排序Top N组合
        rules = rules.sort_values('support', ascending=False).head(top_n)
        if rules.empty:
            continue

        # 标准化处理（区间内相对比例）
        max_support = rules['support'].max()
        normalized_support = rules['support'] / max_support if max_support > 0 else 0

        affix_combinations = rules['itemsets'].apply(lambda x: ", ".join(sorted(x)))
        y_positions = [label_mapping[comb] for comb in affix_combinations]

        # 绘制气泡图
        ax.scatter(
            x=[price_range] * len(rules),
            y=y_positions,
            s=rules['support'] * max_bubble_size,
            c=normalized_support,
            cmap=cmap,
            alpha=alpha_level,
            edgecolors=edge_color,
            linewidths=1.5,
            zorder=3
        )

    # 坐标轴美化
    ax.set_yticks(ticks=list(label_mapping.values()))
    ax.set_yticklabels(list(label_mapping.keys()),
                       fontsize=10,
                       color='#6B3E00')  # 深棕色标签

    ax.set_xlabel(x_label_name,
                  fontsize=12,
                  labelpad=10,
                  color='#6B3E00')  # 统一文字颜色

    ax.set_ylabel(f"{affix_count}词缀组合",
                  fontsize=12,
                  labelpad=10,
                  color='#6B3E00')

    # 标题设置
    ax.set_title(f"{chart_title}\n(气泡大小和颜色深浅均表示该组合在对应价格区间的出现比例)",
                 fontsize=14,
                 pad=20,
                 color='#8B2500',  # 深红色标题
                 weight='semibold')

    # 网格线设置
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)

    # X轴标签旋转
    plt.xticks(rotation=45,
               ha='right',
               color='#6B3E00')  # 刻度文字颜色

    # 颜色条设置
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, pad=0.02)

    # 颜色条美化
    cbar.set_label('区间内相对比例',
                   rotation=270,
                   labelpad=25,
                   color='#6B3E00')
    cbar.outline.set_edgecolor('#B34700')  # 边框颜色
    cbar.ax.tick_params(color='#6B3E00')  # 刻度线颜色
    plt.setp(cbar.ax.get_yticklabels(), color='#6B3E00')  # 刻度文字

    # 添加气泡尺寸图例
    def add_size_legend():
        legend_supports = [0.1, 0.3, 0.5]
        legend_elements = [
            plt.scatter([], [],
                        s=s * max_bubble_size,
                        c='#FF6F00',  # 统一橙色
                        alpha=alpha_level,
                        edgecolors=edge_color,
                        linewidths=1.5,
                        label=f'{s:.0%} 出现比例')
            for s in legend_supports
        ]
        ax.legend(
            handles=legend_elements,
            loc='upper right',
            title="气泡大小说明",
            title_fontsize=10,
            bbox_to_anchor=(1.28, 1),
            labelcolor='#6B3E00',  # 图例文字颜色
            frameon=True,
            edgecolor='#FFE4B5'  # 图例边框颜色
        )

    add_size_legend()
    plt.tight_layout()
    fig = plt.gcf()
    fig.text(
        x=0.8,
        y=0.15,
        s="@bilibili 宅本熊",
        fontsize=54,
        color='gray',
        alpha=0.3,
        ha='right',
        va='bottom',
        rotation=0,
        zorder=100
    )
    plt.savefig(f'bubble{affix_count}.webp', format='webp', dpi=300)
    plt.show()
    plt.close()

def plot_3_affix_pairs_bubble_chart(data, top_n=3):
    # 提取价位区间的交易数据
    transactions_by_price = extract_transactions_by_price(data)

    # 存储不同词缀数量的频繁项集
    all_rules_2, all_rules_3, all_rules_4 = {}, {}, {}

    for price_range, (transactions, transaction_counts) in transactions_by_price.items():
        total_combinations = sum(transaction_counts)  # 计算当前价位区间的总组合数

        # 进行频繁项集挖掘
        frequent_itemsets, rules = mine_frequent_itemsets(transactions, transaction_counts, min_support=0.05)
        # 调试信息：查看挖掘的规则
        # **修正：检查 rules 是否为空**
        # 调试信息：查看挖掘的规则
        if rules.empty:
            continue  # 如果当前区间没有挖掘到频繁项集，则跳过

        # 分类存储 2、3、4 词缀的关联规则
        # 2 词缀：只存储 2 词缀组合
        all_rules_2[price_range] = (rules[rules['itemsets'].apply(lambda x: len(x) == 2)], total_combinations)
        all_rules_3[price_range] = (rules[rules['itemsets'].apply(lambda x: len(x) == 3)], total_combinations)
        all_rules_4[price_range] = (rules[rules['itemsets'].apply(lambda x: len(x) == 4)], total_combinations)

    plot_bubble_chart(all_rules_2, 2, "2 词缀组合", top_n=3)
    plot_bubble_chart(all_rules_3, 3, "3 词缀组合", top_n=3)
    plot_bubble_chart(all_rules_4, 4, "4 词缀组合", top_n=3)
    plt.show()