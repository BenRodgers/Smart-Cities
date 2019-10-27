import datetime
import calendar
import json, csv
from datetime import timedelta  
from csv import writer


#Create header for the output csv
with open('uqWeek41Wifi7.csv', 'a') as csv_file:
    fieldnames = ['DayOfWeek', 'TimeOfDay', 'Longitude', 'Latitude', 'UserType', 'Building', 'Connection']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader() 

# Read each line of the JSON 
f = open('uq-wireless-locations-w41-2018.json', "r")
for line in f:
    #Hold each line to be written to the csv file
    data = []
    #Load JSON Object
    parsed_json = (json.loads(line))
    #Get timestamps
    timestamp = (parsed_json['_source']['@timestamp'])
    #Convert JSON to datetime format
    t = datetime.datetime.strptime(timestamp.split(".")[0], '%Y-%m-%dT%H:%M:%S')
    #Convert from UTC to Brisbane Time
    t = t + timedelta(hours = 8)
    
    #Get the individual time components from JSON: day, month, year etc ...
    year = t.year
    month = t.month
    day = t.day
    hour = t.hour
    minute = t.minute
    second = t.second
    
    #Get day of the week
    dayOfTheWeek = calendar.day_name[calendar.weekday(year, month, day)]
    #Get the week of the year
    weekOfTheYear = datetime.date(year, month, day).isocalendar()[1]+1
    
    #Combine datime
    timeOfDay = datetime.time(hour, minute, second)
    
    #Get the individual longitude and latitude locations
    splitGeolocation = (parsed_json['_source']['source']['geoip']['location'].split(', '))
    longitude = splitGeolocation[0]
    latitude = splitGeolocation[1]

    #Get the Client type: Student, Staff and Guest
    if 'wireless' in parsed_json['_source']:
        user = parsed_json['_source']['wireless']['clientType']
    else: 
        user = 'NULL'

    #Get the building number (or Outside)
    if 'source' in parsed_json['_source']:
        if 'location' in parsed_json['_source']['source']:
            building = parsed_json['_source']['source']['location']['building_comp']
        else:
            building = 'Outside'
    else: 
        building = 'Outside'
    
    #Get the type of service (Wifi, Local connection)
    if 'user' in parsed_json['_source']:
        service = parsed_json['_source']['user']['service']
    else:
        service = 'NULL'
    
    #Make a dictionary of the values
    row = {'DayOfWeek': dayOfTheWeek, 'TimeOfDay': timeOfDay, 'Longitude': longitude, 'Latitude': latitude, 'UserType': user, 'Building': building, 'Connection': service }
    #Add to row (to be appended to the csv file)
    data.append(row)

    #Append new row to the csvfile
    with open('uqWeek41Wifi7.csv', 'a') as csv_file:
        fieldnames = ['DayOfWeek', 'TimeOfDay' , 'Longitude', 'Latitude', 'UserType', 'Building', 'Connection']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        for row in data: 
            writer.writerow(row)
