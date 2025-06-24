# AI Music Genre Classifier

An AI-powered music genre classification system built with FastAPI and machine learning. This project can download music from YouTube and analyze audio files to predict their musical genre.

## 🎯 Project Vision

Build an AI system that can:

1. **Download music** from YouTube as MP3 files
2. **Analyze audio features** (tempo, spectral characteristics, timbre)
3. **Classify genres** into main categories: Rock, Jazz, Metal, Classical, EDM
4. **Future goal**: Classify subgenres (prog-rock, nu-metal, acid-jazz, etc.)

## 🏗️ Project Structure

```
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── .gitignore                      # Git ignore file (includes data/ and downloads/)
├── routes/
│   ├── downloads.py                # YouTube download endpoints
│   └── analysis.py                 # Audio analysis endpoints
├── services/
│   ├── youtube_service.py          # YouTube download logic
│   └── audio_analysis_service.py   # Audio feature extraction
├── models/schemas/
│   ├── download_schemas.py         # Download API schemas
│   └── analysis_schemas.py         # Analysis API schemas
└── data/                           # GTZAN dataset (gitignored)
    └── genres_original/
        ├── rock/
        ├── jazz/
        ├── metal/
        ├── classical/
        └── electronic/
```

## 🚀 Development Phases

### ✅ Phase 1: Audio Analysis Foundation (COMPLETED)

- [x] Audio preprocessing service
- [x] Feature extraction (tempo, spectral features, MFCCs)
- [x] API endpoint: `POST /analysis/features`
- [x] Integration with existing FastAPI structure

### 🔄 Phase 2: Dataset & Training Pipeline (IN PROGRESS)

- [ ] GTZAN dataset processing
- [ ] Feature extraction for entire dataset
- [ ] Model training with scikit-learn
- [ ] Model persistence and loading

### 📋 Phase 3: Genre Prediction API (PLANNED)

- [ ] API endpoint: `POST /analysis/predict-genre`
- [ ] Model inference service
- [ ] Confidence scoring

### 🎯 Phase 4: Enhanced Features (FUTURE)

- [ ] Multiple model ensemble
- [ ] Subgenre classification
- [ ] Real-time analysis improvements

## 🛠️ Technology Stack

**Backend Framework:**

- FastAPI (Python web framework)
- Uvicorn (ASGI server)

**Audio Processing:**

- librosa (audio analysis)
- yt-dlp (YouTube downloads)
- FFmpeg (audio conversion)

**Machine Learning:**

- scikit-learn (classification models)
- numpy (numerical computing)
- pandas (data manipulation)

**API & Validation:**

- Pydantic (data validation)
- Type hints throughout

## 📊 Audio Features Extracted

The system extracts comprehensive musical features:

**Basic Features:**

- `tempo`: Beats per minute (BPM)
- `duration`: Track length in seconds

**Spectral Features:**

- `spectral_centroid`: "Brightness" of sound
- `spectral_rolloff`: Energy distribution
- `zcr`: Zero crossing rate (noisiness)
- `rms`: Root mean square energy (loudness)

**MFCC Features:**

- 13 Mel-Frequency Cepstral Coefficients
- Capture timbre and texture characteristics
- Each MFCC has mean and standard deviation (26 features total)

## 🔧 Installation & Setup

### Quick Setup (Recommended)

**Windows:**

```bash
# Run the setup script
setup.bat

# Start development server
dev.bat
```

**macOS/Linux:**

```bash
# Make scripts executable
chmod +x setup.sh dev.sh

# Run the setup script
./setup.sh

# Start development server
./dev.sh
```

### Manual Setup

1. **Create and activate virtual environment:**

   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate

   # You should see (.venv) in your terminal prompt
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure FFmpeg is installed:**

   - Windows: Download from https://ffmpeg.org/
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

4. **Prepare GTZAN dataset:**

   - Place dataset in `data/genres_original/`
   - Should contain folders: rock, jazz, classical, metal, electronic

5. **Run the application:**
   ```bash
   python main.py
   ```

## 📡 API Endpoints

### Downloads

- `POST /downloads/download` - Download MP3 from YouTube
  ```json
  {
    "track_name": "song name or artist - song"
  }
  ```

### Analysis

- `POST /analysis/features` - Extract audio features

  ```json
  {
    "file_path": "path/to/audio/file.mp3"
  }
  ```

- `GET /analysis/test` - Test analysis service

### Root

- `GET /` - API information and available endpoints

## 🎵 Dataset Information

**GTZAN Dataset:**

- 1000 audio tracks (30 seconds each)
- 10 genres, 100 tracks per genre
- 22050 Hz sample rate
- Currently using 5 main genres: rock, jazz, classical, metal, electronic

## 👨‍💻 Developer Context

**Developer Background:**

- Node.js fullstack developer (2 years experience)
- Learning Python, backend development, and ML/AI
- New to audio processing and machine learning concepts

**Learning Goals:**

- Python language and ecosystem
- FastAPI backend development
- Machine learning fundamentals
- Audio signal processing
- Building end-to-end AI applications

## 🧪 Testing

**Test audio analysis:**

```bash
# Direct service test
cd services
python audio_analysis_service.py

# API test
curl http://localhost:8000/analysis/test
```

**Test feature extraction:**

```bash
curl -X POST http://localhost:8000/analysis/features \
-H "Content-Type: application/json" \
-d '{"file_path": "data/genres_original/rock/rock.00000.wav"}'
```

## 🔍 Key Concepts Learned

**Python Concepts:**

- Type hints and Pydantic models
- Dictionary unpacking (`**kwargs`)
- f-string formatting
- Exception handling (`try/except`)
- Class-based services

**Audio Processing:**

- Sample rates and audio loading
- Feature extraction from waveforms
- Spectral analysis and MFCCs
- Audio preprocessing pipelines

**API Design:**

- FastAPI routing and dependency injection
- Request/response schemas
- Error handling and HTTP status codes
- Modular service architecture

## 📝 Next Steps

1. **Complete Phase 2**: Train initial genre classifier
2. **Implement model inference**: Add prediction endpoint
3. **Optimize performance**: Batch processing and caching
4. **Add subgenre classification**: Expand to more specific genres
5. **Create web interface**: Frontend for easy testing

## 📞 Development Notes

- All audio files are converted to mono for consistency
- Feature extraction is optimized for 30-second clips
- Model will be trained on GTZAN dataset patterns
- API follows RESTful conventions
- Comprehensive error handling and logging included

---

**Status**: Phase 1 Complete - Ready for dataset processing and model training
