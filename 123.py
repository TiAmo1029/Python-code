import requests
import csv
import chardet

API_KEY = '6c5cf6d027ceacbde0f5694ce8530543'  # 替换为你的高德API密钥
input_file = 'E:/Totalapp/Pycharm/pq/58tongchenglg.csv'  # 替换为你的CSV文件路径
output_file = 'E:/Totalapp/Pycharm/pq/小区信息_带经纬度230.csv'  # 替换为你的输出CSV文件路径

def get_lat_lng(query):
    url = f'https://restapi.amap.com/v3/geocode/geo?address={query}&key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        geocodes = response.json().get('geocodes')
        if geocodes:
            location = geocodes[0].get('location')
            lng, lat = location.split(',')
            return float(lat), float(lng)
    return None, None

# 处理地址信息
def clean_address(address):
    # 去除多余空格
    address = address.strip()
    # 替换特殊字符（根据实际情况修改）
    address = address.replace('，', ',')
    return address

# 检测文件编码
with open(input_file, 'rb') as f:
    result = chardet.detect(f.read())
    encoding = result['encoding']

with open(input_file, 'r', encoding=encoding) as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile)  # 使用 csv.reader 读取 CSV 数据
    fieldnames = ['房源名称', '面积', '朝向', '楼层', '建筑年份', '价格', '地址', '纬度', '经度']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # 从CSV文件中提取必要的信息
        community_name = row[0]  # 房源名称
        # 使用更详细的地址信息进行搜索
        query = f"{clean_address(row[6])} {clean_address(community_name)}"  # 使用地址信息和小区名称
        lat, lng = get_lat_lng(query)
        # 如果第一次编码失败，尝试使用不同的地址信息进行再次编码
        if lat is None:
            query = f"{clean_address(row[6])} {clean_address(row[1])} {clean_address(community_name)}"  # 使用地址信息、面积和小区名称
            lat, lng = get_lat_lng(query)
        # 将编码结果写入CSV文件
        writer.writerow({
            '房源名称': community_name,
            '面积': row[1],
            '朝向': row[2],
            '楼层': row[3],
            '建筑年份': row[4],
            '价格': row[5],
            '地址': row[6],
            '纬度': lat,
            '经度': lng
        })