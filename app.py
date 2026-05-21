from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def prinpage():
    return render_template('index.html')


@app.route('/information')
def information():
    return render_template('info.html')

@app.route('/conceps')
def conceps():
    return render_template('conceps.html')

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    return render_template('classification.html')

if __name__ == '__main__':
    app.run(debug=True)