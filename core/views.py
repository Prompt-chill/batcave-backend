import os
import io
import datetime
import numpy as np
import librosa
import random

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from pydub import AudioSegment


from .models import Recording


def _parse_timestamp(ts_str):
    if not ts_str:
        return None
    try:
        return datetime.datetime.fromisoformat(ts_str)
    except Exception:
        return None

def _analyze_audio(file_obj):
    """
    Analyzes an audio file (including .m4a) using librosa to extract features 
    like MFCCs, spectral centroid, and chroma features.
    """
    try:
        # Load audio file with pydub, which supports .m4a, .mp3, .wav, etc.
        audio = AudioSegment.from_file(file_obj, format="m4a")

        # Convert audio to numpy array for librosa
        y = np.array(audio.get_array_of_samples(), dtype=np.float32)
        # Normalize audio to range [-1.0, 1.0]
        y /= np.iinfo(audio.array_type).max
        sr = audio.frame_rate  # Sample rate

        # Extract features using librosa
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        chroma_features = librosa.feature.chroma_stft(y=y, sr=sr)

        # Aggregate features (e.g., by taking the mean)
        analysis_result = {
            'sample_rate': sr,
            'duration_s': len(y) / sr,  # Duration in seconds
            'mfcc_mean': np.mean(mfccs, axis=1).tolist(),
            'spectral_centroid_mean': np.mean(spectral_centroid),
            'chroma_features_mean': np.mean(chroma_features, axis=1).tolist(),
        }

        return analysis_result
    except Exception as e:
        # Catch any exception and return it in a structured way
        return {'error': f'analysis_failed: {str(e)}'}



@csrf_exempt
def recording_create(request):
    """Accept multipart/form-data POST with 'audio_file', optional 'device_id' and 'timestamp'."""
    if request.method != 'POST':
        return JsonResponse({'error': 'method not allowed'}, status=405)    
    # Check which files were uploaded
    audio = request.FILES.get('file')
    device_id = request.POST.get('device_id') #TODO
    timestamp_raw = request.POST.get('timestamp') 
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    if not latitude or not longitude:
        return JsonResponse({'error': 'coordinates are required'}, status=400)
    if not audio:
        return JsonResponse({'error': 'audio_file is required'}, status=400)

    ts = _parse_timestamp(timestamp_raw)
    if ts is None:
        ts = timezone.now()
    # Analyze the audio file
    analysis = _analyze_audio(audio)

    # Simple drone detection logic
    is_drone_suspicious = False
    if analysis.get('spectral_centroid_mean', 0) > 2000:
        is_drone_suspicious = True
    
    # Rewind file pointer for Django to save it correctly
    try:
        audio.seek(0)
    except Exception:
        pass

    rec = Recording.objects.create(
        device_id=device_id,
        audio_file=audio,
        timestamp=ts,
        analysis=analysis or {},
        is_drone_suspicious=is_drone_suspicious,
        latitude=latitude,
        longitude = longitude,
    )

    return JsonResponse({
        'id': rec.id,
        'audio_url': rec.audio_file.url,
        'analysis': rec.analysis,
        'is_drone_suspicious': rec.is_drone_suspicious,
        'longitude' : rec.longitude,
        'latitude' : rec.latitude

    })
