import pandas as pd
import zipfile
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Unzip the file and load the datasets
with zipfile.ZipFile(r'C:\Sidhant\Projects\HackX\wellnessSync\health_data.zip', 'r') as z:
    z.extractall()

train_df = pd.read_csv('Train_Data.csv')
test_df = pd.read_csv('Test_Data.csv')

# Define feature columns based on the new dataset
numerical_features = ['Age', 'BMI', 'Illness count last year']
categorical_features = ['Specific ailments', 'Food preference', 'Smoker?', 'Living in?', 'Any heriditary condition?', 
                        'Follow Diet', 'Physical activity', 'Regular sleeping hours', 'Alcohol consumption', 
                        'Social interaction', 'Taking supplements', 'Mental health management']

# Define the preprocessing pipeline
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Apply transformations
X_train = train_df.drop(columns=['ID1', 'ID2'])
y_train = train_df['Illness count last year']
X_test = test_df.drop(columns=['ID1', 'ID2'])
y_test = test_df['Illness count last year']

# Handle NaN values in the target variable
y_train = y_train.fillna(y_train.median())
y_test = y_test.fillna(y_test.median())

X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Define the model
model = Ridge()

# Cross-validation (Commented out as not necessary for the core functionality)
# scores = cross_val_score(model, X_train_preprocessed, y_train, scoring='neg_mean_squared_error', cv=5)
# mse_scores = -scores
# mean_mse = mse_scores.mean()
# print(f'Cross-validated Mean Squared Error: {mean_mse}')

# Train the model
model.fit(X_train_preprocessed, y_train)

# Evaluate the model (Commented out as not necessary for the core functionality)
# y_pred = model.predict(X_test_preprocessed)
# mse = mean_squared_error(y_test, y_pred)
# mae = mean_absolute_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
# print(f'Mean Squared Error: {mse}')
# print(f'Mean Absolute Error: {mae}')
# print(f'R-squared: {r2}')

# Save the model and preprocessor
joblib.dump(model, 'model.pkl')
joblib.dump(preprocessor, 'preprocessor.pkl')
