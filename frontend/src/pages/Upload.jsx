import { useState } from "react";
import { uploadFile, analyzeData } from "../services/api";
import { useNavigate } from "react-router-dom";
import {
  UploadCloud,
  Building2,
  AlertTriangle,
  FileSpreadsheet,
  CheckCircle,
  XCircle,
  FileIcon,
  FileJson // Added for specific icon
} from "lucide-react";

function Upload() {
  // --- Main Financial File State ---
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  // --- New GST JSON File State ---
  const [gstFile, setGstFile] = useState(null);
  const [gstDragOver, setGstDragOver] = useState(false);

  // --- General State ---
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

      // Note: You may need to update your uploadFile service to handle both files
      // e.g., const uploadRes = await uploadFile(file, gstFile);
      const uploadRes = await uploadFile(file);

      if (!uploadRes.monthly_data || uploadRes.monthly_data.length === 0) {
        throw new Error(
          uploadRes.error || "No usable financial data found in uploaded file"
        );
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

  // --- Handlers for Main Financial File ---
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['.csv', '.xlsx', '.xls', '.pdf'];
      const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
      
      if (validTypes.includes(fileExtension)) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError(`Unsupported file type. Please upload ${validTypes.join(', ')} files.`);
        setFile(null);
      }
    }
  };

  const handleDragOver = (e) => { e.preventDefault(); setDragOver(true); };
  const handleDragLeave = (e) => { e.preventDefault(); setDragOver(false); };
  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files[0]) {
      handleFileChange({ target: { files: e.dataTransfer.files } });
    }
  };
  const removeFile = () => { setFile(null); setWarnings([]); setError(null); };

  // --- Handlers for GST JSON File ---
  const handleGstFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['.json'];
      const fileExtension = selectedFile.name.substring(selectedFile.name.lastIndexOf('.')).toLowerCase();
      
      if (validTypes.includes(fileExtension)) {
        setGstFile(selectedFile);
        setError(null);
      } else {
        setError("Invalid format. Please upload a .json file for GST data.");
        setGstFile(null);
      }
    }
  };

  const handleGstDragOver = (e) => { e.preventDefault(); setGstDragOver(true); };
  const handleGstDragLeave = (e) => { e.preventDefault(); setGstDragOver(false); };
  const handleGstDrop = (e) => {
    e.preventDefault();
    setGstDragOver(false);
    if (e.dataTransfer.files[0]) {
      handleGstFileChange({ target: { files: e.dataTransfer.files } });
    }
  };
  const removeGstFile = () => { setGstFile(null); };

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
        <label className="block text-sm font-medium text-gray-700 mb-3.5">
          Select Industry
        </label>
        <select
          value={industry}
          onChange={(e) => setIndustry(e.target.value)}
          className="w-full rounded-lg border border-gray-300 px-4 py-2 mb-6"
        >
          <option value="Retail">Retail</option>
          <option value="Manufacturing">Manufacturing</option>
          <option value="Services">Services</option>
          <option value="Agriculture">Agriculture</option>
          <option value="Logistics">Logistics</option>
          <option value="E-commerce">E-commerce</option>
        </select>

        {/* 1. MAIN FILE UPLOAD AREA */}
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload Financial Statements
        </label>
        
        {!file ? (
          <div
            className={`border-2 border-dashed rounded-xl p-8 mb-6 text-center cursor-pointer transition-all duration-200 ${
              dragOver 
                ? 'border-indigo-500 bg-indigo-50' 
                : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
            }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-upload').click()}
          >
            <div className="flex flex-col items-center justify-center gap-3">
              <div className="p-3 rounded-full bg-indigo-100">
                <UploadCloud className="text-indigo-600" size={24} />
              </div>
              <div>
                <p className="font-medium text-gray-700 mb-1">
                  Choose a file or drag & drop
                </p>
                <p className="text-sm text-gray-500">
                  CSV, XLSX, or PDF files (max 10MB)
                </p>
              </div>
              <button
                type="button"
                className="mt-2 px-4 py-2 text-sm font-medium text-indigo-700 bg-indigo-100 rounded-lg hover:bg-indigo-200 transition-colors"
              >
                Browse files
              </button>
            </div>
            <input
              id="file-upload"
              type="file"
              accept=".csv,.xlsx,.xls,.pdf"
              onChange={handleFileChange}
              className="hidden"
            />
          </div>
        ) : (
          <div className="border rounded-xl p-4 mb-6 bg-gray-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-emerald-100">
                  <CheckCircle className="text-emerald-600" size={20} />
                </div>
                <div>
                  <p className="font-medium text-gray-800">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024 / 1024).toFixed(2)} MB • Ready to upload
                  </p>
                </div>
              </div>
              <button
                onClick={removeFile}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-full transition-colors"
                type="button"
              >
                <XCircle size={20} />
              </button>
            </div>
          </div>
        )}

        {/* 2. GST JSON UPLOAD AREA (NEW) */}
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Upload GST Filing Data (JSON)
        </label>

        {!gstFile ? (
          <div
            className={`border-2 border-dashed rounded-xl p-6 mb-6 text-center cursor-pointer transition-all duration-200 ${
              gstDragOver 
                ? 'border-indigo-500 bg-indigo-50' 
                : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
            }`}
            onDragOver={handleGstDragOver}
            onDragLeave={handleGstDragLeave}
            onDrop={handleGstDrop}
            onClick={() => document.getElementById('gst-file-upload').click()}
          >
            <div className="flex flex-col items-center justify-center gap-3">
              <div className="p-3 rounded-full bg-orange-100">
                <FileJson className="text-orange-600" size={24} />
              </div>
              <div>
                <p className="font-medium text-gray-700 mb-1">
                  Upload GST JSON
                </p>
                <p className="text-sm text-gray-500">
                  Official GST Filing JSON only
                </p>
              </div>
            </div>
            <input
              id="gst-file-upload"
              type="file"
              accept=".json"
              onChange={handleGstFileChange}
              className="hidden"
            />
          </div>
        ) : (
          <div className="border rounded-xl p-4 mb-6 bg-gray-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-emerald-100">
                  <CheckCircle className="text-emerald-600" size={20} />
                </div>
                <div>
                  <p className="font-medium text-gray-800">{gstFile.name}</p>
                  <p className="text-sm text-gray-500">
                    GST Data • Ready to upload
                  </p>
                </div>
              </div>
              <button
                onClick={removeGstFile}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-full transition-colors"
                type="button"
              >
                <XCircle size={20} />
              </button>
            </div>
          </div>
        )}

        <p className="muted-text mb-6">
          Supported formats: CSV, XLSX, PDF for financials, and JSON for GST data.
        </p>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className={`primary-btn w-full flex items-center justify-center gap-2 transition-all ${
            !file ? 'opacity-50 cursor-not-allowed' : ''
          } ${loading ? 'animate-pulse' : ''}`}
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              Analyzing...
            </>
          ) : (
            <>
              <UploadCloud size={18} />
              Upload & Analyze
            </>
          )}
        </button>

        {/* ERROR */}
        {error && (
          <div className="mt-4 p-3 bg-rose-50 border border-rose-200 rounded-lg">
            <p className="text-sm text-rose-600 flex items-center gap-2">
              <AlertTriangle size={16} />
              {error}
            </p>
          </div>
        )}

        {/* WARNINGS */}
        {warnings.length > 0 && (
          <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
            <h4 className="text-sm font-semibold text-amber-600 mb-2 flex items-center gap-2">
              <AlertTriangle size={16} />
              Data Warnings
            </h4>
            <ul className="list-disc list-inside text-sm text-amber-700">
              {warnings.map((w, i) => (
                <li key={i}>{w}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Help Text */}
      <div className="mt-8 text-center text-sm text-gray-500 max-w-2xl mx-auto">
        <p>
          Your data is processed securely and never stored. We support standard accounting exports from QuickBooks, Xero, Tally, and other major platforms.
        </p>
      </div>
    </div>
  );
}

export default Upload;