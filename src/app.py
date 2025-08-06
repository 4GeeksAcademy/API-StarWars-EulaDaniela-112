"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Vehicle, Fav
from sqlalchemy.orm import joinedload
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():

    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users])
    except Exception as e:
        return jsonify({"error": "Error al obtener usuarios"}), 500

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.serialize())

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usualio eliminado con éxito"}), 200


@app.route('/characters', methods=['GET'])
def get_characters():

    try:
        characters = Character.query.all()
        return jsonify([character.serialize() for character in characters])
    except Exception as e:
        return jsonify({"error": "Error al obtener los personajes"}), 500

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(character.serialize())    


@app.route('/character/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Personaje no encontrado"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"message": "Personaje eliminado con éxito"}), 200


@app.route('/planets', methods=['GET'])
def get_planets():

    try:
        planets = Planet.query.all()
        return jsonify([planet.serialize() for planet in planets])
    except Exception as e:
        return jsonify({"error": "Error al obtener los planetas"}), 500

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize())    


@app.route('/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planeta no encontrado"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planeta eliminado con éxito"}), 200



@app.route('/vehicles', methods=['GET'])
def get_vehicles():

    try:
        vehicles = Vehicle.query.all()
        return jsonify([vehicle.serialize() for vehicle in vehicles])
    except Exception as e:
        return jsonify({"error": "Error al obtener los vehiculos"}), 500

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": "Vehiculo no encontrado"}), 404
    return jsonify(vehicle.serialize())    


@app.route('/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get(vehicle_id)
    if vehicle is None:
        return jsonify({"error": "Vehículo no encontrado"}), 404
    db.session.delete(vehicle)
    db.session.commit()
    return jsonify({"message": "Vehículo eliminado con éxito"}), 200

#=====favoritos

@app.route('/users/<int:user_id>/favorites', methods=['POST'])
def add_favorite(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "usuario no encontrado"}), 404
    
    fav = Fav(user_id=user_id, character_id=data.get('character_id'), planet_id=data.get('planet_id'), vehicle_id=data.get('vehicle_id'))
    db.session.add(fav)
    db.session.commit()
    return jsonify({"msg": "Favorito agregado! B)"}), 201

@app.route('/users/<int:user_id>/favorites/<int:fav_id>', methods=['DELETE'])
def delete_favorite(user_id, fav_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    fav = Fav.query.get(fav_id)
    if fav is None:
        return jsonify({"error": "Favorito no encontrado"}), 404
    
    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Favorito eliminado"}), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    favorites = Fav.query.options(
        joinedload(Fav.character),
        joinedload(Fav.planet),
        joinedload(Fav.vehicle)
    ).filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites])


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
