import numpy as np
import librosa

from .audio_processing import load_audio, normalize_audio


def extract_features(file_path):
    """
    Extract numerical audio features for the ML model.
    """

    audio, sr = load_audio(file_path)

    audio = normalize_audio(audio)

    features = []

    # --------------------------------------------------------
    # MFCC
    # --------------------------------------------------------

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=20
    )

    features.extend(np.mean(mfcc, axis=1))
    features.extend(np.std(mfcc, axis=1))

    # --------------------------------------------------------
    # Mel Spectrogram
    # --------------------------------------------------------

    mel = librosa.feature.melspectrogram(
        y=audio,
        sr=sr,
        n_mels=40
    )

    mel_db = librosa.power_to_db(
        mel,
        ref=np.max
    )

    features.extend(np.mean(mel_db, axis=1))
    features.extend(np.std(mel_db, axis=1))

    # --------------------------------------------------------
    # Spectral Centroid
    # --------------------------------------------------------

    centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sr
    )

    features.append(np.mean(centroid))
    features.append(np.std(centroid))

    # --------------------------------------------------------
    # Spectral Bandwidth
    # --------------------------------------------------------

    bandwidth = librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sr
    )

    features.append(np.mean(bandwidth))
    features.append(np.std(bandwidth))

    # --------------------------------------------------------
    # Zero Crossing Rate
    # --------------------------------------------------------

    zcr = librosa.feature.zero_crossing_rate(audio)

    features.append(np.mean(zcr))
    features.append(np.std(zcr))

    # --------------------------------------------------------
    # Spectral Rolloff
    # --------------------------------------------------------

    rolloff = librosa.feature.spectral_rolloff(
        y=audio,
        sr=sr
    )

    features.append(np.mean(rolloff))
    features.append(np.std(rolloff))

    # --------------------------------------------------------
    # RMS Energy
    # --------------------------------------------------------

    rms = librosa.feature.rms(y=audio)

    features.append(np.mean(rms))
    features.append(np.std(rms))

    return np.asarray(features, dtype=np.float32)