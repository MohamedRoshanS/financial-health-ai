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

      {/* ===================== */}
      {/* FINANCIAL HEALTH SCORE */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* SCORE BREAKDOWN */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* WORKING CAPITAL (GAP 3) */}
      {/* ===================== */}
      {result.working_capital && (
        <div className="card">
          <h3 className="card-title mb-4">
            Working Capital Optimization
          </h3>

          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-4">
            <div>
              DSO: <b>{result.working_capital.dso} days</b>
            </div>
            <div>
              DPO: <b>{result.working_capital.dpo} days</b>
            </div>
            <div>
              CCC: <b>{result.working_capital.cash_conversion_cycle} days</b>
            </div>
            <div>
              Risk:{" "}
              <b
                className={
                  result.working_capital.risk_level === "High"
                    ? "text-rose-600"
                    : result.working_capital.risk_level === "Medium"
                    ? "text-amber-600"
                    : "text-emerald-600"
                }
              >
                {result.working_capital.risk_level}
              </b>
            </div>
          </div>

          {result.working_capital.actions?.length > 0 && (
            <ul className="list-disc list-inside text-sm text-gray-700">
              {result.working_capital.actions.map((a, i) => (
                <li key={i}>{a}</li>
              ))}
            </ul>
          )}
        </div>
      )}
      {/* BOOKKEEPING */}
      {result.bookkeeping && (
        <div className="card">
          <h3 className="card-title mb-4">
            Automated Bookkeeping
          </h3>

          <p className="text-sm mb-3">
            Total Expenses: ₹{result.bookkeeping.summary.total_expenses.toLocaleString()}
          </p>

          <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-3 text-sm">
            {result.bookkeeping.ledger.map((row, i) => (
              <div key={i} className="border rounded px-4 py-3">
                <strong>{row.account}</strong>
                <div className="text-gray-600">
                  ₹{row.expense_amount.toLocaleString()}
                </div>
              </div>
            ))}
          </div>

          {result.bookkeeping.issues.length > 0 && (
            <ul className="mt-4 text-xs text-amber-600 list-disc list-inside">
              {result.bookkeeping.issues.map((issue, i) => (
                <li key={i}>{issue}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* GST COMPLIANCE */}
      {result.gst && (
        <div className="card">
          <h3 className="card-title mb-4">
            GST Compliance Status
          </h3>

          <p className="text-sm">
            <strong>Status:</strong>{" "}
            <span
              className={
                result.gst.status === "Compliant"
                  ? "text-emerald-600"
                  : "text-rose-600"
              }
            >
              {result.gst.status}
            </span>
          </p>

          <p className="text-sm mt-2">
            GST Paid: ₹{result.gst.gst_paid} <br />
            GST Due: ₹{result.gst.gst_due}
          </p>
        </div>
      )}
      {/* BANK INTEGRATION */}
      {result.bank_summary && (
        <div className="card">
          <h3 className="card-title mb-4">
            Bank Account Activity
          </h3>

          <div className="grid sm:grid-cols-3 gap-4 text-sm">
            <div>
              <strong>Inflows</strong>
              <div className="text-emerald-600">
                ₹{result.bank_summary.inflows.toLocaleString()}
              </div>
            </div>

            <div>
              <strong>Outflows</strong>
              <div className="text-rose-600">
                ₹{result.bank_summary.outflows.toLocaleString()}
              </div>
            </div>

            <div>
              <strong>Transactions</strong>
              <div>{result.bank_summary.transaction_count}</div>
            </div>
          </div>
        </div>
      )}

      {/* ===================== */}
      {/* ACTION BUTTONS */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* RISKS */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* WARNINGS */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* BENCHMARKS */}
      {/* ===================== */}
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

      {/* ===================== */}
      {/* FORECAST */}
      {/* ===================== */}
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
