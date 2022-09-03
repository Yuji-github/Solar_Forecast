import pandas as pd
import matplotlib.pyplot as plt

'''Data Checking'''
# Between 2022-03-29 and 2022-06-28
df = pd.read_csv("DATA_SCIENCE_SAMPLE_DATA_PostCode_5000.csv")  # PS: 5000 = Adelade (Australia)
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
# # plt.savefig("src/avg_pv_hour.png")
# plt.show()

'''Shifting Time 12 Hours'''
for itr, val in enumerate(df["Time"].to_list()):
    temp = (int(val[:2]) + 12) % 24  # over 24 becomes 0, 1, 2, ... 23
    temp = str(temp)  # convert
    if len(temp) != 2:  # if 1 -> 01
        temp = "0" + temp
    df.loc[itr, "Time"] = temp + val[2:]  # replace the hours
df["Hour"] = pd.to_datetime(df["Time"]).dt.hour  # recalculate hours

df.groupby("Hour").mean().plot(kind="line")
plt.title("Average: PV Per Day")
plt.ylabel("Solar Generation")
plt.xticks(range(0, 24, 1))
# plt.savefig("src/switched.png")
plt.show()