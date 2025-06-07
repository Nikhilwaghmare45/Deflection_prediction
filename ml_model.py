import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import logging
from data_processor import DataProcessor

class MLModel:
    def __init__(self):
        self.model = None
        self.data_processor = DataProcessor()
        self.model_path = 'models/rf_model.pkl'
        self.processor_path = 'models/data_processor.pkl'
        self.is_model_trained = False
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Try to load existing model
        self.load_model()
    
    def create_rf_model(self):
        """Create Random Forest model"""
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        return model
    
    def train_model(self):
        """Train the Random Forest model"""
        try:
            # Load and preprocess data
            X, y, df = self.data_processor.load_and_preprocess_data()
            
            if X is None or y is None:
                logging.error("Failed to load training data")
                return False
            
            logging.info(f"Training data shape: X={X.shape}, y={y.shape}")
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Create model
            self.model = self.create_rf_model()
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logging.info(f"Model training completed. MSE: {mse:.4f}, R2: {r2:.4f}")
            
            # Save model and processor
            self.save_model()
            self.is_model_trained = True
            
            return True
            
        except Exception as e:
            logging.error(f"Error training model: {e}")
            return False
    
    def predict(self, beam_type, length_mm, width_mm, depth_mm, reinforcement_percent, load_kn):
        """Make a prediction using the trained model"""
        try:
            if not self.is_model_trained or self.model is None:
                raise ValueError("Model is not trained or loaded")
            
            # Preprocess input
            X_input = self.data_processor.preprocess_single_input(
                beam_type, length_mm, width_mm, depth_mm, reinforcement_percent, load_kn
            )
            
            # Make prediction
            prediction = self.model.predict(X_input)
            
            # Return the predicted deflection
            return float(prediction[0])
            
        except Exception as e:
            logging.error(f"Error making prediction: {e}")
            return None
    
    def save_model(self):
        """Save the trained model and data processor"""
        try:
            if self.model is not None:
                joblib.dump(self.model, self.model_path)
                logging.info(f"Model saved to {self.model_path}")
            
            # Save data processor
            joblib.dump(self.data_processor, self.processor_path)
            logging.info(f"Data processor saved to {self.processor_path}")
            
        except Exception as e:
            logging.error(f"Error saving model: {e}")
    
    def load_model(self):
        """Load the trained model and data processor"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.processor_path):
                self.model = joblib.load(self.model_path)
                self.data_processor = joblib.load(self.processor_path)
                self.is_model_trained = True
                logging.info("Model and data processor loaded successfully")
                return True
            else:
                logging.info("No saved model found")
                return False
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            return False
    
    def is_trained(self):
        """Check if model is trained and ready for predictions"""
        return self.is_model_trained and self.model is not None
