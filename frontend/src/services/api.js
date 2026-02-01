const API_BASE =
  import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
};

export const analyzeData = async (monthlyData, industry, gstData = null) => {
  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      monthly_data: monthlyData,
      industry,
      gst_data: gstData
    })
  });

  if (!res.ok) throw new Error("Analysis failed");
  return res.json();
};
