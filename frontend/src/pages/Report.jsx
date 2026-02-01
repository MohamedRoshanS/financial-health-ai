import { useLocation } from "react-router-dom";
import { FileText, Download, Info, Clock, CheckCircle, AlertTriangle } from "lucide-react";
import { useState } from "react";

export default function Report() {
  const location = useLocation();
  const analysis = location.state?.analysis;
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState(null);

  const downloadReport = async () => {
    try {
      setDownloading(true);
      setError(null);

      const res = await fetch("http://127.0.0.1:8000/report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ analysis })
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to generate report: ${res.status} ${errorText}`);
      }

      const blob = await res.blob();
      
      // Create filename from response headers or use default
      const contentDisposition = res.headers.get('Content-Disposition');
      let filename = "financial_health_report.pdf";
      
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="(.+)"/);
        if (match) {
          filename = match[1];
        }
      }

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

    } catch (err) {
      console.error("Download error:", err);
      setError(err.message || "Failed to download report. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  if (!analysis) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-20 text-center">
        <div className="card">
          <AlertTriangle className="w-12 h-12 text-amber-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No Analysis Data</h2>
          <p className="text-gray-600 mb-6">
            Please complete a financial analysis first to generate a report.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-12">
      
      {/* HEADER */}
      <div className="text-center mb-10">
        <FileText className="w-16 h-16 text-indigo-600 mx-auto mb-4" />
        <h1 className="text-3xl font-bold text-gray-900 mb-3">
          Financial Health Report
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Download a comprehensive PDF report with detailed analysis, benchmarks, 
          forecasts, and AI-powered insights for investors and stakeholders.
        </p>
      </div>

      {/* REPORT PREVIEW CARD */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row md:items-center gap-6 mb-6">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Report Preview
            </h3>
            <p className="text-sm text-gray-600">
              Your report will include:
            </p>
            
            <ul className="mt-4 space-y-3">
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Executive summary with overall health score</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Detailed score breakdown by category</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Risk assessment with severity levels</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Industry benchmark comparisons</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Working capital analysis</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>6-month financial forecast</span>
              </li>
              <li className="flex items-center gap-3 text-sm">
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>AI-generated insights & recommendations</span>
              </li>
            </ul>
          </div>

          <div className="md:w-48 flex flex-col items-center justify-center p-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border border-indigo-100">
            <div className="text-5xl font-bold text-indigo-700 mb-2">
              {analysis.score}
            </div>
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              analysis.status === "Healthy" 
                ? "bg-green-100 text-green-800"
                : analysis.status === "Watch" 
                ? "bg-amber-100 text-amber-800"
                : "bg-red-100 text-red-800"
            }`}>
              {analysis.status}
            </div>
            <div className="text-xs text-gray-500 mt-2">Overall Score /100</div>
          </div>
        </div>

        {/* ERROR MESSAGE */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start gap-3">
              <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-medium text-red-800">Download Failed</p>
                <p className="text-sm text-red-600 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* DOWNLOAD BUTTON */}
        <button
          onClick={downloadReport}
          disabled={downloading}
          className="w-full primary-btn flex items-center justify-center gap-2 py-3 text-lg"
        >
          {downloading ? (
            <>
              <Clock className="w-5 h-5 animate-spin" />
              Generating Report...
            </>
          ) : (
            <>
              <Download className="w-5 h-5" />
              Download Full PDF Report
            </>
          )}
        </button>

        {/* INFO SECTION */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-gray-400 mt-0.5 flex-shrink-0" />
            <div>
              <p className="text-sm text-gray-600">
                <span className="font-medium">Note:</span> The report generation may take a few moments as it includes AI-powered insights. 
                The PDF contains all analysis data including working capital metrics, GST compliance status, 
                and bank activity summary. Report is generated in real-time and not stored on our servers.
              </p>
              <p className="text-xs text-gray-500 mt-2">
                Format: PDF | Pages: 3-5 | File size: ~200-500KB
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}