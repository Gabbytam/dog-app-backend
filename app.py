from flask import Flask, jsonify, request, g
from flask_cors import CORS

#import models from the models file
import models
#import dog from dogs file (comes from Blueprint)
from resources.dogs import dog 

app = Flask(__name__)

#MIDDLEWARE that does checks before getting to the responses 
# when developing a web application, it’s common to open a connection when a request starts, and close it when the response is returned. 
#before the request is sent, we connect to the database
@app.before_request
def before_request():
    #connect to the database before each request, DATABASE comes from models file
    # g stands for global and we are setting up a global access to our database throughout the app.
    g.db = models.DATABASE
    g.db.connect()

#after the request is sent, we close the database and return the response
@app.after_request
def after_request(response):
    #close the database connection after each request
    g.db.close()
    return response

CORS(dog, origins=['http://localhost:3000'], supports_credentials=True)

#equivalent to app.use(dogs, '/api/vi/dogs')
#pass in dog and the url pattern, dog is the Blueprint for the dogs routes
app.register_blueprint(dog, url_prefix = '/api/v1/dogs')






#ROUTES:
#simple route example #start all routes with @app.route
#use @app.route and pass in the url pattern and then give it a callback function
@app.route('/')
def index():
    return 'Hola biznatches'

#how to pass params to the route/url pattern: put param in < > and also pass it into function
@app.route('/sayhello/<name>')
#pass your function the param from url pattern
def say_hello(name):

    #declare a variable to catch a value that is passed to params after ? #pass get the key and it will save the value pair
    band = request.args.get('bandname')
    #whatever is passed will return in json format
    return jsonify(
        msg = 'Hello',
        band_name = band,
        status = 200,
        list = ['Franklin', 'Delphene', 'Braxton'],
        artist = 'Ted '+ name)


#set up to start listening for requests
if __name__ == '__main__':
    #when you start the server this calls the models initialize function that will call database and create the table
    models.initialize()
    app.run(port = 8000, debug = True)

#debug = True will add CSS to make the error appear more clearly on the browser