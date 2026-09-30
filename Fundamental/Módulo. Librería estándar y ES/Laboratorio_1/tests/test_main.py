import json
from pathlib import Path

from src.main import calculate_metrics, export_to_json, read_csv


def test_read_csv(tmp_path: Path):
    csv_file = tmp_path / "sales.csv"

    csv_file.write_text(
        "id,product,amount\n1,Laptop,15000\n2,Mouse,500\n",
        encoding="utf-8",
    )

    result = read_csv(csv_file)

    assert len(result) == 2
    assert result[0]["product"] == "Laptop"
    assert result[0]["amount"] == "15000"


def test_calculate_metrics():
    records = [
        {"id": "1", "product": "Laptop", "amount": "15000"},
        {"id": "2", "product": "Mouse", "amount": "500"},
        {"id": "3", "product": "Keyboard", "amount": "1200"},
    ]

    result = calculate_metrics(records)

    assert result["count"] == 3
    assert result["total"] == 16700
    assert result["average"] == 5566.666666666667
    assert result["maximum"] == 15000
    assert result["minimum"] == 500


def test_calculate_metrics_ignores_invalid_amount():
    records = [
        {"id": "1", "product": "Laptop", "amount": "15000"},
        {"id": "2", "product": "Mouse", "amount": "abc"},
        {"id": "3", "product": "Keyboard", "amount": "1200"},
    ]

    result = calculate_metrics(records)

    assert result["count"] == 2
    assert result["total"] == 16200
    assert result["maximum"] == 15000
    assert result["minimum"] == 1200


def test_export_to_json(tmp_path: Path):
    json_file = tmp_path / "metrics.json"

    data = {
        "count": 3,
        "total": 16700,
        "average": 5566.67,
        "maximum": 15000,
        "minimum": 500,
    }

    export_to_json(data, json_file)

    assert json_file.exists()

    result = json.loads(
        json_file.read_text(encoding="utf-8"),
    )

    assert result == data
