
import os
import sys
from pathlib import Path

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

HERE = Path(__file__).parent
GITHUB_URL = "https://github.com/YOUR-USER/YOUR-REPO"  # TODO: put your repo URL here


class IceCreamWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # TODO (student): define the two lists that will hold the file data

        self.setWindowTitle("Ice Cream Revenue")
        self.resize(900, 680)
        self._build_ui()
        self.plot_data()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        central = QWidget()
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        title = QLabel("Ice Cream Revenue vs. Temperature")
        title.setObjectName("titleLabel")
        root.addWidget(title)

        top = QHBoxLayout()
        self.load_button = QPushButton("Load Data File")
        self.load_button.setObjectName("primaryButton")
        self.load_button.clicked.connect(self.on_load_clicked)
        self.file_label = QLabel("No file selected")
        self.file_label.setObjectName("fileLabel")
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.on_about_clicked)
        top.addWidget(self.load_button)
        top.addWidget(self.file_label, 1)
        top.addWidget(self.about_button)
        root.addLayout(top)

        # matplotlib canvas + toolbar (zoom, pan, save figure)
        plot_card = QWidget()
        plot_card.setObjectName("plotCard")
        card_layout = QVBoxLayout(plot_card)
        self.figure = Figure(figsize=(8, 5), tight_layout=True)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        card_layout.addWidget(self.toolbar)
        card_layout.addWidget(self.canvas, 1)
        root.addWidget(plot_card, 1)

        self.setCentralWidget(central)

    # ------------------------------------------------------------ plotting
    def plot_data(self):
        """Draws on the graph. Currently a TEMPORARY placeholder plot.

        TODO (student): replace the placeholder with the real graph:
          - scatter with point size 1
          - revenue on Y, outside temperature on X
          - hide the top and right spines
          - correct title and axis labels
          - then call self.draw_trend_line(x, y) with your two lists
        """
        self.ax.clear()

        # --- temporary placeholder (delete me) ---
        x = np.linspace(0, 10, 50)
        self.ax.plot(x, np.sin(x))
        self.ax.set_title("Temporary plot - load a file")
        # -----------------------------------------

        self.canvas.draw()

    def draw_trend_line(self, x, y):
        """Fit a straight trend line with np.polyfit, draw it and show its equation.

        np.polyfit(x, y, deg) finds the polynomial of degree `deg` that minimises
        the sum of squared vertical distances to the points (least squares).
        With deg=1 it returns [slope, intercept] for y = m*x + b.
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        m, b = np.polyfit(x, y, 1)

        line_x = np.array([x.min(), x.max()])
        line_y = m * line_x + b
        self.ax.plot(line_x, line_y, color="#e11d48", linewidth=2, label="Trend line")

        sign = "+" if b >= 0 else "-"
        equation = f"y = {m:.2f}x {sign} {abs(b):.2f}"
        self.ax.text(
            0.03, 0.95, equation, transform=self.ax.transAxes, va="top", fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="#e11d48"),
        )
        self.ax.legend(loc="lower right")

    # ------------------------------------------------------------ handlers
    def on_load_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select data file", str(HERE / "data"), "CSV files (*.csv);;All files (*)"
        )
        if not file_name:
            return
        self.file_label.setText(os.path.basename(file_name))

        # TODO (student):
        #   open file_name for reading and scan its data into the two lists
        #   defined in __init__, then call self.plot_data()

    def on_about_clicked(self):
        QMessageBox.about(
            self,
            "About",
            "<h3>Ice Cream Revenue</h3>"
            "<p>Advanced Coding - Files &amp; Graphs exercise.</p>"
            "<p>Author: Yuval Dekel</p>"
            f'<p>Source code: <a href="{GITHUB_URL}">{GITHUB_URL}</a></p>',
        )


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet((HERE / "icecream.qss").read_text(encoding="utf-8"))
    window = IceCreamWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
