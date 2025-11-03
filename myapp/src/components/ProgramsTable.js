import React, { useState, useEffect } from "react";
import axios from "axios";
import AddScholarshipForm from "./AddScholarshipForm";
import "./EntityTable.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function ProgramsTable() {
  const [programs, setPrograms] = useState([]);
  const [search, setSearch] = useState("");
  const [duration, setDuration] = useState("All");
  const [showAdd, setShowAdd] = useState(false);
  const [editingProgram, setEditingProgram] = useState(null);

  useEffect(() => {
    fetchPrograms();
  }, []);

  function fetchPrograms() {
    axios.get(`${API_BASE}/show-programs/`)
      .then(res => setPrograms(res.data.scholarship_programs || []));
  }

  function handleAddProgram(data) {
    axios.post(`${API_BASE}/add-scholarship-program/`, data)
      .then(() => fetchPrograms());
  }

  function handleUpdateProgram(id, data) {
    axios.put(`${API_BASE}/update-scholarship-program/${id}/`, data)
      .then(() => fetchPrograms());
  }

  function handleDeleteProgram(id) {
    if (!window.confirm("Delete this program?")) return;
    axios.delete(`${API_BASE}/delete-scholarship-program/${id}/`)
      .then(() => fetchPrograms());
  }

  const filtered = programs.filter(
    p =>
      (
        (p.program_name && p.program_name.toLowerCase().includes(search.toLowerCase())) ||
        (p.program_id && String(p.program_id).toLowerCase().includes(search.toLowerCase())) ||
        (p.sponsor_id && String(p.sponsor_id).toLowerCase().includes(search.toLowerCase()))
      ) &&
      (duration === "All" || (p.duration === duration))
  );

  const durationOptions = ["All", ...Array.from(new Set(programs.map(p => p.duration).filter(Boolean)))];

  return (
    <div className="entity-table-container">
      <div className="search-bar">
        <input type="text" placeholder="Search by program name or ID..." value={search} onChange={e => setSearch(e.target.value)} className="search-field"/>
        <div className="search-filters">
          <div>
            <label className="filter-label">Duration</label>
            <select value={duration} onChange={e => setDuration(e.target.value)}>
              {durationOptions.map(opt => <option key={opt}>{opt}</option>)}
            </select>
          </div>
        </div>
        <button className="export-btn">Export</button>
        <button className="list-btn"><span role="img" aria-label="table">&#9776;</span></button>
      </div>
      <div className="entity-header">
        <h2>Scholarship Programs</h2>
        <button className="primary-btn" onClick={() => setShowAdd(true)}>
          + Add Scholarship
        </button>
      </div>
      <table className="entity-table">
        <thead>
          <tr>
            <th>Program ID</th>
            <th>Sponsor ID</th>
            <th>Program Name</th>
            <th>Amount per Student</th>
            <th>Duration</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(p => (
            <tr key={p.program_id}>
              <td>{p.program_id}</td>
              <td>{p.sponsor_id}</td>
              <td>{p.program_name}</td>
              <td>{p.amount_per_student}</td>
              <td>{p.duration}</td>
              <td>
                <button className="primary-btn" onClick={() => setEditingProgram(p)}>Edit</button>
                <button className="export-btn" style={{ marginLeft: 8 }} onClick={() => handleDeleteProgram(p.program_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showAdd && (
        <AddScholarshipForm
          onClose={() => setShowAdd(false)}
          onSave={data => {
            handleAddProgram(data);
            setShowAdd(false);
          }}
        />
      )}
      {editingProgram && (
        <AddScholarshipForm
          mode="edit"
          initialData={editingProgram}
          onClose={() => setEditingProgram(null)}
          onSave={data => {
            handleUpdateProgram(editingProgram.program_id, data);
            setEditingProgram(null);
          }}
        />
      )}
    </div>
  );
}
