import { useLocation } from "react-router-dom";
import { useState } from "react";
import { Sparkles, Loader2, Info } from "lucide-react";

export default function Insights() {
  const location = useLocation();
  const analysis = location.state?.analysis;

  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      setError(null);

      const res = await fetch("http://127.0.0.1:8000/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ analysis })
      });

      const data = await res.json();
      setInsights(data.insights);
    } catch (err) {
      setError("Failed to generate AI insights. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!analysis) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <p className="text-gray-600">No analysis available.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">

      {/* HEADER */}
      <div className="mb-8">
        <h2 className="section-title flex items-center gap-2">
          <Sparkles size={20} />
          AI Financial Insights
        </h2>
        <p className="muted-text">
          Plain-language interpretation and recommendations based on your
          financial analysis.
        </p>
      </div>

      {/* ACTION CARD */}
      <div className="card mb-8">
        <button
          onClick={fetchInsights}
          disabled={loading}
          className="primary-btn flex items-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Generating Insights...
            </>
          ) : (
            <>
              <Sparkles size={16} />
              Generate AI Insights
            </>
          )}
        </button>

        <div className="mt-4 flex items-start gap-2 text-sm text-gray-500">
          <Info size={16} className="mt-0.5" />
          <p>
            AI explains verified financial metrics only. No numbers are
            recalculated or assumed.
          </p>
        </div>
      </div>

      {/* INSIGHTS OUTPUT */}
      {error && (
        <div className="card mb-6 border-rose-200">
          <p className="text-sm text-rose-600">{error}</p>
        </div>
      )}

      {insights && (
        <div className="card">
          <h3 className="card-title mb-4">Insights & Recommendations</h3>
          <div className="whitespace-pre-wrap text-gray-800 leading-relaxed text-sm">
            {insights}
          </div>
        </div>
      )}
    </div>
  );
}
