import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Messy 15-day weather log (16 rows incl. one duplicate)
dates = ["2026-04-01", "2026-04-02", "2026-04-03", "2026-04-04", "2026-04-05",
         "2026-04-06", "2026-04-07", "2026-04-08", "2026-04-09", "2026-04-10",
         "2026-04-11", "2026-04-12", "2026-04-13", "2026-04-14", "2026-04-15"]
city = ["islamabad", "Islamabad ", " ISLAMABAD", "Islamabad", "islamabad ",
        "Islamabad", " islamabad", "ISLAMABAD", "Islamabad ", "islamabad",
        "Islamabad", " Islamabad", "ISLAMABAD ", "islamabad", "Islamabad"]
temp = ["32C", "30C", "27C", "25C", "33C", "34C", "28C", "26C",
        "24C", "35C", "31C", "29C", "23C", "33C", "36C"]
hum = [45, 60, np.nan, 72, 40, 38, np.nan, 70,
       78, 35, 50, np.nan, 82, 42, 33]
cond = ["sunny", " Rainy", "CLOUDY ", "Rainy", "sunny",
        "Sunny ", "cloudy", "RAINY", " Cloudy", "SUNNY",
        "sunny", "Cloudy", "rainy ", "Sunny", "sunny"]

df = pd.DataFrame({"Date": dates, "City": city, "Temperature": temp,
                   "Humidity": hum, "Condition": cond})

# Add a duplicated row (copy of the last day)
df = pd.concat([df, df.iloc[[-1]]], ignore_index=True)

# (a) Cleaning
df["City"] = df["City"].str.strip().str.title()
df["Condition"] = df["Condition"].str.strip().str.title()
df["Temperature"] = pd.to_numeric(df["Temperature"].str.replace("C", "", regex=False))
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop_duplicates()
print("Rows after dropping duplicates:", len(df))

median_hum = df["Humidity"].median()
df["Humidity"] = df["Humidity"].fillna(median_hum)
print("Missing Humidity filled with median:", median_hum)

# (b) One-hot encoding of Condition
encoded = pd.get_dummies(df, columns=["Condition"], dtype=int)
print(encoded.filter(like="Condition_").head())

# (d) Correlation
corr = df["Temperature"].corr(df["Humidity"])
print("Correlation (Temperature, Humidity):", round(corr, 2))

# (e) Condition counts
counts = df["Condition"].value_counts()
print("Condition counts:")
print(counts)

# (c)-(f) 2 x 2 dashboard
fig, axes = plt.subplots(2, 2, figsize=(12, 9))

axes[0, 0].plot(df["Date"], df["Temperature"], marker="o", color="steelblue")
axes[0, 0].set_title("Temperature over Date")
axes[0, 0].set_xlabel("Date")
axes[0, 0].set_ylabel("Temperature (C)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(df["Temperature"], df["Humidity"], color="darkorange", s=60)
axes[0, 1].set_title("Temperature vs. Humidity")
axes[0, 1].set_xlabel("Temperature (C)")
axes[0, 1].set_ylabel("Humidity (%)")
axes[0, 1].grid(True, alpha=0.3)

axes[1, 0].pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
axes[1, 0].set_title("Days per Condition")

axes[1, 1].hist(df["Temperature"], bins=5, color="seagreen", edgecolor="white")
axes[1, 1].set_title("Temperature Distribution")
axes[1, 1].set_xlabel("Temperature (C)")
axes[1, 1].set_ylabel("Number of Days")

fig.suptitle("Weather Overview", fontsize=16)
plt.tight_layout()
plt.savefig("weather_dashboard.png")
plt.show()
print("Saved weather_dashboard.png")