import pandas as pd
from utils.distance_calc import road_distance
from core.rules import apply_priority_rules, apply_distance_rules
from core.scheduler import build_schedule


def allocate_centers(students_df: pd.DataFrame,
                     centers_df: pd.DataFrame,
                     params: dict) -> pd.DataFrame:
    """
    Allocate students to centers and slots based on given parameters.

    :param students_df: DataFrame of students
    :param centers_df: DataFrame of centers
    :param params: dict containing 'exam_type', 'dates', 'max_distance', 'scope'
    :return: allocations DataFrame with columns:
             ['Reg. No.', 'Name', 'Center Name', 'Address', 'Slot Time', 'Date']
    """
    # 1. Build schedule structure: nested dict {(date, slot): {center_name: remaining_capacity}}
    dates = params.get('dates', [params.get('date')])
    schedule = build_schedule(dates, params['exam_type'], centers_df)

    # 2. Sort students by priority rules
    students_sorted = apply_priority_rules(students_df, params)

    # 3. Initialize allocation records
    allocations = []

    # 4. Iterate over students and assign
    for _, student in students_sorted.iterrows():
        eligible_centers = apply_distance_rules(student, centers_df, params)
        assigned = False
        for date in dates:
            for slot, center_caps in schedule.items():
                # slot key is tuple (date, slot_time); extract slot_time
                d, slot_time = slot
                if d != date:
                    continue
                # Try each center in eligible order
                for _, center in eligible_centers.iterrows():
                    cname = center['Center Name']
                    if center_caps.get(cname, 0) > 0:
                        # Assign here
                        allocations.append({
                            'Reg. No.': student['Reg. No.'],
                            'Name': student['Name'],
                            'Center Name': cname,
                            'Address': center['Address'],
                            'Date': date,
                            'Slot Time': slot_time
                        })
                        # Decrement capacity
                        schedule[(date, slot_time)][cname] -= 1
                        assigned = True
                        break
                if assigned:
                    break
            if assigned:
                break
        if not assigned:
            # Overflow: assign any center with capacity in same state
            for date in dates:
                for slot, center_caps in schedule.items():
                    d, slot_time = slot
                    if d != date:
                        continue
                    # find any center in student's state
                    state_centers = centers_df[centers_df['City'].str.contains(
                        student['State Applied For'], case=False, na=False)]
                    for _, center in state_centers.iterrows():
                        cname = center['Center Name']
                        if center_caps.get(cname, 0) > 0:
                            allocations.append({
                                'Reg. No.': student['Reg. No.'],
                                'Name': student['Name'],
                                'Center Name': cname,
                                'Address': center['Address'],
                                'Date': date,
                                'Slot Time': slot_time
                            })
                            schedule[(date, slot_time)][cname] -= 1
                            assigned = True
                            break
                    if assigned:
                        break
                if assigned:
                    break
        # If still unassigned, leave blank or log

    # 5. Return final allocations DataFrame
    alloc_df = pd.DataFrame(allocations)
    return alloc_df
