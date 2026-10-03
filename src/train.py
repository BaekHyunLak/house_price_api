import json
import logging
from datetime import datetime,timezone
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split

from src.ml.pipeline import (
    build_lr_pipeline, 
    build_rf_pipeline,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES)

from src.config import settings


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def calculate_metrics(y_true, y_pred) -> dict:
    return{
        "r2_score": float(r2_score(y_true, y_pred)),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred)))
    }

def train_and_evaluate():

    RAW_DATA_PATH = settings.raw_data_path
    MODEL_PATH = Path(settings.model_path)
    metadata_path = MODEL_PATH.parent / "model_metadata.json"

    df = pd.read_csv(RAW_DATA_PATH)
    X = df.drop(columns=['price'])
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Linear Regression train
    logger.info(" Training (Linear Regression)...")
    lr_pl = build_lr_pipeline()
    lr_pl.fit(X_train, y_train)
    y_pred_lr = lr_pl.predict(X_test)
    metrics_lr = calculate_metrics(y_test, y_pred_lr)
    logger.info(f"Linear Regression -> R2: {metrics_lr['r2_score']:.4f} | MAE: {metrics_lr['mae']:,.0f} | RMSE: {metrics_lr['rmse']:,.0f}")

    # Random Forest + Hyperparameter Tuning (GridSearch 5-Fold) train
    logger.info("Training Random Forest (Hyperparameter Tuning)...")
    rf_pl = build_rf_pipeline()

    # Định nghĩa không gian tìm kiếm
    param_grid = {
        "model__n_estimators": [50, 100, 150],
        "model__max_depth": [None, 10, 20],
        "model__min_samples_split": [2, 5],
    }

    grid_search = GridSearchCV(
        estimator=rf_pl,
        param_grid=param_grid,
        cv=5,
        scoring='r2',
        n_jobs=-1,
        verbose=1,
    )   
    grid_search.fit(X_train, y_train)

    best_rf_pl = grid_search.best_estimator_
    best_rf_params = grid_search.best_params_
    logger.info(f"Siêu tham số tốt nhất cho Random Forest: {best_rf_params}")

    y_pred_rf = best_rf_pl.predict(X_test)
    metrics_rf = calculate_metrics(y_test, y_pred_rf)
    logger.info(f"Random Forest (Tuned) -> R2: {metrics_rf['r2_score']:.4f} | MAE: {metrics_rf['mae']:,.0f} | RMSE: {metrics_rf['rmse']:,.0f}")

    # So sánh và lựa chọn model tối ưu
    if metrics_rf['r2_score'] > metrics_lr['r2_score']:
        selected_model = best_rf_pl
        selected_name = "RandomForestRegressor"
        selected_metrics = metrics_rf
        selected_params = best_rf_params
    else:
        selected_model = lr_pl
        selected_name = "LinearRegression"
        selected_metrics = metrics_lr
        selected_params = {}

    logger.info(f"Mô hình được chọn: {selected_name}")

    # Xuất model artifact và metadata

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(selected_model, MODEL_PATH)
    logger.info(f"Đã lưu mô hình thành công tại: {MODEL_PATH}")

    # Metadata ghi nhận thông tin phục vụ audit / reproducibility
    metadata = {
        "model_name": selected_name,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "features": {
            "numeric": NUMERIC_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
        },
        "best_hyperparameters": selected_params,
        "evaluation_metrics": selected_metrics,
        "comparison": {
            "linear_regression": metrics_lr,
            "random_forest_tuned": metrics_rf,
        },
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    logger.info(f"Đã lưu metadata mô hình tại: {metadata_path}")

if __name__ == "__main__":
    train_and_evaluate()
