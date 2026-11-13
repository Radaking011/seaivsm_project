from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

RANDOM_SEED = 42
NUMBER_OF_ORDERS = 120

REQUIRED_COLUMNS = [
    "case_id",
    "event_id",
    "activity",
    "product_family",
    "machine_id",
    "operator_id",
    "start_time",
    "end_time",
    "duration_minutes",
    "event_status",
    "is_rework",
]
