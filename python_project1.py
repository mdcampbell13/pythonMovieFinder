import http.client
import json
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
from os import system
import math
import os
from dotenv import load_dotenv
import pandas as pd


import csv

load_dotenv()


OPENAPIKEY = os.getenv('OPENAPI_KEY')


def movie_finder():
    dTitle1 = "Not Found"
    dPoster1 = "Not Found"
    dStars1 = "Not Found"
    dYear1 = "Not Found"

    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': OPENAPIKEY,
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
        }

    m_string = input('\nEnter a movie you would like to search for.  ')

    if " " in m_string:
        m_string = m_string.replace(" ", "_")

    conn.request("GET", "/auto-complete?q={}".format(m_string), headers=headers)

    res = conn.getresponse()
    data = res.read()
    dataJson = json.loads(data)

    try:
        dTitle1 = dataJson["d"][0]["l"]
        dPoster1 = dataJson["d"][0]["i"]["imageUrl"]
        dStars1 = dataJson["d"][0]["s"]
        last_char_index = dStars1.rfind(",")
        dStars1 = dStars1[:last_char_index] + " and" + dStars1[last_char_index+1:]
        dYear1 = dataJson["d"][0]["y"]
    except KeyError:
        print("\nEntering nothing results in the first occurance in IMDB's database being retrieved.")



    if dTitle1 == "Not Found":
        if "_" in m_string:
            m_string = m_string.replace("_", " ")
        print(" ")
        print('"{}" not found in IMDB API database.'.format(m_string))
    else:
        print(" ")
        print("\nTitle: {}".format(dTitle1))
        print("Movie Image URL: {}".format(dPoster1))
        print("Stars: {}".format(dStars1))
        print("Year Released: {}".format(dYear1))
        print(" ")


def holiday():
    conn = http.client.HTTPSConnection("public-holiday.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': OPENAPIKEY,
        'x-rapidapi-host': "public-holiday.p.rapidapi.com"
        }

    tz = timezone('EST')

    fnow = datetime.datetime.now(tz).year

    fconn = "/{}/US".format(fnow)

    conn.request("GET", fconn, headers=headers)

    res = conn.getresponse()
    data = res.read()

    data2 = json.loads(data)


    i = 0
    while i < len(data2):
        if datetime.datetime.now(tz) < datetime.datetime.strptime(data2[i]["date"], "%Y-%m-%d").replace(tzinfo=timezone('EST')):
            t_diff = datetime.datetime.strptime(data2[i]["date"], "%Y-%m-%d").replace(tzinfo=timezone('EST')) - datetime.datetime.now(tz)
            print("\nThe next holiday is {}.\nThe party starts in {} days!".format(data2[i]["name"], t_diff.days))
            break
        i += 1


def property_search():

# A note regarding this function. A completed list of Jefferson county streets can be easily scraped from 'https://geographic.org/streetview/usa/ky/jefferson/louisville.html' and iterated through
# inserting every street name in the county into the street variable. This would compile a complete listing of every property in Jefferson county, the data attributes of them and place them in a
# csv file. I did not include any code to do that since it would take literally days for it to run if not longer.


    print("\n")

    prop_dict = []

    page_num = 1

    address = input("What street would you like to search? ")

    address = address.replace(".", "")


    print("\n")

    # This block of code gets the number of records off the initial webpage and then calculates the number of pages based on 25 properties per page

    try:
        r1 = requests.get("https://jeffersonpva.ky.gov/property-search/property-listings/?order=ASC&sort=street&psfldAddress={}&searchType=StreetSearch&searchPage={}#results".format(address, page_num),
             headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
        c1=r1.content
        soup1=BeautifulSoup(c1, "html.parser")


        records_found1 = soup1.find("h1", {"id": "results"}).find_next("h3")

        num_str = records_found1.text.split()[0]

        print(num_str + " Records Found")

        num_int = int(num_str)

        total_pages = math.ceil(num_int / 25)

        j = 0

        # This block of code iterates through the number of pages and scrapes info from pages

        while j < total_pages:
            try:
                r2 = requests.get("https://jeffersonpva.ky.gov/property-search/property-listings/?order=ASC&sort=street&psfldAddress={}&searchType=StreetSearch&searchPage={}#results".format(address, page_num),
                headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
                c2=r2.content
                soup2=BeautifulSoup(c2, "html.parser")
                all2=soup2.find_all("td")
            except IndexError:
                print("Oppps. You can only enter a street name, not a full address")



            for span_tag in soup2.findAll("span"):
                span_tag.replace_with("")



            for i in range(0, len(all2), 5):

                all2_image_rep = all2[i].a.img['src']

                all2_image_rep2 = all2_image_rep.replace("w75-h57", "w600-h456")

                # This block of code reaches into the individual property page of each property and scrapes the assessed value of each property

                val_pg = all2[i].a['href']

                r3 = requests.get(("https://jeffersonpva.ky.gov" + val_pg).format(address, page_num),
                     headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
                c3=r3.content
                soup3=BeautifulSoup(c3, "html.parser")
                all3=soup3.find_all("dd")




                prop_dict2 = {"Property_image": "https://jeffersonpva.ky.gov" + all2_image_rep2, "property_owner": all2[i+2].text, "property_address": all2[i+1].text, "property_type": all2[i+3].text, "parcel_ID": all2[i+4].text, "acres": all3[3].text, "Neighborhood": all3[4].text, "Value": all3[2].text}

                print("\nProp. Image:     " + "https://jeffersonpva.ky.gov" + all2_image_rep2)
                print("Owner:           " + all2[i+2].text)
                print("Address:         " + all2[i+1].text)
                print("Prop. Type:      " + all2[i+3].text)
                print("Parcel ID:       " + all2[i+4].text)
                print("Acres:           " + all3[3].text)
                print("Neighborhood:    " + all3[4].text)
                print("Value:           $" + all3[2].text)

                prop_dict.append(prop_dict2)
                
            page_num += 1
            j += 1


    except AttributeError:
        print("Oppps. Something went wrong.")


    a = prop_dict  

    type(a[0])

    df = pd.DataFrame(a)

    df.to_csv(r'CSV_files/property_info.csv')

    print('\n A CSV file containing the information from this query has been created in the "CSV_files" folder in the root of this directory.\n')


    

while True:

    print('\nFor Movie Info Enter "1"\nFor Upcoming Holiday Counter Enter "2"\nFor Jefferson County Street Property Search enter "3"\nTo Quit Enter "Q"')
    command = input('\nPlease Enter A Selection:  ')
    if command == "1":
        try:
            movie_finder()
        except ValueError:
            print("\nSorry. You must enter a value.")
    elif command == "2":
        holiday()
    elif command == "3":
        property_search()
    elif command == "Q" or command == "q":
        print("\n")
        break
    else:
        print("\nSorry. You must enter a valid option.")