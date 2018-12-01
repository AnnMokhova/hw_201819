import matplotlib.pyplot as plt

from flask import Flask

from flask import url_for, render_template, request


app = Flask(__name__)


#  Создает csv-файл, в который будут записываться все ответы.
#  Создает 4 текстовых файла, в который будут записываться
#  значимые для статистики ответы. Названия файлов
#  соответствуют числу объекта и субъекта предложений.
#  В анкете исследуется, может ли форма числа объекта
#  повлиять на спряжение респондентом сказуемого.

def intro():
    data = 'Пол\tВозраст\tМесто рождения\tsg+sg\tsg+pl\tpl+sg\tpl+pl\n'

    with open('results.csv', 'w') as f:
        f.write(data)

    with open('sg_sg.txt', 'w') as fl_1:
        fl_1.write(' ')

    with open('sg_pl.txt', 'w') as fl_2:
        fl_2.write(' ')

    with open('pl_sg.txt', 'w') as fl_3:
        fl_3.write(' ')

    with open('pl_pl.txt', 'w') as fl_4:
        fl_4.write(' ')

    with open('json.txt', 'w') as data:
        data.write('')

    with open('search_res.txt', 'w', encoding='utf-8') as search_res:
        search_res.write('')
    return data, f


intro()


@app.route('/')
def ask():
    if request.args:
        gender = request.args['gender']
        age = request.args['age']
        place = request.args['place']
        first = request.args['first']
        second = request.args['second']
        third = request.args['third']
        forth = request.args['forth']

        json_string = """{"gender":"%s", "age":"%s", "place_of_birth":"%s", \
        "sg_sg":"%s", "sg_pl":"%s", "pl_sg":"%s","pl_pl":"%s"}"""

        json_data = json_string % (gender, age, place, first, second, third,
                                   forth)

        with open('json.txt', 'a', encoding='utf-8') as data:
            data.write(json_data)

        info = '%s\t%s\t%s\t%s\t%s\t%s\t%s\n'

        get_info = info % (gender, age, place, first, second, third, forth)

        with open('results.csv', 'a+') as fl:
            fl.write(get_info)

        with open('sg_sg.txt', 'a', encoding='utf-8') as fl_1:
            fl_1.write(first)
            fl_1.write(' ')

        with open('sg_pl.txt', 'a', encoding='utf-8') as fl_2:
            fl_2.write(second)
            fl_2.write(' ')

        with open('pl_sg.txt', 'a', encoding='utf-8') as fl_3:
            fl_3.write(third)
            fl_3.write(' ')

        with open('pl_pl.txt', 'a', encoding='utf-8') as fl_4:
            fl_4.write(forth)
            fl_4.write(' ')

        return render_template('ask.html', gender=gender,
                               age=age, place=place, first=first,
                               second=second, third=third, forth=forth)

    return render_template('ask.html')


@app.route('/stats')
def stats():
    first_sg = 0
    first_pl = 0
    second_sg = 0
    second_pl = 0
    third_sg = 0
    third_pl = 0
    forth_sg = 0
    forth_pl = 0
    res = ''

    urls = {'нажмите сюда': url_for('ask')}

    with open('sg_sg.txt', 'r', encoding='utf-8') as fl_1:
        text = fl_1.read()
        splited_words = text.split()
        for word in splited_words:
            if word == 'останавливается':
                first_sg += 1
            else:
                first_pl += 1
        res = res + 'Количество употреблений SG глагола с SG субъекта' \
                    ' и SG объекта: ' + str(first_sg) + '\n'
        res = res + 'Количество употреблений PL глагола с SG субъекта' \
                    ' и SG объекта: ' + str(first_pl) + '\n'

    with open('sg_pl.txt', 'r', encoding='utf-8') as fl_2:
        text = fl_2.read()
        splited_words = text.split()
        for word in splited_words:
            if word == 'насыщает':
                second_sg += 1
            else:
                second_pl += 1
        res = res + 'Количество употреблений SG глагола с SG субъекта' \
                    ' и PL объекта: ' + str(second_sg) + '\n'
        res = res + 'Количество употреблений PL глагола с SG субъекта' \
                    ' и PL объекта: ' + str(second_pl) + '\n'

    with open('pl_sg.txt', 'r', encoding='utf-8') as fl_3:
        text = fl_3.read()
        splited_words = text.split()
        for word in splited_words:
            if word == 'столкнулся':
                third_sg += 1
            else:
                third_pl += 1
        res = res + 'Количество употреблений SG глагола с PL субъекта' \
                    ' и SG объекта: ' + str(third_sg) + '\n'
        res = res + 'Количество употреблений PL глагола с PL субъекта' \
                    ' и SG объекта: ' + str(third_pl) + '\n'

    with open('pl_pl.txt', 'r', encoding='utf-8') as fl_4:
        text = fl_4.read()
        splited_words = text.split()
        for word in splited_words:
            if word == 'завянет':
                forth_sg += 1
            else:
                forth_pl += 1
        res = res + 'Количество употреблений SG глагола с PL субъекта' \
                    ' и PL объекта: ' + str(forth_sg) + '\n'
        res = res + 'Количество употреблений PL глагола с PL субъекта' \
                    ' и PL объекта: ' + str(forth_pl) + '\n'

    with open('results.txt', 'w', encoding='utf-8') as f:
        f.write(res)

    with open('results.txt', 'r', encoding='utf-8') as f:
        content = f.read().split('\n')

    x1 = ['1_sg', '1_pl']
    x2 = ['2_sg', '2_pl']
    x3 = ['3_sg', '3_pl']
    x4 = ['4_sg', '4_pl']
    y1 = [int(first_sg), int(first_pl)]
    y2 = [int(second_sg), int(second_pl)]
    y3 = [int(third_sg), int(third_pl)]
    y4 = [int(forth_sg), int(forth_pl)]
    plt.bar(x1, y1, color='g')
    plt.bar(x2, y2, color='mediumseagreen')
    plt.bar(x3, y3, color='mediumaquamarine')
    plt.bar(x4, y4, color='mediumturquoise')

    plt.savefig('static/stats.png', fromat='png')

    return render_template('stats.html', content=content,
                           urls=urls, url='static/stats.png')


@app.route('/json')
def json_data():
    with open('json.txt', 'r', encoding='utf-8') as f:
        content = f.read().split('} ')
    return render_template('json.html', content=content)


@app.route('/search')
def search():

    if request.args:
        search_age = request.args['search_age']
        search = True if 'search' in request.args else False

        print(search_age)
        print(search)

        result = ''

        with open('json.txt', 'r', encoding='utf-8') as data:
            text = data.read()
            splited_lines = text.split('}')
            print(splited_lines)
            if search is True:
                for line in splited_lines:
                    if ("останавливаются" or "насыщают" or "столкнулся"
                        or "завянет") and search_age in line:
                        result = result + line + '}' + '\n'
            else:
                for line in splited_lines:
                    if ("останавливается" and "насыщает" and "столкнулись"
                        and "завянут") and search_age in line:
                        result = result + line + '}' + '\n'

        with open('search_res.txt', 'w', encoding='utf-8') as search_res:
            search_res.write(result)

        return render_template('search.html', search_age=search_age, search=search)

    return render_template('search.html')


@app.route('/results')
def results():
    with open('search_res.txt', 'r', encoding='utf-8') as f:
        content = f.read().split('/n')
    return render_template('results.html', content=content)


if __name__ == '__main__':
    app.run(debug=True)