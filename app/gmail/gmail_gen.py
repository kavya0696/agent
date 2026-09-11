import os
import json
import re
import time
import random
import urllib.request
import urllib.error

API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

def generate_email_with_gemini(command):
    if not API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing.")

    prompt = f"""
You are a professional Gmail email writing assistant.

Convert the user's voice command into a professional email.

Rules:
- Do not copy the command literally.
- Do not explain anything.
- Do not invent names, dates, prices, companies, attachments, or facts.
- Keep the email natural and concise.
- Include an appropriate greeting and closing.

Output exactly:

SUBJECT: <subject>
BODY:
<email body>

User command:
{command}
"""

    url = (
        f"https://generativelanguage.googleapis.com/"
        f"v1beta/models/{MODEL}:generateContent"
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 800
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        },
        method="POST"
    )

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode())

            text = data["candidates"][0]["content"]["parts"][0]["text"]
            text = re.sub(r"```(?:text)?|```", "", text).strip()

            subject = re.search(r"SUBJECT:\s*(.+)", text, re.I)
            body = re.search(r"BODY:\s*([\s\S]+)", text, re.I)

            if not subject or not body:
                raise RuntimeError("Gemini returned an invalid email format.")

            return {
                "subject": subject.group(1).strip(),
                "body": body.group(1).strip()
            }

        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 3:
                try:
                    detail = e.read().decode()
                except Exception:
                    detail = str(e)
                raise RuntimeError(f"Gemini API error: {detail}")

            time.sleep((2 ** attempt) + random.random())

        except Exception:
            if attempt == 3:
                raise
            time.sleep(1)
