# encoding=utf-8

import mysql.connector
import json
import random

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
    # if i[0] not in periods:
      # periods.append(i[0])
    if {'name': i[0]} not in periods:
      periods.append({'name': i[0]})
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
  genre['name'] = g
  genre['children'] = w
  return genre


def formDictPeriods(p, g):
  period = {}
  period['name'] = p
  period['children'] = g
  return period


def formDictRegion(r, p):
  region = {}
  # region['region'] = {'name': r }
  region['name'] = r
  region['children'] = p
  return region


# 调用各种函数整理数据
def sortPeriodData(r, d):
  periods = getPeriods(d)
  data = {}
  # periods_dicts = []
  # for i in periods:
  #   genres = getGenres(r, i)
  #   genres_dicts = []
  #   for j in genres:
  #     writers = getWriters(r, i , j)
  #     writers_dicts = []
  #     # print(writers)
  #     # 构造要被json化的字典
  #     for k in writers:
  #       writers_dicts.append(formDictWriters(k))
  #     genres_dicts.append(formDictGenres(j, writers_dicts))
  #   periods_dicts.append(formDictPeriods(i, genres_dicts))
  #   data = formDictRegion(r, periods_dicts)
    # print(json.dumps(data, ensure_ascii=False))
  data = formDictRegion(r, periods)
  return data


def sortGenreData(r, p, g):
  data = {}
  genres_dicts = []
  for j in g:
    writers = getWriters(r, p , j)
    writers_dicts = []
    # print(writers)
    # 构造要被json化的字典
    for k in writers:
      writers_dicts.append(formDictWriters(k))
    genres_dicts.append(formDictGenres(j, writers_dicts))
  data = formDictPeriods(p, genres_dicts)
  # print(data)
  return data


def sortForWordCloud(d):
  data = []
  random.shuffle(d)
  if len(d) <= 50:
    for i in d:
      data.append(i[0])
      if i[1]:
        data.append(i[1])
  else:
    for i in range(50):
      data.append(d[i][0])
      if d[i][1]:
        data.append(d[i][1])
  print(data)
  return list(set(data))


def readPeriodData(r):
  sql = "SELECT period, genre, writer, tags, works FROM regions \
      WHERE region = %s"
  # print(r)
  mycursor.execute(sql, (r,))
  data = mycursor.fetchall()
  sorted_data = sortPeriodData(r, data)
  # mydb.close()
  return sorted_data


def readGenreData(r, p):
  genres = getGenres(r, p)
  sorted_data = sortGenreData(r, p, genres)
  return sorted_data


def readWriterPerPeriod(r):
  sql = "SELECT writer, works FROM regions \
      WHERE region = %s"
  mycursor.execute(sql, (r,))
  data = mycursor.fetchall()
  # print(data)
  return sortForWordCloud(data)


def ifRegionExit(r):
  sql = "select period from regions where region = %s"
  mycursor.execute(sql, (r,))
  data = mycursor.fetchall()
  if data:
    return True
  else:
    return False


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


if __name__ == "__main__":
  data = readPeriodData("日本")
  print(data)