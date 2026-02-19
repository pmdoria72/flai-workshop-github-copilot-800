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

  if (loading) return <div className="container mt-4"><div className="alert alert-info">Loading teams...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">OctoFit Teams</h2>
      <div className="row">
        {teams.map((team, index) => (
          <div key={team._id || index} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{team.name}</h5>
                <p className="card-text">
                  <strong>Description:</strong> {team.description}<br />
                  <strong>Captain:</strong> {team.captain?.username || 'N/A'}<br />
                  <strong>Members:</strong> {team.member_count || team.members?.length || 0}<br />
                  <strong>Total Points:</strong> {team.total_points}
                </p>
                {team.members && team.members.length > 0 && (
                  <div className="mt-2">
                    <strong>Team Members:</strong>
                    <ul className="list-unstyled ms-3">
                      {team.members.map(member => (
                        <li key={member.id}>• {member.username}</li>
                      ))}
                    </ul>
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
