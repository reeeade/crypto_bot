import matplotlib.pyplot as plt
import pandas as pd
import os


def create_chart(data, coin_name):
    prices = []
    for coin in data:
        if coin['name'] == coin_name:
            prices = coin['sparkline_in_7d']['price']
            break

    if not prices:
        raise KeyError(f"'{coin_name}' does not contain 'sparkline_in_7d' key.")

    dates = pd.date_range(start=pd.Timestamp.now() - pd.Timedelta(days=len(prices)), periods=len(prices))

    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, label=coin_name)
    plt.xlabel('Дата')
    plt.ylabel('Цена (USD)')
    plt.title(f'График цены {coin_name}')
    plt.legend()
    plt.grid(True)

    # Сохраняем график и проверяем, что он действительно создается
    image_path = f'{coin_name}.png'
    plt.savefig(image_path)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Не удалось создать график: {image_path}")

    plt.close()
    return image_path
