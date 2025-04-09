import pandas as pd
import numpy as np

# 定义指标的总权重 (总权重，来自 AHP 分析)
weights = {
    "H1": 0.059241,
    "H2a": 0.237461,
    "H2b": 0.351412,
    "H2c": 0.101887,
    "V1": 0.013103,
    "V2": 0.023973,
    "V3": 0.067652,
    "V4": 0.040493,
    "V5": 0.066864,
    "V6": 0.037916
}

# 假设风险等级划分为 5 级，根据实际数据调整
risk_levels = {
    "极低": 1,
    "低": 2,
    "中等": 3,
    "高": 4,
    "极高": 5
}


# 1. 读取数据
try:
    data = pd.read_csv("E:/NearTerm_Target/CNNFactor/Results/building_risk_assessment2.csv", encoding = "utf_8_sig")
except FileNotFoundError:
    print("文件不存在，请检查路径")
    exit()
# 打印文件信息，确认导入没有问题
print(data.head())
# 2. 风险计算
#H1是沉降速率，危险性，现在需要转换成数字
#思路如下,将风险划分的5个等级定义对应的数字,然后根据不同的沉降速率所处的范围，赋予变量不同的数值。
def calculate_risk_score(row):
        H1 = row['H1']
        H2a = row['H2a']
        H2b = row['H2b']
        H2c = row['H2c']
        V1 = row['V1']
        V2 = row['V2']
        V3 = row['V3']
        V4 = row['V4']
        V5 = row['V5']
        V6 = row['V6']
        return weights['H1']*H1+weights['H2a']*H2a+weights['H2b']*H2b+weights['H2c']*H2c+\
            weights['V1']*V1+weights['V2']*V2+weights['V3']*V3+weights['V4']*V4+\
                weights['V5']*V5+weights['V6']*V6

data['RiskScore'] = data.apply(calculate_risk_score,axis = 1)

print(data['RiskScore'])
# 3. 根据风险评分进行等级划分（请根据实际情况调整）
def assign_risk_level(risk_score):
        if risk_score < 1.5:
            return "极低"
        elif 1.5 <= risk_score < 2.5:
            return "低"
        elif 2.5 <= risk_score < 3.5:
            return "中等"
        elif 3.5 <= risk_score < 4.5:
            return "高"
        else:
            return "极高"

data['RiskLevel'] = data['RiskScore'].apply(assign_risk_level)



# 计算完成，导出
print(data.head())
data.to_csv("building_risk_assessment3.csv", encoding="utf_8_sig", index=False)