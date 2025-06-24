from fastapi import APIRouter, HTTPException
from pathlib import Path

from models.schemas.analysis_schemas import AudioAnalysisRequest, AudioFeaturesResponse
from services.audio_analysis_service import AudioAnalyzer

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)

# Create a single instance of our analyzer
analyzer = AudioAnalyzer()


@router.post("/features", response_model=AudioFeaturesResponse)
def extract_audio_features(request: AudioAnalysisRequest):
    """
    Extract musical features from an audio file
    This is like getting the 'DNA' of a song - tempo, brightness, energy, etc.
    """
    try:
        # Check if file exists
        if not Path(request.file_path).exists():
            raise HTTPException(
                status_code=404, detail=f"Audio file not found: {request.file_path}"
            )

        # Extract features using our analyzer
        features = analyzer.analyze_file(request.file_path)

        # Return features in our structured format
        return AudioFeaturesResponse(**features)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Feature extraction failed: {str(e)}"
        )


@router.get("/test")
def test_analysis_endpoint():
    """Test endpoint to make sure our analysis service is working"""
    return {
        "message": "Analysis service is running",
        "available_endpoints": {
            "/analysis/features": "POST - Extract features from audio file",
            "/analysis/test": "GET - Test if service is working",
        },
    }
