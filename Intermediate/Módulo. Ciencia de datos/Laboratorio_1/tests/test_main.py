from pathlib import Path

import pandas as pd

from src.main import (
    clean_data,
    evaluate_model,
    load_data,
    load_model,
    predict,
    prepare_data,
    save_model,
    split_data,
    train_model,
)


def test_load_data(tmp_path: Path) -> None:
    csv_file = tmp_path / "data.csv"

    csv_file.write_text(
        "age,income,purchase_count,purchased\n25,20000,2,0\n35,40000,6,1\n"
    )

    dataframe = load_data(csv_file)

    assert isinstance(dataframe, pd.DataFrame)

    assert len(dataframe) == 2

    assert list(dataframe.columns) == [
        "age",
        "income",
        "purchase_count",
        "purchased",
    ]


def test_clean_data() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [25, 30, 30, None],
            "income": [20000, 30000, 30000, 40000],
            "purchase_count": [2, 4, 4, 5],
            "purchased": [0, 1, 1, 1],
        }
    )

    result = clean_data(dataframe)

    assert len(result) == 2

    assert result.isnull().sum().sum() == 0

    assert result.duplicated().sum() == 0


def test_prepare_data() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [25, 35],
            "income": [20000, 40000],
            "purchase_count": [2, 6],
            "purchased": [0, 1],
        }
    )

    features, target = prepare_data(dataframe)

    assert list(features.columns) == [
        "age",
        "income",
        "purchase_count",
    ]

    assert target.name == "purchased"

    assert len(features) == 2
    assert len(target) == 2


def test_split_data() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
            "income": [
                15000,
                20000,
                25000,
                30000,
                35000,
                40000,
                45000,
                50000,
                55000,
                60000,
            ],
            "purchase_count": [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9,
                10,
            ],
            "purchased": [
                0,
                0,
                0,
                0,
                1,
                1,
                1,
                1,
                1,
                1,
            ],
        }
    )

    features, target = prepare_data(dataframe)

    (
        features_train,
        features_test,
        target_train,
        target_test,
    ) = split_data(
        features,
        target,
    )

    assert len(features_train) == 8
    assert len(features_test) == 2

    assert len(target_train) == 8
    assert len(target_test) == 2


def test_train_model() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [20, 25, 30, 35, 40, 45],
            "income": [
                15000,
                20000,
                25000,
                30000,
                35000,
                40000,
            ],
            "purchase_count": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "purchased": [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
        }
    )

    features, target = prepare_data(dataframe)

    model = train_model(
        features,
        target,
    )

    assert model is not None

    assert hasattr(
        model,
        "predict",
    )


def test_evaluate_model() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [20, 25, 30, 35, 40, 45],
            "income": [
                15000,
                20000,
                25000,
                30000,
                35000,
                40000,
            ],
            "purchase_count": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "purchased": [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
        }
    )

    features, target = prepare_data(dataframe)

    model = train_model(
        features,
        target,
    )

    accuracy = evaluate_model(
        model,
        features,
        target,
    )

    assert 0 <= accuracy <= 1


def test_save_and_load_model(
    tmp_path: Path,
) -> None:
    dataframe = pd.DataFrame(
        {
            "age": [20, 25, 30, 35, 40, 45],
            "income": [
                15000,
                20000,
                25000,
                30000,
                35000,
                40000,
            ],
            "purchase_count": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "purchased": [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
        }
    )

    features, target = prepare_data(dataframe)

    model = train_model(
        features,
        target,
    )

    model_path = tmp_path / "model.joblib"

    save_model(
        model,
        model_path,
    )

    assert model_path.exists()

    loaded_model = load_model(
        model_path,
    )

    original_prediction = model.predict([[35, 30000, 4]])

    loaded_prediction = loaded_model.predict([[35, 30000, 4]])

    assert original_prediction[0] == loaded_prediction[0]


def test_predict() -> None:
    dataframe = pd.DataFrame(
        {
            "age": [20, 25, 30, 35, 40, 45],
            "income": [
                15000,
                20000,
                25000,
                30000,
                35000,
                40000,
            ],
            "purchase_count": [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            "purchased": [
                0,
                0,
                0,
                1,
                1,
                1,
            ],
        }
    )

    features, target = prepare_data(dataframe)

    model = train_model(
        features,
        target,
    )

    prediction = predict(
        model,
        age=35,
        income=30000,
        purchase_count=4,
    )

    assert prediction in [0, 1]
