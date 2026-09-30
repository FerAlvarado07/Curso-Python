import csv
import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def read_csv(file_path: Path) -> list[dict[str, str]]:
    """Lee un archivo CSV y devuelve sus registros."""
    logger.info("Leyendo archivo CSV: %s", file_path)

    if not file_path.exists():
        logger.error("El archivo no existe: %s", file_path)
        raise FileNotFoundError(file_path)

    with file_path.open(
        mode="r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        records = list(reader)

    logger.info("Se leyeron %d registros", len(records))
    logger.debug("Registros obtenidos: %s", records)

    return records


def calculate_metrics(records: list[dict[str, str]]) -> dict[str, float]:
    """Calcula métricas a partir de los registros."""
    logger.info("Calculando métricas")

    amounts = []

    for record in records:
        try:
            amount = float(record["amount"])
            amounts.append(amount)
        except (KeyError, ValueError):
            logger.warning(
                "Registro ignorado por tener un amount inválido: %s",
                record,
            )

    if not amounts:
        logger.error("No existen valores válidos para calcular métricas")
        return {
            "count": 0,
            "total": 0,
            "average": 0,
            "maximum": 0,
            "minimum": 0,
        }

    metrics = {
        "count": len(amounts),
        "total": sum(amounts),
        "average": sum(amounts) / len(amounts),
        "maximum": max(amounts),
        "minimum": min(amounts),
    }

    logger.debug("Métricas calculadas: %s", metrics)

    return metrics


def export_to_json(
    data: dict[str, float],
    file_path: Path,
) -> None:
    """Exporta los datos a un archivo JSON."""
    logger.info("Exportando métricas a JSON: %s", file_path)

    with file_path.open(
        mode="w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    logger.info("Exportación completada")


def main() -> None:
    csv_path = Path("data/sales.csv")
    json_path = Path("output/metrics.json")

    logger.info("Iniciando procesamiento")

    records = read_csv(csv_path)

    metrics = calculate_metrics(records)

    json_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    export_to_json(metrics, json_path)

    logger.info("Procesamiento finalizado")


if __name__ == "__main__":
    main()
