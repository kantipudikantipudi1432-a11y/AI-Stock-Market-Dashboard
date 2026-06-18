import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense

def predict_next_price(data):

    prices = data["Close"].values.reshape(-1, 1)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(prices)

    X = []
    y = []

    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])

    X = np.array(X)
    y = np.array(y)

    X = X.reshape(
        X.shape[0],
        X.shape[1],
        1
    )

    model = Sequential([
        LSTM(
            50,
            return_sequences=True,
            input_shape=(60, 1)
        ),
        LSTM(50),
        Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    model.fit(
        X,
        y,
        epochs=3,
        batch_size=32,
        verbose=0
    )

    last_60 = scaled_data[-60:]
    X_test = np.array([last_60])

    prediction = model.predict(
        X_test,
        verbose=0
    )

    prediction = scaler.inverse_transform(
        prediction
    )

    return float(prediction[0][0])
