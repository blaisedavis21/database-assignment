import React, { useState, useEffect } from "react";
import "./StudentForm.css";

export default function AddAllocationForm({ onClose, onSave, initialData, mode = "add" }) {
  const [form, setForm] = useState({
    allocation_id: "",
    student_id: "",
    program_id: "",
    start_date: "",
    end_date: "",
    status: ""
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        allocation_id: initialData.allocation_id || "",
        student_id: initialData.student_id || "",
        program_id: initialData.program_id || "",
        start_date: initialData.start_date || initialData.startdate || "",
        end_date: initialData.end_date || initialData.enddate || "",
        status: initialData.status || ""
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
          <span className="modal-title">{mode === "edit" ? "Edit Sponsorship Allocation" : "Add Sponsorship Allocation"}</span>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <label>Allocation ID *</label>
          <input name="allocation_id" type="text" value={form.allocation_id} onChange={handleChange} required />
          <label>Student ID *</label>
          <input name="student_id" type="text" value={form.student_id} onChange={handleChange} required />
          <label>Program ID *</label>
          <input name="program_id" type="text" value={form.program_id} onChange={handleChange} required />
          <label>Start Date *</label>
          <input name="start_date" type="date" value={form.start_date} onChange={handleChange} required />
          <label>End Date *</label>
          <input name="end_date" type="date" value={form.end_date} onChange={handleChange} required />
          <label>Status *</label>
          <select name="status" value={form.status} onChange={handleChange} required>
            <option value="">Select Status</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
          </select>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 26 }}>
            <button type="button" className="modal-cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="modal-save-btn">{mode === "edit" ? "Update Allocation" : "Save Allocation"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
