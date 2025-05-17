from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QComboBox,
    QDateEdit, QSlider, QTableView, QGroupBox
)
from PyQt5.QtCore import Qt, QDate
import pandas as pd
from utils.data_loader import load_students, load_centers
from utils.distance_calc import road_distance
from core.allocator import allocate_centers  # placeholder import
from ui.pandas_model import PandasModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IBPS Center Allocation Algorithm")
        self.setGeometry(100, 100, 1200, 800)
        self._init_ui()

    def _init_ui(self):
        # Central widget and layout
        central = QWidget()
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)
        self.setCentralWidget(central)

        # File upload section
        file_group = QGroupBox("Data Upload")
        file_layout = QHBoxLayout()
        file_group.setLayout(file_layout)

        self.btn_upload_students = QPushButton("Upload Student Data")
        self.btn_upload_students.clicked.connect(self._on_upload_students)
        self.btn_upload_centers = QPushButton("Upload Center Data")
        self.btn_upload_centers.clicked.connect(self._on_upload_centers)

        file_layout.addWidget(self.btn_upload_students)
        file_layout.addWidget(self.btn_upload_centers)
        main_layout.addWidget(file_group)

        # Controls section (toggles, sliders, date pickers)
        controls_group = QGroupBox("Exam Configuration")
        controls_layout = QVBoxLayout()
        controls_group.setLayout(controls_layout)

        # Exam Type Toggle
        self.cmb_exam_type = QComboBox()
        self.cmb_exam_type.addItems(["Prelims", "Mains", "Interview"])
        controls_layout.addWidget(QLabel("Exam Type:"))
        controls_layout.addWidget(self.cmb_exam_type)

        # Date picker for exam days
        self.date_picker = QDateEdit()
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDate(QDate.currentDate())
        controls_layout.addWidget(QLabel("Select Exam Date:"))
        controls_layout.addWidget(self.date_picker)

        # Distance slider
        self.slider_max_dist = QSlider(Qt.Horizontal)
        self.slider_max_dist.setMinimum(0)
        self.slider_max_dist.setMaximum(1000)
        self.slider_max_dist.setValue(300)
        controls_layout.addWidget(QLabel("Max Travel Distance (km):"))
        controls_layout.addWidget(self.slider_max_dist)

        main_layout.addWidget(controls_group)

        # Preview panel
        preview_group = QGroupBox("Allocation Preview")
        preview_layout = QVBoxLayout()
        preview_group.setLayout(preview_layout)

        self.table_preview = QTableView()
        preview_layout.addWidget(self.table_preview)

        main_layout.addWidget(preview_group)

        # Generate button
        self.btn_generate = QPushButton("Generate Allocation")
        self.btn_generate.clicked.connect(self._on_generate_allocation)
        main_layout.addWidget(self.btn_generate)

    def _on_upload_students(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Student Data", "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        if path:
            self.students_df = load_students(path)
            self._update_preview()
            print(f"Loaded {len(self.students_df)} students from {path}")

    def _on_upload_centers(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Center Data", "",
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)"
        )
        if path:
            self.centers_df = load_centers(path)
            self._update_preview()
            print(f"Loaded {len(self.centers_df)} centers from {path}")

    def _update_preview(self):
        if hasattr(self, 'students_df') and hasattr(self, 'centers_df'):
            combined = pd.concat([
                self.students_df.assign(Source='Students'),
                self.centers_df.assign(Source='Centers')
            ], ignore_index=True)
            model = PandasModel(combined)
            self.table_preview.setModel(model)

    def _on_generate_allocation(self):
        params = {
            'exam_type': self.cmb_exam_type.currentText(),
            'date': self.date_picker.date().toPyDate(),
            'max_distance': self.slider_max_dist.value(),
        }
        allocations = allocate_centers(
            self.students_df, self.centers_df, params
        )
        model = PandasModel(allocations)
        self.table_preview.setModel(model)
        print("Allocation generated.")
