import express from 'express';
import cors from 'cors';
import fetch from 'node-fetch';
import dotenv from 'dotenv';
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const REMOTE_API_URL = "https://utkarshsingh09-market-anomaly-detector.hf.space";

app.post('/api/analyze', async (req, res) => {
    const { ticker } = req.body;
    if (!ticker) return res.status(400).json({ error: "Ticker symbol is required" });

    try {
        console.log(`Analyzing ${ticker}...`);

        // Fetch Data from Remote Space
        const remoteResponse = await fetch(`${REMOTE_API_URL}/analyze_stock`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stock_symbol: ticker })
        });

        const data = await remoteResponse.json();

        // Detect IF the AI explanation looks like an error (Quota, Invalid Key, etc.)
        const aiText = data.ai_explanation || "";
        const isErrorInAi = aiText.includes("429") ||
            aiText.includes("400") ||
            aiText.includes("error") ||
            aiText.includes("unavailable") ||
            aiText.includes("INVALID_ARGUMENT") ||
            aiText.includes("RESOURCE_EXHAUSTED");

        if (isErrorInAi) {
            console.log("⚠️ Remote AI encountered an error. Returning professional message.");
            data.ai_explanation = "Analysis temporarily unavailable due to high demand. Please consult the price action and news headlines above for immediate context.";
        }

        // Fix Chart URL
        if (data.chart_url && data.chart_url.startsWith('/')) {
            data.chart_url = `${REMOTE_API_URL}${data.chart_url}`;
        }

        res.json(data);

    } catch (e) {
        console.error("Backend Error:", e);
        res.status(500).json({ error: "Analysis temporarily unavailable. Please try again later." });
    }
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log("Connected to Remote Hugging Face Space (Direct Mode)");
});
