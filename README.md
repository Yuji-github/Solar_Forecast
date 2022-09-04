### 1.Purposes
Our climate is changing every single day because we consume more fuel since we have discovered the power of fuel. We believe that we should shift to using more recyclable energy sources like solar. However, generating power by solar is unstable because of the weather conditions, and [a new reserach](https://www.sciencedirect.com/science/article/abs/pii/S0306261921008898?via%3Dihub) found how weather events can reduce the amount of energy produced by the United States. To solve the problem, we need to predict the generation of power, and we can store the power in the battery effectively. This project demonstrates how to predict the generation of power for 7 days by using machine learning.

### 2.Dependecy 
- Python

### 3.Data Analysis: Post Code 5000 Data Set
<p align="center">
<img src="src/avg_pv_hour.png" alt="average generating PV" title="Avg: PV" height="256" width="300">
<p>
Between 9 p.m. and 7 a.m., PV is generated. On the other hand, in the daytime (8 a.m. to 8 p.m.), PV is not generated for 3 months on average. As a result, we can assume that the time should be switched between a.m. and p.m. Otherwise, Adelaide has the sunlight at midnight.

<p align="center">
<img src="src/switched.png" alt="average generating PV" title="Avg: PV" height="256" width="300">
<p>
After switching between the daytime and nighttime, we can clearly and logically see the actual PV behaviors.

Since the research found the correlation between PV and weather, we need to add weather conditions to our dataset. Thus, we concatenate [weather datasets](http://www.bom.gov.au/climate/dwo/IDCJDW5081.latest.shtml) into our dataframe. From the weather dataset, we extract rain and temperature. However, the dataset does not cover every hour of temperature and rain information. We alternatively select values following the methods.
- Rain: Assume that if it rains in Adelaide on a given day, we assume that it will rain all day. <br>
On April 6, there was 5.2 mm of rain. So, every hour contains 5.2 mm of rain.
- Temperature: There are 4 temperatures in the dataset; min, max, 9 am and 3 pm. <br>
Before 7 am, we assume the temperature is min.<br>
Between 8 and 10 am, we assume the temperature is the same as at 9 am.<br>
Between 11 am and 1 pm, we assume the temperature is max.<br>
Between 2 and 4 pm, we assume the temperature is the same as at 3 am.<br>
After 5 pm, we assume the temperature is min.<br>

Correlation between PV and Time, Weather, and Temperature: 

|     | PV  | Time | Weather | Temperature |
|:---:| :---: | :---: | :---: | :---: |
| PV  | 1.0 | -0.558 | -0.08 | -0.18 | 

From the above table, there is negatively strong relation between PV and Time.

<img src="src/corr.png" alt="corr" title="corr" height="300" width="300"><br>
[More details](https://www.researchgate.net/publication/334308527_Usefulness_of_Correlation_Analysis)

Thus, we add sunrise and sunset times in Adelaide between March and June into our dataset. To do so, we are able to calculate the solar elevation angles roughly. *In April, there is a time change in Adelaide.

The solar elevation formula is as follows:<br>
<p align="center">
sin(ɑ) = sin(ɸ)sin(δ) + cos(ɸ)cos(δ)cos(h)
<p>
Where ɑ is the solar elevation angle, δ is the declination angle, ɸ is the latitude of your location, and h is the solar hour angle.
