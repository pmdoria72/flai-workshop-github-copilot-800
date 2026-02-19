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

  const getRankIcon = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return '🏅';
  };

  if (loading) return <div className="container mt-4"><div className="alert alert-info"><i className="bi bi-hourglass-split"></i> Loading leaderboard...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger"><i className="bi bi-exclamation-triangle"></i> Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">🏆 Weekly Leaderboard</h2>
        <span className="badge bg-danger">{leaderboard.length} Competitors</span>
      </div>
      
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th width="8%">Rank</th>
              <th width="25%">User</th>
              <th width="20%">Team</th>
              <th width="12%">Points</th>
              <th width="15%">Calories</th>
              <th width="20%">Period</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.map((entry, index) => (
              <tr key={entry._id || index} className={entry.rank <= 3 ? 'table-warning' : ''}>
                <td>
                  <div className="d-flex align-items-center">
                    <span 
                      className="badge rounded-circle d-inline-flex align-items-center justify-content-center" 
                      style={{
                        backgroundColor: getRankColor(entry.rank), 
                        width: '45px', 
                        height: '45px',
                        fontSize: '1.1rem',
                        fontWeight: 'bold'
                      }}
                    >
                      #{entry.rank}
                    </span>
                    <span className="ms-2" style={{fontSize: '1.5rem'}}>{getRankIcon(entry.rank)}</span>
                  </div>
                </td>
                <td>
                  <div>
                    <strong className="d-block">{entry.user?.username || 'Unknown'}</strong>
                    <small className="text-muted">
                      {entry.user?.first_name} {entry.user?.last_name}
                    </small>
                  </div>
                </td>
                <td>
                  {entry.team ? (
                    <span className="badge bg-info">{entry.team.name}</span>
                  ) : (
                    <span className="text-muted">No Team</span>
                  )}
                </td>
                <td>
                  <span className="badge bg-primary fs-5 px-3 py-2">{entry.points.toLocaleString()} pts</span>
                </td>
                <td>
                  <span className="badge bg-danger">{entry.total_calories?.toLocaleString() || 0} cal</span>
                </td>
                <td>
                  <small className="text-muted">
                    <strong>Start:</strong> {new Date(entry.period_start).toLocaleDateString()}<br />
                    <strong>End:</strong> {new Date(entry.period_end).toLocaleDateString()}
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
