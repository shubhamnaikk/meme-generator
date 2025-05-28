from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from starlette.requests import Request
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(
    image: UploadFile = File(...),
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    data = await image.read()
    img = Image.open(BytesIO(data))
    draw = ImageDraw.Draw(img)


    def draw_caption(text, y, anchor):
        x = img.width // 2
        font_size = img.width // 10
        max_width = img.width * 0.9
        font_path = "static/fonts/Impact.ttf"
        font = ImageFont.truetype(font_path, font_size)

        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]

        
        while text_width > max_width and font_size > 10:
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            
        # outline
        for dx in (-2,-1,0,1,2):
            for dy in (-2,-1,0,1,2):
                draw.text((x+dx, y+dy), text, font=font, fill="black", anchor=anchor)
        draw.text((x, y), text, font=font, fill="white", anchor= anchor)

    if top_text:
        draw_caption(top_text.upper(), y=10, anchor="mt")
    if bottom_text:
        draw_caption(bottom_text.upper(), y=img.height - 10, anchor="mb")

    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
