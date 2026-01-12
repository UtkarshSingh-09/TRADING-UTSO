import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import faiss
import numpy as np
import finnhub
from datetime import datetime
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# =================================================================
# 🛠️ ENV CONFIG
# =================================================================
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash" 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =================================================================
# 📈 HELPER FUNCTIONS (Must be defined before they are used)
# =================================================================

def get_live_stock_data(stock_symbol):
    finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
    quote = finnhub_client.quote(stock_symbol)
    if not quote or quote.get('c') == 0:
        return []
    return [
        {"time": "Prev Close", "price": quote['pc']},
        {"time": "Open", "price": quote['o']},
        {"time": "High", "price": quote['h']},
        {"time": "Low", "price": quote['l']},
        {"time": "Current", "price": quote['c']}
    ]

def get_live_news(stock_symbol: str) -> list:
    gnews_token = os.getenv("GNEWS_API_KEY", "demo")
    url = f"https://gnews.io/api/v4/search?q={stock_symbol}&lang=en&max=10&token={gnews_token}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return [a['title'] for a in r.json().get('articles', [])]
    except: 
        return ["No major news found."]
    return ["No major news found."]

def is_movement_significant(stock_data: list, threshold_sigma: float = 0.1) -> tuple[bool, float]:
    if len(stock_data) < 5: return (False, 0.0)
    df = pd.DataFrame(stock_data)
    prices = df['price']
    mean_price, std_dev = prices.mean(), prices.std()
    if std_dev == 0: return (False, 0.0)
    z_scores = (prices - mean_price) / std_dev
    significant = z_scores.abs().max() >= threshold_sigma
    percent_change = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
    return significant, percent_change

def generate_chart_image(stock_data, symbol):
    save_path = f"/tmp/chart_{symbol.upper()}.png"
    df = pd.DataFrame(stock_data)
    
    # --- FIX STARTS HERE ---
    # Create a fresh figure and axis object for EVERY request
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Use 'ax' instead of 'plt' to draw
    ax.plot(df['time'], df['price'], marker='o', linestyle='-', color='#3b82f6', linewidth=2)
    
    ax.set_title(f"{symbol} Price Movement")
    ax.set_xlabel("Point")
    ax.set_ylabel("Price (USD)")
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Save using the figure object
    fig.savefig(save_path)
    
    # Crucial: Explicitly close the figure to free up memory
    plt.close(fig) 
    # --- FIX ENDS HERE ---
    
    return save_path

def get_market_narrative(chart_image_path: str, time_series_data: dict, retrieved_headlines: list) -> str:
    try:
        with open(chart_image_path, "rb") as f:
            image_bytes = f.read()
        prompt_text = (
            "Provide a one-sentence explanation for this stock movement using these headlines:\n" + 
            "\n- ".join(retrieved_headlines)
        )
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt_text, types.Part.from_bytes(data=image_bytes, mime_type="image/png")]
        )
        return response.text.strip()
    except Exception as e:
        return f"AI Insight unavailable: {e}"

class MyEncoder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    def __call__(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

# =================================================================
# 🧠 MAIN ANALYSIS LOGIC
# =================================================================

def run_analysis_for_stock(stock_symbol: str) -> dict | None:
    symbol = stock_symbol.upper()
    stock_data = get_live_stock_data(symbol)
    if not stock_data: return None
    
    # Extract the current price from the last entry in stock_data
    # In your get_live_stock_data, the last item is {"time": "Current", "price": quote['c']}
    current_actual_price = stock_data[-1]['price']
    
    is_anomaly, percent_change = is_movement_significant(stock_data)
    chart_path = generate_chart_image(stock_data, symbol)
    
    # Base dictionary that ALWAYS includes the price
    response_data = {
        "stock_symbol": symbol,
        "current_price": current_actual_price, # <--- THIS WAS MISSING
        "price_change_percent": round(percent_change, 2),
        "chart_url": f"/get_chart/{symbol}"
    }

    if not is_anomaly:
        response_data["status"] = "stable"
        response_data["ai_explanation"] = "Market is trading within normal volatility ranges."
        return response_data

    # If it is an anomaly, add the extra AI details
    headlines = get_live_news(symbol)
    retrieved = headlines[:3] 
    explanation = get_market_narrative(chart_path, {"ticker": symbol}, retrieved)
    
    response_data.update({
        "status": "anomaly_detected",
        "ai_explanation": explanation,
        "news_context": retrieved
    })
    
    return response_data
# =================================================================
# 🚀 API ROUTES
# =================================================================

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalysisRequest(BaseModel):
    stock_symbol: str

@app.get("/")
async def read_index():
    if os.path.exists('static/index.html'):
        return FileResponse('static/index.html')
    return {"message": "API Online. Please visit /static/index.html"}

@app.post("/analyze_stock")
async def analyze_stock(request_data: AnalysisRequest):
    result = run_analysis_for_stock(request_data.stock_symbol)
    return result if result else {"error": "Analysis failed."}

@app.get("/get_chart/{symbol}")
async def get_chart(symbol: str):
    chart_path = f"/tmp/chart_{symbol.upper()}.png"
    if os.path.exists(chart_path):
        return FileResponse(chart_path, media_type="image/png")
    return {"error": "Chart not found"}
