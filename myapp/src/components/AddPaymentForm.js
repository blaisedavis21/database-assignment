import React, { useState, useEffect } from "react";
import "./StudentForm.css";

export default function AddPaymentForm({ onClose, onSave, initialData, mode = "add" }) {
  const [form, setForm] = useState({
    payment_id: "",
    allocation_id: "",
    amount: "",
    payment_date: "",
    semester: ""
  });

  useEffect(() => {
    if (initialData) {
      setForm({
        payment_id: initialData.payment_id || "",
        allocation_id: initialData.allocation_id || "",
        amount: initialData.amount || initialData.amount_id || "",
        payment_date: initialData.payment_date || initialData.paymentdate || "",
        semester: String(initialData.semester || "")
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
          <span className="modal-title">{mode === "edit" ? "Edit Payment" : "Add Payment"}</span>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>
        <form onSubmit={handleSubmit}>
          <label>Payment ID *</label>
          <input name="payment_id" type="text" value={form.payment_id} onChange={handleChange} required />
          <label>Allocation ID *</label>
          <input name="allocation_id" type="text" value={form.allocation_id} onChange={handleChange} required />
          <label>Amount *</label>
          <input name="amount" type="text" value={form.amount} onChange={handleChange} required />
          <label>Payment Date *</label>
          <input name="payment_date" type="date" value={form.payment_date} onChange={handleChange} required />
          <label>Semester *</label>
          <select name="semester" value={form.semester} onChange={handleChange} required>
            <option value="">Select Semester</option>
            <option value="1">1</option>
            <option value="2">2</option>
          </select>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 26 }}>
            <button type="button" className="modal-cancel-btn" onClick={onClose}>Cancel</button>
            <button type="submit" className="modal-save-btn">{mode === "edit" ? "Update Payment" : "Save Payment"}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
