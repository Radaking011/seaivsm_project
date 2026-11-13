"""Generate clearly labelled synthetic CNC manufacturing event data."""

from __future__ import annotations

import numpy as np
import pandas as pd

ACTIVITIES = [
    ("Order Released", "ADMIN"),
    ("Material Issue", "STORE"),
    ("CNC Setup", "CNC"),
    ("CNC Machining", "CNC"),
    ("Deburring", "FINISH"),
    ("Quality Inspection", "QUALITY"),
    ("Packing", "PACK"),
    ("Dispatch", "LOGISTICS"),
]


def generate_synthetic_events(number_of_orders: int = 120,
                              seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    origin = pd.Timestamp("2026-01-05 08:00:00")

    for order_no in range(1, number_of_orders + 1):
        case_id = f"ORD-{order_no:05d}"
        product = rng.choice(
            ["Carbide Drill", "Threading Tap", "End Mill"],
            p=[0.40, 0.30, 0.30],
        )
        # Orders enter the system over several working weeks.
        order_start = origin + pd.Timedelta(
            days=int(rng.integers(0, 25)),
            hours=int(rng.integers(0, 9)),
            minutes=int(rng.integers(0, 60)),
        )
        cursor = order_start

        for event_no, (activity, department) in enumerate(ACTIVITIES, start=1):
            # Waiting time before the activity starts (minutes).
            wait = int(rng.gamma(shape=2.0, scale=18.0))
            if activity == "CNC Machining":
                wait += int(rng.choice([0, 30, 90, 180], p=[0.65, 0.20, 0.10, 0.05]))
            start = cursor + pd.Timedelta(minutes=wait)

            typical = {
                "Order Released": 8,
                "Material Issue": 18,
                "CNC Setup": 35,
                "CNC Machining": 95,
                "Deburring": 22,
                "Quality Inspection": 25,
                "Packing": 16,
                "Dispatch": 12,
            }[activity]
            duration = max(3, int(rng.normal(typical, typical * 0.18)))

            # Small fraction of orders require a quality rework loop.
            is_rework = (
                activity == "CNC Machining"
                and rng.random() < 0.08
            )
            if is_rework:
                duration += int(rng.integers(20, 55))

            end = start + pd.Timedelta(minutes=duration)
            machine_id = (
                f"CNC-{int(rng.integers(1, 5)):02d}"
                if department == "CNC"
                else department
            )
            operator_id = f"OP-{int(rng.integers(1, 13)):02d}"

            rows.append({
                "case_id": case_id,
                "event_id": event_no,
                "activity": activity,
                "product_family": product,
                "machine_id": machine_id,
                "operator_id": operator_id,
                "start_time": start,
                "end_time": end,
                "duration_minutes": duration,
                "event_status": "completed",
                "is_rework": bool(is_rework),
                "data_origin": "synthetic",
            })
            cursor = end

    df = pd.DataFrame(rows)
    return df.sort_values(["case_id", "event_id"]).reset_index(drop=True)
