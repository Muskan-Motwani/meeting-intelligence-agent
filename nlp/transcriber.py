from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path: str) -> str:
    segments, info = model.transcribe(file_path)
    full_text = " ".join([segment.text for segment in segments])
    return full_text.strip()