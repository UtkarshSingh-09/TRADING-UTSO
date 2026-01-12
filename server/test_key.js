import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
dotenv.config();

async function testKey() {
    console.log("Testing API Key...");
    if (!process.env.GOOGLE_API_KEY) {
        console.error("❌ No GOOGLE_API_KEY found in environment!");
        return;
    }
    console.log(`Key found: ${process.env.GOOGLE_API_KEY.substring(0, 5)}...`);

    const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

    // Try what the user requested (2.5 flash)
    try {
        console.log("\nAttempting generation with 'gemini-2.5-flash'...");
        const model = genAI.getGenerativeModel({ model: "gemini-2.5-flash" });
        const result = await model.generateContent("Hello, this is a test from Trading Sout. Are you active?");
        console.log("✅ Success with 2.5-flash!", result.response.text());
    } catch (e) {
        console.error("❌ Failed with gemini-2.5-flash:", e.message);
        console.log("Full Error details if any:", e);
    }
}

testKey();
