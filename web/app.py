from flask import Flask, request, render_template, redirect, url_for, jsonify
from translator import translate
import mydb

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/region')
def region():
    return render_template('region.html')


@app.route('/region/<region>')
def getRegionData(region):
    ch_region = translate(region)
    print(ch_region)

    return render_template('region.html')


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