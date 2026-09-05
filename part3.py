
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Weather AI")
        self.setFixedSize(600, 700)

        self.background = WeatherBackground()
        self.background.setParent(self)
        self.background.resize(self.size())

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(45, 35, 45, 35)
        main_layout.setSpacing(15)

        title = QLabel("WEATHER AI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: 2px;
        """)

        subtitle = QLabel("Machine Learning Weather Prediction")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: rgba(255,255,255,220);
            font-size: 14px;
        """)

        input_card = QFrame()
        input_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,235);
                border-radius: 18px;
            }
        """)

        input_layout = QHBoxLayout(input_card)
        input_layout.setContentsMargins(15, 12, 15, 12)

        self.kota_input = QLineEdit()
        self.kota_input.setPlaceholderText("Search city...")
        self.kota_input.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                color: #1E293B;
                font-size: 16px;
                padding: 8px;
            }
        """)

        button = QPushButton("CHECK WEATHER")
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background: #4F46E5;
                color: white;
                border: none;
                border-radius: 12px;
                padding: 12px 20px;
                font-size: 13px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #6366F1;
            }

            QPushButton:pressed {
                background: #4338CA;
            }
        """)

        button.clicked.connect(self.cek_cuaca)
        self.kota_input.returnPressed.connect(self.cek_cuaca)

        input_layout.addWidget(self.kota_input)
        input_layout.addWidget(button)

        self.weather_title = QLabel("Enter a city to check the weather")
        self.weather_title.setAlignment(Qt.AlignCenter)
        self.weather_title.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: bold;
        """)

        self.weather_description = QLabel("Real-time weather data powered by OpenWeatherMap")
        self.weather_description.setAlignment(Qt.AlignCenter)
        self.weather_description.setStyleSheet("""
            color: rgba(255,255,255,210);
            font-size: 13px;
        """)

        self.temperature = QLabel("--°")
        self.temperature.setAlignment(Qt.AlignCenter)
        self.temperature.setStyleSheet("""
            color: white;
            font-size: 64px;
            font-weight: 300;
        """)

        self.prediction = QLabel("ML PREDICTION")
        self.prediction.setAlignment(Qt.AlignCenter)
        self.prediction.setStyleSheet("""
            background: rgba(255,255,255,235);
            color: #312E81;
            border-radius: 14px;
            padding: 14px;
            font-size: 18px;
            font-weight: bold;
        """)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        self.humidity_card = self.create_card("HUMIDITY", "-- %")
        self.wind_card = self.create_card("WIND", "-- m/s")
        self.pressure_card = self.create_card("PRESSURE", "-- hPa")

        stats_layout.addWidget(self.humidity_card)
        stats_layout.addWidget(self.wind_card)
        stats_layout.addWidget(self.pressure_card)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(15)
        main_layout.addWidget(input_card)
        main_layout.addSpacing(25)
        main_layout.addWidget(self.weather_title)
        main_layout.addWidget(self.weather_description)
        main_layout.addWidget(self.temperature)
        main_layout.addWidget(self.prediction)
        main_layout.addSpacing(10)
        main_layout.addLayout(stats_layout)
        main_layout.addStretch()

    def create_card(self, title, value):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,225);
                border-radius: 16px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 15, 10, 15)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #64748B;
            font-size: 10px;
            font-weight: bold;
            letter-spacing: 1px;
        """)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            color: #1E293B;
            font-size: 17px;
            font-weight: bold;
        """)

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.value_label = value_label

        return card

    def cek_cuaca(self):
        kota = self.kota_input.text().strip()

        if kota == "":
            self.weather_title.setText("Please enter a city")
            self.weather_description.setText("Type a city name in the search box")
            return

        self.weather_title.setText("Loading...")
        self.weather_description.setText("Getting real-time weather data")

        QApplication.processEvents()

        url = f"https://api.openweathermap.org/data/2.5/weather?q={kota}&appid={api_key}&units=metric"

        try:
            response = requests.get(url, timeout=10)
            data_api = response.json()

            if data_api.get("cod") != 200:
                self.weather_title.setText("City not found")
                self.weather_description.setText("Try another city name")
                self.temperature.setText("--°")
                self.prediction.setText("ML PREDICTION")
                self.background.set_weather("default")
                return

            suhu = data_api["main"]["temp"]
            kelembapan = data_api["main"]["humidity"]
            angin = data_api["wind"]["speed"]
            tekanan = data_api["main"]["pressure"]

            hasil = model.predict([[suhu, kelembapan, angin, tekanan]])[0]

            self.weather_title.setText(kota.title())
            self.weather_description.setText(data_api["weather"][0]["description"].title())
            self.temperature.setText(f"{suhu:.1f}°")

            self.humidity_card.value_label.setText(f"{kelembapan}%")
            self.wind_card.value_label.setText(f"{angin:.1f} m/s")
            self.pressure_card.value_label.setText(f"{tekanan} hPa")

            if hasil == "Cerah":
                self.prediction.setText("ML PREDICTION   •   CERAH")
                self.background.set_weather("Cerah")
                self.weather_description.setText("Clear weather predicted")
            else:
                self.prediction.setText("ML PREDICTION   •   HUJAN")
                self.background.set_weather("Hujan")
                self.weather_description.setText("Rainy weather predicted")

        except requests.exceptions.Timeout:
            self.weather_title.setText("Connection timeout")
            self.weather_description.setText("Please check your internet connection")

        except Exception as e:
            self.weather_title.setText("Something went wrong")
            self.weather_description.setText(str(e))

app = QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())
