from flask import Flask, render_template, redirect, url_for, request
from mongoengine import *
import os
import csv
connect ('DB_COUNTRIES2')




app = Flask(__name__)
app.config.from_object('config')


class Country(Document):
  name = StringField()
  data = DictField()

namePage= "Aisea Busa Tawake"
@app.route('/')
def index():
    return render_template('index.html', name=namePage), 200

@app.route('/inspiration')
def inspiration():
    return render_template('inspiration.html', name=namePage), 200

# @app.route('/addCountry')
# def addCountry():
#     return render_template('addCountry.html',name=namePage), 200

# @app.route('/deleteCountry')
# def deleteCountry():
#     return render_template('deleteCountry.html',name=namePage), 200

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html'), 200


@app.route('/countries', methods=['GET','POST','PUT'])
@app.route('/countries/<name>', methods=['GET'])
def getCountries(name=None):
   countries = None
   if name is None:
        countries = Country.objects
   else:
        countries = Country.objects.get(name = name)
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
        path = os.path.join(app.config['FILES_FOLDER'],filename)
        f = open(path)
        r = csv.DictReader(f) 
        d = list(r)
        for data in d:
            country = Country() # a blank placeholder country
            libs = {} # a blank placeholder data dict
            for key in data: # iterate through the header keys
                if key == "country": # check if this country already exists in the db
                
                # if the country does not exist, we can use the new blank country we created above, and set the name  
                    if Country.objects(name = data[key]).count() == 0:
                        country['name'] = data[key]                        
                    else:
                        # if the country already exists, replace the blank country with the existing country from the db, and replace the blank dict with the current country's 
                        # data      
                        country = Country.objects.get(name = data[key])  
                        libs = country['data']           
                else:
                    f = filename.replace(".csv","") # we want to trim off the ".csv" as we can't save anything with a "." as a mongodb field name
                    if f in libs: # check if this filename is already a field in the dict
                        libs[f][key] = data[key] # if it is, just add a new subfield which is key : data[key] (value)
                    else:
                        libs[f] = {key:data[key]} # if it is not, create a new object and assign it to the dict
                country['data'] = libs
            country.save()   
  return render_template('countryData.html'), 200

if __name__ =="__main__":
	#app.run(debug=True, port=80, host='0.0.0.0')
  app.run(debug=True, port=8080)


