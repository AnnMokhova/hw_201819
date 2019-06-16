from flask import Flask

from flask import url_for, render_template

app = Flask(__name__)

@app.route('/')
def print():
    return render_template('start.html')

@app.route('/lingvo')
def lingvo():
    return render_template('lingvo.html')

@app.route('/medusa')
def medusa():
    return render_template('medusa.html')

@app.route('/cska')
def cska():
    return render_template('cska.html')


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
