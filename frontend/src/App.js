
import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8001/analytics/cpm/123")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      <h1>CreatorIQ Dashboard</h1>
      {data && <p>CPM: {data.cpm}</p>}
    </div>
  );
}
export default App;
