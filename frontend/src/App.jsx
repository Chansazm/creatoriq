
import React, { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8001";

const formatCurrency = (value) =>
  new Intl.NumberFormat("en-US", {
    currency: "USD",
    maximumFractionDigits: 2,
    style: "currency",
  }).format(value);

const formatNumber = (value) => new Intl.NumberFormat("en-US").format(value);

function App() {
  const [creatorId, setCreatorId] = useState("123");
  const [draftCreatorId, setDraftCreatorId] = useState("123");
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    setError("");

    fetch(`${API_BASE_URL}/analytics/cpm/${creatorId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Request failed with status ${res.status}`);
        }
        return res.json();
      })
      .then(setData)
      .catch((err) => {
        setData(null);
        setError(err.message);
      })
      .finally(() => setIsLoading(false));
  }, [creatorId]);

  const updateCreator = (event) => {
    event.preventDefault();
    setCreatorId(draftCreatorId.trim() || "123");
  };

  return (
    <div className="app-shell">
      <main className="dashboard">
        <header className="topbar">
          <div>
            <p className="eyebrow">CreatorIQ Analytics</p>
            <h1>Creator performance dashboard</h1>
          </div>

          <form className="creator-switcher" onSubmit={updateCreator}>
            <label htmlFor="creator-id">Creator ID</label>
            <input
              id="creator-id"
              value={draftCreatorId}
              onChange={(event) => setDraftCreatorId(event.target.value)}
            />
            <button type="submit">Load</button>
          </form>
        </header>

        {isLoading && <div className="loading">Loading creator metrics...</div>}
        {error && <div className="error">Unable to load creator metrics: {error}</div>}

        {data && !isLoading && (
          <>
            <section className="summary" aria-label="Creator summary">
              <div className="primary-metric">
                <p className="label">CPM</p>
                <p className="value primary-value">{formatCurrency(data.cpm)}</p>
                <p className="meta">{data.creator_name} · Creator {data.creator}</p>
              </div>

              <div>
                <p className="label">Spend</p>
                <p className="value">{formatCurrency(data.total_spend_usd)}</p>
              </div>

              <div>
                <p className="label">Impressions</p>
                <p className="value">{formatNumber(data.total_impressions)}</p>
              </div>

              <div>
                <p className="label">Campaigns</p>
                <p className="value">{formatNumber(data.campaign_count)}</p>
              </div>
            </section>

            <section className="panel">
              <div className="panel-header">
                <h2>Data source</h2>
                <span className="status-pill">
                  {data.source === "remote_api" ? "Live API" : "Local fallback"}
                </span>
              </div>

              <div className="detail-grid">
                <div className="detail-item">
                  <p className="label">Formula</p>
                  <p className="meta">Spend divided by impressions, multiplied by 1,000.</p>
                </div>
                <div className="detail-item">
                  <p className="label">Endpoint</p>
                  <p className="meta">/analytics/cpm/{data.creator}</p>
                </div>
                <div className="detail-item">
                  <p className="label">Source mode</p>
                  <p className="meta">{data.source}</p>
                </div>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}
export default App;
