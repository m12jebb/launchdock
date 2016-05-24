import datetime
import config

from argon2 import PasswordHasher
from peewee import *


DATABASE = SqliteDatabase('launch.sqlite')
HASHER = PasswordHasher()

class User(Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField()

class Meta:
	database = DATABASE

	@classmethod
	def create_user(cls, username, email, password, **kwargs):
		email = email.lower()
		try:
			cls.select().where(
				(cls.email==email)|(cls.username**username)
				).get()
		except cls.DoesNotExist:
			user = cls(username=username, email=email)
			user.password = user.set_password(password)
			user.save()
			return user
		else:
			raise Exception("User with that email or username already exists")

	@staticmethod
	def set_password(password):
		return HASHER.hash(password)

	def verify_password(self, password):
		return HASHER.verify(self.password, password)




class Company(Model):
	name = CharField()
	address = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Marina(Model):
	name = CharField()
	address = CharField()
	company = ForeignKeyField(Company, related_name='marinas')
	created_at = DateTimeField(default=datetime.datetime.now)
	created_by = ForeignKeyField(User, related_name='marina_set')

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Company, Marina], safe=True)
	DATABASE.close()
