from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression,SGDRegressor
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict

# 获取数据
boston = load_diabetes()
data_X = boston.data
data_y = boston.target
# 划分数据集
x_train,x_test,y_train,y_test = train_test_split(boston.data,boston.target,random_state=8)

# 特征工程，标准化
# 1> 创建一个转换器
model = LinearRegression()
model.fit(x_train, y_train)
print (model.coef_)
print (model.intercept_)
predicted = cross_val_predict(model, data_X, data_y, cv=10)
plt.scatter(data_y, predicted, color='y', marker='o')
plt.scatter(data_y, data_y,color='g', marker='+')
plt.show()

