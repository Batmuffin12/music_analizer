from pydantic import BaseModel
from typing import Dict, Optional, List


class AudioAnalysisRequest(BaseModel):
    """Request schema for audio analysis"""

    file_path: str


class AudioFeaturesResponse(BaseModel):
    """Response schema for audio feature extraction"""

    # Basic audio properties
    tempo: float
    duration: float

    # Spectral features (brightness, energy distribution)
    spectral_centroid_mean: float
    spectral_centroid_std: float
    spectral_rolloff_mean: float

    # Temporal features (rhythm, dynamics)
    zcr_mean: float  # Zero crossing rate
    zcr_std: float
    rms_mean: float  # RMS energy
    rms_std: float

    # MFCC features (timbre characteristics)
    # We'll have 13 MFCCs, each with mean and std
    mfcc_0_mean: float
    mfcc_0_std: float
    mfcc_1_mean: float
    mfcc_1_std: float
    mfcc_2_mean: float
    mfcc_2_std: float
    mfcc_3_mean: float
    mfcc_3_std: float
    mfcc_4_mean: float
    mfcc_4_std: float
    mfcc_5_mean: float
    mfcc_5_std: float
    mfcc_6_mean: float
    mfcc_6_std: float
    mfcc_7_mean: float
    mfcc_7_std: float
    mfcc_8_mean: float
    mfcc_8_std: float
    mfcc_9_mean: float
    mfcc_9_std: float
    mfcc_10_mean: float
    mfcc_10_std: float
    mfcc_11_mean: float
    mfcc_11_std: float
    mfcc_12_mean: float
    mfcc_12_std: float

    # Metadata
    file_path: str


class GenrePrediction(BaseModel):
    """schema for genre prediction"""
    predicted_genre: str
    confidence: float
    all_probabilities: Dict[str, float]

class GenrePredictionResponse(GenrePrediction) :
    """Response schema for genre prediction"""
    file_path: str
    available_genres: List[str] = ["classical", "jazz", "metal", "rock", "blues"]


class BatchAnalysisRequest(BaseModel):
    folder_path : str
    max_files: Optional[int] = 50

class BatchAnalysisResponse(BaseModel):
    total_files: int
    successful_analyses: int
    failed_analyses: Optional[int] = 0
    folder_path: str
    processing_time: float
    results: list[GenrePrediction] 