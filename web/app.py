from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/region')
def region():
    return render_template('region.html')


@app.route('/')
def main():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)