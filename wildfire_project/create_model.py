import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def create_and_save_model():
    # Generate more realistic sample data
    np.random.seed(42)
    n_samples = 1000
    
    # Generate features with realistic ranges
    ffmc = np.random.uniform(18.7, 96.2, n_samples)  # Fine Fuel Moisture Code
    dmc = np.random.uniform(1.1, 291.3, n_samples)   # Duff Moisture Code
    dc = np.random.uniform(7.9, 860.6, n_samples)    # Drought Code
    isi = np.random.uniform(0.0, 56.1, n_samples)    # Initial Spread Index
    temp = np.random.uniform(2.2, 33.3, n_samples)   # Temperature
    rh = np.random.uniform(15.0, 100.0, n_samples)   # Relative Humidity
    wind = np.random.uniform(0.4, 9.4, n_samples)    # Wind Speed
    rain = np.random.uniform(0.0, 6.4, n_samples)    # Rain

    # Create feature matrix
    X = np.column_stack([ffmc, dmc, dc, isi, temp, rh, wind, rain])
    
    # Create more realistic target values based on feature relationships
    # Higher values of these factors generally lead to larger fire spread
    y = (
        0.3 * ffmc +                  # Higher FFMC increases spread
        0.2 * dmc +                   # Higher DMC increases spread
        0.15 * dc +                   # Higher DC increases spread
        0.5 * isi +                   # ISI has strong effect on spread
        0.4 * temp +                  # Higher temperature increases spread
        -0.3 * rh +                   # Higher humidity decreases spread
        0.35 * wind +                 # Higher wind speed increases spread
        -0.4 * rain                   # Rain decreases spread
    )
    
    # Add some noise to make it more realistic
    y += np.random.normal(0, 0.5, n_samples)
    
    # Ensure all areas are positive and scale to realistic hectares
    y = np.abs(y)
    y = (y - y.min()) / (y.max() - y.min()) * 100  # Scale to 0-100 hectares
    
    # Create and train the model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    # Scale the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train the model
    model.fit(X_scaled, y)
    
    # Save both the model and scaler
    with open('forest_fire_model.pkl', 'wb') as f:
        pickle.dump({'model': model, 'scaler': scaler}, f)
    
    print("Model created and saved successfully!")
    
    # Print feature importances
    feature_names = ['FFMC', 'DMC', 'DC', 'ISI', 'Temperature', 'RH', 'Wind', 'Rain']
    importances = model.feature_importances_
    for name, importance in zip(feature_names, importances):
        print(f"{name}: {importance:.4f}")

if __name__ == "__main__":
    create_and_save_model() 