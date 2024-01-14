from pokemon_oracle import PokemonOracle
import flask
from flask import Flask
from datetime import datetime

def parse_birthday(birthday_str):
    try:
        birthday = datetime.strptime(birthday_str, "%m/%d")
        return birthday
    except ValueError:
        print("Invalid response. Please enter the birthday in MM/DD format.")

app = Flask(__name__)
oracle = PokemonOracle()

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = flask.request.form['name']
    birthday_str = flask.request.form['birthday']
    birthday = parse_birthday(birthday_str)

    if birthday is None:
        result_text = 'Invalid birthday. Please try again.'
        return flask.render_template('index.html', result_text=result_text)

    pokemon_name, pokemon_image_url = oracle.get_spirit_pokemon(name, birthday)
    result_text = 'Your spirit pokemon is ' + pokemon_name.upper() + '!'
    return flask.render_template('index.html', result_text=result_text, pokemon_image=pokemon_image_url, pokemon_image_alt_text=pokemon_name)


if __name__ == "__main__":
    app.run()