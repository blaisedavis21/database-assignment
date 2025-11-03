import React, { useState, useEffect } from "react";
import axios from "axios";
import AddPaymentForm from "./AddPaymentForm";
import "./EntityTable.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function PaymentsTable() {
  const [payments, setPayments] = useState([]);
  const [search, setSearch] = useState("");
  const [semester, setSemester] = useState("All");
  const [showAdd, setShowAdd] = useState(false);
  const [editingPayment, setEditingPayment] = useState(null);

  useEffect(() => {
    fetchPayments();
  }, []);

  function fetchPayments() {
    axios.get(`${API_BASE}/show-payments/`)
      .then(res => setPayments(res.data.payments || []));
  }

  function handleAddPayment(data) {
    axios.post(`${API_BASE}/add-payment/`, data)
      .then(() => fetchPayments());
  }

  function handleUpdatePayment(id, data) {
    axios.put(`${API_BASE}/update-payment/${id}/`, data)
      .then(() => fetchPayments());
  }

  function handleDeletePayment(id) {
    if (!window.confirm("Delete this payment?")) return;
    axios.delete(`${API_BASE}/delete-payment/${id}/`)
      .then(() => fetchPayments());
  }

  const filtered = payments.filter(
    p =>
      (
        (p.payment_id && String(p.payment_id).toLowerCase().includes(search.toLowerCase())) ||
        (p.allocation_id && String(p.allocation_id).toLowerCase().includes(search.toLowerCase())) ||
        (p.amount && String(p.amount).toLowerCase().includes(search.toLowerCase()))
      ) &&
      (semester === "All" || String(p.semester) === semester)
  );

  return (
    <div className="entity-table-container">
      <div className="search-bar">
        <input type="text" placeholder="Search by payment ID, allocation ID, or amount..." value={search} onChange={e => setSearch(e.target.value)} className="search-field"/>
        <div className="search-filters">
          <div>
            <label className="filter-label">Semester</label>
            <select value={semester} onChange={e => setSemester(e.target.value)}>
              <option>All</option>
              <option>1</option>
              <option>2</option>
            </select>
          </div>
        </div>
        <button className="export-btn">Export</button>
        <button className="list-btn"><span role="img" aria-label="table">&#9776;</span></button>
      </div>
      <div className="entity-header">
        <h2>Payments</h2>
        <button className="primary-btn" onClick={() => setShowAdd(true)}>
          + Add Payment
        </button>
      </div>
      <table className="entity-table">
        <thead>
          <tr>
            <th>Payment ID</th>
            <th>Allocation ID</th>
            <th>Amount</th>
            <th>Payment Date</th>
            <th>Semester</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map(p => (
            <tr key={p.payment_id}>
              <td>{p.payment_id}</td>
              <td>{p.allocation_id}</td>
              <td>{p.amount}</td>
              <td>{p.payment_date}</td>
              <td>{p.semester}</td>
              <td>
                <button className="primary-btn" onClick={() => setEditingPayment(p)}>Edit</button>
                <button className="export-btn" style={{ marginLeft: 8 }} onClick={() => handleDeletePayment(p.payment_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showAdd && (
        <AddPaymentForm
          onClose={() => setShowAdd(false)}
          onSave={data => {
            handleAddPayment(data);
            setShowAdd(false);
          }}
        />
      )}
      {editingPayment && (
        <AddPaymentForm
          mode="edit"
          initialData={editingPayment}
          onClose={() => setEditingPayment(null)}
          onSave={data => {
            handleUpdatePayment(editingPayment.payment_id, data);
            setEditingPayment(null);
          }}
        />
      )}
    </div>
  );
}
