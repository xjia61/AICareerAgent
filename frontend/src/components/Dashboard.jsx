import React from "react";

function Dashboard({jobs = [], applications = []}){
    const totalJobs = jobs.length;
    
    const totalApplications = applications.length;

    const interviewCount = applications.filter(
        (app) => app.status ==="interview"
    ).length;
    const rejectedCount = applications.filter(
        (app) => app.status ==="rejected"
    ).length;

    const offerCount = applications.filter(
      (app) => app.status === "offer"
    ).length;

      return (
    <section>
      <h2>Dashboard</h2>

      <p>Total Jobs: {totalJobs}</p>
      <p>Applications: {totalApplications}</p>
      <p>Interview: {interviewCount}</p>
      <p>Offer: {offerCount}</p>
      <p>Rejected: {rejectedCount}</p>
    </section>
  );

}


export default Dashboard;