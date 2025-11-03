import React, { useState, useEffect } from "react";
import "./StudentForm.css";

export default function StudentForm({ onClose, onSave, initialData, mode = "add" }) {
  const [form, setForm] = useState({
    name: "",
    gender: "Male",
    date_of_birth: "",
    contact: "",
    email: "",
    university: "Makerere University",
    course: "",
    year_of_study: ""
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        name: initialData.name || "",
        gender: initialData.gender || "Male",
        date_of_birth: initialData.date_of_birth || "",
        contact: initialData.contact || "",
        email: initialData.email || "",
        university: initialData.university || "Makerere University",
        course: initialData.course || "",
        year_of_study: String(initialData.year_of_study || "")
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
          <span className="modal-title">{mode === "edit" ? "Edit Student" : "Add New Student"}</span>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <label>Full Name *</label>
          <input name="name" type="text" placeholder="Enter full name" value={form.name} onChange={handleChange} required />
          <label>Gender *</label>
          <div style={{ marginBottom: 10 }}>
            <label><input type="radio" name="gender" value="Male" checked={form.gender === "Male"} onChange={handleChange} /> Male</label>
            <label style={{ marginLeft: 18 }}><input type="radio" name="gender" value="Female" checked={form.gender === "Female"} onChange={handleChange} /> Female</label>
          </div>
          <label>Date of Birth *</label>
          <input name="date_of_birth" type="date" value={form.date_of_birth} onChange={handleChange} required />
          <label>Contact Number *</label>
          <input name="contact" type="text" value={form.contact} onChange={handleChange} required />
          <label>Email Address *</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required />
          <label>University *</label>
          <select name="university" value={form.university} onChange={handleChange} required>
            <option>Makerere University</option>
            <option>Kyambogo University</option>
            <option>UCU</option>
            <option>MUST</option>
            <option>Gulu University</option>
            <option>MUBS</option>
            <option>Busitema University</option>
          </select>
          <label>Course/Program *</label>
          <input name="course" type="text" value={form.course} onChange={handleChange} required />
          <label>Year of Study *</label>
          <select name="year_of_study" value={form.year_of_study} onChange={handleChange} required>
            <option value="">Select Year</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
          </select>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 26 }}>
            <button type="button" className="modal-cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="modal-save-btn">{mode === "edit" ? "Update Student" : "Save Student"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
