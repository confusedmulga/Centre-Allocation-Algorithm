# IBPS Centre Allocation Algorithm 🏫📋

A scalable and intelligent desktop application to automate large-scale exam center and slot allocation for IBPS-style exams (Prelims, Mains, Interviews), built for handling over 2 million candidates across thousands of centers with smart preference, gender, and logistics rules.

---

## 🔧 Purpose

This project was designed to solve a real-world logistical challenge: **allocating exam centers and time slots for lakhs of students**, while balancing gender ratios, travel constraints, and accessibility rules. It aims to serve organizations like IBPS, UPSC, or state-level recruitment boards conducting exams at scale.

---

## ✅ Key Features

### 📥 Input Handling
- Upload **Student Data** (`.csv`, `.xlsx`) with fields: name, address, registration number, gender, disability %, preferred city, etc.
- Upload **Center Data** (`.csv`, `.xlsx`) with fields: center name, location, capacity per slot, type (small/large).
- Set **Exam Dates**, **Slot Configurations**, and **Control Parameters**.

### ⚙️ Smart Allocation Logic
- **Priority Rules**: Disabled > Female > Male.
- **Gender Ratio Enforcement**: 50:50 until 4PM; post that, flexible.
- **Distance-based fallback**: If preferred city is full, fallback to nearest center within 300 km.
- **Consecutive Exam Distance Rule**: Ensures back-to-back exam candidates aren’t moved more than 400 km.
- **State vs National Level Toggle**: Assigns centers based on exam scope.
- **Overflow Handling**: Alerts user if centers/days are insufficient for the batch.

### 📊 Preview & Export
- Preview exam summary before generating.
- Final allocation is exported as an Excel file with:
  - Candidate name
  - Registration number
  - Allocated center & address
  - Slot timing
  - Roll number
  - System-generated password (optional)
  - Future-ready for Barcode/Admit card generation

---

## 🖥️ Technologies Used

| Area         | Stack/Library |
|--------------|---------------|
| Language     | Python 3.12   |
| GUI          | PyQt6         |
| Data Parsing | Pandas, openpyxl |
| Packaging    | PyInstaller   |
| Distance API | Modular support for MapMyIndia, OpenStreetMap (future) |
| File Formats | `.xlsx`, `.csv` |

---

## 🧠 Core Logic Modules

| Module        | Responsibility |
|---------------|----------------|
| `core/`       | Allocation logic & rules engine |
| `ui/`         | PyQt6 interface components |
| `utils/`      | Distance handling, file validation, slot generation |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/IBPS-Center-Allocator.git
cd IBPS-Center-Allocator
````

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

### 5. (Optional) Build Windows `.exe`

```bash
pyinstaller --noconfirm --onefile --windowed ^
  --name IBPSAllocator ^
  --add-data "ui;ui" ^
  --add-data "core;core" ^
  --add-data "utils;utils" ^
  main.py
```

Output will be in `dist/IBPSAllocator.exe`.

---

## 📁 Sample File Format

You’ll find example files in the `sample_data/` folder:

* `students_sample.xlsx`
* `centers_sample.xlsx`

---

