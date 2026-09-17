import joblib
import pandas as pd

model = joblib.load('laptop_price_model.pkl')

df = pd.read_csv("laptops_cleaned.csv")
df_encoded = pd.get_dummies(df, columns=['brand'], drop_first=True)

feature_cols = [
    'ram_gb',
    'ssd_gb',
    'is_discrete_gpu',
] + [c for c in df_encoded.columns if c.startswith('brand_')]

def predict_laptop_price(ram_gb, ssd_gb, is_discrete_gpu,brand_name):
    data = {col: 0 for col in feature_cols}
    data['ram_gb'] = ram_gb
    data['ssd_gb'] = ssd_gb
    data['is_discrete_gpu'] = is_discrete_gpu

    brand_col = f"brand_{brand_name}"
    if brand_col in data:
        data[brand_col] = 1

    input_df = pd.DataFrame([data])

    predicted_price = model.predict(input_df)[0]
    return predicted_price

price_1 = predict_laptop_price(ram_gb=16,ssd_gb=512,is_discrete_gpu=True,brand_name='Asus')

print(f"Оценочная стоимость ноутбука Asus(16/512):{price_1}")