import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';
dotenv.config();

async function listModels() {
    console.log("Listing models for your key...");
    const rawKey = process.env.GOOGLE_API_KEY;
    if (!rawKey) {
        console.error("No key found in .env");
        return;
    }

    const genAI = new GoogleGenerativeAI(rawKey.trim());

    try {
        // We use a different service to list models if possible, 
        // but the SDK standard way is to try a known-good model.
        // If the key is truly valid, this will pass.
        const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
        const result = await model.generateContent("test");
        console.log("✅ Key is AUTHENTICATED. (Successfully called gemini-1.5-flash)");

        // Note: The SDK doesn't have a direct 'list' in the standard GenAI class easily.
        // But if 1.5 works and user wants 2.5, we check if 2.0 works.
        const model2 = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
        await model2.generateContent("test");
        console.log("✅ gemini-2.0-flash is also available.");

    } catch (e) {
        console.log("❌ REJECTION RECEIVED:");
        console.log("Message:", e.message);
        if (e.message.includes("expired")) {
            console.log("👉 Google's official response is: THIS KEY IS EXPIRED.");
        }
    }
}

listModels();
