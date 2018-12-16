from flask import Flask, request, jsonify, redirect, url_for
from app import app
from app.models import *

user_schema = UserSchema()
users_schema = UserSchema(many=True)
property_schema = PropertySchema()
properties_schema = PropertySchema(many=True)

#Create new user
@app.route("/user", methods=["POST"])
def add_user():
	lastname_req = request.json['lastname']
	user = User.query.filter(User.lastname==str(lastname_req)).first()
	
	if user is None:
		lastname = request.json['lastname']
		firstname = request.json['firstname']
		birthday = request.json['birthday']
		new_user = User(lastname, firstname, birthday)

		db.session.add(new_user)
		db.session.commit()

		return user_schema.jsonify(new_user)

	return redirect(url_for('.get_user_properties', owner = user.id))

# Get user detail using user id
@app.route("/user/<id>", methods=["GET"])
def user_detail(id):
	user = User.query.get(id)

	return user_schema.jsonify(user)

# Get all users
@app.route("/users", methods=["GET"])
def get_all_users():
	users = User.query.all()
	result = users_schema.dump(users)

	return jsonify(result.data)

# Update information of a user
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
	user = User.query.get(id)
	if user != None:
		user.lastname = request.json["lastname"]
		user.firstname = request.json["firstname"]
		user.birthday = request.json["birthday"]

		db.session.commit()

		return user_schema.jsonify(user)

	return  "User update is impossible because parameters are wrong"

# Add a new property
@app.route("/property", methods=["POST"])
def add_property():
	user = User.query.filter(User.id==str(request.json["owner"])).first()	
	if user != None: 
		name = request.json["name"]
		propertyType = request.json["propertyType"]
		description = request.json["description"]
		rooms = request.json["rooms"]
		comments = request.json["comments"]
		owner = request.json["owner"]
		city = request.json["city"]
		new_property = Property(name, propertyType, description, rooms, comments, owner, city)

		db.session.add(new_property)
		db.session.commit()

		return property_schema.jsonify(new_property)
	return "Cannot add a property because owner does not exist"

# Get all properties of a user 
@app.route("/property/<owner>", methods=["GET"])
def get_user_properties(owner):
	properties = Property.query.filter(Property.owner == owner)

	return properties_schema.jsonify(properties)

# Get all properties for a chosen city
@app.route("/properties/<city>", methods=["GET"])
def get_properties(city):
	properties = Property.query.filter(Property.city == city)
	result = properties_schema.dump(properties)

	return properties_schema.jsonify(result.data)
	
# Update property information 
@app.route("/property/<owner>/update/<property>", methods=["PUT"])
def update_property(owner, property):
	property_found = Property.query.filter(Property.owner == owner, Property.id == property).first()
	propertyDB = Property.query.get(property)
 	if property_found != None:
 		print propertyDB.name
 		propertyDB.name = request.json["name"]
		propertyDB.propertyType = request.json["propertyType"]
		propertyDB.description = str(request.json["description"])
		propertyDB.rooms = request.json["rooms"]
		propertyDB.comments = request.json["comments"]
		propertyDB.owner = request.json["owner"]
		propertyDB.city = request.json["city"]

		db.session.commit()

		return property_schema.jsonify(propertyDB)
	return  "Property update is impossible because parameters are wrong"