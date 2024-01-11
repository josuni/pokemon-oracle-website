from pokemon_oracle import PokemonOracle
from flask import Flask, request, render_template
from datetime import datetime

def get_birthday():
    while True:
        birthday_str = input("Enter birthday in MM/DD format: ")
    
        try:
            birthday = datetime.strptime(birthday_str, "%m/%d")
            return birthday
        except ValueError:
            print("Invalid response. Please enter the birthday in MM/DD format.")

#name = input("Enter name: ")
#birthday = get_birthday()

app = Flask(__name__)
oracle = PokemonOracle()
#print(oracle.get_spirit_pokemon(name, birthday))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    birthday_str = request.form['birthday']
    birthday = datetime.strptime(birthday_str, "%m/%d")

    pokemon_result = oracle.get_spirit_pokemon(name, birthday)
    result_text = 'Your spirit pokemon is ' + pokemon_result.upper() + '!'
    return render_template('index.html', result_text=result_text)


if __name__ == "__main__":
    app.run()