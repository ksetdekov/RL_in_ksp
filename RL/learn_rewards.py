import pandas as pd
from xgboost import XGBRegressor

# print(os.listdir())
train_path = 'train_data.csv'
train_data = pd.read_csv(train_path)

model = XGBRegressor()

train_x = train_data.iloc[:,0:-1]
train_y = train_data[['rewards']]

model.fit(train_x, train_y)


