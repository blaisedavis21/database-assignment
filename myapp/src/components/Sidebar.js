import React from "react";
import "./Sidebar.css";

const sidebarItems = [
  "Dashboard",
  "Students",
  "Sponsors",
  "Scholarship Programs",
  "Allocations",
  "Payments",
  "Reports",
];

export default function Sidebar({ selected, onSelect }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">SSMS</div>
      <ul className="sidebar-list">
        {sidebarItems.map(item => (
          <li
            key={item}
            className={selected === item ? "selected" : ""}
            onClick={() => onSelect(item)}
          >
            {item}
          </li>
        ))}
      </ul>
    </aside>
  );
}
