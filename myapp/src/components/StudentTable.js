import React, { useState, useEffect } from "react";
import axios from "axios";
import StudentForm from "./StudentForm";
import "./StudentTable.css";

const universityOptions = [
  "All Universities",
  "Makerere University",
  "Kyambogo University",
  "UCU",
  "MUST",
  "Gulu University",
  "MUBS",
  "Busitema University"
];

export default function StudentTable() {
  const [students, setStudents] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [search, setSearch] = useState("");
  const [university, setUniversity] = useState("All Universities");
  const [year, setYear] = useState("All Years");
  const [gender, setGender] = useState("All");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, []);

  function fetchStudents() {
    setLoading(true);
    axios.get("http://127.0.0.1:8000/api/show-students/")
      .then(res => setStudents(res.data.students))
      .finally(() => setLoading(false));
  }

  function handleAddStudent(data) {
    axios.post("http://127.0.0.1:8000/api/add-student/", data)
      .then(() => fetchStudents());
  }

  function handleUpdateStudent(id, data) {
    axios.put(`http://127.0.0.1:8000/api/update-student/${id}/`, data)
      .then(() => fetchStudents());
  }

  function handleDeleteStudent(id) {
    if (!window.confirm("Delete this student?")) return;
    axios.delete(`http://127.0.0.1:8000/api/delete-student/${id}/`)
      .then(() => fetchStudents());
  }

  const filtered = students.filter((s) => (
    (s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.email.toLowerCase().includes(search.toLowerCase()) ||
      String(s.student_id).toLowerCase().includes(search.toLowerCase())) &&
    (university === "All Universities" || s.university === university) &&
    (year === "All Years" || String(s.year_of_study) === year) &&
    (gender === "All" || s.gender === gender)
  ));

  return (
    <div className="students-table-container">
      <div className="search-bar">
        <input type="text" placeholder="Search by name, email, or student ID..." value={search} onChange={e => setSearch(e.target.value)} className="search-field"/>
        <div className="search-filters">
          <div>
            <label className="filter-label">Filter by University</label>
            <select value={university} onChange={e => setUniversity(e.target.value)}>
              {universityOptions.map(opt => <option key={opt}>{opt}</option>)}
            </select>
          </div>
          <div>
            <label className="filter-label">Filter by Year</label>
            <select value={year} onChange={e => setYear(e.target.value)}>
              <option>All Years</option>
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
            </select>
          </div>
          <div>
            <label className="filter-label">Gender</label>
            <select value={gender} onChange={e => setGender(e.target.value)}>
              <option>All</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>
        </div>
        <button className="export-btn">Export</button>
        <button className="list-btn"><span role="img" aria-label="table">&#9776;</span></button>
      </div>
      <div className="students-header">
        <h2>Students Management</h2>
        <button className="primary-btn" onClick={() => setShowForm(true)}>
          + Add Student
        </button>
      </div>
      {loading ? <div>Loading...</div> : (
        <table className="students-table">
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Name</th>
              <th>Gender</th>
              <th>Date of Birth</th>
              <th>Contact</th>
              <th>Email</th>
              <th>University</th>
              <th>Course</th>
              <th>Year of Study</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((s) => (
              <tr key={s.student_id}>
                <td>{s.student_id}</td>
                <td>{s.name}</td>
                <td>{s.gender}</td>
                <td>{s.date_of_birth}</td>
                <td>{s.contact}</td>
                <td>{s.email}</td>
                <td>{s.university}</td>
                <td>{s.course}</td>
                <td>{s.year_of_study}</td>
                <td>
                  <button className="primary-btn" onClick={() => setEditingStudent(s)}>Edit</button>
                  <button className="export-btn" style={{ marginLeft: 8 }} onClick={() => handleDeleteStudent(s.student_id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {showForm && (
        <StudentForm
          onClose={() => setShowForm(false)}
          onSave={data => {
            handleAddStudent(data);
            setShowForm(false);
          }}
        />
      )}
      {editingStudent && (
        <StudentForm
          mode="edit"
          initialData={editingStudent}
          onClose={() => setEditingStudent(null)}
          onSave={data => {
            handleUpdateStudent(editingStudent.student_id, data);
            setEditingStudent(null);
          }}
        />
      )}
    </div>
  );
}
