def analyze_gst(gst_payload: dict, monthly_df):
    """
    gst_payload expected (minimal):
    {
      "gst_paid": number,
      "gst_due": number,
      "period": "YYYY-MM"
    }
    """

    gst_paid = gst_payload.get("gst_paid", 0)
    gst_due = gst_payload.get("gst_due", 0)

    status = "Compliant"
    risks = []

    if gst_due > gst_paid:
        status = "At Risk"
        risks.append({
            "type": "GST Compliance Risk",
            "severity": "Medium",
            "reason": f"GST due ₹{gst_due - gst_paid} pending"
        })

    return {
        "gst_paid": gst_paid,
        "gst_due": gst_due,
        "status": status,
        "risks": risks
    }
