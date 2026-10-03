"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list containing the systolic value from every encounter."""
    return [encounter[2] for encounter in encounters]


def mean_systolic(readings):
    """Return the mean systolic reading, or None when the list is empty."""
    if not readings:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patient IDs in the encounters."""
    patient_ids = {encounter[0] for encounter in encounters}
    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return distinct patient IDs with a reading at or above the cutoff."""
    patient_ids = {
        encounter[0]
        for encounter in encounters
        if encounter[2] >= cutoff
    }

    return patient_ids
