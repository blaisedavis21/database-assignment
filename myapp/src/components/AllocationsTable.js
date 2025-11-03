import React, { useState, useEffect } from "react";
import axios from "axios";
import AddAllocationForm from "./AddAllocationForm";
import "./EntityTable.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function AllocationsTable() {
  const [allocations, setAllocations] = useState([]);
  const [search, setSearch] = useState("");
  const [status, setStatus] = useState("All");
  const [showAdd, setShowAdd] = useState(false);
  const [editingAllocation, setEditingAllocation] = useState(null);

  useEffect(() => {
    fetchAllocations();
  }, []);

  function fetchAllocations() {
    axios.get(`${API_BASE}/show-allocations/`)
      .then(res => setAllocations(res.data.sponsorship_allocations || []));
  }

  function handleAddAllocation(data) {
    axios.post(`${API_BASE}/add-allocation/`, data)
      .then(() => fetchAllocations());
  }

  function handleUpdateAllocation(id, data) {
    axios.put(`${API_BASE}/update-allocation/${id}/`, data)
      .then(() => fetchAllocations());
  }

  function handleDeleteAllocation(id) {
    if (!window.confirm("Delete this allocation?")) return;
    axios.delete(`${API_BASE}/delete-allocation/${id}/`)
      .then(() => fetchAllocations());
  }

  const filtered = allocations.filter(
    a =>
      (
        (a.allocation_id && String(a.allocation_id).toLowerCase().includes(search.toLowerCase())) ||
        (a.student_id && String(a.student_id).toLowerCase().includes(search.toLowerCase())) ||
        (a.program_id && String(a.program_id).toLowerCase().includes(search.toLowerCase()))
      ) &&
      (status === "All" || a.status === status)
  );

  return (
    <div className="entity-table-container">
      <div className="search-bar">
        <input type="text" placeholder="Search by allocation ID, student ID, or program ID..." value={search} onChange={e => setSearch(e.target.value)} className="search-field"/>
        <div className="search-filters">
          <div>
            <label className="filter-label">Status</label>
            <select value={status} onChange={e => setStatus(e.target.value)}>
              <option>All</option>
              <option>Active</option>
              <option>Inactive</option>
            </select>
          </div>
        </div>
        <button className="export-btn">Export</button>
        <button className="list-btn"><span role="img" aria-label="table">&#9776;</span></button>
      </div>
      <div className="entity-header">
        <h2>Sponsorship Allocations</h2>
        <button className="primary-btn" onClick={() => setShowAdd(true)}>
          + Add Allocation
        </button>
      </div>
      <table className="entity-table">
        <thead>
          <tr>
            <th>Allocation ID</th>
            <th>Student ID</th>
            <th>Program ID</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(a => (
            <tr key={a.allocation_id}>
              <td>{a.allocation_id}</td>
              <td>{a.student_id}</td>
              <td>{a.program_id}</td>
              <td>{a.start_date}</td>
              <td>{a.end_date}</td>
              <td>{a.status}</td>
              <td>
                <button className="primary-btn" onClick={() => setEditingAllocation(a)}>Edit</button>
                <button className="export-btn" style={{ marginLeft: 8 }} onClick={() => handleDeleteAllocation(a.allocation_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showAdd && (
        <AddAllocationForm
          onClose={() => setShowAdd(false)}
          onSave={data => {
            handleAddAllocation(data);
            setShowAdd(false);
          }}
        />
      )}
      {editingAllocation && (
        <AddAllocationForm
          mode="edit"
          initialData={editingAllocation}
          onClose={() => setEditingAllocation(null)}
          onSave={data => {
            handleUpdateAllocation(editingAllocation.allocation_id, data);
            setEditingAllocation(null);
          }}
        />
      )}
    </div>
  );
}
