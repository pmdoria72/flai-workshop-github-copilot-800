import React, { useState, useEffect } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Build API URL using environment variable or localhost fallback
  const getApiUrl = () => {
    const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
    if (codespaceName) {
      return `https://${codespaceName}-8000.app.github.dev/api/activities/`;
    }
    return 'http://localhost:8000/api/activities/';
  };

  useEffect(() => {
    const apiUrl = getApiUrl();
    console.log('Activities Component - Fetching from API:', apiUrl);

    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities Component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Activities Component - Processed activities:', activitiesData);
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Activities Component - Error fetching activities:', error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-4"><div className="alert alert-info"><i className="bi bi-hourglass-split"></i> Loading activities...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger"><i className="bi bi-exclamation-triangle"></i> Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2 className="mb-0">📊 Recent Activities</h2>
        <span className="badge bg-success">{activities.length} Activities</span>
      </div>
      
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th>User</th>
              <th>Activity Type</th>
              <th>Duration</th>
              <th>Distance</th>
              <th>Calories</th>
              <th>Points</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity, index) => (
              <tr key={activity._id || index}>
                <td><strong>{activity.user?.username || 'Unknown'}</strong></td>
                <td>
                  <span className="badge bg-info">
                    {activity.activity_type.charAt(0).toUpperCase() + activity.activity_type.slice(1)}
                  </span>
                </td>
                <td>{activity.duration} min</td>
                <td>{activity.distance ? `${activity.distance} km` : 'N/A'}</td>
                <td>{activity.calories_burned} cal</td>
                <td><span className="badge bg-warning text-dark">{activity.points_earned} pts</span></td>
                <td>{new Date(activity.date).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Activities;
