from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
from llm import ask_question

app = FastAPI()

@app.get("/")
def home():
    return {"status": "running"}


@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    form = await request.form()
    user_msg = form.get("Body")

    if not user_msg:
        user_msg = "hello"

    reply = ask_question(user_msg)

    # IMPORTANT: force plain string
    reply = str(reply)

    # WhatsApp safe length (optional but recommended)
    reply = reply[:1500]

    resp = MessagingResponse()
    resp.message(reply)

    return Response(
        content=str(resp),
        media_type="application/xml"
    )