import os
import json
import re

def _sanitize_filename(name):
    """
    一个辅助函数，用于清理字符串，使其成为合法的文件或目录名。
    它会移除所有不被操作系统允许的特殊字符。
    """
    # 移除或替换掉Windows和Linux/macOS都不允许的字符
    # 替换空格为下划线
    name = name.replace(" ", "_")
    # 移除其他非法字符: < > : " / \ | ? *
    return re.sub(r'[<>:"/\\|?*]', '', name)


def _get_semantic_filepath(date, endDate, type, className, directory="testData"):
    """
    根据参数生成一个具有业务含义的文件路径。
    结构: testData/{type}/{className}/{startDate}_to_{endDate}.json
    """
    # 1. 清理各个部分，确保它们是合法的文件/目录名
    safe_type = _sanitize_filename(type)
    safe_class_name = _sanitize_filename(className)

    # 2. 构建目录路径
    # 例如: testData/MetricA/some_class_name
    dir_path = os.path.join(directory, safe_type, safe_class_name)

    # 3. 构建文件名
    # 例如: 2023-01-01_to_2023-01-31.json
    filename = f"data.json"

    # 4. 返回完整的文件路径
    return os.path.join(dir_path, filename)

def req_item(date, endDate, type, className, interval, unit):
    return read_from_local(date, endDate, type, className, interval, unit)


def read_from_local(date, endDate, type, className, interval, unit):
    """
    根据与req_item同样的参数，从本地的语义化路径读取数据。
    """
    # 1. 根据同样的参数获取应该读取的文件路径
    filepath = _get_semantic_filepath(date, endDate, type, className.replace(" ", "_"))

    # 2. 检查文件是否存在
    if not os.path.exists(filepath):
        print(f"本地示例数据未找到: {filepath}")
        return None

    # 3. 读取并解析JSON文件
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"从本地示例数据成功读取: {filepath}")
        return data
    except (IOError, json.JSONDecodeError) as e:
        print(f"错误：无法读取或解析文件 {filepath}。原因: {e}")
        return None

def history_req_item(date, endDate, type, className, interval, unit):
    return read_from_local(date, endDate, type, className, interval, unit)