from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from supabase import create_client, Client
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Supabase Credentials
URL = "https://qwlpbmrffilvnomdrlxq.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3bHBibXJmZmlsdm5vbWRybHhxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njg2MjE2NiwiZXhwIjoyMDkyNDM4MTY2fQ.HQAUtJY2naTKY0-HdjqKFIKLxOvw5CApDXTb9VSG75g"
supabase: Client = create_client(URL, KEY)

@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/reveal", response_class=HTMLResponse)
async def reveal_message(request: Request, username: str = Form(...), password: str = Form(...)):
    # Query Supabase for the user
    response = supabase.table("appreciation_messages") \
        .select("*") \
        .eq("username", username) \
        .eq("password", password) \
        .execute()

    if not response.data:
        return "<h3>Wrong credentials, bro! Try again.</h3>"

    user_data = response.data[0]
    return templates.TemplateResponse(
    request=request, 
    name="message.html", 
    context={
        "name": user_data['colleague_name'],
        "message": user_data['message']
    }
)