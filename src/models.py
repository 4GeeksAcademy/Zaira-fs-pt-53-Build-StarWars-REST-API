from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index= True, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    subscription_date = db.Column(db.DateTime, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    birthdate = db.Column(db.Date)
    favorites = db.relationship("Favorites", back_populates="user")

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}>'

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "subscription_date": self.subscription_date,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthdate": self.birthdate
        }
    
    def hash_password(self, password):
        # Convert the password to bytes before hashing it
        password_bytes = password.encode('utf-8')

        # Use the SHA-256 hash algorithm
        hashed_bytes = hashlib.sha256(password_bytes)

        # Get the hexadecimal representation of the hash
        hashed_password = hashed_bytes.hexdigest()

        return hashed_password

    def set_password(self, password):
        # Hash the password before assigning it
        self.password = self.hash_password(password)

    def check_password(self, password):
        # Check if a plain text password matches the hashed password stored
        return self.password == self.hash_password(password)

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="favorites")
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    character = db.relationship("Characters", back_populates="favorites")
    species = db.relationship("Species", back_populates="favorites")
    vehicle = db.relationship("Vehicles", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")

    def __repr__(self):
        return f'<Favorites id={self.id}, user_id={self.user_id}'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "species_id": self.species_id,
            "vehicle_id": self.vehicle_id,
            "planet_id": self.planet_id
        }


class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, index= True, nullable=False)
    birth_year = db.Column(db.Integer)
    homeworld = db.Column(db.String(250), db.ForeignKey('planets.name'))
    gender = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    skin_color = db.Column(db.String(250))
    favorites = db.relationship("Favorites", back_populates="character")

    def __repr__(self):
        return f'<Characters id={self.id}, name={self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "homeworld": self.homeworld,
            "gender": self.gender,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }
    

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, index= True, nullable=False)
    climate = db.Column(db.String(250), index= True)
    population = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    diameter = db.Column(db.Integer)
    surface_water = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    favorites = db.relationship("Favorites", back_populates="planet")

    def __repr__(self):
        return f'<Planets id={self.id}, name={self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "surface_water": self.surface_water,
            "gravity": self.gravity,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
        }



class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, index= True, nullable=False)
    classification = db.Column(db.String(250), index= True)
    designation = db.Column(db.String(250))
    language = db.Column(db.String(250))
    average_height = db.Column(db.Integer)
    average_lifespan = db.Column(db.Integer)
    eye_colors = db.Column(db.String(250))
    hair_colors = db.Column(db.String(250))
    skin_colors = db.Column(db.String(250))
    favorites = db.relationship("Favorites", back_populates="species")

    def __repr__(self):
        return f'<Species id={self.id}, name={self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "classification": self.classification,
            "designation": self.designation,
            "language": self.language,
            "average_height": self.average_height,
            "average_lifespan": self.average_lifespan,
            "eye_colors": self.eye_colors,
            "hair_colors": self.hair_colors,
            "skin_colors": self.skin_colors,    
        }


class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, index= True, nullable=False)
    model = db.Column(db.String(250), index= True)
    vehicle_class = db.Column(db.String(250))
    consumables = db.Column(db.String(250))
    length = db.Column(db.Integer)
    max_atmosphering_speed = db.Column(db.Integer)
    cargo_capacity = db.Column(db.Integer)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    manufacturer = db.Column(db.String(250))
    favorites = db.relationship("Favorites", back_populates="vehicle")

    def __repr__(self):
        return f'<Vehicles id={self.id}, name={self.name}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "consumables": self.consumables,
            "length": self.length,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "crew": self.crew,
            "passengers": self.passengers,
            "manufacturer": self.manufacturer,
        }