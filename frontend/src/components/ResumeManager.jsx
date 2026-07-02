import React from "react";

function ResumeManager({
  resumes,
  resumeFile,
  setResumeFile,
  uploadResume,
  extractResume,
  extractions,
}) {
  return (
    <section>
      <h2>Resume Manager</h2>

      {resumes.length === 0 && <p>No resumes uploaded yet.</p>}

      {resumes.map((resume) => (
        <div key={resume.id}>
          <h4>{resume.filename}</h4>
          <p>Status: Uploaded</p>
          <p>
            AI Extraction:{" "}
            {extractions[resume.id] ? "Extracted" : "Not extracted"}
          </p>

          <button onClick={() => extractResume(resume.id)}>
            {extractions[resume.id] ? "View Extracted Profile" : "Extract Profile with AI"}
          </button>

          <button
            onClick={() => {
              if (window.confirm("Delete this resume?")) {
                alert("Delete function coming next.");
              }
            }}
          >
            Delete
          </button>
        </div>
      ))}

      <form onSubmit={uploadResume}>
        <input
          type="file"
          accept=".pdf,.txt"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />
        <button type="submit">Upload Resume</button>
      </form>
    </section>
  );
}

export default ResumeManager;