# -----------------------------------------------------------------------------
# Name: Briefing.py
# Author: Andrew Doan
# -----------------------------------------------------------------------------

import urllib.request
import urllib.error
import re
import sys
import datetime
import pyowm
import os
# Enter your function definitions here
def urltostring(url,topic):
    try:
        openurl=urllib.request.urlopen(url)
    except urllib.error.URLError as x:
        print("Error opening url: {}\n{}".format(url,x))
    else:
        try:
            urltext=openurl.read().decode("UTF-8")
        except UnicodeError as e:
            print("Error decoding url:{}\n{}".format(url,e))
        else:
            pattern=  r'\>([^\<]*\b{}\b.*?)\<'.format(topic)
            matches=re.findall(pattern,urltext,re.IGNORECASE|re.DOTALL)
            if matches:
                return("Source url: {}\n\n".format(url)+('\n'.join(matches))+"\n--------------------------------\n")
            else:
                return
    openurl.close()

def main():
    date=datetime.datetime.now()
    filename='{}{}{}'.format(date.month,date.day,date.year)+"_Briefing.txt"
    if not os.path.exists('C:/Users/Public/Briefings'):
        os.mkdir('C:/Users/Public/Briefings')
        if not os.path.exists('C:/Users/Public/Briefings/Files'):
            os.mkdir('C:/Users/Public/Briefings/Files')
    with open('C:/Users/Public/Briefings/'+filename,"w") as file:
        file.write('--------------------------------\nWEATHER\n--------------------------------\n')
        owm=pyowm.OWM('79322f3c896f90418a7bdf87cc947675')
        with open('C:/Users/Public/Briefings/Files/location.txt') as locationfile:
            for location in locationfile:
                file.write('Weather at {} is:\n{}\n'.format(location.rstrip('\n'),owm.weather_at_place(location.rstrip('\n')).get_weather().get_temperature('fahrenheit')))
        file.write('--------------------------------\nNEWS\n--------------------------------\n')
        with open('C:/Users/Public/Briefings/Files/websites.txt') as urlfile:
            with open('C:/Users/Public/Briefings/Files/topics.txt') as topicfile:
                for topic in topicfile:
                    file.write('{}\n--------------------------------\n'.format(topic))
                    for line in urlfile:
                      try:
                          file.write(urltostring(line.rstrip('\n'),topic.rstrip('\n')))
                      except Exception:
                           continue
                    file.write('--------------------------------\n')
if __name__ == '__main__':
    main()
    
