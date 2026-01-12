import { useState, useEffect } from 'react'
import axios from 'axios'
import { Search, TrendingUp, Activity, BarChart2, Globe } from 'lucide-react'
import './index.css'

function App() {
  const [ticker, setTicker] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null); // Changed from '' to null

  const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:3000";

  // Dynamic Title Update
  useEffect(() => {
    if (result && result.current_price) {
      document.title = `${result.stock_symbol} $${result.current_price.toFixed(2)} | TRADING UTSO`
    } else {
      document.title = 'TRADING UTSO'
    }
  }, [result])

  const handleAnalyze = async (e) => {
    e.preventDefault()
    if (!ticker) return
    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/api/analyze`, { ticker })
      if (response.data.error) {
        setError(response.data.error)
        setResult(null)
      } else {
        setResult(response.data)
      }
    } catch (err) {
      console.error(err)
      setError('Connection Failed. Is backend running?')
    } finally {
      setLoading(false)
    }
  }

  // Determine flash color class
  const getFlashClass = (change) => {
    if (!result) return ''
    return change >= 0 ? 'flash-up' : 'flash-down'
  }

  const isPositive = result?.price_change_percent >= 0

  return (
    <div className="dashboard-container">

      {/* 0. START SCREEN (If no result) */}
      {!result && (
        <div className="search-overlay">
          <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>TRADING <span style={{ color: 'var(--accent-primary)' }}>UTSO</span></h1>
          <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Institutional Grade Anomaly Detection</p>

          <form onSubmit={handleAnalyze} style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div className="input-group">
              <Search style={{ position: 'absolute', left: '1rem', top: '1.25rem', color: '#666' }} />
              <input
                autoFocus
                type="text"
                placeholder="SEARCH TICKER (e.g. AAPL)"
                value={ticker}
                onChange={e => setTicker(e.target.value.toUpperCase())}
              />
            </div>
            <button className="search-btn" disabled={loading}>
              {loading ? <div className="spinner" style={{ margin: '0 auto' }} /> : 'INITIALIZE SCAN'}
            </button>
          </form>

          {error && <div style={{ color: 'var(--danger)', marginTop: '1rem' }}>{error}</div>}
        </div>
      )}

      {/* 1. PRO DASHBOARD (If result exists) */}
      {result && (
        <div className="pro-dashboard">

          {/* HEADER (IDENTITY) */}
          <div className="header-card">
            <div className="stock-identity">
              <h1>{result.stock_symbol} <span className="stock-badge">NASDAQ</span></h1>
            </div>

            <div className="price-display">
              <div key={result.current_price} className={`current-price ${getFlashClass(result.price_change_percent)}`}>
                ${result.current_price ? result.current_price.toFixed(2) : '---'}
              </div>
              <div className="price-change" style={{
                background: isPositive ? 'var(--success-bg)' : 'var(--danger-bg)',
                color: isPositive ? 'var(--success)' : 'var(--danger)'
              }}>
                {isPositive ? '+' : ''}{result.price_change_percent}%
              </div>
            </div>
          </div>

          {/* HERO CHART (THE STORY) */}
          <div className="chart-card">
            {result.chart_url ? (
              <img src={result.chart_url} alt="Chart" />
            ) : (
              <div style={{ color: '#444' }}>NO CHART DATA</div>
            )}

            {/* Overlay Status */}
            <div style={{
              position: 'absolute', top: '1rem', left: '1rem',
              padding: '0.5rem 1rem', background: 'rgba(0,0,0,0.6)',
              borderRadius: '8px', backdropFilter: 'blur(4px)',
              border: `1px solid ${result.status === 'stable' ? 'var(--success)' : 'var(--danger)'}`,
              color: result.status === 'stable' ? 'var(--success)' : 'var(--danger)',
              fontWeight: 'bold', textTransform: 'uppercase', fontSize: '0.8rem'
            }}>
              {result.status === 'stable' ? 'System Stable' : 'Anomaly Detected'}
            </div>
          </div>

          {/* SIDEBAR STATS (THE VITALS) */}
          <div className="stats-sidebar">
            <div className="stat-card">
              <div className="stat-label flex items-center gap-2"><Activity size={14} /> Status</div>
              <div className="stat-value" style={{ color: result.status === 'stable' ? 'var(--success)' : 'var(--danger)' }}>
                {result.status.toUpperCase()}
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-label flex items-center gap-2"><Globe size={14} /> Sentiment</div>
              <div className="stat-value">Mixed</div> {/* Placeholder until backend provides */}
            </div>

            {/* New Analysis Box (Moved to sidebar/bottom right) */}
            <div className={`narrative-card ${result.ai_explanation?.includes('429') || result.ai_explanation?.includes('Quota exceeded') ? 'error-card' : ''}`}>
              <div className="stat-label flex items-center gap-2" style={{ color: result.ai_explanation?.includes('429') ? 'var(--danger)' : 'var(--accent-primary)', marginBottom: '0.8rem' }}>
                {result.ai_explanation?.includes('429') ? <Activity size={14} /> : <TrendingUp size={14} />}
                {result.ai_explanation?.includes('429') ? 'Service Busy' : 'AI Insight'}
              </div>
              <p style={{ fontSize: '0.95rem', lineHeight: '1.6', color: '#ddd' }}>
                {result.ai_explanation?.includes('429') || result.ai_explanation?.includes('Quota exceeded')
                  ? "High traffic detected. The AI analysis quota has been temporarily exceeded. Please try again in 60 seconds."
                  : (result.ai_explanation || "No narrative available.")
                }
              </p>
            </div>
          </div>

          {/* NEWS FEED (Bottom Right) */}
          <div className="info-section">
            <div className="stat-label">HEADLINES</div>
            {result.news_context?.slice(0, 3).map((news, i) => (
              <div key={i} className="news-item">
                {news}
              </div>
            ))}

            <button
              onClick={() => setResult(null)}
              style={{ background: 'transparent', border: '1px solid #333', color: '#666', padding: '0.8rem', borderRadius: '8px', cursor: 'pointer', marginTop: '1rem' }}
            >
              NEW SEARCH
            </button>
          </div>

        </div>
      )}
    </div>
  )
}

export default App
