import { useLocation } from "react-router-dom";
import { FileText, Download, Info } from "lucide-react";

export default function Report() {
  const location = useLocation();
  const analysis = location.state?.analysis;

  const downloadReport = async () => {
    const res = await fetch("http://127.0.0.1:8000/report", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ analysis })
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "financial_health_report.pdf";
    a.click();
  };

  if (!analysis) {
    return (
      <div className="max-w-3xl mx-auto px-6 py-20 text-center">
        <p className="text-gray-600">
          No analysis available. Please upload data first.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <div className="card text-center">
        
        {/* HEADER */}
        <div className="flex justify-center mb-4">
          <FileText size={32} className="text-indigo-600" />
        </div>

        <h2 className="section-title mb-3">
          Investor-Ready Financial Report
        </h2>

        <p className="muted-text mb-8">
          Download a professionally formatted PDF summarizing your financial
          health score, risks, benchmarks, forecasts, and AI insights.
        </p>

        {/* ACTION */}
        <button
          onClick={downloadReport}
          className="primary-btn w-full flex items-center justify-center gap-2"
        >
          <Download size={18} />
          Download PDF Report
        </button>

        {/* INFO */}
        <div className="mt-6 flex items-start gap-2 text-sm text-gray-500 text-left">
          <Info size={16} className="mt-0.5" />
          <p>
            The report is generated directly from your uploaded data and AI
            insights. No information is stored after download.
          </p>
        </div>
      </div>
    </div>
  );
}
