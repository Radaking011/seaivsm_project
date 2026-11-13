from src.config import NUMBER_OF_ORDERS, OUTPUT_DIR, RAW_DATA_DIR, RANDOM_SEED
from src.synthetic_data import generate_synthetic_events
from src.validation import validate_event_log
from src.metrics import calculate_order_metrics, calculate_activity_summary


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    events = generate_synthetic_events(
        number_of_orders=NUMBER_OF_ORDERS,
        seed=RANDOM_SEED,
    )

    errors = validate_event_log(events)
    if errors:
        print("DATA VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    raw_path = RAW_DATA_DIR / "synthetic_cnc_events.csv"
    events.to_csv(raw_path, index=False)

    order_metrics = calculate_order_metrics(events)
    activity_summary = calculate_activity_summary(events)

    order_metrics.to_csv(OUTPUT_DIR / "order_metrics.csv", index=False)
    activity_summary.to_csv(OUTPUT_DIR / "activity_summary.csv", index=False)

    print("SE-AI-VSM starter pipeline completed successfully.")
    print(f"Orders: {events['case_id'].nunique()}")
    print(f"Events: {len(events)}")
    print(f"Raw event log: {raw_path}")
    print(f"Reports: {OUTPUT_DIR}")
    print("\\nActivity summary:")
    print(activity_summary.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
