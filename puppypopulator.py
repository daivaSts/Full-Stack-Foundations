# Udacity.com /ud088 / Full Stack Foundations
# PS1: Puppy Shelters
# file 2 of 2

# Assignment:
# Create a database for the Uda County District of Animal Shelters and populate the database with
# puppies and shelters.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from puppies import Base, Shelter, Puppy

#from flask.ext.sqlalchemy import SQLAlchemy
from random import randint
import datetime
import random
from decimal import *


engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#ADD DATA TO THE DATABASES:
#Add Shelters
shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zipCode = "94601", website = "oaklandanimalservices.org")
session.add(shelter1)

shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zipCode = "94103", website = "sfspca.org")
session.add(shelter2)

shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zipCode = "94103", website = "http://wonderdogrescue.org")
session.add(shelter3)

shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zipCode = "94501", website = "hsalameda.org")
session.add(shelter4)

shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zipCode = "94025", website = "paloaltohumane.org")
session.add(shelter5)


#Add Puppies
male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]
female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']
puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct","http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct","http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct","http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg","http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct","http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct","http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct","http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct","http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

#This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
def CreateRandomAge():
	today = datetime.date.today()
	days_old = randint(0,540)
	birthday = today - datetime.timedelta(days = days_old)
	return birthday

#This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
def CreateRandomWeight():
	return random.uniform(1.0, 40.0)

for i,x in enumerate(male_names):
	new_puppy = Puppy(name = x, gender = "male", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images) ,shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()

for i,x in enumerate(female_names):
	new_puppy = Puppy(name = x, gender = "female", dateOfBirth = CreateRandomAge(),picture=random.choice(puppy_images),shelter_id=randint(1,5), weight= CreateRandomWeight())
	session.add(new_puppy)
	session.commit()


#Using SQLAlchemy perform the following queries on your database:

# 1. Query all of the puppies and return the results in ascending alphabetical order
puppies = session.query(Puppy).order_by(Puppy.name)
count = 0
for puppy in puppies:
	count += 1
	print str(count) +". " + str(puppy.name)


# 2. Query all of the puppies that are less than 6 months old organized by the youngest first
puppies = session.query(Puppy).order_by(Puppy.dateOfBirth.desc())
half_year_ago = datetime.date.today() - datetime.timedelta(days=180)
for puppy in puppies:
	if puppy.dateOfBirth > half_year_ago:
		print str(puppy.name) + "'s birth day is " +  str(puppy.dateOfBirth)

# 3. Query all puppies by ascending weight
puppies = session.query(Puppy).order_by(Puppy.weight)
for puppy in puppies:
	puppy_weight = Decimal(puppy.weight).quantize(Decimal('.01'), rounding=ROUND_DOWN)
	print str(puppy.name) + " weights " + str(puppy_weight) + " lb."


# 4. Query all puppies grouped by the shelter in which they are staying
shelters = session.query(Shelter).group_by(Shelter.name)
puppies = session.query(Puppy).order_by(Puppy.shelter_id)
for puppy in puppies:
	print str(puppy.name) + ": "+ str(puppy.shelter.name)

# 5. Clear the database
puppies = session.query(Puppy).filter(Puppy.name > 'A')
for i in puppies:
	session.delete(i)
session.commit()

puppies = session.query(Puppy).order_by(Puppy.name)
count = 0
for puppy in puppies:
	count += 1
	print str(count) +". " + str(puppy.name)