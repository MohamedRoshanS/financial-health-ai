import { useState } from "react";
import { uploadFile, analyzeData } from "../services/api";
import { useNavigate } from "react-router-dom";
import {
  UploadCloud,
  Building2,
  AlertTriangle,
  FileSpreadsheet
} from "lucide-react";

function Upload() {
  const [file, setFile] = useState(null);
  const [warnings, setWarnings] = useState([]);
  const [error, setError] = useState(null);
  const [industry, setIndustry] = useState("Retail");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleUpload = async () => {
    try {
      setError(null);
      setWarnings([]);
      setLoading(true);

      const uploadRes = await uploadFile(file);

      if (!uploadRes.monthly_data) {
        throw new Error("Normalized data missing from upload response");
      }

      const analysis = await analyzeData(
        uploadRes.monthly_data,
        industry
      );

      navigate("/dashboard", {
        state: {
          analysis,
          warnings: uploadRes.warnings
        }
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">

      {/* HERO / INTRO */}
      <div className="text-center max-w-3xl mx-auto mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Financial Health Assessment for SMEs
        </h1>
        <p className="text-lg text-gray-600">
          Upload your financial data to instantly understand business health,
          risks, benchmarks, and future outlook — powered by AI.
        </p>
      </div>

      {/* INFO CARDS */}
      <div className="grid md:grid-cols-3 gap-6 mb-16">
        <div className="card">
          <FileSpreadsheet className="text-indigo-600 mb-3" size={22} />
          <h3 className="card-title mb-1">Upload Financials</h3>
          <p className="muted-text">
            CSV or Excel files exported from accounting systems.
          </p>
        </div>

        <div className="card">
          <AlertTriangle className="text-amber-500 mb-3" size={22} />
          <h3 className="card-title mb-1">Identify Risks</h3>
          <p className="muted-text">
            Detect cash flow, debt, and compliance risks early.
          </p>
        </div>

        <div className="card">
          <Building2 className="text-emerald-600 mb-3" size={22} />
          <h3 className="card-title mb-1">Industry Benchmarks</h3>
          <p className="muted-text">
            Compare your performance with industry averages.
          </p>
        </div>
      </div>

      {/* UPLOAD CARD */}
      <div className="card max-w-2xl mx-auto">
        <h2 className="section-title mb-6">Upload Financial Data</h2>

        {/* Industry */}
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Industry
        </label>
        <select
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          className="w-full rounded-lg border border-gray-300 px-4 py-2 mb-6 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        >
          <option value="Retail">Retail</option>
          <option value="Manufacturing">Manufacturing</option>
          <option value="Services">Services</option>
        </select>

        {/* File Upload */}
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload File
        </label>
        <div className="flex items-center gap-4 mb-6">
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={(e) => setFile(e.target.files[0])}
            className="w-full text-sm"
          />
        </div>

        <p className="muted-text mb-6">
          Supported formats: CSV, XLSX
        </p>

        {/* Action */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className="primary-btn w-full flex items-center justify-center gap-2"
        >
          <UploadCloud size={18} />
          {loading ? "Analyzing..." : "Upload & Analyze"}
        </button>

        {/* ERROR */}
        {error && (
          <p className="mt-4 text-sm text-rose-600">
            {error}
          </p>
        )}

        {/* WARNINGS */}
        {warnings.length > 0 && (
          <div className="mt-6">
            <h4 className="text-sm font-semibold text-amber-600 mb-2">
              Data Warnings
            </h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {warnings.map((w, i) => (
                <li key={i}>{w}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

export default Upload;
