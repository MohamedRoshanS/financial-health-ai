import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { UploadCloud, LayoutDashboard, Sparkles, FileText } from "lucide-react";

import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import Insights from "./pages/Insights";
import Report from "./pages/Report";

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">

        {/* NAVBAR */}
        <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
            
            {/* Brand */}
            <div className="text-lg font-semibold text-gray-900">
              Financial Health AI
            </div>

            {/* Navigation */}
            <div className="flex gap-6 text-sm font-medium">
              <NavLink
                to="/"
                className={({ isActive }) =>
                  `flex items-center gap-2 ${
                    isActive ? "text-indigo-600" : "text-gray-600 hover:text-gray-900"
                  }`
                }
              >
                <UploadCloud size={16} />
                Upload
              </NavLink>

              <NavLink
                to="/dashboard"
                className={({ isActive }) =>
                  `flex items-center gap-2 ${
                    isActive ? "text-indigo-600" : "text-gray-600 hover:text-gray-900"
                  }`
                }
              >
                <LayoutDashboard size={16} />
                Dashboard
              </NavLink>

              <NavLink
                to="/insights"
                className={({ isActive }) =>
                  `flex items-center gap-2 ${
                    isActive ? "text-indigo-600" : "text-gray-600 hover:text-gray-900"
                  }`
                }
              >
                <Sparkles size={16} />
                Insights
              </NavLink>

              <NavLink
                to="/report"
                className={({ isActive }) =>
                  `flex items-center gap-2 ${
                    isActive ? "text-indigo-600" : "text-gray-600 hover:text-gray-900"
                  }`
                }
              >
                <FileText size={16} />
                Report
              </NavLink>
            </div>
          </div>
        </nav>

        {/* PAGE CONTENT */}
        <main className="max-w-6xl mx-auto px-6 py-8">
          <Routes>
            <Route path="/" element={<Upload />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/report" element={<Report />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
