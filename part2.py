    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())

        if self.weather == "Cerah":
            gradient.setColorAt(0, QColor("#87CEEB"))
            gradient.setColorAt(1, QColor("#FDE68A"))
        elif self.weather == "Hujan":
            gradient.setColorAt(0, QColor("#172554"))
            gradient.setColorAt(1, QColor("#475569"))
        else:
            gradient.setColorAt(0, QColor("#667EEA"))
            gradient.setColorAt(1, QColor("#764BA2"))
        painter.fillRect(self.rect(), gradient)
        if self.weather == "Cerah":
            painter.setBrush(QColor("#FACC15"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.width() - 130, 50, 75, 75)
            painter.setBrush(QColor(255, 255, 255, 180))
            painter.drawEllipse(40, 70, 100, 45)
            painter.drawEllipse(90, 55, 100, 60)
            painter.drawEllipse(145, 75, 90, 40)
        elif self.weather == "Hujan":
            painter.setPen(QColor(147, 197, 253, 150))
            for drop in self.raindrops:
                painter.drawLine(drop[0], drop[1], drop[0] - 4, drop[1] + 12)
            painter.setBrush(QColor(71, 85, 105, 230))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(100, 55, 100, 45)
            painter.drawEllipse(145, 40, 110, 60)
            painter.drawEllipse(195, 60, 90, 40)
