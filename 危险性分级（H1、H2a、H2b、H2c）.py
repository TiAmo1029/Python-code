def assign_H1_level(velocity):
    """根据平均沉降速率 (mm/year) 划分H1风险等级 (1-5)"""
    if velocity is None or not isinstance(velocity, (int, float)):
        return 0 # 处理空值或无效值
    try:
        rate = float(velocity)
        # --- 使用你最终确认的沉降速率分级标准 ---
        if rate <= -0.04: return 1 # 极低风险 (假设, 需要确认负值含义和标准)
        elif -0.04 < rate <= -0.006: return 2 # 低风险 (假设)
        elif -0.006 < rate <= 0.018: return 3 # 中等风险
        elif 0.018 < rate <= 0.036: return 4 # 高风险
        else: # > 0.036
            return 5 # 极高风险
    except ValueError:
        return 0 # 处理转换错误

def assign_H2a_level(elevation):
    """根据平均高程 (米) 划分H2a风险等级 (1-5)"""
    if elevation is None or not isinstance(elevation, (int, float)):
        return 0 # 处理空值或无效值
    try:
        elev = float(elevation)
        # --- 使用你最终确认的高程分级标准 (考虑负值和实际分布) ---
        if elev <= -7: return 1 # 极低风险 (示例, 基于你的数据调整)
        elif -7 < elev <= 0: return 2 # 低风险 (示例)
        elif 0 < elev <= 48: return 3 # 中等风险 (示例)
        elif 48 < elev <= 116: return 4 # 高风险 (示例)
        else: # > 116
             return 5 # 极高风险 (示例)
        # --- 或者使用之前的标准 ---
        # if elev < 0: return 1
        # elif 0 <= elev < 10: return 2
        # elif 10 <= elev < 30: return 3
        # elif 30 <= elev < 60: return 4
        # else: return 5 # >= 60
    except ValueError:
        return 0

def assign_H2b_level(slope):
    """根据平均坡度 (度) 划分H2b风险等级 (1-5)"""
    if slope is None or not isinstance(slope, (int, float)) or slope < 0: # 坡度通常>=0
        return 0
    try:
        s = float(slope)
        # --- 使用标准坡度分级 ---
        if s > 15: return 1
        elif 8 < s <= 15: return 2
        elif 3 < s <= 8: return 3
        elif 1 < s <= 3: return 4
        else: # <= 1
            return 5
    except ValueError:
        return 0


def assign_H2c_level(aspect):
    """根据平均坡向 (度) 划分H2c风险等级 (1-5)"""
    if aspect is None or not isinstance(aspect, (int, float)):
        return 0
    try:
        a = float(aspect)
        # --- 使用标准坡向分级 (-1 和 0-360 循环) ---
        if a == -1 or (315 <= a <= 360) or (0 <= a < 22.5): return 1 # 平坦或北
        elif 157.5 <= a < 202.5: return 2 # 南
        elif (112.5 <= a < 157.5) or (202.5 <= a < 247.5): return 3 # 东南或西南
        elif (67.5 <= a < 112.5) or (247.5 <= a < 292.5): return 4 # 东或西
        elif (22.5 <= a < 67.5) or (292.5 <= a < 315): return 5 # 东北或西北
        else: return 0 # 处理其他异常值
    except ValueError:
        return 0