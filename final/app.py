from flask import Flask

from flask import url_for, render_template

app = Flask(__name__)

@app.route('/')
def print():
    return render_template('final.html')


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
