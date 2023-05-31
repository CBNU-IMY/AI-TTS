import os
import io
import onnxruntime
import torch
import numpy as np
import time

from TTS.utils.synthesizer import Synthesizer
from TTS.tts.utils.synthesis import synthesis, trim_silence

_synthesizer = Synthesizer(
        os.environ['TTS_MODEL_FILE'],
        os.environ['TTS_MODEL_CONFIG'],
        None,
        None,
        None,
        None,
        None,
        False,
    )

def synthesize(text):
    wavs = _synthesizer.tts(text, None, None)
    out = io.BytesIO()
    _synthesizer.save_wav(wavs, out)
    return out