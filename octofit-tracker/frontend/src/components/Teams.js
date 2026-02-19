import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Build API URL using environment variable or localhost fallback
  const getApiUrl = () => {
    const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
    if (codespaceName) {
      return `https://${codespaceName}-8000.app.github.dev/api/teams/`;
    }
    return 'http://localhost:8000/api/teams/';
  };

  useEffect(() => {
    const apiUrl = getApiUrl();
    console.log('Teams Component - Fetching from API:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams Component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams Component - Processed teams:', teamsData);
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><div className="alert alert-info"><i className="bi bi-hourglass-split"></i> Loading teams...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger"><i className="bi bi-exclamation-triangle"></i> Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">👥 OctoFit Teams</h2>
        <span className="badge bg-info">{teams.length} Teams</span>
      </div>
      
      <div className="row">
        {teams.map((team, index) => (
          <div key={team._id || index} className="col-lg-6 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="card-title mb-0">{team.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text text-muted">{team.description}</p>
                <ul className="list-group list-group-flush">
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <strong>Captain:</strong>
                    <span className="badge bg-warning text-dark">{team.captain?.username || 'N/A'}</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <strong>Members:</strong>
                    <span className="badge bg-info">{team.member_count || team.members?.length || 0}</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between align-items-center">
                    <strong>Total Points:</strong>
                    <span className="badge bg-success">{team.total_points} pts</span>
                  </li>
                </ul>
                {team.members && team.members.length > 0 && (
                  <div className="mt-3">
                    <h6 className="text-muted">Team Members:</h6>
                    <div className="d-flex flex-wrap gap-2">
                      {team.members.map(member => (
                        <span key={member.id} className="badge bg-secondary">{member.username}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Teams;
