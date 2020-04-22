# encoding=utf-8

from flask import Flask, request, render_template, redirect, url_for, jsonify, flash
from translator import translate
import mydb
import json
import time

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.secret_key = 'random string'


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/region/<region>/<period>', methods=['GET'])
def getPeriodData(region, period):
    ch_region = translate(region)
    data = mydb.readGenreData(ch_region, period)
    data = json.dumps(data, ensure_ascii=False)
    return render_template('period.html', region=region, ch_region=ch_region, period=period, data=data)


@app.route('/region/<region>', methods=['GET', 'POST'])
def getRegionData(region):
    ch_region = translate(region)
    if request.method == 'GET':
        data = mydb.readPeriodData(ch_region)
        data = json.dumps(data, ensure_ascii=False)
        writers = mydb.readWriterPerPeriod(ch_region)
        writers = json.dumps(writers, ensure_ascii=False)
        return render_template('region.html', region=region, ch_region=ch_region, data=data, words=writers)
    elif request.method == 'POST':
        period = str(request.get_data(), encoding='utf-8')
        return jsonify(dict(state=True, redirect=url_for('getPeriodData', region=region, period=period)))
        # return render_template('period.html', region=region, period=period, data=data)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def getRegion():
    if request.method == 'POST':
        region = str(request.get_data(), encoding='utf-8')
        # print(region)
        if mydb.is_contains_chinese(region) == False:
            ch_region = translate(region)
        # print(region)
        if mydb.ifRegionExit(ch_region):
            return jsonify(dict(state=True, redirect=url_for('getRegionData', region=region)))
        else:
            return jsonify(dict(state=False))


if __name__ == "__main__":
    app.run(debug=True)