import React, { useState, useEffect } from "react";
import "./StudentForm.css"; // Same modal CSS

export default function AddSponsorForm({ onClose, onSave, initialData, mode = "add" }) {
  const [form, setForm] = useState({
    sponsor_id: "",
    organization_name: "",
    contact_person: "",
    contact: "",
    email: "",
    address: ""
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        sponsor_id: initialData.sponsor_id || "",
        organization_name: initialData.organization_name || initialData.Organization_name || "",
        contact_person: initialData.contact_person || "",
        contact: initialData.contact || "",
        email: initialData.email || "",
        address: initialData.address || ""
      });
    }
  }, [initialData]);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  function handleSubmit(e) {
    e.preventDefault();
    onSave(form);
    onClose();
  }

  return (
    <div className="student-modal-overlay">
      <div className="student-modal">
        <div className="modal-header">
          <span className="modal-title">{mode === "edit" ? "Edit Sponsor" : "Add Sponsor"}</span>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <label>Sponsor ID *</label>
          <input name="sponsor_id" type="text" value={form.sponsor_id} onChange={handleChange} required />
          <label>Organization Name *</label>
          <input name="organization_name" type="text" value={form.organization_name} onChange={handleChange} required />
          <label>Contact Person *</label>
          <input name="contact_person" type="text" value={form.contact_person} onChange={handleChange} required />
          <label>Contact *</label>
          <input name="contact" type="text" value={form.contact} onChange={handleChange} required />
          <label>Email *</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required />
          <label>Address *</label>
          <input name="address" type="text" value={form.address} onChange={handleChange} required />
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 26 }}>
            <button type="button" className="modal-cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="modal-save-btn">{mode === "edit" ? "Update Sponsor" : "Save Sponsor"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
