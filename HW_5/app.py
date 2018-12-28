import sqlite3
import os
import re
from flask import Flask
from flask import request, render_template
from pymystem3 import Mystem

app = Flask(__name__)


def create_txt():
    with open('request.txt', 'w') as f:
        f.write('')

create_txt()


def database():

    conn = sqlite3.connect('newspaper.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS newspaper(title, url, plain, '
              'mystem, lemma)')

    for root, dirs, files in os.walk('newspaper'):
        for file in files:
            if file.endswith('.txt') and file.startswith('article'):
                plain_path = os.path.join(root, file)
                with open(plain_path, 'r', encoding='utf-8') as file:
                    plain = file.read()
                    title = re.findall('@ti(.*?)\n', plain)
                    title = ''.join(title)
                    url = re.findall('@url(.*?)\n', plain)
                    url = ''.join(url)
                    regMeta = re.compile('@(.*?)\n', re.DOTALL)
                    plain = regMeta.sub('', plain)
                    m = Mystem()
                    lemmas = m.lemmatize(plain)
                    lemmas = ''.join(lemmas)
                    article_number = str(url[-5:])
                    for root, dirs, files in os.walk('newspaper'):
                        for file in files:
                            if file.endswith(article_number + '.txt') and \
                                    file.startswith('morpho_aticle'):
                                morpho_path = os.path.join(root, file)
                                with open(morpho_path, 'r', encoding='utf-8') \
                                        as file:
                                    mystem = file.read()
                                    c.execute('INSERT INTO newspaper VALUES(?,'
                                              '?, ?, ?, ?)', (title, url,
                                                              plain, mystem,
                                                              lemmas))
                                    conn.commit()

    conn.close()

database()


@app.route('/')
def search():
    if request.args:
        search = request.args['search']
        with open('request.txt', 'w', encoding='utf-8') as fl:
            fl.write(search)
        with open('request.txt', 'r', encoding='utf-8') as f1:
            req = f1.read()
            m = Mystem()
            lemma_text = m.lemmatize(req)
            lemma_text = ' ' + str(''.join(lemma_text)) + ' '

        lemma_res = '%' + str(lemma_text).replace('\n', '') + '%'

        conn = sqlite3.connect('newspaper.db')
        c = conn.cursor()

        c.execute("SELECT title, url, plain FROM newspaper WHERE lemma LIKE ?",
                  (lemma_res,))

        rows = c.fetchall()

        res = []
        for row in rows:
            res.append(row)

        return render_template('search.html', search=search, res=res)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)