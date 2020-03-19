# encoding=utf-8

from flask import Flask, request, render_template, redirect, url_for, jsonify
from translator import translate
import mydb
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/region/<region>', methods=['GET'])
def getRegionData(region):
    ch_region = translate(region)
    data = mydb.readData(ch_region)
    print('hello')
    data = json.dumps(data, ensure_ascii=False)
    # return jsonify(dict(region=region, data=data))
    return render_template('region.html', region=region, data=data)
    # return data


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/', methods=['GET', 'POST'])
def getRegion():
    if request.method == 'POST':
        region = str(request.get_data(), encoding='utf-8')
        print(region)
        return jsonify(dict(state=True, redirect=url_for('getRegionData', region=region)))


if __name__ == "__main__":
    app.run(debug=True)