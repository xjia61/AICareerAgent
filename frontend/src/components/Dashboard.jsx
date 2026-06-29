import React from "react";
import "./Dashboard.css";

function Dashboard({ jobs = [], applications = [] }) {
  const totalJobs = jobs.length;
  const totalApplications = applications.length;

  const interviewCount = applications.filter(
    (app) => app.status === "interview"
  ).length;

  const offerCount = applications.filter(
    (app) => app.status === "offer"
  ).length;

  const rejectedCount = applications.filter(
    (app) => app.status === "rejected"
  ).length;

  return (
    <section className="dashboard">
      <h2>Dashboard</h2>

      <div className="dashboard-grid">
        <div className="dashboard-card">
          <span>Total Jobs</span>
          <strong>{totalJobs}</strong>
        </div>

        <div className="dashboard-card">
          <span>Applications</span>
          <strong>{totalApplications}</strong>
        </div>

        <div className="dashboard-card">
          <span>Interview</span>
          <strong>{interviewCount}</strong>
        </div>

        <div className="dashboard-card">
          <span>Offer</span>
          <strong>{offerCount}</strong>
        </div>

        <div className="dashboard-card">
          <span>Rejected</span>
          <strong>{rejectedCount}</strong>
        </div>
      </div>
    </section>
  );
}

export default Dashboard;


