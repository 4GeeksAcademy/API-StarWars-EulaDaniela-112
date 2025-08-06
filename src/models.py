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
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=True)
    fav: Mapped["Fav"] = relationship(back_populates="user")

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
    fav: Mapped["Fav"] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
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
    fav: Mapped["Fav"] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
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
    fav: Mapped["Fav"] = relationship(back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicle_class": self.vehicle_class,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cargo_capacity": self.cargo_capacity,
            "passengers": self.passengers,

        }


class Fav(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(
        String(120), unique=False, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int | None] = mapped_column(
        ForeignKey("character.id"))
    planet_id: Mapped[int | None] = mapped_column(ForeignKey("planet.id"))
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicle.id"))

    user: Mapped["User"] = relationship("User", back_populates="fav")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="fav")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="fav")
    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="fav")

    def serialize(self):
        result = {
            "id": self.id,
        }
        if self.character:
            result["character"] = self.character.serialize()
        if self.planet:
            result["planet"] = self.planet.serialize()
        if self.vehicle:
            result["vehicle"] = self.vehicle.serialize()
        return result
