# -*- coding: cp936 -*-
import urllib.request

#首先伪装一下浏览器访问
headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
k=0.01097#每张图之间差的单位数 这是17级地图每张相差的数量，其他等级的需要自己去尝试
n=int(input("输入需要爬取的x坐标跨度倍数"))-1#简单来说就是要获取多大范围的图纸，n*k+x1 = x(x代表获取图片范围右下角图片的中心x坐标）
x1= 119.996761#代表需要获取天地图范围左上角第一张图的中心坐标
y1= 30.299575#代表需要获取天地图范围左上角第一张图的中心坐标
index = 0

def get_url(x,y):
    url = 'https://api.tianditu.gov.cn/staticimage?center='+str(x)+','+str(y)+'&width=5120&height=5120&zoom=17&layers=vec_c&tk=095e1a97646c203b113ea9d99cb13853'
    # 创建一个opener
    opener = urllib.request.build_opener()
    # 将headers添加到opener中
    opener.addheaders=[headers]
    # 将opener安装为全局
    urllib.request.install_opener(opener)
    # 用urlopen打开网页
    data = urllib.request.urlopen(url)
    return data

def file_name(index):
    map_name = 'E://Totalapp//ArcGIS//天地图下载//hsd2//'+str(index)+'.tif'#下载图片文件夹，注意间隔符号是 // 而不是 \
    return map_name

def coordinate_name(index):
    coordinate_name = 'E://Totalapp//ArcGIS//天地图下载//hsd2//' + str(index) + '.tfw'
    return coordinate_name

def write_mapfile(n,d):
    f = open(n,'wb')
    f.write(d.read())
    f.close()

def write_coordinatefile(n,x,y):
    content = '''
1.07129E-05
0
-0
-1.07129E-05
{}
{}
    '''.format(x,y)
    f = open(n,'w')
    f.write(content)
    f.close()

for i in range(0,n+1):
    y = y1-i*k
    for j in range(0,n+1):
        x = x1+j*k
        index=index+1
        data = get_url(x,y)
        map_name = file_name(index)
        tfw_name = coordinate_name(index)
        write_coordinatefile(tfw_name, x-0.000010712890625*512, y+0.000010712890625*512)
        write_mapfile(map_name,data)
        print('总计'+str(pow(n+1,2))+'张图片 '+"正在下载第 "+str(index)+' 张图片')
