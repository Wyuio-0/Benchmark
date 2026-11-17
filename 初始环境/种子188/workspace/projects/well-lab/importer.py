def to_ug_l(value):
    return float(value) * 1000.0


def passes_lead_limit(value):
    return to_ug_l(value) <= 10.0
