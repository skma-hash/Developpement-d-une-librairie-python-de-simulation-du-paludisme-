import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout, QGroupBox,
    QLabel, QSlider, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Malaria Simulation Dashboard")
        self.resize(1200, 600)

        # =========================
        # WIDGET CENTRAL
        # =========================
        central = QWidget()
        central.setStyleSheet("background-color: #F4F6F8;")
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)

        # =========================
        # COLONNE 1 : PARAMÈTRES
        # =========================
        params_box = QGroupBox("Simulation Parameters")
        params_layout = QVBoxLayout(params_box)

        # Population humaine
        params_layout.addWidget(QLabel("Human population (Nh)"))
        self.slider_humans = QSlider(Qt.Horizontal)
        self.slider_humans.setRange(100, 100000)
        self.slider_humans.setValue(1000)
        params_layout.addWidget(self.slider_humans)

        # Population moustiques
        params_layout.addWidget(QLabel("Mosquito population (Nm)"))
        self.slider_mosquitoes = QSlider(Qt.Horizontal)
        self.slider_mosquitoes.setRange(100, 200000)
        self.slider_mosquitoes.setValue(5000)
        params_layout.addWidget(self.slider_mosquitoes)

        # Taux de transmission
        params_layout.addWidget(QLabel("Transmission rate (β)"))
        self.slider_beta = QSlider(Qt.Horizontal)
        self.slider_beta.setRange(1, 100)
        self.slider_beta.setValue(30)
        params_layout.addWidget(self.slider_beta)

        # Période d'incubation
        params_layout.addWidget(QLabel("Incubation period (days)"))
        self.slider_incubation = QSlider(Qt.Horizontal)
        self.slider_incubation.setRange(1, 30)
        self.slider_incubation.setValue(10)
        params_layout.addWidget(self.slider_incubation)

        self.btn_start = QPushButton("Launch Simulation")
        params_layout.addWidget(self.btn_start)

        params_layout.addStretch()

        # =========================
        # COLONNE 2 : SORTIE (VIDE)
        # =========================
        output_box = QGroupBox("Simulation Output")
        output_layout = QVBoxLayout(output_box)

        placeholder = QLabel("Simulation results will appear here")
        placeholder.setAlignment(Qt.AlignCenter)
        output_layout.addWidget(placeholder)

        # =========================
        # COLONNE 3 : LOGS
        # =========================
        results_box = QGroupBox("Results / Logs")
        results_layout = QVBoxLayout(results_box)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.append("Interface ready.")

        results_layout.addWidget(self.log)

        # =========================
        # LAYOUT PRINCIPAL
        # =========================
        main_layout.addWidget(params_box, 1)
        main_layout.addWidget(output_box, 2)
        main_layout.addWidget(results_box, 1)

        # =========================
        # CONNEXION (SANS SIMULATION)
        # =========================
        self.btn_start.clicked.connect(self.collect_parameters)

    def collect_parameters(self):
        """
        Récupère les paramètres (sans lancer de simulation)
        """
        params = {
            "Nh": self.slider_humans.value(),
            "Nm": self.slider_mosquitoes.value(),
            "beta": self.slider_beta.value() / 100,
            "incubation": self.slider_incubation.value()
        }

        self.log.append("Parameters collected:")
        for k, v in params.items():
            self.log.append(f" - {k} = {v}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


