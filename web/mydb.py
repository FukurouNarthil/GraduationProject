# encoding=utf-8

import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",       # 数据库主机地址
  user="root",    # 数据库用户名
  password="123456",     # 数据库密码
  database="literature",
  charset="utf8"
)
mycursor = mydb.cursor()


# 按时代分隔数组
def getPeriods(d):
  periods = []
  for i in d:
    if i[0] not in periods:
      periods.append(i[0])
  return periods


# 根据国家和时代取体裁
def getGenres(r, p):
  sql = "SELECT genre FROM regions \
      WHERE region = %s AND period = %s"
  mycursor.execute(sql, (r, p))
  genres = [item[0] for item in mycursor.fetchall()]
  return list(set(genres))


# 根据体裁取作家
def getWriters(r, p, g):
  sql = "SELECT writer, tags, works FROM regions \
      WHERE region = %s AND period = %s AND genre = %s"
  mycursor.execute(sql, (r, p, g))
  writer = mycursor.fetchall()
  return writer


# 构造要被json化的字典
def formDictWriters(w):
  writer = {}
  writer['name'] = w[0]
  writer['tags'] = w[1]
  writer['works'] = w[2]
  return writer


def formDictGenres(g, w):
  genre = {}
  genre['genre'] = g
  genre['writers'] = w
  return genre


def formDictPeriods(p, g):
  period = {}
  period['period'] = p
  period['genres'] = g
  return period


def formDictRegion(r, p):
  region = {}
  region['region'] = r
  region['periods'] = p
  return region


# 调用各种函数整理数据
def sortData(r, d):
  periods = getPeriods(d)
  data = {}
  periods_dicts = []
  for i in periods:
    genres = getGenres(r, i)
    genres_dicts = []
    for j in genres:
      writers = getWriters(r, i , j)
      writers_dicts = []
      # print(writers)
      # 构造要被json化的字典
      for k in writers:
        writers_dicts.append(formDictWriters(k))
      genres_dicts.append(formDictGenres(j, writers_dicts))
    periods_dicts.append(formDictPeriods(i, genres_dicts))
    data = formDictRegion(r, periods_dicts)
    print(json.dumps(data, ensure_ascii=False))
  return data


def readData(r):
  sql = "SELECT period, genre, writer, tags, works FROM regions \
      WHERE region = %s"
  mycursor.execute(sql, (r,))
  data = mycursor.fetchall()
  sorted_data = sortData(r, data)
  mydb.close()
  return sorted_data


if __name__ == "__main__":
  data = readData("日本")
  print(data)