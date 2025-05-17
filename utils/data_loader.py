import pandas as pd

REQUIRED_STUDENT_COLS = {
    'Name', 'Permanent Address', 'Correspondence Address',
    'Reg. No.', 'Preferred City', 'State Applied For',
    'Gender', 'Disability Status (%)'
}

REQUIRED_CENTER_COLS = {
    'Center Name', 'Address', 'City',
    'Capacity Per Slot', 'Center Type'
}

def load_students(path: str) -> pd.DataFrame:
    """
    Load student data from CSV or Excel, validate required columns, return DataFrame.
    """
    ext = path.split('.')[-1].lower()
    if ext == 'csv':
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    missing = REQUIRED_STUDENT_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing student columns: {missing}")
    df = df.rename(columns=lambda c: c.strip())
    df = df.dropna(subset=['Reg. No.', 'Preferred City'])
    return df

def load_centers(path: str) -> pd.DataFrame:
    """
    Load center data from CSV or Excel, validate columns, return DataFrame.
    """
    ext = path.split('.')[-1].lower()
    if ext == 'csv':
        df = pd.read_csv(path)
    else:
        df = pd.read_excel(path)
    missing = REQUIRED_CENTER_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing center columns: {missing}")
    df = df.rename(columns=lambda c: c.strip())
    df['Capacity Per Slot'] = pd.to_numeric(
        df['Capacity Per Slot'], errors='coerce'
    )
    df = df.dropna(subset=['Center Name', 'Capacity Per Slot'])
    return df
