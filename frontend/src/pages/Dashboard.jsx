import { useLocation, useNavigate } from "react-router-dom";
import {
  Activity,
  TrendingUp,
  AlertTriangle,
  ShieldCheck,
  Sparkles,
  FileDown
} from "lucide-react";

export default function Dashboard() {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state?.analysis;
  const warnings = location.state?.warnings || [];

  if (!result) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <p className="text-gray-600">
          No analysis data available. Please upload a file.
        </p>
      </div>
    );
  }

  const statusBadge =
    result.status === "Healthy"
      ? "badge-success"
      : result.status === "Watch"
      ? "badge-warning"
      : "badge-danger";

  return (
    <div className="max-w-6xl mx-auto px-6 py-10 space-y-8">

      {/* HEADER / SCORE */}
      <div className="card flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div>
          <h2 className="section-title">Financial Health Overview</h2>
          <p className="muted-text">
            Overall performance based on uploaded financial data
          </p>
        </div>

        <div className="text-right">
          <div className="text-4xl font-bold text-gray-900">
            {result.score} / 100
          </div>
          <span className={`${statusBadge} mt-2 inline-block`}>
            {result.status}
          </span>
        </div>
      </div>

      {/* SCORE BREAKDOWN */}
      <div className="card">
        <h3 className="card-title mb-4 flex items-center gap-2">
          <Activity size={18} />
          Score Breakdown
        </h3>

        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-4 text-sm">
          {Object.entries(result.breakdown).map(([key, value]) => (
            <div
              key={key}
              className="flex justify-between rounded-lg border border-gray-200 px-4 py-3"
            >
              <span className="text-gray-600">
                {key.replace("_", " ").toUpperCase()}
              </span>
              <span className="font-semibold">{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ACTIONS */}
      <div className="flex flex-wrap gap-4">
        <button
          onClick={() =>
            navigate("/insights", { state: { analysis: result } })
          }
          className="primary-btn flex items-center gap-2"
        >
          <Sparkles size={16} />
          Generate AI Insights
        </button>

        <button
          onClick={() =>
            navigate("/report", { state: { analysis: result } })
          }
          className="secondary-btn flex items-center gap-2"
        >
          <FileDown size={16} />
          Download PDF Report
        </button>
      </div>

      {/* RISKS */}
      <div className="card">
        <h3 className="card-title mb-4 flex items-center gap-2">
          <AlertTriangle size={18} />
          Identified Financial Risks
        </h3>

        {result.risks.length === 0 ? (
          <p className="text-sm text-emerald-600 flex items-center gap-2">
            <ShieldCheck size={16} />
            No major risks detected.
          </p>
        ) : (
          <ul className="space-y-2 text-sm">
            {result.risks.map((risk, index) => (
              <li key={index}>
                <strong>{risk.type}</strong> ({risk.severity}) — {risk.reason}
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* WARNINGS */}
      {warnings.length > 0 && (
        <div className="card">
          <h3 className="card-title mb-3 text-amber-600">
            Data Warnings
          </h3>
          <ul className="list-disc list-inside text-sm text-gray-700">
            {warnings.map((w, i) => (
              <li key={i}>{w}</li>
            ))}
          </ul>
        </div>
      )}

      {/* BENCHMARKS */}
      <div className="card">
        <h3 className="card-title mb-4 flex items-center gap-2">
          <TrendingUp size={18} />
          Industry Benchmark Comparison
        </h3>

        <table className="table-base">
          <thead>
            <tr>
              <th>Metric</th>
              <th>Your Business</th>
              <th>Industry Avg</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(result.benchmarks).map(([metric, data]) => (
              <tr key={metric}>
                <td>{metric.replace("_", " ")}</td>
                <td>{data.business}</td>
                <td>{data.industry_avg}</td>
                <td
                  className={
                    data.status === "Better"
                      ? "text-emerald-600 font-medium"
                      : "text-rose-600 font-medium"
                  }
                >
                  {data.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* FORECAST */}
      <div className="card">
        <h3 className="card-title mb-4">Financial Forecast</h3>

        <p className="text-sm mb-4">
          <strong>Estimated Cash Runway:</strong>{" "}
          {result.forecast.cash_runway_months === "Stable"
            ? "Stable"
            : `${result.forecast.cash_runway_months} months`}
        </p>

        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-3 text-sm">
          {result.forecast.revenue_forecast_6_months.map((rev, idx) => (
            <div
              key={idx}
              className="rounded-lg border border-gray-200 px-4 py-3"
            >
              Month {idx + 1}: ₹{rev.toLocaleString()}
            </div>
          ))}
        </div>

        <p className="mt-6 text-xs text-gray-500 italic">
          *Forecasts and insights are AI-assisted and indicative, based on
          uploaded historical financial data.
        </p>
      </div>
    </div>
  );
}
