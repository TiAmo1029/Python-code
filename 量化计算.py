import pandas as pd
import os # 用于路径操作

# --- 配置 ---
# 重要：请将 'path/to/your/Building_Final_risk_attributes.csv' 替换为你【最终包含所有信息】的 CSV 文件路径
# 这个文件应该有 H1-V6 (数字1-5), RiskLevel (中文), Longitude, Latitude 等列
csv_file_path = 'E:/Totalapp/Pycharm/风险矩阵计算/building_risk_assessment3.csv' # 假设这是你最终的文件，请修改

# 列名配置（根据之前的截图和讨论）
indicator_level_columns = {
    "H1": "H1", "H2a": "H2a", "H2b": "H2b", "H2c": "H2c",
    "V1": "V1", "V2": "V2", "V3": "V3", "V4": "V4", "V5": "V5", "V6": "V6"
}
# 最终风险等级列名（中文文本）
final_risk_level_column_text = 'RiskLevel'
# 经纬度列名（确认它们在你的CSV中）
longitude_column = 'Longitude'
latitude_column = 'Latitude'

# 输出统计结果的CSV文件名
# 获取输入文件所在目录
output_directory = os.path.dirname(csv_file_path)
output_stats_csv = os.path.join(output_directory, 'risk_level_final_statistics_2.csv') # 文件名


# 风险等级名称映射 (用于数字和中文的转换及索引)
risk_level_map_numeric_to_text = {
    1: "极低", 2: "低", 3: "中等", 4: "高", 5: "极高", 0: "未知/空值"
}
risk_level_map_text_to_numeric = {v: k for k, v in risk_level_map_numeric_to_text.items()}
# 预期的最终风险等级中文列表
final_risk_levels_chinese = ["极低", "低", "中等", "高", "极高", "未知/空值"]

# --- 结束配置 ---

def format_statistics_dataframe(stats_df, level_map):
    """格式化统计DataFrame，添加描述并设置统一索引"""
    try:
        # 确保索引是整数，用于映射
        stats_df.index = stats_df.index.astype(int)
        # 添加 '等级描述' 列
        stats_df['等级描述'] = stats_df.index.map(lambda x: level_map.get(x, f'未知({x})'))
        stats_df.index.name = '风险等级值'
        # 设置两层索引: ('等级描述', '风险等级值')
        stats_df = stats_df.set_index('等级描述', append=True).swaplevel(0, 1)

        # 确保所有定义的等级都包含在内
        expected_levels = sorted(level_map.keys())
        multi_index_tuples = [(level_map.get(i, f'未知({i})'), i) for i in expected_levels]
        all_levels_multi_index = pd.MultiIndex.from_tuples(multi_index_tuples, names=['等级描述', '风险等级值'])
        stats_df = stats_df.reindex(all_levels_multi_index, fill_value=0)

    except Exception as e:
        print(f"格式化DataFrame时出错: {e}")
        # 如果出错，至少保留原始索引
        stats_df.index.name = '风险等级值'
    return stats_df

def calculate_numeric_statistics(df, column_name, indicator_name=""):
    """计算数字等级列(1-5)的数量和百分比，并格式化"""
    total_buildings = len(df)
    if total_buildings == 0: return None
    print(f"\n--- 指标: {indicator_name} ({column_name}) ---")
    if column_name not in df.columns:
        print(f"--- 警告: 列 '{column_name}' 未找到! ---")
        return None
    try:
        numeric_series = pd.to_numeric(df[column_name], errors='coerce').fillna(0).astype(int)
        counts = numeric_series.value_counts().sort_index()
    except Exception as e:
        print(f"统计列 '{column_name}' (数值) 时出错: {e}")
        return None
    percentages = (counts / total_buildings * 100).round(2)
    stats_df = pd.DataFrame({'数量': counts, '百分比 (%)': percentages})
    # 使用通用格式化函数
    formatted_stats_df = format_statistics_dataframe(stats_df, risk_level_map_numeric_to_text)
    print(formatted_stats_df)
    return formatted_stats_df

