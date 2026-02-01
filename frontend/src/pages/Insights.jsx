import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import { 
  Sparkles, 
  Loader2, 
  Info, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle, 
  Lightbulb,
  Target,
  Calendar,
  DollarSign
} from "lucide-react";

export default function Insights() {
  const location = useLocation();
  const analysis = location.state?.analysis;

  const [insights, setInsights] = useState(null);
  const [formattedInsights, setFormattedInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchInsights = async () => {
    try {
      setLoading(true);
      setError(null);
      setInsights(null);

      const res = await fetch("http://127.0.0.1:8000/insights", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ analysis })
      });

      if (!res.ok) {
        throw new Error(`API responded with status: ${res.status}`);
      }

      const data = await res.json();
      setInsights(data.insights);
      formatInsights(data.insights);
    } catch (err) {
      console.error("Error fetching insights:", err);
      setError(err.message || "Failed to generate AI insights. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Format raw text into structured components
  const formatInsights = (rawText) => {
    if (!rawText) return;

    // Split by common section markers
    const sections = rawText.split(/\n\n+/);
    
    const formatted = {
      summary: "",
      positives: [],
      concerns: [],
      recommendations: [],
      compliance: [],
      rawText: rawText
    };

    let currentSection = 'summary';
    
    sections.forEach(section => {
      const trimmed = section.trim();
      if (!trimmed) return;

      // Detect section headers
      if (trimmed.toLowerCase().includes('positive') || trimmed.toLowerCase().includes('going well')) {
        currentSection = 'positives';
      } else if (trimmed.toLowerCase().includes('attention') || trimmed.toLowerCase().includes('concern') || trimmed.toLowerCase().includes('risk')) {
        currentSection = 'concerns';
      } else if (trimmed.toLowerCase().includes('recommend') || trimmed.toLowerCase().includes('action')) {
        currentSection = 'recommendations';
      } else if (trimmed.toLowerCase().includes('gst') || trimmed.toLowerCase().includes('compliance')) {
        currentSection = 'compliance';
      }

      // Process bullets/numbered lists
      if (trimmed.match(/^[•\-*]\s/) || trimmed.match(/^\d+\.\s/)) {
        const items = trimmed.split('\n').map(item => item.replace(/^[•\-*\d\.]\s+/, '').trim());
        
        if (currentSection === 'positives') {
          formatted.positives = [...formatted.positives, ...items];
        } else if (currentSection === 'concerns') {
          formatted.concerns = [...formatted.concerns, ...items];
        } else if (currentSection === 'recommendations') {
          formatted.recommendations = [...formatted.recommendations, ...items];
        } else if (currentSection === 'compliance') {
          formatted.compliance = [...formatted.compliance, ...items];
        }
      } else if (currentSection === 'summary') {
        formatted.summary += (formatted.summary ? '\n\n' : '') + trimmed;
      }
    });

    setFormattedInsights(formatted);
  };

  // Auto-fetch insights when component mounts
  useEffect(() => {
    if (analysis && !insights) {
      fetchInsights();
    }
  }, [analysis]);

  if (!analysis) {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <p className="text-gray-600">No analysis available. Please go back to dashboard.</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 sm:py-10">

      {/* HEADER */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-600" />
            AI Financial Insights
          </h2>
          <div className="flex items-center gap-2">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              analysis.status === "Healthy" 
                ? "bg-green-100 text-green-800"
                : analysis.status === "Watch" 
                ? "bg-amber-100 text-amber-800"
                : "bg-red-100 text-red-800"
            }`}>
              {analysis.status} ({analysis.score}/100)
            </span>
          </div>
        </div>
        <p className="text-gray-600 text-sm sm:text-base">
          Personalized analysis and recommendations based on your complete financial data
        </p>
      </div>

      {/* LOADING STATE */}
      {loading && (
        <div className="card mb-8 animate-pulse">
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
              <p className="text-gray-600">Generating AI-powered insights...</p>
              <p className="text-xs text-gray-500 mt-2">Analyzing all financial metrics and patterns</p>
            </div>
          </div>
        </div>
      )}

      {/* ERROR STATE */}
      {error && (
        <div className="card mb-8 border-red-200 bg-red-50">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
            <div>
              <p className="font-medium text-red-800">Failed to generate insights</p>
              <p className="text-sm text-red-600 mt-1">{error}</p>
              <button 
                onClick={fetchInsights}
                className="mt-3 px-4 py-2 bg-red-100 text-red-700 rounded-md text-sm font-medium hover:bg-red-200 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      )}

      {/* FORMATTED INSIGHTS */}
      {formattedInsights && !loading && (
        <div className="space-y-6">
          {/* EXECUTIVE SUMMARY */}
          {formattedInsights.summary && (
            <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
              <h3 className="card-title mb-3 flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-blue-600" />
                Executive Summary
              </h3>
              <div className="text-gray-800 leading-relaxed whitespace-pre-line">
                {formattedInsights.summary}
              </div>
            </div>
          )}

          {/* POSITIVES & CONCERNS SIDE BY SIDE */}
          {(formattedInsights.positives.length > 0 || formattedInsights.concerns.length > 0) && (
            <div className="grid md:grid-cols-2 gap-6">
              {/* POSITIVES */}
              {formattedInsights.positives.length > 0 && (
                <div className="card border-green-200 bg-green-50">
                  <h3 className="card-title mb-3 flex items-center gap-2 text-green-800">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    What's Going Well
                  </h3>
                  <ul className="space-y-3">
                    {formattedInsights.positives.map((item, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <CheckCircle className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-800">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* CONCERNS */}
              {formattedInsights.concerns.length > 0 && (
                <div className="card border-amber-200 bg-amber-50">
                  <h3 className="card-title mb-3 flex items-center gap-2 text-amber-800">
                    <AlertTriangle className="w-5 h-5 text-amber-600" />
                    Areas Needing Attention
                  </h3>
                  <ul className="space-y-3">
                    {formattedInsights.concerns.map((item, index) => (
                      <li key={index} className="flex items-start gap-3">
                        <AlertTriangle className="w-4 h-4 text-amber-500 mt-0.5 flex-shrink-0" />
                        <span className="text-sm text-gray-800">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* ACTIONABLE RECOMMENDATIONS */}
          {formattedInsights.recommendations.length > 0 && (
            <div className="card border-purple-200 bg-purple-50">
              <h3 className="card-title mb-4 flex items-center gap-2 text-purple-800">
                <Target className="w-5 h-5 text-purple-600" />
                Actionable Recommendations
              </h3>
              <div className="grid sm:grid-cols-2 gap-4">
                {formattedInsights.recommendations.map((rec, index) => (
                  <div 
                    key={index} 
                    className="bg-white rounded-lg p-4 border border-gray-200 hover:border-purple-300 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">
                        {index + 1}
                      </div>
                      <div>
                        <h4 className="font-medium text-gray-900 mb-1">Step {index + 1}</h4>
                        <p className="text-sm text-gray-700">{rec}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* COMPLIANCE NOTES */}
          {formattedInsights.compliance.length > 0 && (
            <div className="card border-blue-200">
              <h3 className="card-title mb-3 flex items-center gap-2">
                <Calendar className="w-5 h-5 text-blue-600" />
                Compliance & Tax Notes
              </h3>
              <ul className="space-y-2">
                {formattedInsights.compliance.map((note, index) => (
                  <li key={index} className="text-sm text-gray-700 pl-4 border-l-2 border-blue-300 py-1">
                    {note}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* RAW TEXT FALLBACK */}
          {(!formattedInsights.summary && !formattedInsights.positives.length && 
            !formattedInsights.recommendations.length) && formattedInsights.rawText && (
            <div className="card">
              <h3 className="card-title mb-4">Insights & Recommendations</h3>
              <div className="whitespace-pre-wrap text-gray-800 leading-relaxed text-sm">
                {formattedInsights.rawText}
              </div>
            </div>
          )}

          {/* DISCLAIMER */}
          <div className="text-center text-xs text-gray-500 italic pt-4 border-t border-gray-200">
            <Info className="w-4 h-4 inline-block mr-1 mb-0.5" />
            AI insights are generated based on your financial data. For critical decisions, consult with a certified financial advisor.
          </div>
        </div>
      )}

      {/* ACTION BUTTON - Only show if no insights loaded yet */}
      {!loading && !insights && !error && (
        <div className="card mb-8 text-center">
          <div className="mb-4">
            <Sparkles className="w-12 h-12 text-blue-500 mx-auto mb-3" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Ready for AI Insights</h3>
            <p className="text-gray-600 text-sm max-w-md mx-auto">
              Generate personalized financial analysis based on your complete business data
            </p>
          </div>
          <button
            onClick={fetchInsights}
            disabled={loading}
            className="primary-btn flex items-center justify-center gap-2 mx-auto px-8 py-3"
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
          <div className="mt-4 flex items-center justify-center gap-2 text-xs text-gray-500">
            <Info size={14} />
            <p>Uses all financial data: Score, Benchmarks, GST, Working Capital, and Bank activity</p>
          </div>
        </div>
      )}
    </div>
  );
}