from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)

CONNECTION_STRING = "mongodb://root:1234@localhost:27018/"
client = MongoClient(CONNECTION_STRING)

db = client['JDG']
pokemon = db['pokemon']

@app.route('/pokemon/', methods=['GET'])
def get(): 
    '''voir la liste des pokemons'''
    if request.method == 'GET':  
        get = pokemon.find({}, {"id":1, "name":1, "image":1, "videoYoutube":1, "stats":1,"_id":0}).limit(5)

        get_list = []
        for x in get:
              get_list.append(x)
        
        return jsonify(get_list)

@app.route('/pokemon/', methods=['POST'])
def post():
    '''ajouter un pokemon'''
    if request.method == 'POST':
        data= request.get_json()
        id = data['id']
        pokedexId = data['pokedexId']
        name = data['name']
        image = data['image']
        videoYoutube = data['videoYoutube']
        slug = data['slug']
        stats= data['stats']

        pokemon.insert_one({"id": id,
                            "pokedexId": pokedexId,
                            "name": f"""{name}""", 
                            "image": f"""{image}""",
                            "videoYoutube": f"""{videoYoutube}""",
                            "slug": f"""{slug}""",
                            "stats": f"""{stats}"""
                            })

        return jsonify({"response":"Nouveau pokemon ajouté au pokedex, le prof Chen est content !"})

@app.route('/pokemon/', methods=['DELETE'])
def delete():
    '''supprimer un pokemon'''
    if request.method == 'DELETE':
        data= request.get_json()
        id = data['id']

        pokemon.delete_one({"id": id})

        return jsonify({"response":"Pokemon supprimé, le prof Chen est très malheureux !!!"})

@app.route('/pokemon/', methods=['PUT'])
def put():
    '''modifier un pokemon'''
    if request.method == 'PUT':
        data= request.get_json()
        id = data['id']
        name = data['name']

        pokemon.update_one({"id": id}, {"$set":{"name": f"""{name}"""}})

        return jsonify({"response":"Pokemon modifié, le prof Chen est dubidatif !!!"})

if __name__ == '__main__':
    app.run(debug=True)
