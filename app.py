import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path  
from sentence_transformers import SentenceTransformer
import pandas as pd
import matplotlib.pyplot as plt
import faiss
import numpy as np
import finnhub
from google import genai
from google.genai import types
from fastapi import FastAPI
from pydantic import BaseModel

# =================================================================
# 🛠️ ENV CONFIG (Updated for Hugging Face Secrets)
# =================================================================
# HF automatically injects your Secrets into os.environ
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ CRITICAL: GOOGLE_API_KEY not found in Environment Secrets.")
else:
    print(f"🔑 API Key Active: ...{API_KEY[-4:]}")

client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

# =================================================================

def is_movement_significant(stock_data: list, threshold_sigma: float = 2.0) -> tuple[bool, float]:
    if len(stock_data) < 5: return (False, 0.0)
    df = pd.DataFrame(stock_data)
    prices = df['price']
    mean_price, std_dev = prices.mean(), prices.std()
    if std_dev == 0: return (False, 0.0)
    z_scores = (prices - mean_price) / std_dev
    significant = z_scores.abs().max() >= threshold_sigma
    percent_change = ((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100
    return significant, percent_change

def get_market_narrative(chart_image_path: str, time_series_data: dict, retrieved_headlines: list) -> str:
    try:
        with open(chart_image_path, "rb") as f:
            image_bytes = f.read()
        prompt_text = (
            "You are an expert financial analyst. Provide a one-sentence explanation for the stock "
            "movement shown in the chart. Prioritize the provided real-time news in your reasoning.\n\n"
            f"**Real-Time News Context:**\n" + "\n- ".join(retrieved_headlines) + "\n\n"
            f"**Time-Series Data:**\n```json\n{json.dumps(time_series_data)}\n```"
        )
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[prompt_text, types.Part.from_bytes(data=image_bytes, mime_type="image/png")],
            config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(include_thoughts=True))
        )
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"

class MyEncoder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    def __call__(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

def generate_chart_image(stock_data: list, save_path: str) -> str:
    df = pd.DataFrame(stock_data)
    df['time'] = pd.to_datetime(df['time'])
    plt.figure(figsize=(6, 3))
    plt.plot(df['time'], df['price'], color='blue', linewidth=2.5)
    plt.axis('off')
    plt.savefig(save_path, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    return save_path

def get_live_stock_data(stock_symbol):
    client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
    quote = client.quote(stock_symbol)
    return quote

def get_live_news(stock_symbol: str) -> list:
    gnews_token = os.getenv("GNEWS_API_KEY", "demo")
    url = f"https://gnews.io/api/v4/search?q={stock_symbol}&lang=en&max=10&token={gnews_token}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return [a['title'] for a in r.json().get('articles', [])]
    except: pass
    ticker = yf.Ticker(stock_symbol)
    return [a.get("title") for a in ticker.news if "title" in a]

def run_analysis_for_stock(stock_symbol: str) -> dict | None:
    stock_data = get_live_stock_data(stock_symbol)
    if not stock_data: return None
    is_anomaly, percent_change = is_movement_significant(stock_data)
    
    if not is_anomaly:
        return {"status": "stable", "stock_symbol": stock_symbol, "percent_change": round(percent_change, 2)}

    encoder = MyEncoder()
    headlines = get_live_news(stock_symbol) or ["No major news found."]
    vectors = np.array([encoder(h) for h in headlines]).astype('float32')
    faiss_index = faiss.IndexFlatL2(vectors.shape[1])
    faiss_index.add(vectors)
    
    query_vec = np.array([encoder(f"{stock_symbol} moved {percent_change:.2f}%")]).astype('float32')
    _, indices = faiss_index.search(query_vec, k=min(3, len(headlines)))
    retrieved = [headlines[i] for i in indices[0]]

    # HF TIP: Use /tmp/ for temporary files
    chart_path = f"/tmp/chart_{stock_symbol}.png"
    generate_chart_image(stock_data, chart_path)
    
    explanation = get_market_narrative(chart_path, {"ticker": stock_symbol}, retrieved)
    
    # Optional logging (using /tmp/ so it doesn't fail on read-only systems)
    log_path = "/tmp/market_events_log.txt"
    with open(log_path, 'a') as f:
        f.write(f"[{datetime.now()}] {stock_symbol}: {explanation}\n")
    
    if os.path.exists(chart_path): os.remove(chart_path)

    return {
        "stock_symbol": stock_symbol,
        "status": "anomaly_detected",
        "price_change_percent": round(percent_change, 2),
        "ai_explanation": explanation,
        "news_context": retrieved
    }

# --- FastAPI App ---
app = FastAPI()

class AnalysisRequest(BaseModel):
    stock_symbol: str

@app.get("/")
def health_check():
    return {"status": "online", "message": "Market Anomaly API is active. Use /analyze_stock (POST)"}

@app.post("/analyze_stock")
async def analyze_stock(request_data: AnalysisRequest):
    result = run_analysis_for_stock(request_data.stock_symbol.upper())
    return result if result else {"error": "Analysis failed."}