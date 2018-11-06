"""Correr el script con python3
"""
import numpy as np

from sklearn.metrics import mean_squared_error

# Regressors
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.multioutput import MultiOutputRegressor

#  input file
input_file_x = '../data/charlie/mano/myo_data'
input_file_y = '../data/charlie/mano/glove_data'

# Load data from file
data_X = np.loadtxt(input_file_x, delimiter=',')
data_y = np.loadtxt(input_file_y, delimiter=',')


X, y = data_X[:], data_y[:]

num_training = int(0.999 * len(X))
num_test = len(X) - num_training

X_train, y_train = X[:num_training], y[:num_training]
X_test, y_test = X[num_training:], y[num_training:]

ESTIMATORS = {
    "K-nn": KNeighborsRegressor(),                          # Accept default parameters
    "Linear regression": LinearRegression(),
    "Ridge": RidgeCV(),
    "Lasso": Lasso(),
    "ElasticNet": ElasticNet(random_state=0),
    "RandomForestRegressor": RandomForestRegressor(max_depth=10, random_state=2),
    "Decision Tree Regressor":DecisionTreeRegressor(max_depth=10),
    "MultiO/P GBR" :MultiOutputRegressor(GradientBoostingRegressor()),
    "MultiO/P AdaB" :MultiOutputRegressor(AdaBoostRegressor())
}

# 9.1 Create an empty dictionary to collect prediction values
y_test_predict = dict()
y_mse = dict()

for name, estimator in ESTIMATORS.items():
    estimator.fit(X_train, y_train)
    y_test_predict[name] = estimator.predict(X_test)
    y_mse[name] = mean_squared_error(y_test, estimator.predict(X_test))
    
print('X de Prueba: ')
print(X_test)

min_name = min(y_mse, key=y_mse.get)
min_val = y_mse[min_name]
print('\nMEJOR RESULTADO: %s %f' % (min_name, min_val))

print('\n*********************')
print('*********************')

    
for name, estimators in ESTIMATORS.items():
    print('\n*********************\n')
    print(f'{ name }  / RMSE: { y_mse[name] }\n')
    print(y_test_predict[name])
    print('*********************')
