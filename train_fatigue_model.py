import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import joblib

print("1. Loading dataset...")
# Load the dataset
df = pd.read_csv('desk_buddy_productivity_dataset.csv')

# Separate inputs (X) and the output target (y)
X = df[['Temperature_C', 'Humidity_pct', 'CO2_ppm', 'Illuminance_lux']]
y = df['Productive']

print("2. Preprocessing data...")
# Split the data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save the scaler so the live predictor can use it
joblib.dump(scaler, 'sensor_scaler.save') 

print("3. Building the Neural Network...")
model = Sequential([
    Dense(16, activation='relu', input_shape=(4,)),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid') 
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

print("4. Training the model...")
history = model.fit(
    X_train_scaled, y_train, 
    epochs=50, 
    batch_size=32, 
    validation_split=0.2, 
    verbose=1
)

loss, accuracy = model.evaluate(X_test_scaled, y_test)
print(f"\nModel Accuracy on unseen test data: {accuracy * 100:.2f}%")

# Save the trained brain!
model.save('desk_buddy_fatigue_model.h5')
print("\nModel saved as 'desk_buddy_fatigue_model.h5'. Ready for deployment!")