def calculate_text_statistics(df, column_name, indicator_name=""):
    """计算文本等级列(中文)的数量和百分比，并格式化"""
    total_buildings = len(df)
    if total_buildings == 0: return None
    print(f"\n--- 指标: {indicator_name} ({column_name}) ---")
    if column_name not in df.columns:
        print(f"--- 警告: 列 '{column_name}' 未找到! ---")
        return None
    try:
        text_series = df[column_name].astype(str).str.strip().fillna("未知/空值")
        counts = text_series.value_counts()
    except Exception as e:
        print(f"统计列 '{column_name}' (文本) 时出错: {e}")
        return None

    percentages = (counts / total_buildings * 100).round(2)
    stats_df = pd.DataFrame({'数量': counts, '百分比 (%)': percentages})
    stats_df.index.name = '等级描述' # 文本统计以描述为索引

    # --- 构造与数值统计兼容的 MultiIndex ---
    stats_df['风险等级值'] = stats_df.index.map(lambda x: risk_level_map_text_to_numeric.get(x, 0))
    stats_df = stats_df.set_index('风险等级值', append=True) # 现在索引是 ('等级描述', '风险等级值')
    # --------------------------------------

    # 确保所有预期的中文等级都显示
    try:
        # 使用与数值统计相同的目标 MultiIndex
        expected_levels_vals = sorted(risk_level_map_numeric_to_text.keys())
        multi_index_tuples = [(risk_level_map_numeric_to_text.get(i, f'未知({i})'), i) for i in expected_levels_vals]
        all_levels_multi_index = pd.MultiIndex.from_tuples(multi_index_tuples, names=['等级描述', '风险等级值'])

        stats_df = stats_df.reindex(all_levels_multi_index, fill_value=0)
        # 不需要 swaplevel，因为 set_index 已经设置了正确的顺序 ('等级描述', '风险等级值')
    except Exception as reindex_e:
        print(f"重索引DataFrame以包含所有中文等级时出错: {reindex_e}")
        stats_df = stats_df.sort_index()

    print(stats_df)
    return stats_df

# --- 主程序 ---
if __name__ == "__main__":
    all_statistics_list = [] # 改用列表存储，方便控制顺序和添加标签
    try:
        # 读取 CSV 文件
        try:
            df_main = pd.read_csv(csv_file_path, encoding='utf_8_sig')
        except UnicodeDecodeError:
            print("UTF-8-SIG 编码失败，尝试 GBK 编码...")
            df_main = pd.read_csv(csv_file_path, encoding='gbk')
        except FileNotFoundError:
             print(f"错误: 文件 '{csv_file_path}' 未找到。请确保路径正确。")
             exit() # 文件找不到，直接退出

        df_main.columns = df_main.columns.str.strip() # 去除列名空格

        print(f"成功读取文件: {csv_file_path}")
        print(f"可用的列名: {df_main.columns.tolist()}")
        # 检查经纬度列是否存在
        if longitude_column not in df_main.columns or latitude_column not in df_main.columns:
            print(f"警告：未能找到经度 ('{longitude_column}') 或纬度 ('{latitude_column}') 列，请检查配置。")
        print(f"建筑物总数: {len(df_main)}\n")


        # --- 统计各单一指标 (用于 3.1) ---
        print("-" * 50)
        print("各单一指标风险等级统计 (用于 3.1 节)")
        print("-" * 50)
        for indicator, col_name in indicator_level_columns.items():
            stats = calculate_numeric_statistics(df_main, col_name, indicator)
            if stats is not None:
                # 为每个指标的统计结果添加一个'指标'列，用于区分
                stats['指标'] = indicator
                all_statistics_list.append(stats.reset_index()) # 重置索引后存入列表

        # --- 统计最终综合风险等级 (用于 3.2.1) ---
        print("\n" + "=" * 50)
        print("最终综合风险等级统计 (用于 3.2.1 节)")
        print("=" * 50)
        final_stats = calculate_text_statistics(df_main, final_risk_level_column_text, "最终综合风险")
        if final_stats is not None:
            final_stats['指标'] = "最终综合风险"
            all_statistics_list.append(final_stats.reset_index()) # 重置索引后存入列表

        # --- 导出所有统计结果到 CSV ---
        if all_statistics_list: # 如果列表不为空
            # 合并所有统计结果
            combined_stats = pd.concat(all_statistics_list, ignore_index=True)
            # 调整列顺序，使'指标'列在前面
            cols = ['指标', '等级描述', '风险等级值', '数量', '百分比 (%)']
            # 检查所有列是否存在
            cols_exist = [col for col in cols if col in combined_stats.columns]
            combined_stats = combined_stats[cols_exist]


            try:
                combined_stats.to_csv(output_stats_csv, encoding='utf_8_sig', index=False)
                print(f"\n统计结果已成功导出到: {output_stats_csv}")
                print("\n请打开 CSV 文件查看详细统计数据，并将其用于填充论文 3.1 和 3.2.1 节。")
            except PermissionError:
                 print(f"\n导出错误: 没有权限写入文件 '{output_stats_csv}'。")
                 print("请检查文件是否被其他程序占用，或者你是否有该目录的写入权限。")
            except Exception as export_e:
                print(f"\n导出统计结果到 CSV 时出错: {export_e}")
        else:
            print("\n没有有效的统计结果可以导出。")


    except KeyError as e:
         print(f"\n错误: 配置文件中的列名 {e} 在 CSV 文件中未找到。")
         print("请仔细检查脚本'配置'部分的 indicator_level_columns 和 final_risk_level_column")
         if 'df_main' in locals():
              print(f"你的CSV文件实际包含的列名(已去除首尾空格): {df_main.columns.tolist()}")
    except Exception as e:
        print(f"\n发生了一个意料之外的错误: {e}")