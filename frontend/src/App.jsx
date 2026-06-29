
//import api from "./services/api";

import { useEffect, useState } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

import Dashboard from "./components/Dashboard";
import ApplicationCard from "./components/ApplicationCard";

function App() {
  const [jobs, setJobs] = useState([]);
  const [applications, setApplications] = useState([]);
  const [resumes, setResumes] = useState([]);
  const [resumeFile, setResumeFile] = useState(null);
  const [extractions, setExtractions] = useState({});

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

  const loadApplications = async () => {
    const res = await axios.get(`${API_URL}/applications/`);
    setApplications(res.data);
  };

  const loadResumes = async () => {
    const res = await axios.get(`${API_URL}/resumes/`);
    setResumes(res.data);
  };

  const uploadResume = async (e) => {
    e.preventDefault();

    if (!resumeFile) {
      alert("Please choose a resume file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", resumeFile);

    await axios.post(`${API_URL}/resumes/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    setResumeFile(null);
    loadResumes();
  };

  const extractResume = async (resumeId) => {
    const res = await axios.post(`${API_URL}/resumes/${resumeId}/extract`);

    setExtractions({
      ...extractions,
      [resumeId]: res.data.extraction_json,
    });
  };

 

  useEffect(() => {
    loadJobs();
    loadApplications();
    loadResumes();
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

  const createApplication = async (jobId) => {
    await axios.post(`${API_URL}/applications/`, {
      job_id: jobId,
      status: "interested",
      next_action: "Tailor resume and apply",
      notes: "Created from saved job.",
    });

    loadApplications();
  };

  const updateApplicationStatus = async (applicationId, status) => {
    await axios.patch(`${API_URL}/applications/${applicationId}`, {
      status,
    });

    loadApplications();
  };

  return (
    <div style={{ padding: "32px", fontFamily: "Arial" }}>
      <h1>AI Career Agent</h1>
      <Dashboard jobs={jobs} applications={applications} />
      <p>
        Full-stack AI job search, RAG matching, and application tracking system.
      </p>

      <hr />

          

      <h2>Resume Upload</h2>

      <form
        onSubmit={uploadResume}
        style={{
          display: "grid",
          gap: "8px",
          maxWidth: "600px",
          marginBottom: "32px",
        }}
      >
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />

        <button type="submit">Upload Resume</button>
      </form>

      <h3>Uploaded Resumes</h3>

      {resumes.length === 0 && <p>No resumes uploaded yet.</p>}

      {resumes.map((resume) => (
        <div
          key={resume.id}
          style={{
            border: "1px solid #ddd",
            padding: "16px",
            marginBottom: "12px",
            borderRadius: "8px",
          }}
        >
          <h4>{resume.filename}</h4>
          <p>
            <strong>Resume ID:</strong> {resume.id}
          </p>
          <p>
            <strong>Extracted Text Preview:</strong>{" "}
            {(resume.parsed_text || "").slice(0, 300)}
            {(resume.parsed_text || "").length > 300 ? "..." : ""}
          </p>

          <button onClick={() => extractResume(resume.id)}>
            Extract Profile with AI
          </button>

          {extractions[resume.id] && (
            <div style={{ marginTop: "12px", background: "#f5f5f5", padding: "12px" }}>
              <h4>AI Extracted Profile</h4>

              <p>
                <strong>Name:</strong> {extractions[resume.id].name}
              </p>

              <p>
                <strong>Summary:</strong> {extractions[resume.id].summary}
              </p>

              <p>
                <strong>Target Roles:</strong>{" "}
                {(extractions[resume.id].target_roles || []).join(", ")}
              </p>

              <p>
                <strong>Technical Skills:</strong>{" "}
                {(extractions[resume.id].technical_skills || []).join(", ")}
              </p>

              <p>
                <strong>Domain Skills:</strong>{" "}
                {(extractions[resume.id].domain_skills || []).join(", ")}
              </p>

              <h5>Projects</h5>
              {(extractions[resume.id].projects || []).map((project, index) => (
                <div key={index}>
                  <strong>{project.name}</strong>
                  <p>{project.description}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}

        <hr />

      <h2>Add Job</h2>

      <form
        onSubmit={createJob}
        style={{
          display: "grid",
          gap: "8px",
          maxWidth: "600px",
          marginBottom: "32px",
        }}
      >
        <input
          name="company"
          placeholder="Company"
          value={form.company}
          onChange={handleChange}
        />

        <input
          name="title"
          placeholder="Job title"
          value={form.title}
          onChange={handleChange}
        />

        <input
          name="location"
          placeholder="Location"
          value={form.location}
          onChange={handleChange}
        />

        <input
          name="job_url"
          placeholder="Job URL"
          value={form.job_url}
          onChange={handleChange}
        />

        <textarea
          name="description"
          placeholder="Job description"
          value={form.description}
          onChange={handleChange}
          rows="6"
        />

        <button type="submit">Save Job</button>
      </form>

      <hr />

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

          <p>
            <strong>Company:</strong> {job.company}
          </p>

          <p>
            <strong>Location:</strong> {job.location}
          </p>

          <p>
            <strong>Status:</strong> {job.status}
          </p>

          <p>
            <strong>Match Score:</strong>{" "}
            {job.match_score ?? "Not analyzed"}
          </p>

          {job.job_url && (
            <p>
              <a href={job.job_url} target="_blank" rel="noreferrer">
                Open Job Link
              </a>
            </p>
          )}

          <button onClick={() => analyzeJob(job.id)}>
            Analyze Match
          </button>

          <button
            onClick={() => createApplication(job.id)}
            style={{ marginLeft: "8px" }}
          >
            Add to Application Tracker
          </button>
        </div>
      ))}

      <hr />

      <h2>Application Tracker</h2>

      {applications.length === 0 && <p>No applications yet.</p>}

      {applications.map((application) => (
        <ApplicationCard
          key={application.id}
          application={application}
          onStatusChange={updateApplicationStatus}
        />
      ))}

      <div><p>done</p></div>

      

          
       
    </div>

           
          
  );
}

export default App;