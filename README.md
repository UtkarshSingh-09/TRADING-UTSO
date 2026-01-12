# TRADING SOUT 🚀

A premium, modern market anomaly detection dashboard built with React and Node.js. It leverages real-time data from a remote Hugging Face Space to provide stock analysis, news, and AI insights.

## Features
- **Pro Z-Pattern Layout**: Optimized for high-speed information scanning.
- **Live Price Flash**: Visual indicators for stock price movements.
- **AI Narrative Fallback**: Professional messaging when external services are under heavy load.
- **Glassmorphism UI**: Beautiful, premium dark mode design.

## Tech Stack
- **Frontend**: React, Vite, Framer Motion, Lucide Icons.
- **Backend**: Node.js, Express.
- **Data Source**: Hugging Face (FastAPI).

## Local Setup

### Prerequisites
- Node.js installed on your machine.

### Installation
1. Clone the repository.
2. Install dependencies for both parts:
   ```bash
   # Install server dependencies
   cd server && npm install
   
   # Install client dependencies
   cd ../client && npm install
   ```

### Running the App
1. Start the backend:
   ```bash
   cd server
   npm start
   ```
2. Start the frontend:
   ```bash
   cd client
   npm run dev
   ```

Open [http://localhost:5173](http://localhost:5173) to see the dashboard.
