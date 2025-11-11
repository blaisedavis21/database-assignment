import React, { useState, useEffect } from "react";
import { BarChart, Bar, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Cell, ResponsiveContainer } from "recharts";

const API_BASE = "http://127.0.0.1:8000/api";

// Color palette
const COLORS = ["#4069F6", "#27c59a", "#ffbb32", "#a772fa", "#ff6b6b", "#4ecdc4"];

export default function Dashboard() {
  const [totals, setTotals] = useState({
    total_students: 0,
    total_sponsors: 0,
    total_active_allocations: 0,
    total_payments: 0
  });

  // State for each visualization
  const [studentsByUniversity, setStudentsByUniversity] = useState([]);
  const [sponsorshipStatus, setSponsorshipStatus] = useState([]);
  const [paymentsPerSemester, setPaymentsPerSemester] = useState([]);
  const [sponsorContributions, setSponsorContributions] = useState([]);
  const [studentsByYear, setStudentsByYear] = useState([]);
  const [genderDistribution, setGenderDistribution] = useState([]);
  const [upcomingEndDates, setUpcomingEndDates] = useState([]);
  const [avgScholarship, setAvgScholarship] = useState([]);
  const [sponsorshipTrends, setSponsorshipTrends] = useState([]);
  const [topPrograms, setTopPrograms] = useState([]);

  useEffect(() => {
    // Fetch existing API data
    fetch(`${API_BASE}/dashboard/totals/`)
      .then(res => res.json())
      .then(data => setTotals(data || {}))
      .catch(err => console.error("Error fetching totals:", err));

    // Try to fetch real data, fallback to mock if API doesn't exist
    fetchWithFallback(`${API_BASE}/dashboard/students-by-university/`, 
      setStudentsByUniversity, getMockStudentsByUniversity());
    
    fetchWithFallback(`${API_BASE}/dashboard/sponsorship-status/`, 
      setSponsorshipStatus, getMockSponsorshipStatus());
    
    fetchWithFallback(`${API_BASE}/dashboard/payments-per-semester/`, 
      setPaymentsPerSemester, getMockPaymentsPerSemester());
    
    fetchWithFallback(`${API_BASE}/dashboard/sponsor-contributions/`, 
      setSponsorContributions, getMockSponsorContributions());
    
    fetchWithFallback(`${API_BASE}/dashboard/students-by-year/`, 
      setStudentsByYear, getMockStudentsByYear());
    
    fetchWithFallback(`${API_BASE}/dashboard/gender-distribution/`, 
      setGenderDistribution, getMockGenderDistribution());
    
    fetchWithFallback(`${API_BASE}/dashboard/upcoming-end-dates/`, 
      setUpcomingEndDates, getMockUpcomingEndDates());
    
    fetchWithFallback(`${API_BASE}/dashboard/average-scholarship-amount/`, 
      setAvgScholarship, getMockAvgScholarship());
    
    fetchWithFallback(`${API_BASE}/dashboard/sponsorship-trends/`, 
      setSponsorshipTrends, getMockSponsorshipTrends());
    
    fetchWithFallback(`${API_BASE}/dashboard/top-programs/`, 
      setTopPrograms, getMockTopPrograms());
  }, []);

  const toArray = (value) => {
    if (Array.isArray(value)) return value;
    if (!value || typeof value !== "object") return [];
    if (Array.isArray(value.results)) return value.results;
    if (Array.isArray(value.data)) return value.data;
    // If object with numeric keys
    const vals = Object.values(value);
    return Array.isArray(vals) && vals.every(v => typeof v === 'object') ? vals : [];
  };

  const fetchWithFallback = (url, setter, mockData) => {
    fetch(url)
      .then(res => res.json())
      .then(data => {
        const arr = toArray(data);
        if (!Array.isArray(arr)) {
          console.warn(`Expected array for ${url}, received`, data);
        }
        setter(Array.isArray(arr) ? arr : []);
      })
      .catch(err => {
        console.log(`Using mock data for ${url}`);
        setter(mockData);
      });
  };

  function renderRotatedCenteredTick({ x, y, payload }) {
    const text = payload.value || "";
    const [firstWord, ...rest] = text.split(" ");
    const secondLine = rest.join(" ");
    return (
      <g transform={`translate(${x},${y + 25})`}>
        <text x={0} y={0} textAnchor="middle" transform="rotate(-45)" style={{ fontSize: 16 }}>
          <tspan x={0} dy={0}>{firstWord}</tspan>
          {secondLine ? <tspan x={0} dy={14}>{secondLine}</tspan> : null}
        </text>
      </g>
    );
  }

  return (
    <div style={{ padding: 28, background: "#f5f7fa", minHeight: "100vh" }}>
      {/* Top Stats Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(4, 1fr)",
        gap: 20,
        marginBottom: 30
      }}>
        <StatCard color="#4069F6" title="Total Students" value={totals.total_students || 0} />
        <StatCard color="#27c59a" title="Total Sponsors" value={totals.total_sponsors || 0} />
        <StatCard color="#ffbb32" title="Active Allocations" value={totals.total_active_allocations || 0} />
        <StatCard color="#a772fa" title="Total Payments" 
          value={totals.total_payments ? "UGX " + Number(totals.total_payments).toLocaleString() : "UGX 0"} />
      </div>

      {/* Row 1: Students by University & Sponsorship Status */}
      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="📊 Students per University">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={studentsByUniversity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="university" tick={renderRotatedCenteredTick} interval={0} height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#4069F6" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🥧 Sponsorship Status">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={sponsorshipStatus} dataKey="count" nameKey="status" cx="50%" cy="50%" 
                outerRadius={80} label>
                {sponsorshipStatus.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Row 2: Payments per Semester & Sponsor Contributions */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="💰 Payments per Semester">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={paymentsPerSemester}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="semester" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="amount" fill="#27c59a" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="🏛️ Top Sponsor Contributions">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sponsorContributions} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="sponsor_name" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="total_amount" fill="#a772fa" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Row 3: Students by Year & Gender Distribution */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="🎓 Students by Year of Study">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={studentsByYear}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="year_of_study" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#ffbb32" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="👩‍🎓 Gender Distribution">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={genderDistribution} dataKey="count" nameKey="gender" cx="50%" cy="50%" 
                outerRadius={80} label>
                {genderDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? "#4069F6" : "#ff6b6b"} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Row 4: Sponsorship Trends & Avg Scholarship Amount */}
      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="📈 Sponsorship Trends Over Time">
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={sponsorshipTrends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="new_allocations" stroke="#4069F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="💵 Avg Scholarship by Sponsor">
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={avgScholarship} dataKey="average_amount" nameKey="sponsor_name" cx="50%" cy="50%" 
                outerRadius={80} label>
                {avgScholarship.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      {/* Row 5: Top Programs & Upcoming End Dates */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 20 }}>
        <ChartCard title="🧮 Top 5 Programs by Funding">
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={topPrograms}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="program_name" tick={renderRotatedCenteredTick} interval={0} height={100} />
              <YAxis />
              <Tooltip />
              <Bar dataKey="amount_per_student" fill="#4ecdc4" />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="📅 Upcoming Sponsorship End Dates">
          <div style={{ maxHeight: 280, overflowY: "auto" }}>
            <table style={{ width: "100%", fontSize: 14 }}>
              <thead>
                <tr style={{ borderBottom: "2px solid #e0e0e0" }}>
                  <th style={{ padding: 8, textAlign: "left" }}>Student</th>
                  <th style={{ padding: 8, textAlign: "left" }}>Program</th>
                  <th style={{ padding: 8, textAlign: "left" }}>End Date</th>
                </tr>
              </thead>
              <tbody>
                {upcomingEndDates.map((item, idx) => (
                  <tr key={idx} style={{ borderBottom: "1px solid #f0f0f0" }}>
                    <td style={{ padding: 8 }}>{item.student_name}</td>
                    <td style={{ padding: 8, fontSize: 12, color: "#666" }}>{item.program_name}</td>
                    <td style={{ padding: 8, fontSize: 12, color: "#999" }}>{item.end_date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </ChartCard>
      </div>
    </div>
  );
}

function StatCard({ color, title, value }) {
  return (
    <div style={{
      background: "#fff",
      borderRadius: 12,
      padding: 24,
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
      display: "flex",
      flexDirection: "column",
      gap: 12
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: color
        }} />
        <span style={{ color: "#666", fontWeight: 500, fontSize: 14 }}>{title}</span>
      </div>
      <div style={{ color: "#243650", fontWeight: "bold", fontSize: 28 }}>{value}</div>
    </div>
  );
}

function ChartCard({ title, children }) {
  return (
    <div style={{
      background: "#fff",
      borderRadius: 12,
      padding: 24,
      boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
    }}>
      <h3 style={{ margin: "0 0 20px 0", fontSize: 16, fontWeight: 600 }}>{title}</h3>
      {children}
    </div>
  );
}

// Mock data functions
function getMockStudentsByUniversity() {
  return [
    { university: "Makerere", count: 145 },
    { university: "Kyambogo", count: 98 },
    { university: "MUBS", count: 76 },
    { university: "UCU", count: 65 },
    { university: "Gulu", count: 42 }
  ];
}

function getMockSponsorshipStatus() {
  return [
    { status: "Active", count: 285 },
    { status: "Completed", count: 142 },
    { status: "Suspended", count: 18 }
  ];
}

function getMockPaymentsPerSemester() {
  return [
    { semester: "2023 Sem 1", amount: 45000000 },
    { semester: "2023 Sem 2", amount: 52000000 },
    { semester: "2024 Sem 1", amount: 48000000 },
    { semester: "2024 Sem 2", amount: 61000000 },
    { semester: "2025 Sem 1", amount: 55000000 }
  ];
}

function getMockSponsorContributions() {
  return [
    { sponsor_name: "ABC Foundation", total_amount: 225000000 },
    { sponsor_name: "XYZ Trust", total_amount: 105000000 },
    { sponsor_name: "Global Fund", total_amount: 89000000 },
    { sponsor_name: "Youth Initiative", total_amount: 67000000 },
    { sponsor_name: "Education Plus", total_amount: 54000000 }
  ];
}

function getMockStudentsByYear() {
  return [
    { year: "Year 1", count: 156 },
    { year: "Year 2", count: 134 },
    { year: "Year 3", count: 98 },
    { year: "Year 4", count: 76 },
    { year: "Year 5", count: 12 }
  ];
}

function getMockGenderDistribution() {
  return [
    { gender: "Male", count: 245 },
    { gender: "Female", count: 231 }
  ];
}

function getMockUpcomingEndDates() {
  return [
    { student_name: "John Doe", program_name: "Computer Science", end_date: "2025-05-15" },
    { student_name: "Jane Smith", program_name: "Business Admin", end_date: "2025-06-20" },
    { student_name: "David Okello", program_name: "Engineering", end_date: "2025-07-10" },
    { student_name: "Sarah Nabwire", program_name: "Medicine", end_date: "2025-08-05" },
    { student_name: "Paul Mugisha", program_name: "Law", end_date: "2025-09-12" }
  ];
}

function getMockAvgScholarship() {
  return [
    { sponsor_name: "ABC Foundation", avg_amount: 5500000 },
    { sponsor_name: "XYZ Trust", avg_amount: 4200000 },
    { sponsor_name: "Global Fund", avg_amount: 3800000 },
    { sponsor_name: "Youth Initiative", avg_amount: 3200000 }
  ];
}

function getMockSponsorshipTrends() {
  return [
    { period: "Q1 2024", new_allocations: 28 },
    { period: "Q2 2024", new_allocations: 35 },
    { period: "Q3 2024", new_allocations: 42 },
    { period: "Q4 2024", new_allocations: 22 },
    { period: "Q1 2025", new_allocations: 30 }
  ];
}

function getMockTopPrograms() {
  return [
    { program_name: "Computer Science", amount: 125000000 },
    { program_name: "Engineering", amount: 98000000 },
    { program_name: "Medicine", amount: 87000000 },
    { program_name: "Business Admin", amount: 76000000 },
    { program_name: "Law", amount: 54000000 }
  ];
}