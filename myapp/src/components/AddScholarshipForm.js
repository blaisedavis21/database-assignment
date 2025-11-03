import React, { useState, useEffect } from "react";
import "./StudentForm.css"; // Same modal CSS

export default function AddScholarshipForm({ onClose, onSave, initialData, mode = "add" }) {
  const [form, setForm] = useState({
    program_id: "",
    sponsor_id: "",
    program_name: "",
    amount_per_student: "",
    duration: "",
    Qualifications: ""
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        program_id: initialData.program_id || "",
        sponsor_id: initialData.sponsor_id || "",
        program_name: initialData.program_name || "",
        amount_per_student: initialData.amount_per_student || "",
        duration: initialData.duration || "",
        Qualifications: initialData.Qualifications || initialData.qualifications || ""
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
          <span className="modal-title">{mode === "edit" ? "Edit Scholarship Program" : "Add Scholarship Program"}</span>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <label>Program ID *</label>
          <input name="program_id" type="text" value={form.program_id} onChange={handleChange} required />
          <label>Sponsor ID *</label>
          <input name="sponsor_id" type="text" value={form.sponsor_id} onChange={handleChange} required />
          <label>Program Name *</label>
          <input name="program_name" type="text" value={form.program_name} onChange={handleChange} required />
          <label>Amount Per Student *</label>
          <input name="amount_per_student" type="text" value={form.amount_per_student} onChange={handleChange} required />
          <label>Duration *</label>
          <input name="duration" type="text" value={form.duration} onChange={handleChange} required />
          <label>Qualifications *</label>
          <input name="Qualifications" type="text" value={form.Qualifications} onChange={handleChange} required />
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 26 }}>
            <button type="button" className="modal-cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="modal-save-btn">{mode === "edit" ? "Update Program" : "Save Program"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
