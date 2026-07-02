import React from "react";

function JobManager({
  jobs,
  form,
  handleChange,
  createJob,
  analyzeJob,
  createApplication,
}) {
  return (
    <section>
      <h2>Job Manager</h2>

      {jobs.length === 0 && <p>No jobs saved yet.</p>}

      {jobs.map((job) => (
        <div key={job.id}>
          <h3>{job.title}</h3>
          <p>{job.company}</p>
          <p>{job.location}</p>
          <p>Match Score: {job.match_score ?? "Not analyzed"}</p>

          <button onClick={() => analyzeJob(job.id)}>Analyze Again</button>
          <button onClick={() => createApplication(job.id)}>
            Add to Application Tracker
          </button>

          <button
            onClick={() => {
              if (window.confirm("Delete this job?")) {
                alert("Delete function coming next.");
              }
            }}
          >
            Delete
          </button>
        </div>
      ))}

      <h3>Add Job</h3>

      <form onSubmit={createJob}>
        <input name="company" placeholder="Company" value={form.company} onChange={handleChange} />
        <input name="title" placeholder="Job title" value={form.title} onChange={handleChange} />
        <input name="location" placeholder="Location" value={form.location} onChange={handleChange} />
        <input name="job_url" placeholder="Job URL" value={form.job_url} onChange={handleChange} />
        <textarea name="description" placeholder="Job description" value={form.description} onChange={handleChange} rows="6" />
        <button type="submit">Save Job</button>
      </form>
    </section>
  );
}

export default JobManager;