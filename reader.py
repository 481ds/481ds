import pandas as pd
import matplotlib.pyplot as plt
import csv

# doesn't work with quotes for some reason? Names with quotes break it
data_frame = pd.read_csv("out_simresults_999.txt", delimiter="␟", header=None, engine='python')

data_frame.columns = ["time", "name", "date", "points"]

data_frame["time"] = pd.to_numeric(data_frame["time"])
# name can be left as name!
data_frame["date"] = pd.to_datetime(data_frame["date"])
data_frame["points"] = pd.to_numeric(data_frame["points"])
# data_frame["manacost"] = pd.to_numeric(data_frame["manacost"])

# just drop all wins, this should probably be some max value but whatever
data_frame["points"] = data_frame[data_frame["points"] < 10000]["points"]
data_frame.dropna()

data_frame["points"] = data_frame[data_frame["points"] > -10000]["points"]
data_frame.dropna()

# 3132 is the amount of points for doing literally nothing.
data_frame["points"] = data_frame["points"] + 3132

data_frame["date"] = data_frame["date"].dt.year

data_frame = data_frame.groupby("date")["points"].mean().reset_index()

print(data_frame)

# Plot
plt.figure(figsize=(7, 5))
plt.plot(data_frame['date'], data_frame['points'], '-o', markersize=4)

plt.xlabel("Release year")
plt.ylabel("Average score")

plt.grid(True, color="grey", linestyle = "dashed", linewidth=.5)
plt.tight_layout()

plt.show()
