// src/layout/Layout.jsx
import { useState } from "react";
import Sidebar from "../components/Sidebar";
import Header from "./Header";
import "../styles/layout.css";

export default function Layout({ children, title }) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="app-container">
      <Sidebar collapsed={collapsed} setCollapsed={setCollapsed} />

      <div className="main-area">
        <Header title={title} />
        <div className="page-content">{children}</div>
      </div>
    </div>
  );
}