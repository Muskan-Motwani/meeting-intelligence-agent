from fastapi import FastAPI
from pydantic import BaseModel
from nlp.extractor import extract_insights
from db.database import save_meeting, get_meeting, get_all_meetings
from fastapi import UploadFile, File
from nlp.transcriber import transcribe_audio
import shutil
import os


app=FastAPI(title="Meeting Intelligence Agent")

class TranscriptRequest(BaseModel):
    text : str

@app.post("/meetings/analyze")
def analyze_transcript(request: TranscriptRequest):
    insights = extract_insights(request.text)
    meeting_id = save_meeting(request.text, insights)
    insights["id"] = meeting_id
    return insights


@app.get("/meetings/{meeting_id}")
def get_meeting_by_id(meeting_id: int):
    meeting = get_meeting(meeting_id)
    if meeting is None:
        return {"error": "Meeting not found"}
    return {
        "id": meeting.id,
        "summary": meeting.summary,
        "action_items": meeting.action_items,
        "decisions": meeting.decisions,
        "overall_tone": meeting.overall_tone
    }

@app.get("/meetings")
def list_meetings():
    meetings = get_all_meetings()
    return [
        {"id": m.id, "summary": m.summary, "overall_tone": m.overall_tone}
        for m in meetings
    ]

@app.post("/meetings/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcribe it
    transcript_text = transcribe_audio(temp_path)

    # Clean up the temp file
    os.remove(temp_path)

    # Run it through the same pipeline as text transcripts
    insights = extract_insights(transcript_text)
    meeting_id = save_meeting(transcript_text, insights)
    insights["id"] = meeting_id
    insights["transcript"] = transcript_text

    return insights

@app.get("/")
def health_check():
    return{"status":"running"}


        