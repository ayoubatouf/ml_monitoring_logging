import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd


def lr_training_demo(df, target):

    X = df.drop(target, axis=1).values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    joblib.dump(model, "linear_regression_model.pkl")

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"Intercept: {model.intercept_:.2f}, Slope: {model.coef_}")


if __name__ == "__main__":

    data = {
        "feature1": np.random.rand(100),
        "feature2": np.random.rand(100),
        "target": np.random.rand(100),
    }
    df = pd.DataFrame(data)

    lr_training_demo(df, "target")
