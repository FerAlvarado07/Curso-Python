from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import polars as pl

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# NumPy


def calculate_statistics(values: list[float]) -> dict[str, float]:
    """
    Calcula estadísticas básicas utilizando NumPy.
    """
    data = np.array(values)

    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "minimum": float(np.min(data)),
        "maximum": float(np.max(data)),
        "standard_deviation": float(np.std(data)),
    }


def multiply_values(
    values: list[float],
    multiplier: float,
) -> np.ndarray:
    """
    Multiplica todos los valores utilizando la vectorización de NumPy.
    """
    data = np.array(values)

    return data * multiplier


# Pandas


def create_pandas_dataframe() -> pd.DataFrame:
    """
    Crea un DataFrame utilizando Pandas.
    """
    data = {
        "hours_studied": [2, 3, 4, 5, 6, 7, 8, 9],
        "exam_score": [50, 55, 60, 65, 70, 75, 80, 85],
    }

    return pd.DataFrame(data)


def filter_pandas_data(
    dataframe: pd.DataFrame,
    minimum_score: float,
) -> pd.DataFrame:
    """
    Filtra las filas del DataFrame utilizando Pandas.
    """
    return dataframe[dataframe["exam_score"] >= minimum_score]


# Polars


def create_polars_dataframe() -> pl.DataFrame:
    """
    Crea un DataFrame utilizando Polars.
    """
    return pl.DataFrame(
        {
            "hours_studied": [2, 3, 4, 5, 6, 7, 8, 9],
            "exam_score": [50, 55, 60, 65, 70, 75, 80, 85],
        }
    )


def filter_polars_data(
    dataframe: pl.DataFrame,
    minimum_score: float,
) -> pl.DataFrame:
    """
    Filtra las filas del DataFrame utilizando Polars.
    """
    return dataframe.filter(pl.col("exam_score") >= minimum_score)


# Machine Learning


def create_dataset() -> tuple[np.ndarray, np.ndarray]:
    """
    Crea el conjunto de datos utilizado para entrenar el modelo.
    """
    hours_studied = np.array(
        [
            [2],
            [3],
            [4],
            [5],
            [6],
            [7],
            [8],
            [9],
        ]
    )

    exam_scores = np.array(
        [
            50,
            55,
            60,
            65,
            70,
            75,
            80,
            85,
        ]
    )

    return hours_studied, exam_scores


def split_dataset(
    features: np.ndarray,
    target: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """
    Divide el conjunto de datos en datos de entrenamiento y prueba.
    """
    return train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=42,
    )


def train_model(
    features: np.ndarray,
    target: np.ndarray,
) -> LinearRegression:
    """
    Entrena un modelo de regresión lineal.
    """
    model = LinearRegression()

    model.fit(features, target)

    return model


def evaluate_model(
    model: LinearRegression,
    features: np.ndarray,
    target: np.ndarray,
) -> dict[str, float]:
    """
    Evalúa el modelo utilizando MSE y R².
    """
    predictions = model.predict(features)

    mse = mean_squared_error(
        target,
        predictions,
    )

    r2 = r2_score(
        target,
        predictions,
    )

    return {
        "mean_squared_error": float(mse),
        "r2_score": float(r2),
    }


# Serialización del modelo


def save_model(
    model: LinearRegression,
    file_path: str | Path,
) -> None:
    """
    Serializa y guarda el modelo entrenado.
    """
    joblib.dump(model, file_path)


def load_model(
    file_path: str | Path,
) -> LinearRegression:
    """
    Carga un modelo previamente serializado.
    """
    return joblib.load(file_path)


# Inferencia


def predict_exam_score(
    model: LinearRegression,
    hours_studied: float,
) -> float:
    """
    Predice la calificación de un examen utilizando el modelo entrenado.
    """
    data = np.array([[hours_studied]])

    prediction = model.predict(data)

    return float(prediction[0])


# Función principal


def main() -> None:
    print("=== NumPy ===")

    values = [10, 20, 30, 40, 50]

    statistics = calculate_statistics(values)

    print(f"Mean: {statistics['mean']}")
    print(f"Median: {statistics['median']}")
    print(f"Minimum: {statistics['minimum']}")
    print(f"Maximum: {statistics['maximum']}")
    print(f"Standard deviation: {statistics['standard_deviation']:.2f}")

    multiplied_values = multiply_values(
        values,
        2,
    )

    print(f"Multiplied values: {multiplied_values}")

    print("\n=== Pandas ===")

    pandas_dataframe = create_pandas_dataframe()

    print(pandas_dataframe)

    filtered_pandas = filter_pandas_data(
        pandas_dataframe,
        70,
    )

    print("\nEstudiantes con calificación >= 70:")
    print(filtered_pandas)

    print("\n=== Polars ===")

    polars_dataframe = create_polars_dataframe()

    print(polars_dataframe)

    filtered_polars = filter_polars_data(
        polars_dataframe,
        70,
    )

    print("\nEstudiantes con calificación >= 70:")
    print(filtered_polars)

    print("\n=== Machine Learning ===")

    features, target = create_dataset()

    (
        features_train,
        features_test,
        target_train,
        target_test,
    ) = split_dataset(
        features,
        target,
    )

    model = train_model(
        features_train,
        target_train,
    )

    metrics = evaluate_model(
        model,
        features_test,
        target_test,
    )

    print(f"MSE: {metrics['mean_squared_error']:.2f}")

    print(f"R²: {metrics['r2_score']:.2f}")

    print("\n=== Serialización del modelo ===")

    model_path = Path("model.joblib")

    save_model(
        model,
        model_path,
    )

    print(f"Modelo guardado en: {model_path}")

    print("\n=== Carga del modelo ===")

    loaded_model = load_model(
        model_path,
    )

    print("Modelo cargado correctamente.")

    print("\n=== Inferencia ===")

    hours_studied = 10

    prediction = predict_exam_score(
        loaded_model,
        hours_studied,
    )

    print(
        f"Calificación predicha para {hours_studied} horas de estudio: {prediction:.2f}"
    )


if __name__ == "__main__":
    main()
