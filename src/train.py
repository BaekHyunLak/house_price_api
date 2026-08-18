from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd

from src.ml.pipeline import build_lr_pipeline, build_rf_pipeline
import numpy as np
import joblib
from src.config import settings

RAW_DATA_PATH = settings.raw_data_path
MODEL_PATH = settings.model_path
df = pd.read_csv(RAW_DATA_PATH)
X = df.drop(columns=['price'])
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Linear Regression train
lr_pl = build_lr_pipeline()
lr_pl.fit(X_train, y_train)
y_pred_lr = lr_pl.predict(X_test)
r2_lr = r2_score(y_test, y_pred_lr) 
mae_lr = mean_absolute_error(y_test, y_pred_lr)

# Random Forest train
rf_pl = build_rf_pipeline()
rf_pl.fit(X_train, y_train)
y_pred_rf = rf_pl.predict(X_test)
r2_rf = r2_score(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)

# R2 Càng gần 1.0 (100%) (Mô hình giải thích được bao nhiêu phần trăm sự biến thiên của giá nhà).
print(f"Linear Regression -> R2: {r2_lr:.4f} | MAE: {mae_lr:,.0f}")

# mae Càng nhỏ càng tốt (Trung bình mỗi căn nhà mô hình đoán lệch bao nhiêu tiền so với giá thực tế).
print(f"Random Forest     -> R2: {r2_rf:.4f} | MAE: {mae_rf:,.0f}")

best_model = rf_pl if r2_rf > r2_lr else lr_pl
joblib.dump(best_model, MODEL_PATH)
print(f'Đã lưu model {best_model} thành công tại: {MODEL_PATH}')


