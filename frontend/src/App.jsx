import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function App() {
  const [jobs, setJobs] = useState([]);
  const [form, setForm] = useState({
    company: "",
    title: "",
    location: "",
    job_url: "",
    description: "",
  });

  const loadJobs = async () => {
    const res = await axios.get(`${API_URL}/jobs/`);
    setJobs(res.data);
  };

  useEffect(() => {
    loadJobs();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const createJob = async (e) => {
    e.preventDefault();
    await axios.post(`${API_URL}/jobs/`, form);
    setForm({
      company: "",
      title: "",
      location: "",
      job_url: "",
      description: "",
    });
    loadJobs();
  };

  const analyzeJob = async (jobId) => {
    await axios.post(`${API_URL}/jobs/${jobId}/analyze`);
    loadJobs();
  };

  return (
    <div style={{ padding: "32px", fontFamily: "Arial" }}>
      <h1>AI Career Agent</h1>
      <p>Full-stack AI job search, RAG matching, and application tracking system.</p>

      <h2>Add Job</h2>
      <form onSubmit={createJob} style={{ display: "grid", gap: "8px", maxWidth: "600px" }}>
        <input name="company" placeholder="Company" value={form.company} onChange={handleChange} />
        <input name="title" placeholder="Job title" value={form.title} onChange={handleChange} />
        <input name="location" placeholder="Location" value={form.location} onChange={handleChange} />
        <input name="job_url" placeholder="Job URL" value={form.job_url} onChange={handleChange} />
        <textarea
          name="description"
          placeholder="Job description"
          value={form.description}
          onChange={handleChange}
          rows="6"
        />
        <button type="submit">Save Job</button>
      </form>

      <h2>Saved Jobs</h2>
      {jobs.map((job) => (
        <div
          key={job.id}
          style={{
            border: "1px solid #ddd",
            padding: "16px",
            marginBottom: "12px",
            borderRadius: "8px",
          }}
        >
          <h3>{job.title}</h3>
          <p><strong>Company:</strong> {job.company}</p>
          <p><strong>Location:</strong> {job.location}</p>
          <p><strong>Status:</strong> {job.status}</p>
          <p><strong>Match Score:</strong> {job.match_score ?? "Not analyzed"}</p>
          <button onClick={() => analyzeJob(job.id)}>Analyze Match</button>
        </div>
      ))}
    </div>
  );
}

export default App;