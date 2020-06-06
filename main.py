#Web scraping and creating a CSV file with Pollution data of a City

#Get the air quality of a location and put into a CSV file

#import all the modules required
import pandas
import requests
from bs4 import BeautifulSoup
import replit

#replit.clear()

#get the entire page source code (unless they take this link down, this code should continue to work)
page = requests.get(
    "https://air-quality.com/place/india/bengaluru/f8edf853?lang=en&standard=aqi_us"
)

#make it to a beautiful soup object, so we can scrape easily
soup = BeautifulSoup(page.content, "html.parser")

#get the weekly content from the soup object. If the container we're interested in doesn't have an id, use class
week = soup.find(class_="daily-forecast-scroll")

#get all week's data elements and put into a list
pollution_all_week = week.find_all(class_="forecast-item")


# This is one way to do it, other way is List comprehenstion
# But through this way, we can avoid multiple for loops.
# Init the lists you need.
dates = []
temps = []
poll_indices = []
short_descs = []

#Start scraping all the data you need now.
for pollution_data in pollution_all_week:
    #date
    dates.append(pollution_data.find(class_='date').get_text())

    #templow and temphigh
    temps.append(pollution_data.find(class_='temperature temp_c').get_text())

    #pollution index - took almost 3 hrs *!*
    level_1 = pollution_data.find(class_="value-wrap")
    if (level_1):
      level_2 = level_1.find(class_="value")
      level_3 = level_2.find("span")
      poll_indices.append(level_3.string)
    else:
      poll_indices.append("N/A")

    #short description - dont know if its an ugly hack or a genius solution. I think its the former
    level_1 = pollution_data.find(class_="value-wrap")
    if (level_1):
      level_2 = level_1.find(class_="value")
      level_3 = level_2.find("span")
      short_descs.append(level_3.next_sibling.next_element)
    else:
      short_descs.append("N/A")

# Put all lists into a dictionary. i.e. make each list a dictionary item.
pollution_dict = {
  "date" : dates,
  "temp" : temps,
  "pollution_index" : poll_indices,
  "short_desc" : short_descs,
}

# Create a Pandas DataFrame with our dictionary
pollution_pd = pandas.DataFrame(pollution_dict)

#### Convert the DataFrame to a CSV file using Pandas
pollution_pd.to_csv("pollution_bangalore_10days.csv")

# Voila! Checkout the CSV file generated in the current folder.
# Good night. Good morning.. Whatever...