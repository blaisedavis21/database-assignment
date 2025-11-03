import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import "./Reports.css";

const API_BASE = "http://127.0.0.1:8000/api";

export default function Reports() {
  const [students, setStudents] = useState([]);
  const [sponsors, setSponsors] = useState([]);
  const [programs, setPrograms] = useState([]);
  const [allocations, setAllocations] = useState([]);
  const [payments, setPayments] = useState([]);

  // Filters (shared per report block)
  const [filters, setFilters] = useState({
    university: "",
    year: "",
    sponsorId: "",
    status: "",
    semester: "",
    dateFrom: "",
    dateTo: "",
    studentId: ""
  });

  useEffect(() => {
    axios.get(`${API_BASE}/show-students/`).then(r => setStudents(r.data.students || []));
    axios.get(`${API_BASE}/show-sponsors/`).then(r => setSponsors(r.data.sponsors || []));
    axios.get(`${API_BASE}/show-programs/`).then(r => setPrograms(r.data.scholarship_programs || []));
    axios.get(`${API_BASE}/show-allocations/`).then(r => setAllocations(r.data.sponsorship_allocations || []));
    axios.get(`${API_BASE}/show-payments/`).then(r => setPayments(r.data.payments || []));
  }, []);

  function updateFilter(name, value) {
    setFilters(prev => ({ ...prev, [name]: value }));
  }

  const [printTarget, setPrintTarget] = useState("");

  function handlePrintAll() {
    window.print();
  }

  function handlePrintOne(targetId) {
    setPrintTarget(targetId);
    // Allow DOM to apply class before printing
    setTimeout(() => {
      window.print();
      setPrintTarget("");
    }, 0);
  }

  // Helper maps
  const studentById = useMemo(() => Object.fromEntries(students.map(s => [String(s.student_id), s])), [students]);
  const sponsorById = useMemo(() => Object.fromEntries(sponsors.map(s => [String(s.sponsor_id), s])), [sponsors]);
  const programById = useMemo(() => Object.fromEntries(programs.map(p => [String(p.program_id), p])), [programs]);

  // a) Student Sponsorship Report
  const a_rows = useMemo(() => {
    let rows = allocations.map(a => {
      const st = studentById[String(a.student_id)] || {};
      const pr = programById[String(a.program_id)] || {};
      const sp = sponsorById[String(pr.sponsor_id)] || {};
      return {
        student_name: st.name,
        university: st.university,
        program: pr.program_name,
        sponsor: sp.organization_name,
        status: a.status
      };
    });
    if (filters.university) rows = rows.filter(r => r.university === filters.university);
    if (filters.year) rows = rows.filter(r => String((studentById || {})[r.student_id]?.year_of_study) === filters.year);
    if (filters.sponsorId) rows = rows.filter(r => {
      const pr = programs.find(p => p.program_name === r.program);
      return pr && String(pr.sponsor_id) === String(filters.sponsorId);
    });
    return rows;
  }, [allocations, studentById, sponsorById, programById, programs, filters.university, filters.year, filters.sponsorId]);

  // b) Payment Summary Report
  const b_rows = useMemo(() => {
    let rows = payments.map(p => {
      const alloc = allocations.find(a => String(a.allocation_id) === String(p.allocation_id)) || {};
      const st = studentById[String(alloc.student_id)] || {};
      return {
        payment_id: p.payment_id,
        student: st.name,
        amount: p.amount,
        date: p.payment_date,
        semester: p.semester
      };
    });
    if (filters.semester) rows = rows.filter(r => String(r.semester) === String(filters.semester));
    if (filters.dateFrom) rows = rows.filter(r => r.date >= filters.dateFrom);
    if (filters.dateTo) rows = rows.filter(r => r.date <= filters.dateTo);
    return rows;
  }, [payments, allocations, studentById, filters.semester, filters.dateFrom, filters.dateTo]);

  // c) Sponsor Contribution Report (aggregate)
  const c_rows = useMemo(() => {
    const map = new Map();
    payments.forEach(p => {
      const alloc = allocations.find(a => String(a.allocation_id) === String(p.allocation_id));
      if (!alloc) return;
      const prog = programById[String(alloc.program_id)];
      if (!prog) return;
      const sponsorId = String(prog.sponsor_id);
      const sponsor = sponsorById[sponsorId];
      const key = sponsor ? sponsor.organization_name : sponsorId;
      const prev = map.get(key) || { sponsor: key, total: 0, students: new Set() };
      prev.total += Number(p.amount || 0);
      if (alloc.student_id) prev.students.add(String(alloc.student_id));
      map.set(key, prev);
    });
    let rows = Array.from(map.values()).map(v => ({ sponsor: v.sponsor, total_amount: v.total, num_students: v.students.size }));
    if (filters.sponsorId) rows = rows.filter(r => {
      const s = sponsors.find(sp => String(sp.sponsor_id) === String(filters.sponsorId));
      return s && r.sponsor === s.organization_name;
    });
    return rows;
  }, [payments, allocations, programById, sponsorById, sponsors, filters.sponsorId]);

  // d) Scholarship Program Summary
  const d_rows = useMemo(() => {
    let rows = programs.map(p => ({
      sponsor: (sponsorById[String(p.sponsor_id)] || {}).organization_name,
      program_name: p.program_name,
      amount_per_student: p.amount_per_student,
      duration: p.duration
    }));
    if (filters.sponsorId) rows = rows.filter(r => String((sponsors.find(s => s.organization_name === r.sponsor) || {}).sponsor_id) === String(filters.sponsorId));
    return rows;
  }, [programs, sponsors, sponsorById, filters.sponsorId]);

  // e) Active vs Completed Sponsorships
  const e_rows = useMemo(() => {
    let rows = allocations.map(a => {
      const st = studentById[String(a.student_id)] || {};
      const pr = programById[String(a.program_id)] || {};
      return {
        student: st.name,
        program: pr.program_name,
        start_date: a.start_date,
        end_date: a.end_date,
        status: a.status
      };
    });
    if (filters.status) rows = rows.filter(r => r.status === filters.status);
    return rows;
  }, [allocations, studentById, programById, filters.status]);

  // f) Students per University Report
  const f_rows = useMemo(() => {
    let filtered = students;
    if (filters.university) filtered = filtered.filter(s => s.university === filters.university);
    const map = new Map();
    filtered.forEach(s => map.set(s.university, (map.get(s.university) || 0) + 1));
    return Array.from(map.entries()).map(([university, count]) => ({ university, count }));
  }, [students, filters.university]);

  const universityOptions = useMemo(() => Array.from(new Set(students.map(s => s.university).filter(Boolean))), [students]);
  const studentOptions = useMemo(() => students.map(s => ({ value: String(s.student_id), label: `${s.name} (${s.student_id})` })), [students]);

  // g) Single Student Detail Report
  const g_student = useMemo(() => {
    if (!filters.studentId) return null;
    return studentById[String(filters.studentId)] || null;
  }, [filters.studentId, studentById]);

  const g_allocations = useMemo(() => {
    if (!filters.studentId) return [];
    return allocations
      .filter(a => String(a.student_id) === String(filters.studentId))
      .map(a => {
        const prog = programById[String(a.program_id)] || {};
        const sponsor = sponsorById[String(prog.sponsor_id)] || {};
        return {
          allocation_id: a.allocation_id,
          program: prog.program_name,
          sponsor: sponsor.organization_name,
          start_date: a.start_date,
          end_date: a.end_date,
          status: a.status
        };
      });
  }, [filters.studentId, allocations, programById, sponsorById]);

  const g_payments = useMemo(() => {
    if (!filters.studentId) return [];
    const allocIds = new Set(
      allocations.filter(a => String(a.student_id) === String(filters.studentId)).map(a => String(a.allocation_id))
    );
    return payments
      .filter(p => allocIds.has(String(p.allocation_id)))
      .map(p => ({ payment_id: p.payment_id, amount: p.amount, payment_date: p.payment_date, semester: p.semester }));
  }, [filters.studentId, allocations, payments]);

  return (
    <div className="reports-container">
      <div className="reports-toolbar no-print">
        <h2>Printable Reports</h2>
        <button className="primary-btn" onClick={handlePrintAll}>Print All</button>
      </div>

      {/* a) Student Sponsorship Report */}
      <ReportCard title="Student Sponsorship Report" id="report-a" onPrintOne={() => handlePrintOne("report-a")} printTarget={printTarget === "report-a"}>
        <div className="filters-row no-print">
          <Select label="University" value={filters.university} onChange={v => updateFilter("university", v)} options={["", ...universityOptions]} />
          <Select label="Year of Study" value={filters.year} onChange={v => updateFilter("year", v)} options={["", "1", "2", "3", "4"]} />
          <Select label="Sponsor" value={filters.sponsorId} onChange={v => updateFilter("sponsorId", v)} options={["", ...sponsors.map(s => ({ value: String(s.sponsor_id), label: s.organization_name }))]} isObject />
        </div>
        <SimpleTable columns={["Student Name", "University", "Program", "Sponsor", "Status"]} rows={a_rows.map(r => [r.student_name, r.university, r.program, r.sponsor, r.status])} />
      </ReportCard>

      {/* b) Payment Summary Report */}
      <ReportCard title="Payment Summary Report" id="report-b" onPrintOne={() => handlePrintOne("report-b")} printTarget={printTarget === "report-b"}>
        <div className="filters-row no-print">
          <Select label="Semester" value={filters.semester} onChange={v => updateFilter("semester", v)} options={["", "1", "2"]} />
          <Input label="From" type="date" value={filters.dateFrom} onChange={v => updateFilter("dateFrom", v)} />
          <Input label="To" type="date" value={filters.dateTo} onChange={v => updateFilter("dateTo", v)} />
        </div>
        <SimpleTable columns={["Payment ID", "Student", "Amount", "Date", "Semester"]} rows={b_rows.map(r => [r.payment_id, r.student, r.amount, r.date, r.semester])} />
      </ReportCard>

      {/* c) Sponsor Contribution Report */}
      <ReportCard title="Sponsor Contribution Report" id="report-c" onPrintOne={() => handlePrintOne("report-c")} printTarget={printTarget === "report-c"}>
        <div className="filters-row no-print">
          <Select label="Sponsor" value={filters.sponsorId} onChange={v => updateFilter("sponsorId", v)} options={["", ...sponsors.map(s => ({ value: String(s.sponsor_id), label: s.organization_name }))]} isObject />
        </div>
        <SimpleTable columns={["Sponsor", "Total Amount", "Number of Students Sponsored"]} rows={c_rows.map(r => [r.sponsor, r.total_amount, r.num_students])} />
      </ReportCard>

      {/* d) Scholarship Program Summary */}
      <ReportCard title="Scholarship Program Summary" id="report-d" onPrintOne={() => handlePrintOne("report-d")} printTarget={printTarget === "report-d"}>
        <div className="filters-row no-print">
          <Select label="Sponsor" value={filters.sponsorId} onChange={v => updateFilter("sponsorId", v)} options={["", ...sponsors.map(s => ({ value: String(s.sponsor_id), label: s.organization_name }))]} isObject />
        </div>
        <SimpleTable columns={["Program Name", "Amount per Student", "Duration", "Sponsor"]} rows={d_rows.map(r => [r.program_name, r.amount_per_student, r.duration, r.sponsor])} />
      </ReportCard>

      {/* e) Active vs Completed Sponsorships */}
      <ReportCard title="Active vs Completed Sponsorships" id="report-e" onPrintOne={() => handlePrintOne("report-e")} printTarget={printTarget === "report-e"}>
        <div className="filters-row no-print">
          <Select label="Status" value={filters.status} onChange={v => updateFilter("status", v)} options={["", "Active", "Completed"]} />
        </div>
        <SimpleTable columns={["Student", "Program", "Start Date", "End Date", "Status"]} rows={e_rows.map(r => [r.student, r.program, r.start_date, r.end_date, r.status])} />
      </ReportCard>

      {/* f) Students per University Report */}
      <ReportCard title="Students per University Report" id="report-f" onPrintOne={() => handlePrintOne("report-f")} printTarget={printTarget === "report-f"}>
        <div className="filters-row no-print">
          <Select label="University" value={filters.university} onChange={v => updateFilter("university", v)} options={["", ...universityOptions]} />
        </div>
        <SimpleTable columns={["University", "Number of Sponsored Students"]} rows={f_rows.map(r => [r.university, r.count])} />
      </ReportCard>

      {/* g) Single Student Detail Report */}
      <ReportCard title="Student Detail Report" id="report-student" onPrintOne={() => handlePrintOne("report-student")} printTarget={printTarget === "report-student"}>
        <div className="filters-row no-print">
          <Select label="Student" value={filters.studentId} onChange={v => updateFilter("studentId", v)} options={["", ...studentOptions]} isObject />
        </div>
        {g_student ? (
          <>
            <SimpleTable
              columns={["Field", "Value"]}
              rows={[
                ["Student ID", g_student.student_id],
                ["Name", g_student.name],
                ["Gender", g_student.gender],
                ["Date of Birth", g_student.date_of_birth],
                ["Contact", g_student.contact],
                ["Email", g_student.email],
                ["University", g_student.university],
                ["Course", g_student.course],
                ["Year of Study", g_student.year_of_study]
              ]}
            />
            <div style={{ height: 12 }} />
            <h4 style={{ margin: "12px 0 6px 0" }}>Allocations</h4>
            <SimpleTable columns={["Allocation ID", "Program", "Sponsor", "Start Date", "End Date", "Status"]} rows={g_allocations.map(a => [a.allocation_id, a.program, a.sponsor, a.start_date, a.end_date, a.status])} />
            <div style={{ height: 12 }} />
            <h4 style={{ margin: "12px 0 6px 0" }}>Payments</h4>
            <SimpleTable columns={["Payment ID", "Amount", "Date", "Semester"]} rows={g_payments.map(p => [p.payment_id, p.amount, p.payment_date, p.semester])} />
          </>
        ) : (
          <div style={{ color: "#777" }}>Select a student to view their details.</div>
        )}
      </ReportCard>
    </div>
  );
}

