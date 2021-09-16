from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash
import re

db = 'artists_schema'

class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.artist_id = data['artist_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artist = f"{data['first_name']} {data['last_name']}" 

    @classmethod
    def addPainting(cls, data):

        is_valid = cls.validatePainting(data)
        if is_valid:
            query = "INSERT INTO paintings (title, description, price, artist_id, created_at, updated_at, quantity) Values(%(title)s, %(description)s, %(price)s, %(artist_id)s, NOW(), NOW(), %(quantity)s)"

            id = MySQLConnection(db).query_db(query, data)

            print("Added Painting to the database with an id of: ", id)

            return id
        else:
            return False
    @staticmethod
    def validatePainting(data):
        is_valid = True

        # Validates name
        if len(data['title']) < 2:
            flash('Title has to be at least 2 characters', 'title')
            is_valid = False
        
        # Validates description
        if len(data['description']) < 10:
            flash('Description must be longer than 10 characters', 'description')
            is_valid = False
        
        # Validates price
        PRICE_REGEX = re.compile(r'^[0-9]+\.[0-9]{1,2}$') 
        if( not PRICE_REGEX.match(data['price'])):
            flash('Must be valid Price. Please enter a postive price. formatted 999.99', 'price')
            is_valid = False

        # Validates date_made
        QUANTITY_REGEX = re.compile(r'^[0-9]+')
        if not QUANTITY_REGEX.match(data['quantity']):
            flash('Must be a positive number.', 'quantity')
            is_valid = False

        return is_valid
    #gets all paintings from db and returns and list of instances
    @classmethod
    def getAllPaintings(cls):
        query = "SELECT * from paintings LEFT JOIN artists ON artist_id = artists.id"

        paintings_fromDB = MySQLConnection(db).query_db(query)

        paintings =[]

        for painting in paintings_fromDB:
            paintings.append(cls(painting))
        
        return paintings

#Returns a painting instance from DB 
    @classmethod
    def getPaintingById(cls, id):
        query = f'SELECT * from paintings LEFT JOIN artists ON artist_id = artists.id WHERE paintings.id = {id}'

        DBdata = MySQLConnection(db).query_db(query)
        print("Painting Returned from DB: ", DBdata)
        if DBdata:
            return cls(DBdata[0])
        else:
            return False

    @staticmethod
    def updatePainting(data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, updated_at = NOW() WHERE id = %(id)s"

        MySQLConnection(db).query_db(query, data)
