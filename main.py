import sys
import requests
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:",self)
        self.city_input = QLineEdit(self)
        self.get_wheather_button = QPushButton("Get Wheather",self)
        self.temperature_label = QLabel(self)
        self.emoji_Label = QLabel(self)
        self.description_Label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Wheather App")

        vBox = QVBoxLayout()
        vBox.addWidget(self.city_label)
        vBox.addWidget(self.city_input)
        vBox.addWidget(self.get_wheather_button)
        vBox.addWidget(self.temperature_label)
        vBox.addWidget(self.emoji_Label)
        vBox.addWidget(self.description_Label)

        self.setLayout(vBox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_Label.setAlignment(Qt.AlignCenter)
        self.description_Label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_wheather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_Label.setObjectName("emoji_label")
        self.description_Label.setObjectName("description_label")

        self.setStyleSheet("""
           QLabel QpushButton {
                           font-family: calibri;
            }
            QLabel#city_label {
                           font-size: 40px;
                           font-style: italic;
            }
            QLineEdit#city_input {
                           font-size: 40px;
            }
            QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight: bold;
            }
            QLabel#temperature_label {
                           font-size: 75px;
            }  
            QLabel#emoji_label {
                           font-size: 100px;
                           font-family: "Segoe UI Emoji";
            }
            QLabel#description_label {
                           font-size: 50px;
            }                       
        """)

        self.get_wheather_button.clicked.connect(self.get_weather)


    def get_weather(self):
        
        api_key = "13d51306333ecf0345f667c113e892f3"
        city = self.city_input.text()
        url = f" https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
           match response.status_code:
               case 400:
                   self.display_error("Bad Request:\n please check your network")
               case 401:
                   self.display_error("unathorised:\n Invalid API Key")
               case 403:
                   self.display_error("forbidden:\n access denied")
               case 404:
                   self.display_error("Not Found:\n City Not Found")
               case 500:
                   self.display_error("internal server error:\n please try again later")
               case 502:
                   self.display_error("Bad Gateway:\n Invaild Response from the server")
               case 503:
                   self.display_error("Service Unavaible:\n Server is down")
               case 504:
                   self.display_error("GateWay time out:\n NO response from the server")
               case _:
                   self.display_error(f"http_error occur:\n {http_error}")
                
        except requests.exceptions.ConnectionError:
            self.display_error("connecton error: \n check your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout Error: \n the request time out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too may rects: \n check the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error: \n {req_error}")


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size : 30px;")
        self.temperature_label.setText(message)
        self.emoji_Label.clear()
        self.description_Label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size : 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]
        
        
    
        self.temperature_label.setText(f"{temperature_c : .2f}°C")
        self.emoji_Label.setText(self.get_weather_emoji(weather_id))
        self.description_Label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 632:
            return "⛄"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🔥"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "💭"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())


