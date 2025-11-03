import React, { useState, useEffect } from "react";
import axios from "axios";
import AddSponsorForm from "./AddSponsorForm";
import "./EntityTable.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function SponsorsTable() {
  const [sponsors, setSponsors] = useState([]);
  const [search, setSearch] = useState("");
  const [address, setAddress] = useState("All Locations");
  const [showAdd, setShowAdd] = useState(false);
  const [editingSponsor, setEditingSponsor] = useState(null);

  useEffect(() => {
    fetchSponsors();
  }, []);

  function fetchSponsors() {
    axios.get(`${API_BASE}/show-sponsors/`)
      .then(res => setSponsors(res.data.sponsors || []));
  }

  function handleAddSponsor(data) {
    axios.post(`${API_BASE}/add-sponsor/`, data)
      .then(() => fetchSponsors());
  }

  function handleUpdateSponsor(id, data) {
    axios.put(`${API_BASE}/update-sponsor/${id}/`, data)
      .then(() => fetchSponsors());
  }

  function handleDeleteSponsor(id) {
    if (!window.confirm("Delete this sponsor?")) return;
    axios.delete(`${API_BASE}/delete-sponsor/${id}/`)
      .then(() => fetchSponsors());
  }

  // Defensive filtering: check for existence before calling string methods!
  const filtered = sponsors.filter(
    s =>
      (
        (s.organization_name && s.organization_name.toLowerCase().includes(search.toLowerCase())) ||
        (s.contact_person && s.contact_person.toLowerCase().includes(search.toLowerCase())) ||
        (s.sponsor_id && String(s.sponsor_id).toLowerCase().includes(search.toLowerCase()))
      ) &&
      (address === "All Locations" || (s.address === address))
  );

  const addressOptions = [
    "All Locations",
    ...Array.from(new Set(sponsors.map(s => s.address).filter(Boolean)))
  ];

  return (
    <div className="entity-table-container">
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search by organization, contact person, or ID..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="search-field"
        />
        <div className="search-filters">
          <div>
            <label className="filter-label">Address</label>
            <select value={address} onChange={e => setAddress(e.target.value)}>
              {addressOptions.map(opt => (
                <option key={opt}>{opt}</option>
              ))}
            </select>
          </div>
        </div>
        <button className="export-btn">Export</button>
        <button className="list-btn">
          <span role="img" aria-label="table">&#9776;</span>
        </button>
      </div>
      <div className="entity-header">
        <h2>Sponsors</h2>
        <button className="primary-btn" onClick={() => setShowAdd(true)}>
          + Add Sponsor
        </button>
      </div>
      <table className="entity-table">
        <thead>
          <tr>
            <th>Sponsor ID</th>
            <th>Organization Name</th>
            <th>Contact Person</th>
            <th>Contact</th>
            <th>Email</th>
            <th>Address</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(s => (
            <tr key={s.sponsor_id}>
              <td>{s.sponsor_id}</td>
              <td>{s.organization_name}</td>
              <td>{s.contact_person}</td>
              <td>{s.contact}</td>
              <td>{s.email}</td>
              <td>{s.address}</td>
              <td>
                <button className="primary-btn" onClick={() => setEditingSponsor(s)}>Edit</button>
                <button className="export-btn" style={{ marginLeft: 8 }} onClick={() => handleDeleteSponsor(s.sponsor_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showAdd && (
        <AddSponsorForm
          onClose={() => setShowAdd(false)}
          onSave={data => {
            handleAddSponsor(data);
            setShowAdd(false);
          }}
        />
      )}
      {editingSponsor && (
        <AddSponsorForm
          mode="edit"
          initialData={editingSponsor}
          onClose={() => setEditingSponsor(null)}
          onSave={data => {
            handleUpdateSponsor(editingSponsor.sponsor_id, data);
            setEditingSponsor(null);
          }}
        />
      )}
    </div>
  );
}
