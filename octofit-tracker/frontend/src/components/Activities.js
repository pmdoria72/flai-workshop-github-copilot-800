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

  if (loading) return <div className="container mt-4"><div className="alert alert-info">Loading activities...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Recent Activities</h2>
      <div className="row">
        {activities.map((activity, index) => (
          <div key={activity._id || index} className="col-md-6 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">
                  {activity.activity_type.charAt(0).toUpperCase() + activity.activity_type.slice(1)}
                </h5>
                <p className="card-text">
                  <strong>User:</strong> {activity.user?.username || 'Unknown'}<br />
                  <strong>Duration:</strong> {activity.duration} minutes<br />
                  {activity.distance && <><strong>Distance:</strong> {activity.distance} km<br /></>}
                  <strong>Calories:</strong> {activity.calories_burned} cal<br />
                  <strong>Points:</strong> {activity.points_earned}<br />
                  <strong>Date:</strong> {new Date(activity.date).toLocaleDateString()}<br />
                  {activity.notes && <><strong>Notes:</strong> {activity.notes}</>}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Activities;
