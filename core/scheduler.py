from datetime import datetime, timedelta

def build_schedule(dates, exam_type: str, centers_df):
    """
    Create a schedule dict mapping (date, slot_time) to a dict of center capacities.
    :param dates: list of datetime.date
    :param exam_type: 'Prelims', 'Mains', or 'Interview'
    :param centers_df: DataFrame with 'Center Name' and 'Capacity Per Slot'
    :return: dict { (date, slot_time): {center_name: capacity, ...}, ... }
    """
    # Define slot times based on exam type
    if exam_type.lower() == 'prelims':
        slot_times = ['09:00-11:00', '12:00-14:00', '15:00-17:00',
                      '18:00-20:00', '21:00-23:00', '00:00-02:00']
    else:
        # Mains and Interview have 2 slots
        slot_times = ['09:00-12:00', '14:00-17:00']

    schedule = {}
    for date in dates:
        for slot in slot_times:
            # Initialize capacities: {center_name: capacity_per_slot}
            caps = centers_df.set_index('Center Name')['Capacity Per Slot'].to_dict()
            schedule[(date, slot)] = caps.copy()
    return schedule
# Rule implementations for student prioritization and center eligibility

import pandas as pd
from utils.distance_calc import road_distance


def apply_priority_rules(students_df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Sort students by priority:
      1. Disability Status (%) > 50
      2. Gender == Female
      3. Others
    Returns a new DataFrame sorted accordingly.
    """
    df = students_df.copy()
    # Ensure Disability Status numeric
    df['Disability Status (%)'] = pd.to_numeric(df['Disability Status (%)'], errors='coerce').fillna(0)
    # Create priority buckets
    df['Priority'] = df['Disability Status (%)'].apply(lambda x: 1 if x > 50 else 2)
    df['Priority'] = df.apply(
        lambda r: 2 if (r['Priority'] != 1 and r['Gender'].strip().lower() == 'female') else r['Priority'],
        axis=1
    )
    # Others as priority 3
    df['Priority'] = df['Priority'].fillna(3).astype(int)
    # Sort by Priority, then optional secondary criteria (e.g., Reg. No.)
    df_sorted = df.sort_values(by=['Priority', 'Reg. No.'], ascending=[True, True])
    # Drop helper column
    df_sorted = df_sorted.drop(columns=['Priority'])
    return df_sorted


def apply_distance_rules(student: pd.Series,
                         centers_df: pd.DataFrame,
                         params: dict) -> pd.DataFrame:
    """
    Filter centers based on max travel distance and state/scope rules.
    Returns eligible centers DataFrame sorted by distance ascending.
    """
    max_dist = params.get('max_distance', 300)
    scope = params.get('scope', 'State').lower()
    # Compute distance to each center
    centers = centers_df.copy()
    # Map distances
    centers['Distance_km'] = centers['Address'].apply(
        lambda addr: road_distance(student['Correspondence Address'], addr)
    )
    # Filter by distance
    eligible = centers[centers['Distance_km'] <= max_dist]
    # If state-level, filter by student's state
    if scope == 'state':
        eligible = eligible[eligible['City'].str.contains(student['State Applied For'], case=False, na=False)]
    # Sort by Distance
    eligible_sorted = eligible.sort_values(by='Distance_km')
    return eligible_sorted
