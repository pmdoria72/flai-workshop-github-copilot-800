import React, { useState, useEffect } from 'react';

const Workouts = () => {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Build API URL using environment variable or localhost fallback
  const getApiUrl = () => {
    const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
    if (codespaceName) {
      return `https://${codespaceName}-8000.app.github.dev/api/workouts/`;
    }
    return 'http://localhost:8000/api/workouts/';
  };

  useEffect(() => {
    const apiUrl = getApiUrl();
    console.log('Workouts Component - Fetching from API:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed workouts:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error fetching workouts:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const getDifficultyBadge = (level) => {
    const badges = {
      beginner: 'success',
      intermediate: 'warning',
      advanced: 'danger'
    };
    return badges[level] || 'secondary';
  };

  if (loading) return <div className="container mt-4"><div className="alert alert-info"><i className="bi bi-hourglass-split"></i> Loading workouts...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger"><i className="bi bi-exclamation-triangle"></i> Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">💪 Workout Suggestions</h2>
        <span className="badge bg-warning text-dark">{workouts.length} Workouts</span>
      </div>
      
      <div className="row">
        {workouts.map((workout, index) => (
          <div key={workout._id || index} className="col-lg-6 mb-4">
            <div className="card h-100">
              <div className="card-header d-flex justify-content-between align-items-center">
                <h5 className="card-title mb-0">{workout.title}</h5>
                <span className={`badge bg-${getDifficultyBadge(workout.difficulty_level)}`}>
                  {workout.difficulty_level.toUpperCase()}
                </span>
              </div>
              <div className="card-body">
                <p className="card-text text-muted">{workout.description}</p>
                <ul className="list-group list-group-flush mb-3">
                  <li className="list-group-item d-flex justify-content-between">
                    <strong>Type:</strong>
                    <span className="badge bg-info">{workout.activity_type}</span>
                  </li>
                  <li className="list-group-item d-flex justify-content-between">
                    <strong>Duration:</strong>
                    <span className="badge bg-primary">{workout.duration} min</span>
                  </li>
                </ul>
                {workout.instructions && (
                  <div>
                    <h6 className="text-muted">Instructions:</h6>
                    <pre className="bg-light p-3 rounded border" style={{whiteSpace: 'pre-wrap', fontSize: '0.9rem'}}>
                      {workout.instructions}
                    </pre>
                  </div>
                )}
              </div>
              <div className="card-footer bg-transparent">
                <button className="btn btn-primary btn-sm w-100">Start Workout</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Workouts;
