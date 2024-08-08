import pandas as  pd

data_series = pd.Series([1,2,3,4,5], index=["a","b","c","d","e"])

df = data_series.to_frame(name = "values")

data_series = df.rename_axis("date")

