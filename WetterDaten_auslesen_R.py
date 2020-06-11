from datetime import datetime, timedelta, date
import json
import urllib.request
import time
from PIL import Image, ImageDraw, ImageFont
apiKey = "a0a71936f344fc6622a1d440a1ee726b"
StadtName = "Hochdorf"


def url_builder( StadtName, apiKey):
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + StadtName + ",de&appid=" + apiKey
    return (url)


def openUrl( url):
    url = urllib.request.urlopen(url)
    content = url.read().decode('utf-8')
    datas = json.loads(content)
    url.close()
    return datas


def data_organizer( text):
    data = dict(
        city=text.get('name'),
        temp=text.get('main').get('temp') - 273.15,
        sky=text['weather'][0]['description'],
    )
    return data


def getDate(Dayctr):
    Weekday = 'Error'
    Year = time.strftime("%Y")
    Year = int(Year)
    Month = time.strftime("%m")
    Month = int(Month)
    Day = time.strftime("%d")
    Day = int(Day)
    Time = time.strftime("%H")

    Wday = 0
    Wday = date(Year, Month, Day).weekday()
    Wday = Wday + Dayctr
    if (Wday >= 7):
        Wday - 7
        if (Wday == 0):
            Weekday = 'Montag'
        if (Wday == 1):
            Weekday = 'Dienstag'
        if (Wday == 2):
            Weekday = 'Mittwoch'
        if (Wday == 3):
            Weekday = 'Donnerstag'
        if (Wday == 4):
            Weekday = 'Freitag'
        if (Wday == 5):
            Weekday = 'Samstag'
        if (Wday == 6):
            Weekday = 'Sonntag'
    else:
        if (Wday == 0):
            Weekday = 'Montag'
        if (Wday == 1):
            Weekday = 'Dienstag'
        if (Wday == 2):
            Weekday = 'Mittwoch'
        if (Wday == 3):
            Weekday = 'Donnerstag'
        if (Wday == 4):
            Weekday = 'Freitag'
        if (Wday == 5):
            Weekday = 'Samstag'
        if (Wday == 6):
            Weekday = 'Sonntag'

    return Weekday, Time


def createTemperatureImage(temp,city):
    black = '#000000'
    date = getDate(0)
    temp = str(temp) + '\xb0' + 'C'
    fontText = ImageFont.truetype("arial.ttf",  30)
    fontTemp = ImageFont.truetype("arial.ttf",  40)
    filen = ('Bilder/wetterA.png')
    img = Image.new('RGB', (300,250), color = 'white')
    d = ImageDraw.Draw(img)
    d.text((10,10),city , font = fontText, fill = black)
    d.text((10,50),date[0] +'  '+  date[1]+ ' Uhr', font = fontText, fill = black)
    d.text((150,125),temp,font = fontTemp, fill = black)
    img.save(filen)

    Day1 =createDates(black, 1,"1")
    Day2 =createDates(black, 2,"2")

    return [filen,Day1,Day2]


def createDates(black,ctr,name):
    Day = getDate(ctr)
    fontText = ImageFont.truetype("arial.ttf", 25)
    filen = ('Bilder/Day'+ name + '.png')
    img = Image.new('RGB', (175, 75), color='white')
    d = ImageDraw.Draw(img)
    d.text((10, 0), Day[0], font=fontText, fill=black)
    img.save(filen)
    return filen


class WeatherDataAktuell():
    def __init__(self):
        self.picturePaths = []
        self.updatePaths()

    def paths(self):
        return self.picturePaths

    def updatePictures(self):
        if self.loopctr %6 == 1:
            self.modelAktuell.updatePaths()

    def updatePaths(self):
        self.picturePaths = []
        self.picturePaths.append('Bilder/wetter/background.png')
        weatherDict = data_organizer(openUrl(url_builder(StadtName, apiKey)))

        self.pathToWeatherPicture(weatherDict['sky'])
        self.picturePaths.extend(createTemperatureImage(int(weatherDict['temp']), weatherDict['city']))

    def pathToWeatherPicture(self,sky):
        self.picturePaths.append('Bilder/wetter/' + sky + '.png')


