from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl
import pytest

from src.main import (
    calculate_statistics,
    create_dataset,
    create_pandas_dataframe,
    create_polars_dataframe,
    evaluate_model,
    filter_pandas_data,
    filter_polars_data,
    load_model,
    multiply_values,
    predict_exam_score,
    save_model,
    split_dataset,
    train_model,
)


def test_calculate_statistics() -> None:
    values = [10, 20, 30, 40, 50]

    result = calculate_statistics(values)

    assert result["mean"] == pytest.approx(30)
    assert result["median"] == pytest.approx(30)
    assert result["minimum"] == 10
    assert result["maximum"] == 50


def test_multiply_values() -> None:
    values = [1, 2, 3]

    result = multiply_values(
        values,
        2,
    )

    expected = np.array([2, 4, 6])

    np.testing.assert_array_equal(
        result,
        expected,
    )


def test_create_pandas_dataframe() -> None:
    result = create_pandas_dataframe()

    assert isinstance(result, pd.DataFrame)

    assert list(result.columns) == [
        "hours_studied",
        "exam_score",
    ]

    assert len(result) == 8


def test_filter_pandas_data() -> None:
    dataframe = create_pandas_dataframe()

    result = filter_pandas_data(
        dataframe,
        70,
    )

    assert len(result) == 4

    assert all(result["exam_score"] >= 70)


def test_create_polars_dataframe() -> None:
    result = create_polars_dataframe()

    assert isinstance(result, pl.DataFrame)

    assert result.columns == [
        "hours_studied",
        "exam_score",
    ]

    assert result.height == 8


def test_filter_polars_data() -> None:
    dataframe = create_polars_dataframe()

    result = filter_polars_data(
        dataframe,
        70,
    )

    assert result.height == 4

    assert result["exam_score"].min() >= 70


def test_create_dataset() -> None:
    features, target = create_dataset()

    assert features.shape == (8, 1)
    assert target.shape == (8,)


def test_split_dataset() -> None:
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

    assert len(features_train) == 6
    assert len(features_test) == 2

    assert len(target_train) == 6
    assert len(target_test) == 2


def test_train_model() -> None:
    features, target = create_dataset()

    model = train_model(
        features,
        target,
    )

    assert model is not None
    assert hasattr(model, "predict")


def test_evaluate_model() -> None:
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

    assert "mean_squared_error" in metrics
    assert "r2_score" in metrics

    assert metrics["mean_squared_error"] >= 0
    assert metrics["r2_score"] > 0


def test_save_and_load_model(
    tmp_path: Path,
) -> None:
    features, target = create_dataset()

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

    assert loaded_model is not None

    original_prediction = model.predict([[10]])

    loaded_prediction = loaded_model.predict([[10]])

    np.testing.assert_array_almost_equal(
        original_prediction,
        loaded_prediction,
    )


def test_predict_exam_score() -> None:
    features, target = create_dataset()

    model = train_model(
        features,
        target,
    )

    prediction = predict_exam_score(
        model,
        10,
    )

    assert prediction == pytest.approx(
        90,
        abs=1,
    )
