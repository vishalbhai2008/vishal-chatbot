
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import gradio as gr
from googletrans import Translator

app = FastAPI()

ADMIN_EMAIL = "vishal47701@gmail.com"
ADMIN_PASSWORD = "vishalbhaiadmin@2008"

translator = Translator()
user_data = []

def chatbot(message, user_type="free"):
    detected_lang = translator.detect(message).lang
    translated_input = translator.translate(message, src=detected_lang, dest='en').text

    if user_type == "pro":
        reply = f"[Pro Version] Detailed Response to: {translated_input}"
    else:
        reply = f"[Free Version] Basic Response to: {translated_input}"

    final_reply = translator.translate(reply, src='en', dest=detected_lang).text
    return final_reply

io = gr.Interface(
    fn=chatbot,
    inputs=[gr.Textbox(label="Your Message"), gr.Radio(choices=["free", "pro"], label="Choose Access")],
    outputs="text",
    title="VishalChatbot (Free + Pro Mode)",
)

@app.get("/", response_class=HTMLResponse)
def login_form():
    return """
    <html><head><title>Login</title></head><body>
    <h2>Login</h2>
    <form action='/login' method='post'>
    Email: <input type='text' name='email'><br>
    Password: <input type='password' name='password'><br>
    <input type='submit' value='Login'>
    </form>
    </body></html>
    """

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...)):
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        return RedirectResponse(url="/admin", status_code=302)
    else:
        return HTMLResponse("<h3>Login Failed! Invalid credentials.</h3>")

@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    return f"""
    <html><head><title>Admin</title></head><body>
    <h1>Welcome Admin</h1>
    <p>Total Messages Stored: {len(user_data)}</p>
    <a href='/gradio'>Access Chatbot</a>
    </body></html>
    """

@app.get("/gradio")
def gradio_ui():
    return gr.mount_gradio_app(app, io, path="/gradio")
