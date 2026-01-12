# TRADING SOUT 🚀

![React](https://img.shields.io/badge/REACT-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/NODE.JS-EXPRESS-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Hugging Face](https://img.shields.io/badge/HUGGING_FACE-FASTAPI-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Vite](https://img.shields.io/badge/VITE-BUNDLER-646CFF?style=for-the-badge&logo=vite&logoColor=white)

A **Premium Market Anomaly Detector** designed to identify institutional-grade price movements and provide real-time AI context using your personal Hugging Face deployment.

TRADING SOUT analyzes stock data via a secure Node.js proxy and returns visual charts, live news, and AI narratives with a sleek, high-fidelity dark mode interface.

---

## 🏗️ System Architecture

The application follows a modern bridge architecture to ensure real-time performance and cross-origin security.

1.  **💻 Presentation Layer** A React 19 frontend implementing a "Pro" Z-pattern layout for optimal scanning speed.
2.  **🛡️ Proxy Layer** A Node.js backend that handles authentication and proxies requests to the remote AI engine.
3.  **🤖 Inference Layer** A FastAPI service hosted on **Hugging Face Spaces** that performs the heavy lifting: data ingestion, vector search, and Gemini-powered narrative generation.

---

## 🚀 Key Features

| Feature | Description |
| :--- | :--- |
| ⚡ **Live Price Flash** | Real-time visual feedback (Green/Red) on all price updates. |
| 📊 **Dynamic Charts** | Instant Matplotlib-generated snapshots of recent price action. |
| 🔍 **Z-Pattern UX** | Specialized dashboard layout designed for professional traders. |
| 🛡️ **Fail-Safe Narrative** | Intelligent fallback system to handle remote AI quota limits gracefully. |
| 🌐 **Dynamic Title** | Browser tab updates in real-time with your target stock's live price. |

---

## 🛠️ Technical Stack

### **Backend & AI**
![NodeJS](https://img.shields.io/badge/Node.js-EXPRESS-339933?style=flat-square&logo=node.js&logoColor=white)
![Express](https://img.shields.io/badge/Express-Middleware-000000?style=flat-square&logo=express&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Remote_Engine-009688?style=flat-square&logo=fastapi&logoColor=white)

### **Frontend**
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Lucide](https://img.shields.io/badge/Lucide-Icons-pink?style=flat-square)
![Framer](https://img.shields.io/badge/Framer_Motion-Animations-black?style=flat-square&logo=framer)
![Vite](https://img.shields.io/badge/Vite-Bundler-646CFF?style=flat-square&logo=vite&logoColor=white)

---

## 📂 Repository Structure

```text
TRADING-SOUT/
├── ⚛️ client/                # React Frontend
│   ├── src/                  # App Logic & Styles
│   │   ├── App.jsx           # Pro Dashboard Component
│   │   └── index.css         # Premium Glassmorphism Theme
│   ├── package.json          # Vite Configuration
│   └── vite.config.js        # Proxy Setup
│
├── 🐍 server/                # Node.js Backend
│   ├── index.js              # Express Proxy & Fallback Logic
│   └── package.json          # Server Dependencies
│
├── 📄 requirements.txt       # Python Logic (Sync with HF Space)
└── 📄 README.md              # Project Documentation
```

---

## ⚡ Getting Started Guide

### Prerequisites
* **Node.js 18+**
* **Active HF Space URL** (Already configured in code)

### Project Configuration

```bash
# Clone the repository
git clone https://github.com/UtkarshSingh-09/TRADING-UTSO.git
cd TRADING-UTSO

# 1. Setup Backend
cd server
npm install
npm start

# 2. Setup Frontend (New Terminal)
cd ../client
npm install
npm run dev
```

**Access app at http://localhost:5173**

---

## 🔌 API Proxy Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/analyze` | **Primary Entry.** Proxies to HF Space and injects local fallback messages. |
| `GET` | `.../get_chart` | **Dynamic Assets.** Automatically resolved absolute URL mapping. |

---

## 🛡️ Stability & Fallbacks

* **Remote Quota Error?**
    * *Behavior:* The backend catches `429` errors and returns a professional "Service Busy" message.
* **Connection Failed?**
    * *Behavior:* The frontend displays an immediate "Connection Failed" warning to the user.

---

<p align="center">
  <sub>Built with ❤️ by Utkarsh Singh</sub>
</p>