function ReportCard({ id, title, children, onPrintOne, printTarget }) {
  return (
    <div className={`report-card ${printTarget ? "print-target" : ""}`} data-report-id={id}>
      <div className="report-header">
        <h3>{title}</h3>
        <button className="primary-btn no-print" onClick={onPrintOne}>Print</button>
      </div>
      {children}
    </div>
  );
}

function Select({ label, value, onChange, options, isObject }) {
  return (
    <div className="filter-field">
      <label>{label}</label>
      <select value={value} onChange={e => onChange(e.target.value)}>
        {options.map(opt => isObject ? (
          <option key={opt.value || opt} value={opt.value || opt}>{opt.label || opt || "All"}</option>
        ) : (
          <option key={opt || "all"} value={opt}>{opt || "All"}</option>
        ))}
      </select>
    </div>
  );
}

function Input({ label, type = "text", value, onChange }) {
  return (
    <div className="filter-field">
      <label>{label}</label>
      <input type={type} value={value} onChange={e => onChange(e.target.value)} />
    </div>
  );
}

function SimpleTable({ columns, rows }) {
  return (
    <table className="report-table">
      <thead>
        <tr>
          {columns.map(c => <th key={c}>{c}</th>)}
        </tr>
      </thead>
      <tbody>
        {rows.map((r, idx) => (
          <tr key={idx}>
            {r.map((cell, i) => <td key={i}>{cell}</td>)}
          </tr>
        ))}
        {rows.length === 0 && (
          <tr>
            <td colSpan={columns.length} style={{ textAlign: "center", color: "#777" }}>No data</td>
          </tr>
        )}
      </tbody>
    </table>
  );
}


