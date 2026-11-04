from flask import request, jsonify, Blueprint
from models import db, User, Character, Planet, Favorite

api = Blueprint('api', __name__)

@api.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200

@api.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Personaje no encontrado"}), 404
    return jsonify(person.serialize()), 200

@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    return jsonify(planet.serialize()), 200

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    current_user_id = 1 
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify([fav.serialize() for fav in user.favorites]), 200

@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    current_user_id = 1
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planeta no encontrado"}), 404
    
    existing = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if existing:
        return jsonify({"message": "El planeta ya está en favoritos"}), 400

    new_fav = Favorite(user_id=current_user_id, planet_id=planet_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Planeta agregado a favoritos con éxito"}), 201

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    current_user_id = 1
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Personaje no encontrado"}), 404
    
    existing = Favorite.query.filter_by(user_id=current_user_id, character_id=people_id).first()
    if existing:
        return jsonify({"message": "El personaje ya está en favoritos"}), 400

    new_fav = Favorite(user_id=current_user_id, character_id=people_id)
    db.session.add(new_fav)
    db.session.commit()
    return jsonify({"message": "Personaje agregado a favoritos con éxito"}), 201

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    current_user_id = 1
    fav = Favorite.query.filter_by(user_id=current_user_id, planet_id=planet_id).first()
    if not fav:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Planeta eliminado de favoritos"}), 200

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    current_user_id = 1
    fav = Favorite.query.filter_by(user_id=current_user_id, character_id=people_id).first()
    if not fav:
        return jsonify({"error": "Favorito no encontrado"}), 404

    db.session.delete(fav)
    db.session.commit()
    return jsonify({"message": "Personaje eliminado de favoritos"}), 200