from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def create_rfm_dataframe() -> pd.DataFrame:
    """
    Create an RFM dataframe from a given dataframe.
    """
    size = 30
    customer_id = [id_ for id_ in np.random.randint(1, 10, size=size)]
    date = [
        datetime.now() - timedelta(days=int(i))
        for i in np.random.randint(1, 365, size=size)
    ]
    amount = np.random.randint(1, 100, size=size)
    dataframe = pd.DataFrame(
        {"customer_id": customer_id, "date": date, "amount": amount}
    )

    return dataframe


def calc_recency(dataframe: pd.DataFrame) -> pd.Series:
    """
    Calculate the recency of the customer.
    """
    today = datetime.now()
    s_recency = today - dataframe.groupby("customer_id")["date"].max()
    return s_recency


def calc_frequency(dataframe: pd.DataFrame) -> pd.Series:
    """
    Calculate the frequency of the customer.
    """
    s_frequency = dataframe.groupby("customer_id").size()
    return s_frequency


def calc_monetary(dataframe: pd.DataFrame) -> pd.Series:
    """
    Calculate the monetary of the customer.
    """
    s_monetary = dataframe.groupby("customer_id")["amount"].sum()
    return s_monetary


def three_split_score(series: pd.Series) -> pd.Series:
    """
    Split the series into three equal parts.
    """
    return pd.qcut(series, 3, labels=[1, 2, 3])


def main():
    dataframe = create_rfm_dataframe()
    s_recency = calc_recency(dataframe)
    s_frequency = calc_frequency(dataframe)
    s_monetary = calc_monetary(dataframe)
    s_recency_score = np.array([int(score) for score in three_split_score(s_recency)])
    s_frequency_score = np.array(
        [int(score) for score in three_split_score(s_frequency)]
    )
    s_monetary_score = np.array([int(score) for score in three_split_score(s_monetary)])
    arr_score = s_recency_score + s_frequency_score + s_monetary_score
    df_scores = pd.DataFrame(
        {"customer_id": sorted(set(dataframe["customer_id"])), "score": arr_score}
    )
    print(df_scores)
    print(df_scores.sort_values(by="score", ascending=True).iloc[:5])


if __name__ == "__main__":
    main()
