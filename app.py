from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def prinpage():
    return render_template('index.html')


@app.route('/information')
def information():
    return render_template('info.html')
