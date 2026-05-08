
import React, { useEffect, useState } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8001";

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${API_BASE_URL}/analytics/cpm/123`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Request failed with status ${res.status}`);
        }
        return res.json();
      })
      .then(setData)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <h1>CreatorIQ Dashboard</h1>
      {error && <p>Unable to load CPM data: {error}</p>}
      {data && <p>CPM: {data.cpm}</p>}
    </div>
  );
}
export default App;
