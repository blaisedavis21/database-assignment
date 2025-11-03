import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./components/Dashboard";
import StudentTable from "./components/StudentTable";
import SponsorsTable from "./components/SponsorsTable";
import ProgramsTable from "./components/ProgramsTable";
import AllocationsTable from "./components/AllocationsTable";
import PaymentsTable from "./components/PaymentsTable";
import Reports from "./components/Reports";
import "./App.css";

function App() {
  const [selected, setSelected] = useState("Dashboard");

  let mainContent;
  switch (selected) {
    case "Dashboard":
      mainContent = <Dashboard />;
      break;
    case "Students":
      mainContent = <StudentTable />;
      break;
    case "Sponsors":
      mainContent = <SponsorsTable />;
      break;
    case "Scholarship Programs":
      mainContent = <ProgramsTable />;
      break;
    case "Allocations":
      mainContent = <AllocationsTable />;
      break;
    case "Payments":
      mainContent = <PaymentsTable />;
      break;
    case "Reports":
      mainContent = <Reports />;
      break;
    default:
      mainContent = <div style={{ margin: 40 }}>Welcome to SSMS Dashboard</div>;
      break;
  }

  return (
    <div style={{ background: "#f3f5fa", minHeight: "100vh" }}>
      <Sidebar selected={selected} onSelect={setSelected} />
      <div
        style={{
          marginLeft: 220,
          minHeight: "100vh",
          paddingBottom: 40,
          overflowY: "auto"
        }}
      >
        {mainContent}
      </div>
    </div>
  );
}

export default App;
