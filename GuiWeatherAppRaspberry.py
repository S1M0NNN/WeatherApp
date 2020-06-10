import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from datetime import datetime
import WetterDaten_auslesen_forecast_R
import WetterDaten_auslesen_R

apiKey = "a0a71936f344fc6622a1d440a1ee726b"

class App(QWidget):

    def __init__(self):
            super(App, self).__init__()
            self.title = 'weather App'
            self.left = 10
            self.top = 10
            self.width = 640
            self.height = 480                
            self.loopctr = 0
            self.loopTimer = QTimer()
            self.modelAktuell = WetterDaten_auslesen_R.WeatherDataAktuell()
            self.modelForecast = WetterDaten_auslesen_forecast_R.WetterDatenForecast('Biberach',apiKey)
            self.initUI()
            self.modelAktuell.updatePaths()
            self.modelForecast.updatePaths()
            self.OnPathsUpdated()


    def initUI(self):

            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            self.background = QLabel(self)
            self.background.move(0,0)

            self.labelWA = QLabel(self)
            self.labelWA.move(25, 0)

            self.labelSkyA = QLabel(self)
            self.labelSkyA.move(0, 105)

            self.labelWF = QLabel(self)
            self.labelWF.move(315, 0)

            self.ForecastF = QLabel(self)
            self.ForecastF.move(50, 320)

            self.wetterD1 = QLabel(self)
            self.wetterD1.move(0, 230)

            self.wetterD2 = QLabel(self)
            self.wetterD2.move(135, 230)
            
            self.nextDay = QLabel(self)
            self.nextDay.move(20, 400)
            
            self.SecondDay = QLabel(self)
            self.SecondDay.move(170, 400)

            self.updateLabel = QLabel(self)
            self.updateLabel.setText('Updatet at:                                   ')
            self.updateLabel.move(25,450)

            self.updateWeatherLabel()
            self.showFullScreen()

    def OnPathsUpdated(self):
            self.loopTimer.timeout.connect(self.updateWeatherLabel)
            self.loopTimer.start(5000)


    def updateWeatherLabel(self):

        self.loopctr += 1
        today = datetime.now()
        mytime = 'Updatet at: ' + datetime.strftime(today, "%d-%m-%y %H:%M")
        
        if self.loopctr %6 == 1:
            self.modelAktuell.updatePaths()

        if self.loopctr == 60:
            self.modelForecast.updatePaths()
            self.updateLabel.setText(mytime)
            self.loopctr = 0

        self.background.setPixmap(QPixmap(self.modelAktuell.paths()[0]))
        self.labelSkyA.setPixmap(QPixmap(self.modelAktuell.paths()[1]))
        self.labelWA.setPixmap(QPixmap(self.modelAktuell.paths()[2]))
        self.wetterD1.setPixmap(QPixmap(self.modelForecast.paths()[2]))
        self.wetterD2.setPixmap(QPixmap(self.modelForecast.paths()[3]))
        self.nextDay.setPixmap(QPixmap(self.modelAktuell.paths()[3]))
        self.SecondDay.setPixmap(QPixmap(self.modelAktuell.paths()[4]))
        self.ForecastF.setPixmap(QPixmap(self.modelForecast.paths()[4]))
        if self.loopctr %2:
            self.labelWF.setPixmap(QPixmap(self.modelForecast.paths()[0]))
        else:
            self.labelWF.setPixmap(QPixmap(self.modelForecast.paths()[1]))


if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = App()
        sys.exit(app.exec_())
