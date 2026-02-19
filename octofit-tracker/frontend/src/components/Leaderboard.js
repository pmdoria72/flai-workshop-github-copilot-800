import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Build API URL using environment variable or localhost fallback
  const getApiUrl = () => {
    const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
    if (codespaceName) {
      return `https://${codespaceName}-8000.app.github.dev/api/leaderboard/`;
    }
    return 'http://localhost:8000/api/leaderboard/';
  };

  useEffect(() => {
    const apiUrl = getApiUrl();
    console.log('Leaderboard Component - Fetching from API:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard Component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard Component - Processed leaderboard:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getRankColor = (rank) => {
    if (rank === 1) return '#FFD700';
    if (rank === 2) return '#C0C0C0';
    if (rank === 3) return '#CD7F32';
    return '#6c757d';
  };

  if (loading) return <div className="container mt-4"><div className="alert alert-info">Loading leaderboard...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Weekly Leaderboard</h2>
      <div className="table-responsive">
        <table className="table table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Points</th>
              <th>Period</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry._id || index}>
                <td>
                  <span 
                    className="badge rounded-circle p-2" 
                    style={{backgroundColor: getRankColor(entry.rank), minWidth: '40px'}}
                  >
                    #{entry.rank}
                  </span>
                </td>
                <td>
                  <strong>{entry.user?.username || 'Unknown'}</strong>
                  <br />
                  <small className="text-muted">
                    {entry.user?.first_name} {entry.user?.last_name}
                  </small>
                </td>
                <td>
                  <span className="badge bg-primary fs-6">{entry.points} pts</span>
                </td>
                <td>
                  <small>
                    {new Date(entry.period_start).toLocaleDateString()} - {new Date(entry.period_end).toLocaleDateString()}
                  </small>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
