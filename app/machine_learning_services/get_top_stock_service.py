import pandas as pd

def get_top_stock_service(prediction_dict: dict):
    top_ten = sorted(prediction_dict.items(), key=lambda item: item[1], reverse=True)
    worst_ten = sorted(prediction_dict.items(), key=lambda item: item[1], reverse=False)
    return top_ten[:10], worst_ten[:10]
