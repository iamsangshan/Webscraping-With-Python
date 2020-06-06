#Web scraping

#Get the air quality of a location and put into a CSV file

import pandas
import requests
from bs4 import BeautifulSoup

# get the page
page = requests.get(
  'https://forecast.weather.gov/MapClick.php?lat=34.099695000000054&lon=-118.33539999999999#.XtjMPTozY2w'
)

#get the page source code
soup = BeautifulSoup(page.content, 'html.parser')
week = soup.find(id='seven-day-forecast-body')

#get the daily air quality forecast content

items = week.find_all(class_="tombstone-container")

# LIST COMPREHENESION  
period_names = [item.find(class_="period-name").get_text() for item in items]
#print(period)
descriptions = [item.find(class_="short-desc").get_text() for item in items]
#print(descriptions)
temperatures = [item.find(class_="temp").get_text()  for item in items]
#print(temperatures)

weatherStuff = pandas.DataFrame(
  {
    'periods' : period_names,
    'descrs'  : descriptions,
    'temps'   : temperatures,
  },
)

print(weatherStuff)

weatherStuff.to_csv("weather_la.csv")