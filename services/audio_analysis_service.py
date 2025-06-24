import librosa
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Set up logging to help us debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioAnalyzer:
    """
    Service for extracting musical features from audio files
    Think of this like a music theory analyzer that can 'hear' tempo, pitch, etc.
    """

    def __init__(self, sample_rate: int = 22050):
        """
        Initialize the analyzer
        sample_rate: How many audio samples per second to analyze
        22050 Hz is standard for music analysis (half of CD quality)
        """
        self.sample_rate = sample_rate

    def load_audio(self, file_path: str) -> tuple:
        """
        Load an audio file and convert it to a format we can analyze
        Returns: (audio_data, sample_rate)

        This is like reading a file in Node.js, but for audio
        """
        try:
            # librosa.load() is like fs.readFile() but for audio
            # It automatically converts to mono and resamples
            audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
            logger.info(f"Loaded audio: {len(audio_data)} samples at {sr}Hz")
            return audio_data, sr
        except Exception as e:
            logger.error(f"Failed to load audio file {file_path}: {e}")
            raise

    def extract_basic_features(self, audio_data: np.ndarray, sr: int) -> Dict:
        """
        Extract basic musical features from audio data
        This is where the 'AI magic' starts - we convert sound waves to numbers
        rock.00000.wav - A902

        """
        features = {}

        try:
            # 1. TEMPO - How fast is the song? (BPM = Beats Per Minute)
            tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
            features["tempo"] = float(tempo)

            # 2. SPECTRAL CENTROID - "Brightness" of the sound
            # Higher values = brighter sound (like cymbals)
            # Lower values = darker sound (like bass guitar)
            spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
            features["spectral_centroid_mean"] = float(np.mean(spectral_centroid))
            features["spectral_centroid_std"] = float(np.std(spectral_centroid))

            # 3. SPECTRAL ROLLOFF - Where most of the energy is concentrated
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)
            features["spectral_rolloff_mean"] = float(np.mean(spectral_rolloff))

            # 4. ZERO CROSSING RATE - How often the audio crosses zero
            # Higher for noisy sounds (distorted guitar), lower for tonal sounds (flute)
            zcr = librosa.feature.zero_crossing_rate(audio_data)
            features["zcr_mean"] = float(np.mean(zcr))
            features["zcr_std"] = float(np.std(zcr))

            # 5. RMS ENERGY - Overall loudness/energy
            rms = librosa.feature.rms(y=audio_data)
            features["rms_mean"] = float(np.mean(rms))
            features["rms_std"] = float(np.std(rms))

            logger.info(f"Extracted {len(features)} basic features")
            return features

        except Exception as e:
            logger.error(f"Feature extraction failed: {e}")
            raise

    def extract_mfcc_features(
        self, audio_data: np.ndarray, sr: int, n_mfcc: int = 13
    ) -> Dict:
        """
        Extract MFCC features - these capture the 'timbre' or 'color' of sound
        MFCC = Mel-Frequency Cepstral Coefficients
        Think of these as fingerprints that distinguish a guitar from a piano
        """
        try:
            # Extract MFCCs - these are the most important features for genre classification
            mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc)

            # Calculate statistics for each MFCC coefficient
            mfcc_features = {}
            for i in range(n_mfcc):
                mfcc_features[f"mfcc_{i}_mean"] = float(np.mean(mfccs[i]))
                mfcc_features[f"mfcc_{i}_std"] = float(np.std(mfccs[i]))

            logger.info(f"Extracted {len(mfcc_features)} MFCC features")
            return mfcc_features

        except Exception as e:
            logger.error(f"MFCC extraction failed: {e}")
            raise

    def analyze_file(self, file_path: str) -> Dict:
        """
        Complete analysis of an audio file
        This is our main function that combines everything
        """
        logger.info(f"Starting analysis of {file_path}")

        # Load the audio file
        audio_data, sr = self.load_audio(file_path)

        # Extract all features
        basic_features = self.extract_basic_features(audio_data, sr)
        mfcc_features = self.extract_mfcc_features(audio_data, sr)

        # Combine all features into one dictionary
        all_features = {
            **basic_features,
            **mfcc_features,
            "file_path": file_path,
            "duration": float(len(audio_data) / sr),  # Duration in seconds
        }

        logger.info(f"Analysis complete: {len(all_features)} features extracted")
        return all_features


if __name__ == "__main__":
    test_analyzer()
