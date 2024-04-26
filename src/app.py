import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorites, Characters, Planets, Species, Vehicles
from datetime import datetime
import hashlib

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

# GET users and individual users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({'error': 'No users found'}), 404
        
        serialized_users = [user.serialize() for user in users]

        response_body = {
            "users": serialized_users
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve users', 'details': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        serialized_user = user.serialize()

        response_body = {
            "user": serialized_user
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user', 'details': str(e)}), 500


# GET complete elements groups or single elements
@app.route('/characters', methods=['GET'])
def get_characters():
    try:
        # Retrieve all characters from the database
        characters = Characters.query.all()
        
        # Check if characters were found
        if not characters:
            # Return a 404 error if no characters were found
            return jsonify({'error': 'No characters found'}), 404
        
        # Serialize the characters
        serialized_characters = [character.serialize() for character in characters]

        # Create the response body with the serialized characters
        response_body = {
            "characters": serialized_characters
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while retrieving characters
        return jsonify({'error': 'Failed to retrieve characters', 'details': str(e)}), 500

@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    try:
        # Retrieve the character with the specified ID from the database
        character = Characters.query.get(id)
        
        # Check if the character was found
        if not character:
            # Return a 404 error if the character was not found
            return jsonify({'error': 'Character not found'}), 404
        
        # Serialize the character
        serialized_character = character.serialize()

        # Create the response body with the serialized character
        response_body = {
            "character": serialized_character
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while retrieving the character
        return jsonify({'error': 'Failed to retrieve character', 'details': str(e)}), 500

@app.route('/planets', methods=['GET'])
def get_planets():
    try:
        planets = Planets.query.all()
        if not planets:
            return jsonify({'error': 'No planets found'}), 404
        
        serialized_planets = [planet.serialize() for planet in planets]

        response_body = {
            "planets": serialized_planets
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve planets', 'details': str(e)}), 500

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    try:
        planet = Planets.query.get(id)
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404
        
        serialized_planet = planet.serialize()

        response_body = {
            "planet": serialized_planet
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve planet', 'details': str(e)}), 500

@app.route('/species', methods=['GET'])
def get_species():
    try:
        species = Species.query.all()
        if not species:
            return jsonify({'error': 'No species found'}), 404
        
        serialized_species = [specie.serialize() for specie in species]

        response_body = {
            "species": serialized_species
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve species', 'details': str(e)}), 500

@app.route('/species/<int:id>', methods=['GET'])
def get_onespecies(id):
    try:
        specie = Species.query.get(id)
        if not specie:
            return jsonify({'error': 'Species not found'}), 404
        
        serialized_specie = specie.serialize()

        response_body = {
            "specie": serialized_specie
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve specie', 'details': str(e)}), 500

@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    try:
        vehicles = Vehicles.query.all()
        if not vehicles:
            return jsonify({'error': 'No vehicles found'}), 404
        
        serialized_vehicles = [vehicle.serialize() for vehicle in vehicles]

        response_body = {
            "vehicles": serialized_vehicles
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve vehicles', 'details': str(e)}), 500

@app.route('/vehicles/<int:id>', methods=['GET'])
def get_vehicle(id):
    try:
        vehicle = Vehicles.query.get(id)
        if not vehicle:
            return jsonify({'error': 'Vehicle not found'}), 404
        
        serialized_vehicle = vehicle.serialize()

        response_body = {
            "vehicle": serialized_vehicle
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to retrieve vehicle', 'details': str(e)}), 500

# GET favorites
@app.route('/users/favorites/<int:user_id>', methods=['GET'])
def get_user_favorites(user_id):
    try:
        # Retrieve favorites associated with the specified user ID from the database
        favorites = Favorites.query.filter_by(user_id=user_id).all()
        
        # Check if any favorites were found
        if not favorites:
            # Return a 404 error if no favorites were found for the user
            return jsonify({'error': 'No favorites found for this user'}), 404
        
        # Serialize the favorites
        serialized_favorites = [favorite.serialize() for favorite in favorites]

        # Create the response body with the serialized favorites
        response_body = {
            "favorites": serialized_favorites
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while retrieving the favorites
        return jsonify({'error': 'Failed to retrieve favorites', 'details': str(e)}), 500


# POST user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    # Validate that required fields are not empty
    required_fields = ['username', 'email', 'password', 'is_active', 'subscription_date', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field.capitalize()} is required'}), 400    

    # Validate subscription date format
    subscription_date_format = '%Y-%m-%d %H:%M:%S'
    if 'subscription_date' in data:
        try:
            subscription_date = datetime.strptime(data['subscription_date'], subscription_date_format)
        except ValueError:
            return jsonify({'error': 'Invalid subscription date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    # Validate birthdate format if present
    if 'birthdate' in data and data['birthdate']:
        try:
            birthdate = datetime.strptime(data['birthdate'], '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid birthdate format. Use YYYY-MM-DD'}), 400
    
    # Process the data and create the user
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        is_active=data['is_active'],
        subscription_date=datetime.strptime(data['subscription_date'], '%Y-%m-%d %H:%M:%S'),
        first_name=data['first_name'],
        last_name=data['last_name'],
        birthdate=datetime.strptime(data['birthdate'], '%Y-%m-%d') if data.get('birthdate') else None
    )
    db.session.add(new_user)
    db.session.commit()

    response_body = {
        "success": "User created successfully",
        "user": new_user.serialize()
    }

    return jsonify(response_body), 201

# POST favorites 
@app.route('/favorites/characters/<int:user_id>/<int:character_id>', methods=['POST'])
def post_favorite_character(user_id, character_id):
    try:
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Check if the character exists
        character = Characters.query.get(character_id)
        if not character:
            return jsonify({'error': f'Character with ID {character_id} not found'}), 404

        # Create a new entry in the database for the favorite
        new_favorite = Favorites(
            user_id=user_id,
            character_id=character_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": f"Character with ID {character_id} added to favorites for user with ID {user_id}"
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to add favorite character', 'details': str(e)}), 500

@app.route('/favorites/planets/<int:user_id>/<int:planet_id>', methods=['POST'])
def post_favorite_planet(user_id, planet_id):
    try:
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Check if the planet exists
        planet = Planets.query.get(planet_id)
        if not planet:
            return jsonify({'error': f'Planet with ID {planet_id} not found'}), 404

        # Create a new entry in the database for the favorite
        new_favorite = Favorites(
            user_id=user_id,
            planet_id=planet_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": f"Planet with ID {planet_id} added to favorites for user with ID {user_id}"
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to add favorite planet', 'details': str(e)}), 500

@app.route('/favorites/species/<int:user_id>/<int:species_id>', methods=['POST'])
def post_favorite_species(user_id, species_id):
    try:
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Check if the species exists
        species = Species.query.get(species_id)
        if not species:
            return jsonify({'error': f'Species with ID {species_id} not found'}), 404

        # Create a new entry in the database for the favorite
        new_favorite = Favorites(
            user_id=user_id,
            species_id=species_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": f"Species with ID {species_id} added to favorites for user with ID {user_id}"
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to add favorite species', 'details': str(e)}), 500

@app.route('/favorites/vehicles/<int:user_id>/<int:vehicle_id>', methods=['POST'])
def post_favorite_vehicle(user_id, vehicle_id):
    try:
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Check if the vehicle exists
        vehicle = Vehicles.query.get(vehicle_id)
        if not vehicle:
            return jsonify({'error': f'Vehicle with ID {vehicle_id} not found'}), 404

        # Create a new entry in the database for the favorite
        new_favorite = Favorites(
            user_id=user_id,
            vehicle_id=vehicle_id
        )
        db.session.add(new_favorite)
        db.session.commit()

        response_body = {
            "msg": f"Vehicle with ID {vehicle_id} added to favorites for user with ID {user_id}"
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to add favorite vehicle', 'details': str(e)}), 500

# DELETE favorites
def delete_favorite(user_id, item_id, item_type):
    try:
        # Retrieve the user from the database based on the provided user ID
        user = User.query.get(user_id)
        if not user:
            # Return a 404 error if the user with the specified ID is not found
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Determine the column name based on the item type
        column_name = f"{item_type}_id"
        
        # Query the Favorites table to find the favorite entry to delete
        favorite = Favorites.query.filter_by(user_id=user_id, **{column_name: item_id}).first()
        if not favorite:
            # Return a 404 error if the favorite with the specified ID is not found
            return jsonify({'error': f'{item_type.capitalize()} with ID {item_id} is not a favorite for user with ID {user_id}'}), 404

        # Delete the favorite entry from the database
        db.session.delete(favorite)
        db.session.commit()

        # Create the response body with a success message
        response_body = {
            "msg": f"{item_type.capitalize()} with ID {item_id} deleted from favorites for user with ID {user_id}"
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while deleting the favorite
        return jsonify({'error': f'Failed to delete favorite {item_type}', 'details': str(e)}), 500

@app.route('/favorites/characters/<int:user_id>/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    return delete_favorite(user_id, character_id, 'character')

@app.route('/favorites/planets/<int:user_id>/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    return delete_favorite(user_id, planet_id, 'planet')

@app.route('/favorites/species/<int:user_id>/<int:species_id>', methods=['DELETE'])
def delete_favorite_species(user_id, species_id):
    return delete_favorite(user_id, species_id, 'species')

@app.route('/favorites/vehicles/<int:user_id>/<int:vehicle_id>', methods=['DELETE'])
def delete_favorite_vehicle(user_id, vehicle_id):
    return delete_favorite(user_id, vehicle_id, 'vehicle')

# POST elements
@app.route('/characters', methods=['POST'])
def post_character():
    try:
        # Extract data from the request JSON
        data = request.json

        # Create a new Character object with the provided data
        new_character = Characters(
            name=data.get('name'),
            birth_year=data.get('birth_year'),
            homeworld=data.get('homeworld'),
            gender=data.get('gender'),
            eye_color=data.get('eye_color'),
            hair_color=data.get('hair_color'),
            height=data.get('height'),
            mass=data.get('mass'),
            skin_color=data.get('skin_color')
        )

        # Add the new character to the database session and commit changes
        db.session.add(new_character)
        db.session.commit()

        # Create the response body with success message and serialized character data
        response_body = {
            "success": "Character created successfully",
            "character": new_character.serialize()
        }

        # Return the response with a 201 status code
        return jsonify(response_body), 201

    except Exception as e:
        # Return a 500 error if an exception occurs while creating the character
        return jsonify({'error': 'Failed to create character', 'details': str(e)}), 500

@app.route('/planets', methods=['POST'])
def post_planet():
    try:
        data = request.json

        new_planet = Planets(
            name=data.get('name'),
            climate=data.get('climate'),
            population=data.get('population'),
            terrain=data.get('terrain'),
            diameter=data.get('diameter'),
            surface_water=data.get('surface_water'),
            gravity=data.get('gravity'),
            rotation_period=data.get('rotation_period'),
            orbital_period=data.get('orbital_period')
        )

        db.session.add(new_planet)
        db.session.commit()

        response_body = {
            "success": "Planet created successfully",
            "planet": new_planet.serialize()
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to create planet', 'details': str(e)}), 500

@app.route('/species', methods=['POST'])
def post_species():
    try:
        data = request.json

        new_species = Species(
            name=data.get('name'),
            classification=data.get('classification'),
            designation=data.get('designation'),
            language=data.get('language'),
            average_height=data.get('average_height'),
            average_lifespan=data.get('average_lifespan'),
            eye_colors=data.get('eye_colors'),
            hair_colors=data.get('hair_colors'),
            skin_colors=data.get('skin_colors')
        )

        db.session.add(new_species)
        db.session.commit()

        response_body = {
            "success": "Species created successfully",
            "species": new_species.serialize()
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to create species', 'details': str(e)}), 500

@app.route('/vehicles', methods=['POST'])
def post_vehicles():
    try:
        data = request.json

        new_vehicle = Vehicles(
            id=data.get('id'),
            name=data.get('name'),
            model=data.get('model'),
            vehicle_class=data.get('vehicle_class'),
            consumables=data.get('consumables'),
            length=data.get('length'),  
            max_atmosphering_speed=data.get('max_atmosphering_speed'),
            cargo_capacity=data.get('cargo_capacity'),
            crew=data.get('crew'),
            passengers=data.get('passengers'),
            manufacturer=data.get('manufacturer')
        )

        db.session.add(new_vehicle)
        db.session.commit()

        response_body = {
            "success": "Vehicle created successfully",
            "vehicle": new_vehicle.serialize()
        }

        return jsonify(response_body), 201

    except Exception as e:
        return jsonify({'error': 'Failed to create vehicle', 'details': str(e)}), 500


# PUT elements (modify)
@app.route('/characters/<int:id>', methods=['PUT'])
def put_character(id):
    try:
        # Extract data from the request JSON
        data = request.json
        
        # Query the database to find the character with the provided ID
        character = Characters.query.get(id)
        
        # Check if the character exists
        if character is None:
            return jsonify({'error': f'Character with ID {id} not found'}), 404
        
        # Update the character attributes with the provided data
        character.name = data.get('name')
        character.birth_year = data.get('birth_year')
        character.homeworld = data.get('homeworld')
        character.gender = data.get('gender')
        character.eye_color = data.get('eye_color')
        character.hair_color = data.get('hair_color')
        character.height = data.get('height')
        character.mass = data.get('mass')
        character.skin_color = data.get('skin_color')
        
        # Commit the changes to the database
        db.session.commit()

        # Create the response body with success message and serialized character data
        response_body = {
            "success": f"Character with ID {id} updated successfully",
            "character": character.serialize()
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while updating the character
        return jsonify({'error': 'Failed to update character', 'details': str(e)}), 500

@app.route('/planets/<int:id>', methods=['PUT'])
def put_planet(id):
    try:
        data = request.json
        
        planet = Planets.query.get(id)
        
        if planet is None:
            return jsonify({'error': f'Planet with ID {id} not found'}), 404
        
        planet.name = data.get('name')
        planet.climate = data.get('climate')
        planet.population = data.get('population')
        planet.terrain = data.get('terrain')
        planet.diameter = data.get('diameter')
        planet.gravity = data.get('gravity')
        planet.rotation_period = data.get('rotation_period')
        planet.orbital_period = data.get('orbital_period')
        
        db.session.commit()

        response_body = {
            "success": f"Planet with ID {id} updated successfully",
            "planet": planet.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to update planet', 'details': str(e)}), 500

@app.route('/species/<int:id>', methods=['PUT'])
def put_species(id):
    try:
        data = request.json
        
        specie = Species.query.get(id)
        
        if specie is None:
            return jsonify({'error': f'Species with ID {id} not found'}), 404
        
        specie.name = data.get('name')
        specie.classification = data.get('classification')
        specie.designation = data.get('designation')
        specie.language = data.get('language')
        specie.average_height = data.get('average_height')
        specie.average_lifespan = data.get('average_lifespan')
        specie.eye_colors = data.get('eye_colors')
        specie.hair_colors = data.get('hair_colors')
        specie.skin_colors = data.get('skin_colors')
        
        db.session.commit()

        response_body = {
            "success": f"Species with ID {id} updated successfully",
            "species": specie.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to update species', 'details': str(e)}), 500

@app.route('/vehicles/<int:id>', methods=['PUT'])
def put_vehicle(id):
    try:
        data = request.json
        
        vehicle = Vehicles.query.get(id)
        
        if vehicle is None:
            return jsonify({'error': f'Vehicle with ID {id} not found'}), 404
        
        vehicle.name = data.get('name')
        vehicle.model = data.get('model')
        vehicle.vehicle_class = data.get('vehicle_class')
        vehicle.manufacturer = data.get('manufacturer')
        vehicle.cost_in_credits = data.get('cost_in_credits')
        vehicle.length = data.get('length')
        vehicle.max_atmosphering_speed = data.get('max_atmosphering_speed')
        vehicle.crew = data.get('crew')
        vehicle.passengers = data.get('passengers')
        vehicle.cargo_capacity = data.get('cargo_capacity')
        vehicle.consumables = data.get('consumables')
        
        db.session.commit()

        response_body = {
            "success": f"Vehicle with ID {id} updated successfully",
            "vehicle": vehicle.serialize()
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to update vehicle', 'details': str(e)}), 500


# DELETE elements
@app.route('/characters/<int:id>', methods=['DELETE'])
def delete_character(id):
    try:
        # Query the database to find the character with the provided ID
        character = Characters.query.get(id)
        
        # Check if the character exists
        if character is None:
            return jsonify({'error': f'Character with ID {id} not found'}), 404
        
        # Delete the character from the database
        db.session.delete(character)
        db.session.commit()

        # Create the response body with success message
        response_body = {
            "success": f"Character with ID {id} deleted successfully"
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while deleting the character
        return jsonify({'error': 'Failed to delete character', 'details': str(e)}), 500

@app.route('/planets/<int:id>', methods=['DELETE'])
def delete_planet(id):
    try:
        planet = Planets.query.get(id)
        
        if planet is None:
            return jsonify({'error': f'Planet with ID {id} not found'}), 404
        
        db.session.delete(planet)
        db.session.commit()

        response_body = {
            "success": f"Planet with ID {id} deleted successfully"
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to delete planet', 'details': str(e)}), 500

@app.route('/species/<int:id>', methods=['DELETE'])
def delete_species(id):
    try:
        specie = Species.query.get(id)
        
        if specie is None:
            return jsonify({'error': f'Species with ID {id} not found'}), 404
        
        db.session.delete(specie)
        db.session.commit()

        response_body = {
            "success": f"Species with ID {id} deleted successfully"
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to delete species', 'details': str(e)}), 500

@app.route('/vehicles/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    try:
        vehicle = Vehicles.query.get(id)
        
        if vehicle is None:
            return jsonify({'error': f'Vehicle with ID {id} not found'}), 404
        
        db.session.delete(vehicle)
        db.session.commit()

        response_body = {
            "success": f"Vehicle with ID {id} deleted successfully"
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({'error': 'Failed to delete vehicle', 'details': str(e)}), 500


# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Query the database to find the user with the provided ID
        user = User.query.get(user_id)
        
        # Check if the user exists
        if user is None:
            return jsonify({'error': f'User with ID {user_id} not found'}), 404
        
        # Get all favorites associated with the user
        user_favorites = Favorites.query.filter_by(user_id=user_id).all()
        
        # Delete user favorites
        for favorite in user_favorites:
            db.session.delete(favorite)
        
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        # Create the response body with success message
        response_body = {
            "success": f"User with ID {user_id} deleted successfully"
        }

        # Return the response with a 200 status code
        return jsonify(response_body), 200

    except Exception as e:
        # Return a 500 error if an exception occurs while deleting the user
        return jsonify({'error': 'Failed to delete user', 'details': str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)