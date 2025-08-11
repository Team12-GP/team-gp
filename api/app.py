from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
import requests
import re

app = FastAPI()

# ✅ Root route for status check
@app.get("/")
def root():
    return {"message": "✅ FastAPI is running. Use /api/v1/call?num=XXXXXXXXXXX"}

@app.get("/api/v1/call")
def call_api(num: str = Query(..., min_length=11, max_length=11)):
    if not re.fullmatch(r'\d{11}', num):
        raise HTTPException(status_code=400, detail="Number must be exactly 11 digits")

    external_url = f"https://funnyapi1.vercel.app/call/api/v1?num={num}"
    
    try:
        response = requests.get(external_url)
        if response.status_code == 200:
            return {
                "Team": "Grandpa Academy",
                "Owner": "Md HR",
                "Telegram": "@Termux_Team_BD_0",
                "Success": True,
                "Response": response.json()
            }
        else:
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "Team": "Grandpa Academy",
                    "Owner": "Md HR",
                    "Telegram": "@Termux_Team_BD_0",
                    "Success": False,
                    "Message": "Failed to get data from source API",
                    "StatusCode": response.status_code
                }
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
