from datetime import datetime, timedelta
import pandas as pd
import xgboost as xgb
from statsmodels.tools.eval_measures import mse, rmse
from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np
from sklearn.model_selection import cross_val_predict

from app.services.dataframe_service import get_technical_data_as_dataframe, get_data_as_dataframe

today = datetime.today().strftime("%Y-%m-%d")

top_50_stock = ["AEFES", "AKBNK", "AKSA", "AKSEN", "ALARK", "ARCLK", "ASELS", "BERA", "BIMAS", "DOHOL",
                "EGEEN", "EKGYO", "ENJSA", "ENKAI", "EREGL", "FROTO", "GARAN", "GESAN", "GUBRF",
                "HALKB", "HEKTS", "ISCTR", "ISGYO", "KCHOL", "KONTR", "KORDS", "KOZAA", "KOZAA",
                "KOZAL", "KRDMD", "MGROS", "ODAS", "OYAKC", "PETKM", "PGSUS", "SAHOL", "SASA",
                "SISE", "SMRTG", "SOKM", "TAVHL", "TCELL", "THYAO", "TKFEN", "TOASO", "TSKB",
                "TTKOM", "TUPRS", "VAKBN", "VESTL", "YKBNK"]

top_1_stock = ["THYAO"]

for stock_symbol in top_1_stock:
    data_technical_info = get_technical_data_as_dataframe(schema_name="technical", table_name=stock_symbol)
    data_basic_info = get_data_as_dataframe(schema_name="public", table_name=stock_symbol)
print(data_technical_info)
print(data_technical_info.info())

data_df = data_technical_info.merge(data_basic_info, on="date", how="left")
data_df = data_df.dropna()

print(data_df)
print(data_df.info())

selected_columns = ["date", "RSI_14", "STOCHk_9_6_3", "STOCHd_9_6_3", "stoch_diff", "STOCHRSIk_14_14_3_3", "MACD_12_26_9", "MACDh_12_26_9",
                    "MACDs_12_26_9", "ADX_14", "DMP_14", "DMN_14", "WILLR_14", "CCI_14_0.015", "ATRr_14", "hl_ratio_14",
                    "UO_7_14_28", "ROC_14", "Bull_power_13", "Bear_power_13", "SMA_interpretation_5", "SMA_interpretation_10",
                    "SMA_interpretation_20", "SMA_interpretation_50",
                    "EMA_interpretation_5", "EMA_interpretation_10", "EMA_interpretation_20", "EMA_interpretation_50",
                    "classic_pivot_interpretation", "fibonacci_pivot_interpretation",
                    "camarilla_pivot_interpretation", "woodie_pivot_interpretation", "demark_pivot_interpretation", "percentage"]

data = data_df[selected_columns]

print(data)
data["percentage"] = data["percentage"].shift(-1)
data = data.dropna()
print(data)

interpretation_columns = [col for col in data.columns if 'interpretation' in col]
for column in interpretation_columns:
    dummies = pd.get_dummies(data[column], prefix=column)
    data = pd.concat([data, dummies], axis=1)
    data.drop(column, axis=1, inplace=True)

print(data)
print(data.info())

y = data["percentage"]
X = data.drop(["date", "percentage"], axis=1)

"""xgb_clf = xgb.XGBRegressor()
xgb_clf.fit(X, y)
predictions = xgb_clf.predict(X)
preds = cross_val_predict(xgb_clf, X, y, cv=2)"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def model_evaluation(models, X, y):
    for i, v in models:
        #prediction = cross_val_predict(v, X, y, cv=2)
        prediction = v.predict(X)
        r2 = r2_score(y, prediction)
        n = X.shape[0]  # örnek sayısı
        p = X.shape[1]  # özellik sayısı
        adjusted_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

        print(f"----------------------------- {i} Model Evaluation -----------------------------")
        print("R-Kare değeri                     : {}".format(r2))
        print("Adj. R-Kare değeri                : {}".format(adjusted_r2))
        print("Ortalama Mutlak Hata (MAE)        : {}".format(mean_absolute_error(y, prediction)))
        print("Ortalama Kare Hata (MSE)          : {}".format(mse(y, prediction)))
        print("Kök Ortalama Kare Hata (RMSE)     : {}".format(rmse(y, prediction)))

xgb_clf = xgb.XGBRegressor()
xgb_clf.fit(X_train, y_train)
models = []
models.append(('XGBOOST', xgb_clf))
print(X_test)
model_evaluation(models, X_test, y_test)


#xgb_clf.fit(X, y)

predictions = xgb_clf.predict(X)
data["predictions"] = predictions
print(data)

def strategy(data):
    BUDGET = 10000
    # İşaret değişimlerini ve ilgili tarihleri saklamak için boş bir liste oluşturma
    sign_changes = []
    data = data.reset_index()
    # İlk satırdan başlayarak her satırı kontrol etme
    for i in range(1, len(data)):
        current_pred = data.loc[i, 'predictions']
        previous_pred = data.loc[i - 1, 'predictions']
        
        # İşaret değişimi kontrolü
        if (current_pred > 0 and previous_pred < 0) or (current_pred < 0 and previous_pred > 0):
            date = data.loc[i, 'date']
            change_type = 'Negatiften Pozitife' if current_pred > 0 else 'Pozitiften Negatife'
            real_date = date + timedelta(days=1)
            sign_changes.append((date, change_type, real_date))

    # İşaret değişimlerini ve ilgili tarihleri yazdırma
    for change in sign_changes:
        print(f"Tarih: {change[0]}, İşaret Değişimi: {change[1]}, Alınması gereken tarih(Sabah): {change[2]}")

strategy(data)

"""data["predictions"] = predictions
data["preds"] = preds
print(data[["percentage", "predictions", "preds"]])"""