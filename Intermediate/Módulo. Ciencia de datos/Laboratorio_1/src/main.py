from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

MODEL_PATH = Path("model.joblib")


# Carga y limpieza de datos
def load_data(file_path: str | Path) -> pd.DataFrame:
    return pd.read_csv(file_path)


# Limpia el DataFrame eliminando filas con valores faltante y duplicados.
def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe.dropna()

    return dataframe


# Preparación de datos
# Separa las características (X) de la variable objetivo (y).


def prepare_data(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    features = dataframe[["age", "income", "purchase_count"]]

    target = dataframe["purchased"]

    return features, target


def split_data(
    features: pd.DataFrame,
    target: pd.Series,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.Series,
    pd.Series,
]:
    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    """
    return train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )


# Entrenamiento


def train_model(
    features: pd.DataFrame,
    target: pd.Series,
) -> RandomForestClassifier:
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(
        features,
        target,
    )

    return model


# Evaluación


def evaluate_model(
    model: RandomForestClassifier,
    features: pd.DataFrame,
    target: pd.Series,
) -> float:
    predictions = model.predict(features)

    accuracy = accuracy_score(
        target,
        predictions,
    )

    return float(accuracy)


# Serialización
# Guarda el modelo utilizando joblib.


def save_model(
    model: RandomForestClassifier,
    file_path: str | Path,
) -> None:
    joblib.dump(
        model,
        file_path,
    )


# Carga del modelo
def load_model(
    file_path: str | Path,
) -> RandomForestClassifier:
    return joblib.load(file_path)


# Inferencia


def predict(
    model: RandomForestClassifier,
    age: int,
    income: float,
    purchase_count: int,
) -> int:
    new_data = pd.DataFrame(
        {
            "age": [age],
            "income": [income],
            "purchase_count": [purchase_count],
        }
    )

    prediction = model.predict(new_data)

    return int(prediction[0])


def main() -> None:
    print("Carga de datos:")

    dataframe = load_data("data.csv")

    print(dataframe)

    print("\nLimpieza de datos:")

    cleaned_data = clean_data(dataframe)

    print(cleaned_data)

    print("\nPreparación de datos:")

    features, target = prepare_data(cleaned_data)

    print("Features:")
    print(features)

    print("\nTarget:")
    print(target)

    print("\nDivisión de datos:")

    (
        features_train,
        features_test,
        target_train,
        target_test,
    ) = split_data(
        features,
        target,
    )

    print(f"Datos de entrenamiento: {len(features_train)}")

    print(f"Datos de prueba: {len(features_test)}")

    print("\nEntrenamiento:")

    model = train_model(
        features_train,
        target_train,
    )

    print("Modelo entrenado correctamente.")

    print("\nEvaluación:")

    accuracy = evaluate_model(
        model,
        features_test,
        target_test,
    )

    print(f"Accuracy: {accuracy:.2%}")

    print("\nSerialización:")

    save_model(
        model,
        MODEL_PATH,
    )

    print(f"Modelo guardado en: {MODEL_PATH}")

    print("\nCarga del modelo:")

    loaded_model = load_model(
        MODEL_PATH,
    )

    print("Modelo cargado correctamente.")

    print("\nInferencia: ")

    prediction = predict(
        loaded_model,
        age=35,
        income=45000,
        purchase_count=8,
    )

    print(f"Predicción: {prediction}")

    if prediction == 1:
        print("El cliente probablemente realizará una compra.")
    else:
        print("El cliente probablemente no realizará una compra.")


if __name__ == "__main__":
    main()
