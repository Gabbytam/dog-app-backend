#import models so we can connect to the database
import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


#Blueprint takes a name and the name youre going to use to import
# first argument is blueprints name
# second argument is it's import/export name
# The third argument is the url_prefix so we don't have to prefix all our apis with /api/v1
dog = Blueprint('dogs', 'dog')

#DOG GET ROUTE
@dog.route('/', methods=["GET"])
def get_all_dogs():
    ## find the dogs and change each one to a dictionary into a new array
    try:
        #models.Dog.select() will query the DB to get all the dogs and return in as an array
        #using list comprehension, for in loop, parse the models into dictionaries with k-v paries
        #change the models to a dictionary (key/value pair object) for each dog in the models table
        #then store it in a new array variable
        dogs_to_dict = [model_to_dict(dog) for dog in models.Dog.select()]
        print(dogs_to_dict)
        return jsonify(data=dogs_to_dict, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#POST ROUTE
@dog.route('/', methods=["POST"])
def create_dogs():
    # see request payload, similar to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')

    # this is the same as the line below it
    # dog = models.Dog.create(name=payload['name'], owner=payload['owner'])

    dog = models.Dog.create(**payload)
    ## see the object
    print(dog.__dict__)

    ## Look at all the methods
    print(dir(dog))

    # Change the model to a dict
    print(model_to_dict(dog), 'model to dict')

    #parse to dog you created above 
    dog_dict = model_to_dict(dog)
    
    return jsonify(data=dog_dict, status={"code": 201, "message": "Success"})