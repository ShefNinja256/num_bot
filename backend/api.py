from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from numerology import calc_numbers, calc_compatibility
from gpt_service import gpt_interpret, gpt_compatibility, gpt_natal, gpt_horoscope

app = FastAPI()

# --- Разрешаем CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # можно ограничить твоим доменом
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DateRequest(BaseModel):
    date: str

class CompatRequest(BaseModel):
    date1: str
    date2: str

class NatalRequest(BaseModel):
    date: str = Field(..., example="15.09.1992")
    time: str = Field(..., example="14:30")
    place: str = Field(..., example="Минск, Беларусь")

class HoroscopeRequest(BaseModel):
    sign: str = Field(..., example="Овен")
    period: str = Field(..., example="неделя")

@app.get("/")
def root():
    return {"ok": True, "message": "Numerology & Astrology API. See /docs"}

@app.post("/analyze")
def analyze(req: DateRequest):
    numbers = calc_numbers(req.date)
    text = gpt_interpret(numbers)
    return {"numbers": numbers, "interpretation": text}

@app.post("/compat")
def compat(req: CompatRequest):
    result = calc_compatibility(req.date1, req.date2)
    text = gpt_compatibility(result)
    return {"person1": result["person1"], "person2": result["person2"], "interpretation": text}


@app.post("/natal")
def natal(req: NatalRequest):
    text = gpt_natal(req.dict())
    return {"interpretation": text}

@app.post("/horoscope")
def horoscope(req: HoroscopeRequest):
    text = gpt_horoscope(req.dict())
    return {"interpretation": text}
