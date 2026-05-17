
import pandas as pd

def load_nh():
    df = pd.read_csv("data/NH.Ts+dSST.csv", skiprows=1, na_values="***")
    df = df[["Year","Jan","Feb","Mar","Apr","May","Jun",
             "Jul","Aug","Sep","Oct","Nov","Dec","J-D"]]
    df.columns = ["Year","Jan","Feb","Mar","Apr","May","Jun",
                  "Jul","Aug","Sep","Oct","Nov","Dec","Annual"]
    df = df.dropna(subset=["Annual"])
    df["Year"]   = df["Year"].astype(int)
    df["Annual"] = df["Annual"].astype(float)
    return df
