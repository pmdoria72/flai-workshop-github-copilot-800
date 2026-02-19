import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Activities from './components/Activities';
import Teams from './components/Teams';
import Workouts from './components/Workouts';
import Leaderboard from './components/Leaderboard';

function Home() {
  return (
    <div className="container mt-5">
      <div className="jumbotron p-5 rounded text-center">
        <h1 className="display-3 mb-4">Welcome to OctoFit Tracker! 🏃‍♂️</h1>
        <p className="lead mb-4">Track your fitness journey, compete with teams, and achieve your goals!</p>
        <hr className="my-4" />
        <p className="mb-4">Use the navigation menu above to explore different sections of the app.</p>
        
        <div className="row g-4 mt-4">
          <div className="col-md-6 col-lg-3">
            <Link to="/users" className="text-decoration-none">
              <div className="card text-center h-100 border-primary">
                <div className="card-body">
                  <div className="display-4 mb-3">👥</div>
                  <h5 className="card-title">Users</h5>
                  <p className="card-text text-muted">View all registered users</p>
                  <button className="btn btn-primary btn-sm">View Users</button>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-6 col-lg-3">
            <Link to="/activities" className="text-decoration-none">
              <div className="card text-center h-100 border-success">
                <div className="card-body">
                  <div className="display-4 mb-3">📊</div>
                  <h5 className="card-title">Activities</h5>
                  <p className="card-text text-muted">Log and track activities</p>
                  <button className="btn btn-success btn-sm">View Activities</button>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-6 col-lg-3">
            <Link to="/teams" className="text-decoration-none">
              <div className="card text-center h-100 border-info">
                <div className="card-body">
                  <div className="display-4 mb-3">🤝</div>
                  <h5 className="card-title">Teams</h5>
                  <p className="card-text text-muted">Join and compete</p>
                  <button className="btn btn-info btn-sm">View Teams</button>
                </div>
              </div>
            </Link>
          </div>
          <div className="col-md-6 col-lg-3">
            <Link to="/leaderboard" className="text-decoration-none">
              <div className="card text-center h-100 border-danger">
                <div className="card-body">
                  <div className="display-4 mb-3">🏆</div>
                  <h5 className="card-title">Leaderboard</h5>
                  <p className="card-text text-muted">Top performers</p>
                  <button className="btn btn-danger btn-sm">View Rankings</button>
                </div>
              </div>
            </Link>
          </div>
        </div>
        
        <div className="row mt-5">
          <div className="col-md-12">
            <Link to="/workouts" className="text-decoration-none">
              <div className="card border-warning">
                <div className="card-body text-center">
                  <h4 className="card-title">💪 Workout Suggestions</h4>
                  <p className="card-text">Get personalized workout recommendations</p>
                  <button className="btn btn-warning">Explore Workouts</button>
                </div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              <strong>🏃 OctoFit Tracker</strong>
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">Home</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/users" element={<Users />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

