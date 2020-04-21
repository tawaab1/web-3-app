from flask import Flask, render_template, redirect, url_for
from mongoengine import *
import os
import csv
connect ('DB_USERS')
connect ('DB_COUNTRY')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length = 50)
    last_name = StringField(max_length = 50)

class Country(Document):
  name = StringField()
  data = DictField()

app = Flask(__name__)
app.config.from_object('config')

namePage= "Aisea Busa Tawake"

@app.route('/')
def index():
    aisea = User(email = 'tawaab1@student.op.ac.nz', first_name = 'Aisea', last_name = 'Tawake')
    aisea.save()
    for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'], filename)
        f = open(path)
        r = csv.reader(f)
        d = list(r)
        for data in d:
        country = Country() # a blank placeholder country
        dict = {} # a blank placeholder data dict
        for key in data: # iterate through the header keys
            if key == "country":
                # check if this country already exists in the db
                
                # if the country does not exist, we can use the new blank country we created above, and set the name

                # if the country already exists, replace the blank country with the existing country from the db, and replace the blank dict with the current country's 
                # data                
            else:
                f = filename.replace(".csv","") # we want to trim off the ".csv" as we can't save anything with a "." as a mongodb field name
                if f in dict: # check if this filename is already a field in the dict
                    dict[f][key] = data[key] # if it is, just add a new subfield which is key : data[key] (value)
                else:
                    dict[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict

            # add the data dict to the country

        # save the country
    return render_template('index.html', name=namePage)

@app.route('/inspiration')
def inspiration():
    return render_template('inspiration.html',name=namePage)



if __name__ =="__main__":
	 app.run(debug=True, port=80, host='0.0.0.0')
     #app.run(debug=True, port=8080)


@app.route('/users', methods=['GET'])
@app.route('/users/<user_id>', methods=['GET'])
def getUsers(user_id=None):
   users = None
   if user_id is None:
        users = User.objects
   else:
        users = User.objects.get(id=user_id)
    return users.to_json()

@app.route('/users', methods=['POST'])
@app.route('/users', methods=['DELETE'])