from app import ma, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(120), index=True)
    firstname = db.Column(db.String(120))
    birthday = db.Column(db.String(128))

    def __init__(self, lastname, firstname, birthday):
    	self.lastname = lastname
    	self.firstname = firstname
    	self.birthday = birthday

class UserSchema(ma.Schema):
	class Meta:
		fields = ('id','lastname', 'firstname', 'birthday')

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    propertyType = db.Column(db.String(140))
    description = db.Column(db.String(140))
    rooms = db.Column(db.Integer)
    comments = db.Column(db.String(140))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    city = db.Column(db.String(140))

    def __init__(self, name, propertyType, description, rooms, comments, owner, city):
    	self.name = name
    	self.propertyType = propertyType
    	self.description = description
    	self.rooms = rooms
    	self.comments = comments
    	self.owner = owner
    	self.city = city

class PropertySchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'propertyType', 'description', 'rooms', 'comments', 'owner', 'city')
