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

  if (loading) return <div className="container mt-4"><div className="alert alert-info">Loading workouts...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Workout Suggestions</h2>
      <div className="row">
        {workouts.map((workout, index) => (
          <div key={workout._id || index} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">
                  {workout.title}
                  <span className={`badge bg-${getDifficultyBadge(workout.difficulty_level)} ms-2`}>
                    {workout.difficulty_level}
                  </span>
                </h5>
                <p className="card-text">
                  <strong>Description:</strong> {workout.description}<br />
                  <strong>Type:</strong> {workout.activity_type}<br />
                  <strong>Duration:</strong> {workout.duration} minutes
                </p>
                {workout.instructions && (
                  <div className="mt-2">
                    <strong>Instructions:</strong>
                    <pre className="mt-2 p-2 bg-light rounded" style={{whiteSpace: 'pre-wrap'}}>
                      {workout.instructions}
                    </pre>
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

export default Workouts;
