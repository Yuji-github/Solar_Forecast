import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import math
from tqdm import tqdm
import joblib

df = pd.read_csv("solar.csv")  # the last date is 2022-06-28

'''Data Preparation'''
index = df[df['Date'] == '2022-06-21'].index.values  # to predict 7 days
# Zenith Angle contain date and time -> remove ['Date', 'Time', "Hour"]
train, test = df[:index[0]].drop(labels=['Date', 'Time', "Hour"], axis=1), df[index[0]:].drop(labels=['Date', 'Time'], axis=1)  # split into train and test
hour = test["Hour"].to_list()  # use this in evaluation
test = test.drop("Hour", axis=1)

"""Finding Outlier"""
plt.figure(figsize=(16, 10))
plt.subplot(1, 3, 1)
plt.scatter(train["Temp"], train["PV"])
plt.ylabel("Solar Generation")
plt.xlabel("Temperature")
plt.subplot(1, 3, 2)
plt.scatter(train["Rain"], train["PV"])
plt.title("Outlier Check Between PV and Temp/Rain/Zenith")  # in the middle
plt.ylabel("Solar Generation")
plt.xlabel("Rain")
plt.subplot(1, 3, 3)
plt.scatter(train["Zenith"], train["PV"])
plt.ylabel("Solar Generation")
plt.xlabel("Zenith Angle")
plt.tight_layout()
# plt.savefig("src/outlier.png")  # saving image
plt.show()
# There was no outlier from the image

'''Machine Learning'''
x_train, y_train = train.iloc[:, 1:], train.iloc[:, 0]
x_test, y_test = test.iloc[:, 1:], test.iloc[:, 0]

'''Scaling by SD'''
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

'''Creating 3 Ensemble Learning Models for GridSearch'''
def estimator():
    clf1 = RandomForestRegressor(random_state=0)
    clf2 = AdaBoostRegressor(random_state=0)
    clf3 = GradientBoostingRegressor(random_state=0, criterion="friedman_mse")

    param1 = {'n_estimators': [10, 50, 100, 150], 'max_depth': [3, 5, None]}
    param2 = {'n_estimators': [10, 50, 100, 150], 'learning_rate': [1e-3, 1e-2, 1e-1]}
    param3 = {'n_estimators': [10, 50, 100, 150], 'learning_rate': [1e-3, 1e-2, 1e-1]}

    clf = [clf1, clf2, clf3]
    params = [param1, param2, param3]

    return clf, params

'''Training'''
clf, params = estimator()
best_score = 0
best_model_name = ''
best_param = {}
for itr in tqdm(range(len(clf))):
    gs = GridSearchCV(clf[itr], params[itr], scoring='r2', cv=5, n_jobs=-1).fit(x_train, y_train)
    if gs.best_score_ > best_score:
        joblib.dump(gs, 'best.pkl')  # save a local best one
        best_score = gs.best_score_
        best_model_name = str(clf[itr])
        best_param = gs.best_params_
print("Name {:s} : Best R2 Score {:.2f}".format(best_model_name, best_score))
print(best_param)

'''Loading Best Model and Eval'''
model = joblib.load("best.pkl")  # loading the best model
y_pred = model.predict(x_test)  # predicting

'''Evaluating'''
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
print("MSE {:.2f} : RMSE {:.2f}".format(mse, rmse))

y_true_df = pd.DataFrame({"Hour": hour, "PV": y_test})
y_pred_df = pd.DataFrame({"Hour": hour, "PV": y_pred})

y_true_df.groupby("Hour")["PV"].mean().plot(kind="line")
y_pred_df.groupby("Hour")["PV"].mean().plot(kind="line", color="red")
plt.legend(["True", "Pred"])
plt.title("Truth vs Prediction: PV Per Day")
plt.ylabel("Solar Generation")
# plt.savefig("src/result.png")  # saving image
plt.show()