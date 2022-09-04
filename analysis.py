import pandas as pd
import matplotlib.pyplot as plt

'''Data Checking'''
# Between 2022-03-29 and 2022-06-28
df = pd.read_csv("DATA_SCIENCE_SAMPLE_DATA_PostCode_5000.csv")  # PS: 5000 = Adelaide (Australia)
time = [val.split("T") for val in df["__time"].to_list()]  # split time into "Date" and Time
df["Date"] = [row[0] for row in time]  # adding date to df
df["Time"] = [row[1].replace(":00.000Z", "") for row in time]  # adding time to df original (12:00:00.000Z) -> 12:00
df["Hour"] = pd.to_datetime(df["Time"]).dt.hour
df = df.drop(["__time"], axis=1)  # drop unnecessary colum
df = df.sort_values(by=['Date', 'Time'])  # sort by Date and Time
df = df.reset_index(drop=True)  # reset the index num

# df.groupby("Hour").mean().plot(kind="line")
# plt.title("Average: PV Per Day")
# plt.ylabel("Solar Generation")
# plt.xticks(range(0, 24, 1))
# # # plt.savefig("src/avg_pv_hour.png")  # saving image
# plt.show()

'''Shifting Time 12 Hours'''
for itr, val in enumerate(df["Time"].to_list()):
    temp = (int(val[:2]) + 12) % 24  # over 24 becomes 0, 1, 2, ... 23
    temp = str(temp)  # convert
    if len(temp) != 2:  # if 1 -> 01
        temp = "0" + temp
    df.loc[itr, "Time"] = temp + val[2:]  # replace the hours
df["Hour"] = pd.to_datetime(df["Time"]).dt.hour  # recalculate hours

# df.groupby("Hour").mean().plot(kind="line")
# plt.title("Average: PV Per Day")
# plt.ylabel("Solar Generation")
# plt.xticks(range(0, 24, 1))
# # plt.savefig("src/switched.png")  # saving image
# plt.show()

'''Import Weather Data'''
march = pd.read_csv('march.csv', skiprows=7)
march = march.dropna(axis=1, how="all")

april = pd.read_csv('april.csv', skiprows=7)
april = april.dropna(axis=1, how="all")

may = pd.read_csv('may.csv', skiprows=7)
may = may.dropna(axis=1, how="all")

jun = pd.read_csv('jun.csv', skiprows=7)
jun = jun.dropna(axis=1, how="all")

def temapture(month, hour, this_idx):
    if hour < 8 or hour >= 17:
        return month.loc[this_idx, "Minimum temperature (�C)"], month.loc[this_idx, "Rainfall (mm)"]
    elif hour in [8, 9, 10]:
        return month.loc[this_idx, "9am Temperature (�C)"], month.loc[this_idx, "Rainfall (mm)"]
    elif hour in [11, 12, 13]:
        return month.loc[this_idx, "Maximum temperature (�C)"], month.loc[this_idx, "Rainfall (mm)"]
    elif hour in [14, 15, 16]:
        return month.loc[this_idx, "3pm Temperature (�C)"], month.loc[this_idx, "Rainfall (mm)"]

for date, hour, idx in zip(df["Date"].to_list(), df["Hour"].to_list(), range(len(df))):
    this_idx = int(date[8:10]) - 1
    if int(date[6]) == 3:
        val = temapture(march, hour, this_idx)
        df.loc[idx, 'Temp'], df.loc[idx, 'Rain'], df.loc[idx, 'Sunrise'], df.loc[idx, 'Sunset'] = val[0], val[1], 7, 19
    elif int(date[6]) == 4:
        val = temapture(april, hour, this_idx)
        df.loc[idx, 'Temp'], df.loc[idx, 'Rain'], df.loc[idx, 'Sunrise'], df.loc[idx, 'Sunset'] = val[0], val[1], 6, 18
    elif int(date[6]) == 5:
        val = temapture(may, hour, this_idx)
        df.loc[idx, 'Temp'], df.loc[idx, 'Rain'], df.loc[idx, 'Sunrise'], df.loc[idx, 'Sunset'] = val[0], val[1], 7, 17
    elif int(date[6]) == 6:
        val = temapture(jun, hour, this_idx)
        df.loc[idx, 'Temp'], df.loc[idx, 'Rain'], df.loc[idx, 'Sunrise'], df.loc[idx, 'Sunset'] = val[0], val[1], 7, 17

print(df)