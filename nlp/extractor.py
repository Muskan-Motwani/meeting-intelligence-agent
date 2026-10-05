from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_insights(transcript: str) -> dict:
    prompt = f"""
    You are analyzing a meeting transcript. Extract the following and return ONLY valid JSON, no markdown, no explanation:

    {{
      "summary": "a concise 3-4 sentence summary",
      "action_items": [{{"task": "...", "owner": "...", "due": "if mentioned, else null"}}],
      "decisions": ["list of key decisions made"],
      "overall_tone": "positive, neutral, or negative"
    }}

    Transcript:
    {transcript}
    """
    response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt
    )
    
    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`").replace("json", "", 1).strip()

    return json.loads(raw_text)


if __name__ == "__main__":
    sample_transcript = """
    Alice: Let's finalize the Q3 budget by Friday.
    Bob: I'll send the draft numbers by Wednesday.
    Alice: Great, and we decided to move forward with the new vendor.
    Bob: Agreed, I'll email them the confirmation.
    """

    result = extract_insights(sample_transcript)
    print(json.dumps(result, indent=2))