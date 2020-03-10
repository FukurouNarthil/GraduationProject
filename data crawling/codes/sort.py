import re
import os 
import sys
import mysql.connector

p_period = re.compile(r'[[](.*?)[]]', re.S)
p_writer = re.compile(".*- (.*)：.*")
p_tags = re.compile(".*（(.*)）.*")
p_works = re.compile(".*《(.*)》.*")
mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  password="123456",     # 数据库密码
  database="literature"
)
mycursor = mydb.cursor()


# 输入数据库
def inputDatabase(r, p, g, w, t, wo):
  sql = "INSERT INTO regions (region, period, genre, writer, tags, works) \
            VALUES (%s, %s, %s, %s, %s, %s)"
  val = (r, p, g, w, t, wo)
  mycursor.execute(sql, val)
  mydb.commit()
  print(val)


# 处理格式
def sortForm(d, r):
  d = d.split('\n\n')
  for i in d:
    period = re.findall(p_period, i)[0]
    i = i.split(']')[1].split('\n<')
    i.pop(0)
    genres = i
    for j in genres:
      genre = j.split('>\n')[0]
      writers = j.split('>\n')[1].split('\n')
      for k in writers:
        writer = re.findall(p_writer, k)[0]
        tags = re.findall(p_tags, k)[0]
        works = re.findall(p_works, k)[0]
        inputDatabase(r, period, genre, writer, tags, works)


# 读取txt文件
def readFile():
  Path = 'D:\\Learning\\GraduationProject\\data crawling\\codes\\data_per_region'
  files = os.listdir(Path)
  for file in files:
    region = file[:-6]
    cpath = os.path.join(Path, file)
    with open(cpath, 'r', encoding='utf-8') as cfile:          
      data = cfile.read()
      if data:
        sortForm(data, region)


if __name__ == "__main__":
  readFile()
  mydb.close()
