import numpy as np

# 定义三个判断矩阵
matrix_H_criteria = np.array([[1, 3],
                                [1/3, 1]])

matrix_H_indicators = np.array([[1, 1, 1/3, 1/5, 1/5, 1/7, 1/5],
                                [1, 1, 1/3, 1/5, 1/5, 1/7, 1/5],
                                [3, 3, 1, 1/3, 1/3, 1/5, 1/3],
                                [5, 5, 3, 1, 1/2, 1/3, 1/2],
                                [7, 7, 5, 2, 1, 3/2, 2],
                                [5, 5, 3, 2, 3/2, 1, 2],
                                [5, 5, 3, 2, 1/2, 1/2, 1]])
matrix_V_indicators = np.array([[1, 1/3, 1/5, 1/4, 1/5, 1/2, 1/4],
                                [3, 1, 1/3, 1/2, 1/3, 1, 1/2],
                                [5, 3, 1, 2, 1/2, 3, 2],
                                [4, 2, 1/2, 1, 1/3, 2, 1],
                                [5, 3, 2, 3, 1, 3/2, 1/2],
                                [2, 1, 1/3, 1/2, 2/3, 1, 1/2],
                                [4, 2, 1/2, 1, 2, 2, 1]])
def calculate_eigen(matrix, name):
    """计算判断矩阵的特征值和特征向量"""
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    max_eigenvalue_index = np.argmax(eigenvalues)
    max_eigenvalue = eigenvalues[max_eigenvalue_index]
    max_eigenvector = eigenvectors[:, max_eigenvalue_index]
    normalized_vector = max_eigenvector / np.sum(max_eigenvector)

    print(f"-----{name}-----")
    print("最大特征值:", max_eigenvalue)
    print("对应的特征向量:", max_eigenvector)
    print("归一化后的权重向量:", normalized_vector)
    return max_eigenvalue, normalized_vector

# 计算并打印结果
calculate_eigen(matrix_H_criteria, "准则层 (H) 判断矩阵")
calculate_eigen(matrix_H_indicators, "危险性指标 (H) 判断矩阵")
calculate_eigen(matrix_V_indicators, "脆弱性指标 (V) 判断矩阵")