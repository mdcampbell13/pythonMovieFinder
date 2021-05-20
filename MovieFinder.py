import http.client
import json
import datetime
from pytz import timezone
from os import system
import os
from dotenv import load_dotenv

load_dotenv()

cls = lambda: system('cls')
cls()

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

    m_string = input('Enter a movie you would like to search for.  ')

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

while True:

    print('\nFor Movie Info Enter "1"\nFor Upcoming Holiday Counter Enter "2"\nTo Quit Enter "Q"')
    command = input('Please Enter A Selection:  ')
    if command == "1":
        try:
            movie_finder()
        except ValueError:
            print("\nSorry. You must enter a value.")
    elif command == "2":
        holiday()
    elif command == "Q" or command == "q":
        print("\n")
        break
    else:
        print("\nSorry. You must enter a valid option.")
