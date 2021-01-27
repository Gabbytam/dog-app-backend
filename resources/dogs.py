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
        # return the object/dict 
        return jsonify(data = dogs_to_dict, status = {"code": 200, "message": "Success"})
    except models.DoesNotExist:
        # return an empty object 
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#POST ROUTE
@dog.route('/', methods=["POST"])
def create_dogs():
    # see request payload, similar to req.body in express. payload comes back as an object 
    payload = request.get_json()
    print(type(payload), 'payload')

    # this is the same as the line below it
    # dog = models.Dog.create(name=payload['name'], owner=payload['owner'])
    # ** says to spread the payload and put it into an object that looks like a payload
    dog = models.Dog.create(**payload)
    ## see the object
    print(dog.__dict__)

    ## Look at all the methods
    #print(dir(dog))

    # Change the model to a dict
    #print(model_to_dict(dog), 'model to dict')

    #parse to dog you created above 
    dog_dict = model_to_dict(dog)
    
    return jsonify(data=dog_dict, status={"code": 201, "message": "Success"})

# GET ROUTE THAT WILL GET ONE DOG BY ITS ID
# to catch a changing url, use <__>
@dog.route('/<dog_id>', methods=['GET'])
def get_dog(dog_id):
    try:
        dog = models.Dog.get_by_id(dog_id)
        dog_dict = model_to_dict(dog)
        return jsonify(data = dog_dict, status = {'code': 200, 'message': 'success'})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# PUT/EDIT ROUTE THT EDITS A DOG BASED ON ID
@dog.route('/<dog_id>', methods = ['PUT'])
def update_dog(dog_id):
    try:
        payload = request.get_json()
        # grab the whole object and update the whole thing
        # grab models, go to Dog model and check if id matched the passed in dog_id
        query = models.Dog.update(**payload).where(models.Dog.id == dog_id)
        query.execute()
        # grab dog and turn it into a dic all in one
        updated_dog = model_to_dict(models.Dog.get_by_id(dog_id))
        return jsonify(data = updated_dog, status = {'code': 200 , 'message': 'updated successfully'})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})


#DELETE ROUTE FOR DELETING A DOG #Delete route only has the D capitalized
@dog.route('/<dog_id>', methods =['Delete'])
def delete_dog(dog_id):
    dog_to_delete = models.Dog.get_by_id(dog_id)
    dog_to_delete.delete_instance()

    #alternative way to delete
    # query = models.Dog.delete().where(models.Dog.id == dog_id)
    # query.execute()
    
    return jsonify(data={}, status = {'code': 200, 'message': 'Resource successfully deleted'})


