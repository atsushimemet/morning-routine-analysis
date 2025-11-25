import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def create_daily_sales_data():
    date_list = pd.date_range(
        start="2025-01-01", periods=30
    )  # NOTE: 30日分の日付のリストを作成
    daily_sales_data = pd.DataFrame(
        {
            "date": date_list,
            "sales": np.random.randint(30000, 120000, size=30),
        }
    )
    return daily_sales_data


def add_weekday_column(daily_sales_data):
    daily_sales_data["weekday"] = daily_sales_data["date"].dt.weekday
    return daily_sales_data


def calc_avg_sales_per_weekday(daily_sales_data):
    avg_sales_per_weekday = daily_sales_data.groupby("weekday")["sales"].mean()
    return avg_sales_per_weekday


def visualize_avg_sales_per_weekday(avg_sales_per_weekday):
    plt.bar(avg_sales_per_weekday.index, avg_sales_per_weekday.values)
    plt.show()


if __name__ == "__main__":
    daily_sales_data = create_daily_sales_data()
    daily_sales_data = add_weekday_column(daily_sales_data)
    avg_sales_per_weekday = calc_avg_sales_per_weekday(daily_sales_data)
    print(avg_sales_per_weekday)
    visualize_avg_sales_per_weekday(avg_sales_per_weekday)
