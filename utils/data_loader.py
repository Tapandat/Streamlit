
import pandas as pd
import urllib.request
import os

def load_nh():
    path = "data/NH.Ts+dSST.csv"

    if not os.path.exists(path):
        os.makedirs("data", exist_ok=True)
        urllib.request.urlretrieve(
            "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv",
            path
        )

    df = pd.read_csv(path, skiprows=1, na_values="***")
    df = df[["Year","Jan","Feb","Mar","Apr","May","Jun",
             "Jul","Aug","Sep","Oct","Nov","Dec","J-D"]]
    df.columns = ["Year","Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec","Annual"]
    df = df.dropna(subset=["Annual"])
    df["Year"]   = df["Year"].astype(int)
    df["Annual"] = df["Annual"].astype(float)
    return df
