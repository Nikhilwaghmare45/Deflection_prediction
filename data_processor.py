import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

class DataProcessor:
    def __init__(self):
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def load_and_preprocess_data(self, csv_path='data/training_data.csv'):
        """Load and preprocess the CSV data for model training"""
        try:
            # Read CSV data
            df = pd.read_csv(csv_path)
            
            # Clean column names
            df.columns = df.columns.str.strip()
            
            # Remove any empty rows
            df = df.dropna()
            
            # Ensure proper data types
            df['LENGTH IN MM'] = pd.to_numeric(df['LENGTH IN MM'], errors='coerce')
            df['WIDTH IN MM'] = pd.to_numeric(df['WIDTH IN MM'], errors='coerce')
            df['DEPTH IN MM'] = pd.to_numeric(df['DEPTH IN MM'], errors='coerce')
            df['REINFORCEMENT (%)'] = pd.to_numeric(df['REINFORCEMENT (%)'], errors='coerce')
            df['LOAD IN KN'] = pd.to_numeric(df['LOAD IN KN'], errors='coerce')
            df['DEFLECTION IN MM'] = pd.to_numeric(df['DEFLECTION IN MM'], errors='coerce')
            
            # Remove any rows with NaN values after conversion
            df = df.dropna()
            
            # Encode beam type
            beam_type_encoded = self.label_encoder.fit_transform(df['BEAM TYPE'])
            
            # Prepare features
            features = np.column_stack([
                beam_type_encoded,
                df['LENGTH IN MM'].values,
                df['WIDTH IN MM'].values,
                df['DEPTH IN MM'].values,
                df['REINFORCEMENT (%)'].values,
                df['LOAD IN KN'].values
            ])
            
            # Target variable
            target = df['DEFLECTION IN MM'].values
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            self.is_fitted = True
            
            return features_scaled, target, df
            
        except Exception as e:
            print(f"Error processing data: {e}")
            return None, None, None
    
    def preprocess_single_input(self, beam_type, length_mm, width_mm, depth_mm, reinforcement_percent, load_kn):
        """Preprocess a single input for prediction"""
        if not self.is_fitted:
            raise ValueError("DataProcessor must be fitted before preprocessing single inputs")
        
        # Encode beam type
        try:
            beam_type_encoded = self.label_encoder.transform([beam_type])[0]
        except ValueError:
            # If beam type not seen during training, use the most common one
            beam_type_encoded = 0
        
        # Create feature array
        features = np.array([[
            beam_type_encoded,
            length_mm,
            width_mm,
            depth_mm,
            reinforcement_percent,
            load_kn
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        return features_scaled
    
    def get_beam_types(self):
        """Get available beam types"""
        if hasattr(self.label_encoder, 'classes_'):
            return self.label_encoder.classes_.tolist()
        return ['MULI', 'MESSY', 'MANGA', 'MESS']
