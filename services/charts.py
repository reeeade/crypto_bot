import matplotlib.pyplot as plt
import pandas as pd
import aiofiles


def create_chart(prices, coin_name):
    dates = [pd.Timestamp.utcfromtimestamp(price[0] / 1000) for price in prices]
    values = [price[1] for price in prices]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, label=coin_name)
    plt.xlabel('Дата')
    plt.ylabel('Цена (USD)')
    plt.title(f'График цены {coin_name}')
    plt.legend()
    plt.grid(True)

    # Formatting x-axis to show daily labels
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator())
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d.%m'))

    plt.gcf().autofmt_xdate()  # Auto format the x-axis labels
    photo_path = f'charts/{coin_name}.png'
    plt.savefig(photo_path)
    plt.close()
    return photo_path
