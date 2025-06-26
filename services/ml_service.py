import joblib
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from services.audio_analysis_service import AudioAnalyzer

class GenreClassifier:
   target_genres = ['classical', 'jazz', 'metal', 'rock', 'blues']
   max_files_per_genre = 20  

   def __init__(self, model_path="Data/model.pkl"):
       self.model_path = Path(model_path)
       self.model = None
       self.feature_columns = None
       self.analyzer = AudioAnalyzer()
       self.ensure_model_ready()
       
   def ensure_model_ready(self):
       if not self.model_path.exists():
           self.train_and_save_model()
       else:
           self.load_model()
        

   def train_and_save_model(self):
       all_data = [] 
       for genre in self.target_genres:
           genre_folder = Path(f"Data/genres_original/{genre}")
           audio_files = list(genre_folder.glob("*.wav"))[:self.max_files_per_genre]
           for i, audio_file in enumerate(audio_files):
               try:
                   features = self.analyzer.analyze_file(str(audio_file))
                   non_numeric_keys = ['file_path', 'filename', 'genre_folder']
                   for key in non_numeric_keys:
                        if key in features:
                            del features[key]
                   features['genre'] = genre
                   all_data.append(features)
               except Exception as e:
                   print(f"Error processing {audio_file}: {e}")

       df = pd.DataFrame(all_data)
       y = df["genre"]
       x = df.drop("genre", axis=1)

       self.feature_columns = x.columns.tolist()

       model = RandomForestClassifier(random_state=42, n_estimators=100)
       model.fit(x, y)
       self.model = model

       self.model_path.parent.mkdir(exist_ok=True)

       model_data = {
           'model': model,
           'feature_columns': self.feature_columns
       }
       joblib.dump(model_data, self.model_path)
       print(f"Model trained and saved to {self.model_path}")

   def load_model(self):
       model_data = joblib.load(self.model_path)
       self.model = model_data['model']
       self.feature_columns = model_data['feature_columns']

   def predict_genre(self, audio_file_path):
       features = self.analyzer.analyze_file(audio_file_path)
       
       feature_values = {col: features[col] for col in self.feature_columns if col in features}
       feature_df = pd.DataFrame([feature_values])
       prediction = self.model.predict(feature_df)[0]
       probabilities = self.model.predict_proba(feature_df)[0]
       genre_probs = dict(zip(self.model.classes_, probabilities))
       return {
        'predicted_genre': prediction,
        'confidence': float(max(probabilities)),
        'all_probabilities': {genre: float(prob) for genre, prob in genre_probs.items()}
        }