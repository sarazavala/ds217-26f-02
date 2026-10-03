#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return usable encounter records and the number of skipped data rows."""
    lines = data_path.read_text(encoding="utf-8").splitlines()

    encounters = []
    skipped = 0

    for line in lines[1:]:
        if not line.strip():
            skipped += 1
            print("Skipping a blank row.")
            continue

        fields = line.split(",")

        if len(fields) != 3:
            skipped += 1
            print(f"Skipping row with {len(fields)} fields: {line}")
            continue

        patient_id, visit_date, systolic_text = fields

        try:
            systolic = int(systolic_text)
        except ValueError:
            skipped += 1
            print(f"Skipping row with a non-integer systolic value: {line}")
            continue

        if systolic < 60 or systolic > 250:
            skipped += 1
            print(f"Skipping row with an implausible systolic value: {line}")
            continue

        encounters.append((patient_id, visit_date, systolic))

    return encounters, skipped
    

def main():
    """Write the clinic vitals summary report."""
    encounters, skipped = read_encounters(DATA_PATH)

    OUTPUT_DIR.mkdir(exist_ok=True)

    readings = systolic_readings(encounters)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {count_patients(encounters)}",
        f"Mean systolic: {mean_systolic(readings):.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    report_path = OUTPUT_DIR / "vitals_report.txt"

    report_path.write_text(
        "\n".join(report_lines) + "\n",
        encoding="utf-8",
    )

    print(report_path.read_text(encoding="utf-8"))
    cutoff = 140

    reason = (
        "This cutoff prioritizes clearly elevated readings while keeping "
        "the follow-up list manageable."
    )

    followup_patients = sorted(
        patients_at_or_above(encounters, cutoff)
    )

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
        *followup_patients,
    ]

    followup_path = OUTPUT_DIR / "followup_list.txt"

    followup_path.write_text(
        "\n".join(followup_lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
