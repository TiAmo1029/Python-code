# -*- coding: cp936 -*-
import urllib.request

#����αװһ�����������
headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
k=0.01097#ÿ��ͼ֮���ĵ�λ�� ����17����ͼÿ�����������������ȼ�����Ҫ�Լ�ȥ����
n=int(input("������Ҫ��ȡ��x�����ȱ���"))-1#����˵����Ҫ��ȡ���Χ��ͼֽ��n*k+x1 = x(x�����ȡͼƬ��Χ���½�ͼƬ������x���꣩
x1= 119.996761#������Ҫ��ȡ���ͼ��Χ���Ͻǵ�һ��ͼ����������
y1= 30.299575#������Ҫ��ȡ���ͼ��Χ���Ͻǵ�һ��ͼ����������
index = 0

def get_url(x,y):
    url = 'https://api.tianditu.gov.cn/staticimage?center='+str(x)+','+str(y)+'&width=5120&height=5120&zoom=17&layers=vec_c&tk=095e1a97646c203b113ea9d99cb13853'
    # ����һ��opener
    opener = urllib.request.build_opener()
    # ��headers��ӵ�opener��
    opener.addheaders=[headers]
    # ��opener��װΪȫ��
    urllib.request.install_opener(opener)
    # ��urlopen����ҳ
    data = urllib.request.urlopen(url)
    return data

def file_name(index):
    map_name = 'E://Totalapp//ArcGIS//���ͼ����//hsd2//'+str(index)+'.tif'#����ͼƬ�ļ��У�ע���������� // ������ \
    return map_name

def coordinate_name(index):
    coordinate_name = 'E://Totalapp//ArcGIS//���ͼ����//hsd2//' + str(index) + '.tfw'
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
        print('�ܼ�'+str(pow(n+1,2))+'��ͼƬ '+"�������ص� "+str(index)+' ��ͼƬ')
