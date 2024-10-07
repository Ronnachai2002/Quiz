from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    # รับค่า ID จาก request body
    pokemon_id = request.json.get('id')

    # URL ของ PokeAPI ที่จะเรียกใช้
    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    pokemon_form_url = f'https://pokeapi.co/api/v2/pokemon-form/{pokemon_id}/'

    # เรียกข้อมูลจาก PokeAPI
    pokemon_response = requests.get(pokemon_url)
    pokemon_form_response = requests.get(pokemon_form_url)

    if pokemon_response.status_code == 200 and pokemon_form_response.status_code == 200:
        # แปลงข้อมูล JSON จากการตอบกลับของ PokeAPI
        pokemon_data = pokemon_response.json()
        pokemon_form_data = pokemon_form_response.json()

        # จัดรูปแบบข้อมูลตามตัวอย่าง JSON
        result = {
            "stats": pokemon_data['stats'],
            "name": pokemon_data['name'],
            "sprites": pokemon_form_data['sprites']
        }

        return jsonify(result)
    else:
        return jsonify({"error": "Unable to fetch data from PokeAPI"}), 400

if __name__ == '__main__':
    app.run(debug=True)
