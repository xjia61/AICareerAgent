import React from "react";
import "./Dashboard.css";

function Dashboard({ jobs = [], applications = [] }) {
  const stats = [
    { label: "Total Jobs", value: jobs.length, icon: "💼" },
    { label: "Applications", value: applications.length, icon: "📬" },
    {
      label: "Interview",
      value: applications.filter((app) => app.status === "interview").length,
      icon: "🎤",
    },
    {
      label: "Offer",
      value: applications.filter((app) => app.status === "offer").length,
      icon: "🎉",
    },
    {
      label: "Rejected",
      value: applications.filter((app) => app.status === "rejected").length,
      icon: "❌",
    },
  ];

  return (
    <section className="dashboard">
      <div className="dashboard-header">
        <div>
          <h2>Dashboard</h2>
          <p>Track your job search progress in one place.</p>
        </div>
      </div>

      <div className="dashboard-grid">
        {stats.map((stat) => (
          <div className="dashboard-card" key={stat.label}>
            <div className="dashboard-icon">{stat.icon}</div>
            <div>
              <span>{stat.label}</span>
              <strong>{stat.value}</strong>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Dashboard;

