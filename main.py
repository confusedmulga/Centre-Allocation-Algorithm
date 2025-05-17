import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    # Create application
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Execute application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
