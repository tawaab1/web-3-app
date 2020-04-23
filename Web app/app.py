from flask import Flask, render_template, redirect, url_for, request
from mongoengine import *
import os
import csv
connect ('DB_COUNTRIES')




app = Flask(__name__)
app.config.from_object('config')

namePage= "Aisea Busa Tawake"
class Country(Document):
  name = StringField()
  data = DictField()
@app.route('/')
def index():
    return render_template('index.html', name=namePage), 200

@app.route('/inspiration')
def inspiration():
    return render_template('inspiration.html'), 200

# @app.route('/addCountry')
# def addCountry():
#     return render_template('addCountry.html',name=namePage), 200

# @app.route('/deleteCountry')
# def deleteCountry():
#     return render_template('deleteCountry.html',name=namePage), 200

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html'), 200


@app.route('/countries', methods=['GET'])
@app.route('/countries/<country_id>', methods=['GET'])
def getCountries(country_id=None):
   countries = None
   if country_id is None:
        countries = Country.objects
   else:
        countries = Country.objects.get(id=country_id)
   return countries.to_json(), 200

@app.route('/addCountry', methods=['POST', 'GET'])
def addCountry():
  if request.method == "POST":
        newCountryName = request.form["countryName"]
        newData = request.form["data"]
        newCountry = Country(name=newCountryName,data=newData)
        newCountry.save()
        return render_template('addCountry.html'), 200
  else:
        return render_template('addCountry.html')

@app.route('/deleteCountry', methods=['GET', 'POST'])
def deleteCountry():
  if request.method == 'POST':
    CountryName = request.form["countryName"]
    deleteCountryName = Country(name=CountryName)
    deleteCountryName.delete()
    return render_template('deleteCountry.html'), 200
  else:
    return render_template('deleteCountry.html')

@app.route('/countryData')
def countryData():
  for file in os.listdir(app.config['FILES_FOLDER']):
        filename = os.fsdecode(file)
        path = os.path.join(app.config['FILES_FOLDER'], filename)
        f = open(path)
        r = csv.reader(f)
        d = list(r)
        for data in d:
         for file in os.listdir(app.config['FILES_FOLDER']):
          filename = os.fsdecode(file)
          path = os.path.join(app.config['FILES_FOLDER'],filename)
          f = open(path)
          r = csv.DictReader(f) 
          d = list(r)
        for data in d:
                  print(data)
                  country = Country() # a blank placeholder country
                  dict = {} # a blank placeholder data dict
        for key in data: # iterate through the header keys
            if key == "country":
                country = Country(name=data[key])# check if this country already exists in the db
                  # if the country does not exist, we can use the new blank country we created above, and set the name
                  
                # if the country already exists, replace the blank country with the existing country from the db, and replace the blank dict with the current country's data                
            else:
                f = filename.replace(".csv","") # we want to trim off the ".csv" as we can't save anything with a "." as a mongodb field name
                if f in dict: # check if this filename is already a field in the dict
                    dict[f][key] = data[key] # if it is, just add a new subfield which is key : data[key] (value)
                else:
                    dict[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict

                    country= Country(name=data[key], data=dict[f])# add the data dict to the country

                country.save()# save the country
        return render_template('countryData.html'), 200

if __name__ =="__main__":
	#app.run(debug=True, port=80, host='0.0.0.0')
  app.run(debug=True, port=8080)


