from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from lxml import html
from random import randint
import requests

app = Flask(__name__)


ask = Ask(app, "/")


@ask.launch
def launch():
    return pick_film()


@ask.intent("PickFilmIntent")
def pick_film():
    page = requests.get('http://www.imdb.com/chart/top')
    tree = html.fromstring(page.content)
    titles = tree.xpath('//td[@class="titleColumn"]/a/text()')
    ratings = tree.xpath('//td[@class="ratingColumn imdbRating"]/strong/text()')

    rint = randint(0, 254)

    response = render_template('chosen', film=titles[rint], rating=ratings[rint])

    return statement(response).simple_card(title='Picked a film', content=titles[rint] + " which is rated " + ratings[rint] + " on IMDB.")


if __name__ == '__main__':
    app.run()
