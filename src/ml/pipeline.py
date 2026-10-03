from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer

NUMERIC_FEATURES = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
CATEGORICAL_FEATURES = [
    'mainroad', 'guestroom', 'basement', 'hotwaterheating', 
    'airconditioning', 'prefarea', 'furnishingstatus'
]

def build_preprocessore() -> ColumnTransformer:
    "Tạo bộ tiền xử lí chuẩn hóa đặc trưng số và mã hóa đặc trưng phân loại"
    return ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERIC_FEATURES),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), CATEGORICAL_FEATURES)
        ]
    )

def build_lr_pipeline():

    return Pipeline([
        ('preprocessor', build_preprocessore()),
        ('model', LinearRegression())
    ])

def build_rf_pipeline():

    return Pipeline([
        ('preprocessor', build_preprocessore()),
        ('model', RandomForestRegressor(random_state=42))
    ])
