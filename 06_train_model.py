import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error,mean_absolute_error,r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("laptops_cleaned.csv")

df_encoded = pd.get_dummies(df, columns=["brand"], drop_first=True)
feature_cols = [
    "ram_gb",
    "ssd_gb",
    "is_discrete_gpu",
] + [c for c in df_encoded.columns if c.startswith("brand")]

X = df_encoded[feature_cols]
y = df_encoded['price_byn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {"Линейная регрессия": LinearRegression(),
          "Случайный лес": RandomForestRegressor(n_estimators=100, random_state=42),
          "Градиентный бустинг": GradientBoostingRegressor(n_estimators=100,learning_rate=0.6,max_depth=3, random_state=42)
          }

print(f"Размер обучающей выборки: {len(X_train)}| Тестовой: {len(X_test)}\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    mae = mean_absolute_error(y_test, prediction)
    rmse = root_mean_squared_error(y_test, prediction)
    r2 = r2_score(y_test, prediction)

    print(f"--- {name} ---")
    print(f"MAE : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2 : {r2:.2f}")