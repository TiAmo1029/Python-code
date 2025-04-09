def assign_V1_level(v1_func_type_id):
    """根据功能区类型(Id)划分V1风险等级 (1-5)"""
    if v1_func_type_id is None:
        return 0 # 默认未知等级

    try:
        func_id = int(v1_func_type_id)
    except (ValueError, TypeError):
        return 0 # Id 无法转为整数

    # --- 根据最终确认的 Id-风险等级 映射 ---
    if func_id in [0, 5, 12]: return 1 # 其他, 公园, 交通 (极低)
    elif func_id in [10, 11]: return 2 # 政府, 旅游 (低)
    elif func_id in [1, 3, 8, 9]: return 3 # 住宅, 学校, 医院, 办公 (中)
    elif func_id in [2, 6, 7, 13]: return 4 # 工业, 商品工业, 商业, 寺庙(假设13) (高)
    # --- 确认 Id=13 的情况 ---
    else:
        return 0 # 其他未定义的 Id


def assign_V2_level(footprint_ratio):
    """根据建筑覆盖比例 (Building Footprint, 0-1) 划分V2风险等级 (1-5)"""
    if footprint_ratio is None or not isinstance(footprint_ratio, (int, float)) or footprint_ratio < 0:
        return 0
    try:
        ratio = float(footprint_ratio)
        # --- 使用基于实际数据分布 (自然断点) 确定的阈值 ---
        if ratio < 0.000093328: return 1
        elif 0.000093328 <= ratio < 0.00025538: return 2
        elif 0.00025538 <= ratio < 0.000579485: return 3
        elif 0.000579485 <= ratio < 0.001297145: return 4
        else: # >= 0.001297145
            return 5
    except ValueError:
        return 0


def assign_V3_level(density):
    """根据人口密度 (人/km²) 划分V3风险等级 (1-5)"""
    if density is None or not isinstance(density, (int, float)) or density < 0:
        return 0
    try:
        density_km = float(density)
        # --- 使用调整后的人口密度分级标准 ---
        if density_km < 2000: return 1
        elif 2000 <= density_km < 5000: return 2
        elif 5000 <= density_km < 15000: return 3
        elif 15000 <= density_km < 25000: return 4
        else: # >= 25000
            return 5
    except ValueError:
        return 0


def assign_V4_level(majority, variety):
    """根据主要土地覆盖类型(MAJORITY)和类型数量(VARIETY)划分V4风险等级(1-5)"""
    # 处理可能的空值
    if majority is None: return 0
    if variety is None: variety = 1 # 如果多样性缺失，假设为单一类型

    try:
        m = int(majority)
        v = int(variety)
    except (ValueError, TypeError):
        return 0 # 如果无法转换为整数

    # --- 使用土地覆盖风险分级规则 ---
    if m in [7, 9, 10] or m < 0: # 稀疏植被, 水域, 湿地 或 其他未知(假设<0)
        return 1
    elif m in [2, 4]: # 林地, 草地
        return 2
    elif m == 5: # 耕地
        return 3
    elif m == 6: # 建设用地
        if v > 1: return 4 # 混合建设用地
        else: return 5 # 纯建设用地
    else:
        return 0 # 其他未定义情况


import re # 引入正则表达式库，用于提取年份

def extract_year(year_str):
    """
    尝试从包含'年建造'或纯数字年份的文本中提取四位数年份。
    如果成功提取且年份在合理范围 (1900-2029), 则返回整数年份，否则返回 None。
    """
    if year_str is None or str(year_str).strip() == "": # 确保输入不是None且去除前后空格
        return None
    # 转换为字符串以进行处理
    year_str = str(year_str).strip()
    try:
        # 尝试匹配 "YYYY年建造" 格式
        match_format1 = re.search(r'(\d{4})年建造', year_str)
        if match_format1:
            year = int(match_format1.group(1))
            if 1900 < year < 2030: # 设定一个合理的年份范围
                return year
        else:
            # 如果不匹配特定格式，尝试直接转换整个字符串为整数（处理纯数字年份）
            # 确保它确实是四位数年份
            if len(year_str) == 4:
                 year = int(year_str)
                 if 1900 < year < 2030:
                     return year
        return None # 如果没有匹配或转换失败或年份范围不合理
    except (ValueError, TypeError, IndexError):
        return None # 处理各种潜在错误

def assign_V5_level_final(v1_func_type_id, original_year_str):
    """
    根据建筑年代（优先，从文本提取）或功能区类型(Id)（次优先）划分V5风险等级 (1-5)。
    对完全未知的情况赋予默认值。
    v1_func_type_id: 功能区 Id 字段的值
    original_year_str: 建筑年代字段的文本值 (例如 建筑_1)
    """
    # 1. 尝试从文本中提取有效年份
    valid_year = extract_year(original_year_str)

    # 2. 如果提取到有效年份，按年份分级
    if valid_year is not None:
        if valid_year >= 2015: return 1
        elif 2010 <= valid_year < 2015: return 2
        elif 2000 <= valid_year < 2010: return 3
        else: return 4 # < 2000

    # 3. 如果年份无效或缺失，根据 V1 功能区 (Id) 赋予等级
    # 先处理 Id 为 None 或无法转为整数的情况
    if v1_func_type_id is None:
        return 3 # 默认中风险 (你需要确认这个默认值)

    try:
        # 确保功能区ID是整数以便比较
        func_id = int(v1_func_type_id)
    except (ValueError, TypeError):
        return 3 # Id 无法转为整数，用默认值

    # --- 根据最终确认的 Id-风险等级 映射 ---
    if func_id in [0, 5, 12]: # 其他, 公园, 交通
        return 1
    elif func_id in [10, 11]: # 政府, 旅游
        return 2
    elif func_id in [1, 3, 8, 9]: # 住宅, 学校, 医院, 办公
        return 3
    elif func_id in [2, 6, 7, 13]: # 工业, 商品工业, 商业, 寺庙(假设13)
        return 4
    # --- 确认 Id=13 的情况是否包含在此，并且风险是4 ---

    # --- 4. 最终默认值 (适用于未在上面明确列出的 Id 值) ---
    else:
        return 3 # 默认中风险 (你需要最终确认这个默认值)


def assign_height_risk_level(height_value):
    """
    根据建筑高度值（米），划分风险等级 (1-5)。
    height_value: 从GHSL栅格提取的高度值 (单位：米)
    """
    if height_value is None or not isinstance(height_value, (int, float)) or height_value < 0:
        # 处理空值、无效值或负值 (GHSL可能有<0)
        # 赋予默认等级 (例如 0 代表未知, 或 1/3/5 根据策略)
        return 0 # 示例：返回0代表无法评级或未知

    try:
        height = float(height_value) # 确保是浮点数

        # --- 使用你最终确定的、基于米的高度分级阈值 ---
        # --- 以下为示例阈值，请务必替换为你最终确定的标准 ---
        if height < 3:
            return 1 # 极低风险
        elif 3 <= height < 10:
            return 2 # 低风险
        elif 10 <= height < 15:
            return 3 # 中等风险
        elif 15 <= height < 30:
            return 4 # 高风险
        else: # >= 30
            return 5 # 极高风险
    except ValueError:
        # 处理其他无法转换为浮点数的情况
        return 0 # 返回0代表无法评级或未知