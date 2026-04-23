from pathlib import Path


def test_initial_migration_contains_all_phase2_tables() -> None:
    sql_path = Path(__file__).resolve().parents[1] / "migrations" / "001_initial_schema.sql"
    sql = sql_path.read_text(encoding="utf-8")

    for table in [
        "CREATE TABLE users",
        "CREATE TABLE devices",
        "CREATE TABLE ride_sessions",
        "CREATE TABLE participants",
        "CREATE TABLE messages",
        "CREATE TABLE audio_events",
        "CREATE TABLE rtc_sessions",
    ]:
        assert table in sql
