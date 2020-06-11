from datetime import datetime, timedelta
import json
import urllib.request
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from collections import Counter
from PyQt5.QtCore import *



def url_builder(cityName,apiKey):
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + cityName + ",de&appid=" + apiKey
    return url


def openUrl(url):
    url = urllib.request.urlopen(url)
    content = url.read().decode('utf-8')
    text = json.loads(content)
    url.close()
    return text


def draw_plots(value, text,x_val,y_val, tempV):
    plt.axes = plt.gca()
    plt.axes.set_ylim([x_val, y_val])

    y = [value[0], value[0], value[0], value[1], value[1], value[1], value[2], value[2], value[2], value[3], value[3],
         value[3],
         value[4], value[4], value[4], value[5], value[5], value[5], value[6], value[6], value[6], value[7], value[7],
         value[7]]
    x = [datetime.now() + timedelta(hours=i) for i in range(24)]

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    plt.xlabel('Datum')
    plt.ylabel(text)


def createPlots(temp, time, weather, humidity):
    draw_plots(temp, 'Temperature in Celsius', -15, 35, '\xb0' + 'C')
    plt.savefig('Bilder/wetter_forecast.png')
    plt.clf()

    draw_plots(humidity, 'Luftfeuchtigkeit', 50, 100, '%')
    plt.savefig('Bilder/rain_forecast.png')
    plt.clf()


def createTemperatureImage(D1,D2):
    black = '#000000'
    filen= 'Bilder/Forecast/temperatureF.png'

    font = ImageFont.truetype("arial.ttf", 30)
    img = Image.new('RGB', (250,100), color='white')
    d = ImageDraw.Draw(img)
    d.text((140, 25), D1, font=font, fill=black)
    d.text((0, 25), D2, font=font, fill=black)
    img.save(filen)
    return filen


def getCelsius(temp):
    temp = int(temp)
    temp = str(temp) + ' C \xB0'
    return temp


def timesetter():

    mytime = datetime.now().hour

    if mytime % 3 == 2:
        time = mytime + 2

    elif mytime % 3 == 1:
        time = mytime + 1

    elif mytime % 3 == 0:
        time = mytime
    return time


def averageTempCalc(temp, time, weather):
    timenow = timesetter()
    timenow = (24-timenow) /3

    tempD1 = temp_NextDays(temp,timenow)
    print("tempD1=")
    print(tempD1)

    tempD2 = temp_NextDays(temp,timenow + 8)
    print("tempD2=")
    print(tempD2)


    wetterD1= weather_NextDays(weather, timenow)
    wetterD2 = weather_NextDays(weather, timenow + 8)

    return wetterD1[0][0],wetterD2[0][0],tempD1,tempD2


def weather_NextDays(weather, timenow):
    list = []
    for i in range (8):
        list.append(weather[int(timenow) + i])

    counterlist = Counter(list)

    return(counterlist.most_common(1))


def temp_NextDays(temp,timenow):
    avgtempDay = 0
    avgtempNight = 0
    avgtempI = 0;

    i = 0
    while i <=3:
        avgtempNight+=(temp[int(timenow + i)])
        i+=1;

    while i <=7:
        avgtempDay += (temp[int(timenow + i)])
        i += 1;

    while i <=8:
        avgtempNight += (temp[int(timenow + i)])
        i += 1;

    for y in range(8):
        avgtempI += (temp[int(timenow + y)])
        print(temp[int(timenow+y)])

    return avgtempI/8


def data_organizer(ctr,text):

    data = dict(
        temp=text['list'][ctr]['main'].get('temp') - 273.15,
        cloudslvl=text['list'][ctr]['weather'][0]['description'],
        date=text['list'][ctr]['dt_txt'],
        humidity=text['list'][ctr]['main'].get('humidity')
    )
    return data


class WetterDatenForecast(QObject):
    def __init__(self, cityName,apiKey):
        super(WetterDatenForecast, self).__init__()
        self.picturePaths = []
        self.CityName = cityName
        self.apiKey = apiKey
        self.updatePaths()

    def paths(self):
        return self.picturePaths

    def updatePaths(self):
        print("create Paths")
        tempTimeWeatherList = self.getForecastDatas()
        createPlots(tempTimeWeatherList[0],tempTimeWeatherList[1],tempTimeWeatherList[2],tempTimeWeatherList[3])
        self.picturePaths.append('Bilder/wetter_forecast.png')
        self.picturePaths.append('Bilder/rain_forecast.png')
        forecast_list = averageTempCalc(tempTimeWeatherList[0], tempTimeWeatherList[1], tempTimeWeatherList[2])
        self.pathToWeatherPicture(forecast_list)
        self.picturePaths.append(createTemperatureImage(getCelsius(forecast_list[2]), getCelsius(forecast_list[3])))

    def pathToWeatherPicture(self,datas):

        path = 'Bilder/wetter/'
        self.picturePaths.append(path + str(datas[0]))
        self.picturePaths.append(path + str(datas[1]))

    def getForecastDatas(self):
        temp_list = []
        time_list = []
        weather_list = []
        humidity_list = []

        for i in range(30):
            datas = data_organizer(i, openUrl(url_builder(self.CityName, self.apiKey)))
            weather_list.append(datas['cloudslvl'])
            temp_list.append(datas['temp'])
            time_list.append(datas['date'])
            humidity_list.append(datas['humidity'])

        return temp_list, time_list, weather_list, humidity_list
