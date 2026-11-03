import numpy as np
import pandas as pd


def clean_data(data):

    data = data.copy()

    data = data.drop_duplicates()

    columns = ["Age", "Blood_Pressure", "Cholesterol"]

    for col in columns:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

        if data[col].notna().any():
            data[col] = data[col].fillna(
                data[col].median()
            )

    data = data.dropna(
        subset=["Age", "Blood_Pressure", "Cholesterol"]
    )

    data = data[
        (data["Age"] > 0) &
        (data["Age"] <= 120) &
        (data["Blood_Pressure"] > 0) &
        (data["Cholesterol"] > 0)
    ]

    return data


def calculate_statistics(data):

    age = np.array(data["Age"])
    bp = np.array(data["Blood_Pressure"])
    cholesterol = np.array(data["Cholesterol"])

    return {
        "Total Patients": len(data),
        "Average Age": np.mean(age),
        "Average BP": np.mean(bp),
        "Average Cholesterol": np.mean(cholesterol)
    }


def calculate_correlation(data):

    return data[
        ["Age", "Blood_Pressure", "Cholesterol"]
    ].corr()