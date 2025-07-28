from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Column, Table, ForeignKey, Integer

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    Fav: Mapped["Fav"] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[str] = mapped_column(nullable=False)
    Fav: Mapped["Fav"] = relationship(back_populates="Character")
    

    def serialize(self):
        return {
            "character_id": self.character_id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "height": self.height,

        }


class Planet (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    population: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    orbital: Mapped[str] = mapped_column(nullable=False)
    Fav: Mapped["Fav"] = relationship(back_populates="Planet")
   

    def serialize(self):
        return {
            "Planet_id": self.planets_id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population,
            "terrain": self.terrain,
            "orbital": self.orbital,
           
        }
class Vehicle (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    vehicle_class: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    manufacturer: Mapped[str] = mapped_column(nullable=False)
    cargo_capacity: Mapped[str] = mapped_column(nullable=False)
    passengers: Mapped[str] = mapped_column(nullable=False)
    Fav: Mapped["Fav"] = relationship(back_populates="Vehicle")
   

    def serialize(self):
        return {
            "Vehicle_id": self.vehicles_id,
            "name": self.name,
            "vehicle_class": self.vehicle_class,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers,
           
        }


class Fav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"))

    user: Mapped["User"] = relationship(back_populates="favorite")
    character: Mapped["Character"] = relationship(back_populates="favorite")
    planet: Mapped["Planet"] = relationship(back_populates="favorite")
    vehicle: Mapped["Vehicle"] = relationship(back_populates="favorite")


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id,
          
        }
