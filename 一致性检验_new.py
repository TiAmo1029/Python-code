import numpy as np

# 定义三个判断矩阵
matrix_H_criteria = np.array([[1, 3],
                             [float(1/3), 1]])

matrix_H_indicators = np.array([[1, float(1/3), float(1/3), float(1/5)],
                                [3, 1, float(1/2), float(1/2)],
                                [3, float(1/2), 1, float(3/2)],
                                [5, float(1/2), float(2/3), 1]])
matrix_V_indicators = np.array([[1, 3, 4, 5, 2, 4],
                                [float(1/3), 1, float(1/2), float(1/3), 1, float(1/2)],
                                [float(1/4), float(1/2), 1, 3, 2, 1],
                                [float(1/5), float(1/3), float(1/3), 1, float(3/2), float(1/2)],
                                [float(1/2), 1, 2/3, 3/2, 1, float(1/2)],
                                [float(1/4), float(1/2), 1, 2, 2, 1]])
RI = {
    1: 0,
    2: 0,
    3: 0.52,
    4: 0.89,
    5: 1.12,
    6: 1.26,
    7: 1.36,
    8: 1.41,
    9: 1.46
}
def calculate_eigen(matrix, name):
    """计算判断矩阵的特征值、特征向量和一致性检验"""
    n = matrix.shape[0] # 获取矩阵维度
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvalue_index = np.argmax(eigenvalues)
    max_eigenvalue = eigenvalues[max_eigenvalue_index].real # 取实部
    max_eigenvector = eigenvectors[:, max_eigenvalue_index].real # 取实部
    normalized_vector = max_eigenvector / np.sum(max_eigenvector)

    # 计算一致性指标 (CI)
    CI = (max_eigenvalue - n) / (n - 1)

    # 计算随机一致性指标 (RI)
    RI_value = RI.get(n)

    print(f"-----{name}-----")
    print("最大特征值 (λmax):", max_eigenvalue)
    print("对应的特征向量:", max_eigenvector)
    print("归一化后的权重向量:", normalized_vector)
    print("一致性指标 (CI):", CI)
    if RI_value is not None and RI_value != 0:
         # 计算一致性比率 (CR)
         CR = CI / RI_value
         print("一致性比率 (CR):", CR)
         if np.isclose(CR,0,atol = 0.1) or CR < 0.1 :
             print("一致性检验通过")
         else:
             print("一致性检验未通过")
    elif RI_value == 0 :
        print("一致性比率 (CR): 0")
        print("该矩阵为2阶，具有天然的一致性，一致性检验通过")
    else:
        print(f"{name}：RI表缺失，无法计算一致性比率 (CR)")
    return max_eigenvalue, normalized_vector

# 计算并打印结果
calculate_eigen(matrix_H_criteria, "准则层 (H) 判断矩阵")
calculate_eigen(matrix_H_indicators, "危险性指标 (H) 判断矩阵")
calculate_eigen(matrix_V_indicators, "脆弱性指标 (V) 判断矩阵")