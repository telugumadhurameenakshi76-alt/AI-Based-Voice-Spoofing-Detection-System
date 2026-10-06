import librosa
import numpy as np


def load_audio(file_path, sample_rate=16000):
    """
    Load an audio file and convert it to mono.
    """

    audio, sr = librosa.load(
        file_path,
        sr=sample_rate,
        mono=True
    )

    if audio is None or len(audio) == 0:
        raise ValueError("Audio file is empty or could not be loaded.")

    return audio, sr


def normalize_audio(audio):
    """
    Normalize audio amplitude.
    """

    max_value = np.max(np.abs(audio))

    if max_value == 0:
        return audio

    return audio / max_value