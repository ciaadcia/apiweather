import sys
import requests
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QFont

data = pd.DataFrame([
    [30, 80, 5, 1008, "Hujan"],
    [32, 65, 8, 1015, "Cerah"],
    [28, 90, 4, 1005, "Hujan"],
    [35, 60, 10, 1018, "Cerah"],
    [27, 95, 3, 1004, "Hujan"],
    [33, 70, 7, 1013, "Cerah"]
], columns=["Suhu", "Kelembapan", "Angin", "Tekanan", "Cuaca"])

x = data[["Suhu", "Kelembapan", "Angin", "Tekanan"]]
y = data["Cuaca"]

model = DecisionTreeClassifier()
model.fit(x, y)

api_key = ""
