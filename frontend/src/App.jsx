import { useEffect, useState, useRef } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

const API = "https://https://fintrack-ai-ugyq.onrender.com/";

const COLORS = [
  "#00d4ff",
  "#00ff88",
  "#ff4d6d",
  "#ffd166",
  "#8338ec",
  "#06d6a0"
];

// ================= LOAD SCRIPT FIX =================

const loadScript = (src) => {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(`script[src="${src}"]`);

    if (existing) {
      resolve();
      return;
    }

    const script = document.createElement("script");

    script.src = src;
    script.async = true;

    script.onload = resolve;
    script.onerror = reject;

    document.body.appendChild(script);
  });
};

function App() {
  const [expenses, setExpenses] = useState([]);
  const [budget, setBudget] = useState(50000);
  const [lightMode, setLightMode] = useState(false);
  const [exporting, setExporting] = useState(false);

  const dashboardRef = useRef(null);

  const [ai, setAi] = useState({
    prediction: 0,
    forecast: { trend: "" },
    risk: "LOW",
    advisor: ""
  });

  const [form, setForm] = useState({
    amount: "",
    category: "food",
    date: ""
  });

  // ================= FETCH =================

  const fetchExpenses = async () => {
    try {
      const res = await axios.get(`${API}/expense/all`);
      setExpenses(res.data || []);
    } catch {
      setExpenses([]);
    }
  };

  const fetchAI = async () => {
    try {
      const res = await axios.get(`${API}/ai/dashboard`);
      setAi(res.data);
    } catch {
      setAi({
        prediction: 0,
        forecast: { trend: "AI offline" },
        risk: "UNKNOWN",
        advisor: "Backend not running"
      });
    }
  };

  useEffect(() => {
    fetchExpenses();
    fetchAI();
  }, []);

  // ================= CALCULATIONS =================

  const total = expenses.reduce(
    (s, e) => s + Number(e.amount || 0),
    0
  );

  const isOverBudget = total > budget;

  // ================= PIE DATA =================

  const pieData = Object.values(
    expenses.reduce((acc, e) => {
      acc[e.category] = acc[e.category] || {
        name: e.category,
        value: 0
      };

      acc[e.category].value += Number(e.amount || 0);

      return acc;
    }, {})
  );

  // ================= LINE DATA =================

  const lineData = Object.values(
    expenses.reduce((acc, e) => {
      const month = e.date
        ? new Date(e.date).toLocaleString("default", {
            month: "short",
            year: "numeric"
          })
        : "Unknown";

      acc[month] = acc[month] || {
        month,
        amount: 0
      };

      acc[month].amount += Number(e.amount || 0);

      return acc;
    }, {})
  );

  // ================= SORT FIX =================

  lineData.sort(
    (a, b) =>
      new Date(`1 ${a.month}`) -
      new Date(`1 ${b.month}`)
  );

  // ================= ADD =================

  const addExpense = async () => {
    // ================= VALIDATION FIX =================

    if (
      !form.amount ||
      Number(form.amount) <= 0 ||
      !form.date
    )
      return;

    try {
      await axios.post(`${API}/expense/add`, {
        amount: Number(form.amount),
        category: form.category,
        date: form.date
      });

      setForm({
        amount: "",
        category: "food",
        date: ""
      });

      fetchExpenses();
      fetchAI();
    } catch (err) {
      console.log(err);
    }
  };

  // ================= CLEAR =================

  const clearAll = async () => {
    try {
      await axios.delete(`${API}/expense/clear`);

      setExpenses([]);

      fetchAI();
    } catch (err) {
      console.log(err);
    }
  };

  // ================= PDF EXPORT =================

  const exportPDF = async () => {
    setExporting(true);

    try {
      await loadScript(
        "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
      );

      const { jsPDF } = window.jspdf;

      const doc = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4"
      });

      const pageW = doc.internal.pageSize.getWidth();
      const pageH = doc.internal.pageSize.getHeight();

      const margin = 14;
      let y = margin;

      // ================= BACKGROUND =================

      doc.setFillColor(
        lightMode ? 245 : 2,
        lightMode ? 248 : 6,
        lightMode ? 255 : 23
      );

      doc.rect(0, 0, pageW, pageH, "F");

      // ================= HEADER =================

      doc.setFillColor(8, 145, 178);

      doc.roundedRect(
        margin,
        y,
        pageW - margin * 2,
        24,
        4,
        4,
        "F"
      );

      doc.setFont("helvetica", "bold");
      doc.setFontSize(24);

      doc.setTextColor(255, 255, 255);

      doc.text("FinTrack AI", margin + 8, y + 10);

      doc.setFontSize(11);

      doc.setTextColor(220, 240, 255);

      doc.text(
        "AI Powered Smart Financial Intelligence Platform",
        margin + 8,
        y + 18
      );

      y += 36;

      // ================= REPORT INFO =================

      doc.setFont("helvetica", "normal");
      doc.setFontSize(10);

      doc.setTextColor(120, 120, 120);

      doc.text(
        `Generated on: ${new Date().toLocaleString()}`,
        margin,
        y
      );

      y += 10;

      // ================= SUMMARY CARD =================

      doc.setFillColor(15, 23, 42);

      doc.roundedRect(
        margin,
        y,
        pageW - margin * 2,
        58,
        4,
        4,
        "F"
      );

      doc.setFont("helvetica", "bold");
      doc.setFontSize(15);

      doc.setTextColor(0, 212, 255);

      doc.text("Financial Summary", margin + 6, y + 10);

      y += 20;

      const summaryRows = [
        ["Monthly Budget", `Rs. ${budget.toLocaleString()}`],
        ["Total Spent", `Rs. ${total.toLocaleString()}`],
        ["Transactions", `${expenses.length}`],
        [
          "Budget Status",
          isOverBudget ? "OVER BUDGET" : "Within Budget"
        ],
        [
          "AI Prediction",
          `Rs. ${Number(ai.prediction || 0).toLocaleString()}`
        ],
        ["Risk Level", ai.risk || "—"],
        ["AI Trend", ai.forecast?.trend || "—"]
      ];

      summaryRows.forEach(([label, value], i) => {
        const rowY = y + i * 5.5;

        doc.setFont("helvetica", "normal");
        doc.setFontSize(10);

        doc.setTextColor(180, 200, 220);

        doc.text(`${label}:`, margin + 8, rowY);

        doc.setFont("helvetica", "bold");

        doc.setTextColor(255, 255, 255);

        doc.text(String(value), margin + 65, rowY);
      });

      y += 48;

      // ================= CATEGORY BREAKDOWN =================

      y += 10;

      doc.setFont("helvetica", "bold");
      doc.setFontSize(15);

      doc.setTextColor(0, 255, 136);

      doc.text("Category Breakdown", margin, y);

      y += 10;

      pieData.forEach((cat, i) => {
        const percent =
          total > 0
            ? ((cat.value / total) * 100).toFixed(1)
            : "0.0";

        if (i % 2 === 0) {
          doc.setFillColor(20, 28, 45);
        } else {
          doc.setFillColor(12, 18, 30);
        }

        doc.roundedRect(
          margin,
          y - 5,
          pageW - margin * 2,
          8,
          2,
          2,
          "F"
        );

        doc.setFont("helvetica", "normal");

        doc.setTextColor(220, 220, 220);

        doc.setFontSize(10);

        doc.text(cat.name.toUpperCase(), margin + 4, y);

        doc.setFont("helvetica", "bold");

        doc.setTextColor(255, 255, 255);

        doc.text(
          `Rs. ${cat.value.toLocaleString()} (${percent}%)`,
          margin + 70,
          y
        );

        y += 10;
      });

      // ================= TRANSACTION TABLE =================

      y += 10;

      doc.setFont("helvetica", "bold");
      doc.setFontSize(15);

      doc.setTextColor(131, 56, 236);

      doc.text("All Transactions", margin, y);

      y += 10;

      // ================= TABLE HEADER =================

      doc.setFillColor(30, 41, 59);

      doc.rect(
        margin,
        y - 5,
        pageW - margin * 2,
        9,
        "F"
      );

      doc.setTextColor(0, 212, 255);

      doc.setFontSize(10);

      doc.text("#", margin + 3, y);
      doc.text("Date", margin + 15, y);
      doc.text("Category", margin + 60, y);
      doc.text("Amount", margin + 120, y);

      y += 10;

      expenses.forEach((e, i) => {
        // ================= PAGE BREAK =================

        if (y > pageH - 20) {
          doc.addPage();

          doc.setFillColor(
            lightMode ? 245 : 2,
            lightMode ? 248 : 6,
            lightMode ? 255 : 23
          );

          doc.rect(0, 0, pageW, pageH, "F");

          y = margin;

          doc.setFillColor(30, 41, 59);

          doc.rect(
            margin,
            y - 5,
            pageW - margin * 2,
            9,
            "F"
          );

          doc.setTextColor(0, 212, 255);

          doc.setFontSize(10);

          doc.text("#", margin + 3, y);
          doc.text("Date", margin + 15, y);
          doc.text("Category", margin + 60, y);
          doc.text("Amount", margin + 120, y);

          y += 10;
        }

        // ================= ZEBRA STRIPING =================

        if (i % 2 === 0) {
          doc.setFillColor(15, 23, 42);
        } else {
          doc.setFillColor(10, 15, 28);
        }

        doc.rect(
          margin,
          y - 5,
          pageW - margin * 2,
          8,
          "F"
        );

        doc.setFont("helvetica", "normal");

        doc.setTextColor(220, 220, 220);

        doc.text(String(i + 1), margin + 3, y);

        doc.text(
          e.date
            ? new Date(e.date).toLocaleDateString()
            : "—",
          margin + 15,
          y
        );

        doc.text(
          e.category
            ? e.category.charAt(0).toUpperCase() +
                e.category.slice(1)
            : "—",
          margin + 60,
          y
        );

        doc.setFont("helvetica", "bold");

        doc.setTextColor(0, 255, 136);

        doc.text(
          `Rs. ${Number(e.amount).toLocaleString()}`,
          margin + 120,
          y
        );

        y += 9;
      });

      // ================= FOOTER =================

      doc.setFont("helvetica", "normal");
      doc.setFontSize(9);

      doc.setTextColor(120, 120, 120);

      doc.text(
        "FinTrack AI — Secure Financial Analytics",
        margin,
        pageH - 8
      );

      // ================= SAVE =================

      doc.save("FinTrack_AI_Report.pdf");
    } catch (err) {
      console.error("PDF export failed:", err);

      alert("PDF export failed. Please try again.");
    }

    setExporting(false);
  };

  // ================= THEME =================

  const lm = lightMode;

  const themeGlass = lm
    ? {
        background: "rgba(255,255,255,0.72)",
        backdropFilter: "blur(22px)",
        WebkitBackdropFilter: "blur(22px)",
        border: "1px solid rgba(0,0,0,0.08)",
        boxShadow:
          "0 8px 32px rgba(0,0,0,0.10), inset 0 1px 1px rgba(255,255,255,0.8)",
        transition: "all 0.35s ease"
      }
    : {
        background: "rgba(255,255,255,0.06)",
        backdropFilter: "blur(22px)",
        WebkitBackdropFilter: "blur(22px)",
        border: "1px solid rgba(255,255,255,0.08)",
        boxShadow:
          "0 8px 32px rgba(0,0,0,0.35), inset 0 1px 1px rgba(255,255,255,0.08)",
        transition: "all 0.35s ease"
      };

  const themeText = lm ? "#1e293b" : "#fff";

  const themeSub = lm ? "#64748b" : "#94a3b8";

  const themeSubLight = lm ? "#475569" : "#cbd5e1";

  const themeBg = lm
    ? "linear-gradient(135deg,#e0f2fe,#f0fdf4,#f8fafc)"
    : "linear-gradient(135deg,#020617,#0f172a,#111827)";

  const themeInput = lm
    ? {
        flex: 1,
        width: "100%",
        minWidth: "140px",
        padding: "15px 18px",
        borderRadius: "16px",
        border: "1px solid rgba(0,0,0,0.12)",
        background: "rgba(255,255,255,0.85)",
        color: "#1e293b",
        outline: "none",
        fontSize: "15px",
        transition: "all 0.3s ease",
        backdropFilter: "blur(12px)"
      }
    : styles.input;

  return (
    <div
      ref={dashboardRef}
      style={{
        ...styles.page,
        background: themeBg,
        color: themeText
      }}
    >
      <div style={styles.blur1}></div>
      <div style={styles.blur2}></div>
      <div style={styles.blur3}></div>

      {/* HEADER */}

      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>💰 FinTrack AI</h1>

          <p
            style={{
              ...styles.subtitle,
              color: themeSub
            }}
          >
            AI Powered Smart Financial Intelligence Platform
          </p>
        </div>

        <div
          style={{
            display: "flex",
            gap: "12px",
            flexWrap: "wrap",
            alignItems: "center"
          }}
        >
          {/* THEME */}

          <button
            style={{
              ...styles.toggleBtn,
              background: lm
                ? "linear-gradient(135deg,#fbbf24,#f59e0b)"
                : "linear-gradient(135deg,#334155,#1e293b)"
            }}
            onClick={() => setLightMode(!lm)}
          >
            {lm ? "🌙 Dark" : "☀️ Light"}
          </button>

          {/* PDF BUTTON FIX */}

          <button
            style={styles.pdfBtn}
            onClick={exportPDF}
            disabled={exporting}
          >
            {exporting
              ? "Generating..."
              : "📄 Export PDF"}
          </button>

          {/* CLEAR */}

          <button
            style={styles.dangerBtn}
            onClick={clearAll}
          >
            🧹 Clear All
          </button>
        </div>
      </div>

      {/* ALERT */}

      {isOverBudget && (
        <div style={styles.alert}>
          🔔 Budget exceeded — optimize your spending
          immediately
        </div>
      )}

      {/* BUDGET */}

      <div
        style={{
          ...styles.budgetCard,
          ...themeGlass
        }}
      >
        <div>
          <p
            style={{
              ...styles.smallLabel,
              color: themeSub
            }}
          >
            Monthly Budget
          </p>

          <h2
            style={{
              ...styles.budgetValue,
              color: themeText
            }}
          >
            ₹{budget.toLocaleString()}
          </h2>
        </div>

        <input
          type="number"
          value={budget}
          onChange={(e) =>
            setBudget(Number(e.target.value))
          }
          style={themeInput}
        />
      </div>

      {/* STATS */}

      <div style={styles.grid}>
        {/* TOTAL */}

        <div
          style={{
            ...styles.card,
            ...themeGlass
          }}
        >
          <div style={styles.shine}></div>

          <p
            style={{
              ...styles.smallLabel,
              color: themeSub
            }}
          >
            Total Spent
          </p>

          <h2
            style={{
              ...styles.cardValue,
              color: themeText
            }}
          >
            ₹{total.toLocaleString()}
          </h2>

          <p
            style={{
              ...styles.cardSub,
              color: themeSubLight
            }}
          >
            Complete spending overview
          </p>
        </div>

        {/* TRANSACTIONS */}

        <div
          style={{
            ...styles.card,
            ...themeGlass
          }}
        >
          <div style={styles.shine}></div>

          <p
            style={{
              ...styles.smallLabel,
              color: themeSub
            }}
          >
            Transactions
          </p>

          <h2
            style={{
              ...styles.cardValue,
              color: themeText
            }}
          >
            {expenses.length}
          </h2>

          <p
            style={{
              ...styles.cardSub,
              color: themeSubLight
            }}
          >
            Financial activities recorded
          </p>
        </div>

        {/* AI */}

        <div style={styles.aiCard}>
          <div style={styles.aiGlow}></div>

          <div style={styles.aiTop}>
            <span>🤖 AI Forecast</span>

            <span style={styles.liveDot}></span>
          </div>

          <h2 style={styles.aiValue}>
            ₹
            {Number(
              ai.prediction || 0
            ).toLocaleString()}
          </h2>

          <p style={styles.aiTrend}>
            {ai.forecast?.trend}
          </p>

          <div style={styles.aiBottom}>
            <div>
              <p style={styles.aiMiniLabel}>Risk</p>

              <h4>{ai.risk}</h4>
            </div>

            <div>
              <p style={styles.aiMiniLabel}>
                Advisor
              </p>

              <h4>{ai.advisor}</h4>
            </div>
          </div>
        </div>
      </div>

      {/* CHARTS */}

      <div style={styles.chartGrid}>
        {/* PIE */}

        <div
          style={{
            ...styles.chartCard,
            ...themeGlass
          }}
        >
          <div style={styles.shine}></div>

          <div style={styles.chartHeader}>
            <h3 style={{ color: themeText }}>
              📊 Spending Categories
            </h3>
          </div>

          <ResponsiveContainer
            width="100%"
            height={320}
          >
            <PieChart>
              <Pie
                data={
                  pieData.length
                    ? pieData
                    : [{ name: "Empty", value: 1 }]
                }
                dataKey="value"
                nameKey="name"
                outerRadius={110}
                innerRadius={55}
                paddingAngle={5}
              >
                {(pieData.length
                  ? pieData
                  : [{ name: "Empty", value: 1 }]
                ).map((_, i) => (
                  <Cell
                    key={i}
                    fill={
                      COLORS[i % COLORS.length]
                    }
                  />
                ))}
              </Pie>

              <Tooltip
                contentStyle={{
                  background: lm
                    ? "#fff"
                    : "#0f172a",
                  border:
                    "1px solid rgba(0,212,255,0.3)",
                  borderRadius: "12px",
                  color: lm
                    ? "#1e293b"
                    : "#fff"
                }}
                labelStyle={{
                  color: lm
                    ? "#1e293b"
                    : "#fff"
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* LINE */}

        <div
          style={{
            ...styles.chartCard,
            ...themeGlass
          }}
        >
          <div style={styles.shine}></div>

          <div style={styles.chartHeader}>
            <h3 style={{ color: themeText }}>
              📈 Monthly Expense Trend
            </h3>
          </div>

          <ResponsiveContainer
            width="100%"
            height={320}
          >
            <LineChart data={lineData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={
                  lm
                    ? "rgba(0,0,0,0.1)"
                    : "rgba(255,255,255,0.08)"
                }
              />

              <XAxis
                dataKey="month"
                stroke={
                  lm ? "#64748b" : "#aaa"
                }
              />

              <YAxis
                stroke={
                  lm ? "#64748b" : "#aaa"
                }
              />

              <Tooltip
                contentStyle={{
                  background: lm
                    ? "#fff"
                    : "#0f172a",
                  border:
                    "1px solid rgba(0,212,255,0.3)",
                  borderRadius: "12px",
                  color: lm
                    ? "#1e293b"
                    : "#fff"
                }}
                labelStyle={{
                  color: lm
                    ? "#1e293b"
                    : "#fff"
                }}
              />

              <Line
                type="monotone"
                dataKey="amount"
                stroke="#00d4ff"
                strokeWidth={4}
                dot={{ r: 5 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* INPUT */}

      <div
        style={{
          ...styles.inputCard,
          ...themeGlass
        }}
      >
        <input
          type="number"
          placeholder="Enter Amount"
          value={form.amount}
          onChange={(e) =>
            setForm({
              ...form,
              amount: e.target.value
            })
          }
          style={themeInput}
        />

        <select
          value={form.category}
          onChange={(e) =>
            setForm({
              ...form,
              category: e.target.value
            })
          }
          style={themeInput}
        >
          <option>food</option>
          <option>transport</option>
          <option>education</option>
          <option>health</option>
          <option>shopping</option>
          <option>bill</option>
        </select>

        <input
          type="date"
          value={form.date}
          onChange={(e) =>
            setForm({
              ...form,
              date: e.target.value
            })
          }
          style={themeInput}
        />

        <button
          style={styles.addBtn}
          onClick={addExpense}
        >
          + Add Expense
        </button>
      </div>

      {/* TRANSACTIONS */}

      <div style={styles.transactionSection}>
        <div style={styles.sectionTop}>
          <h3 style={{ color: themeText }}>
            Recent Transactions
          </h3>
        </div>

        {expenses.length === 0 ? (
          <div
            style={{
              ...styles.empty,
              ...themeGlass,
              color: themeText
            }}
          >
            No transactions added yet
          </div>
        ) : (
          expenses.map((e, i) => (
            <div
              key={`${e.date}-${e.amount}-${i}`}
              style={{
                ...styles.transactionItem,
                ...themeGlass
              }}
            >
              <div>
                <h4
                  style={{
                    ...styles.amount,
                    color: themeText
                  }}
                >
                  ₹
                  {Number(
                    e.amount
                  ).toLocaleString()}
                </h4>

                <p
                  style={{
                    ...styles.category,
                    color: themeSub
                  }}
                >
                  {e.category}
                </p>
              </div>

              <div
                style={{
                  ...styles.date,
                  color: themeSubLight
                }}
              >
                {e.date
                  ? new Date(
                      e.date
                    ).toLocaleDateString(
                      "en-IN",
                      {
                        day: "2-digit",
                        month: "short",
                        year: "numeric"
                      }
                    )
                  : "No Date"}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;

// ================= STYLES =================

const styles = {
  page: {
    minHeight: "100vh",
    width: "100%",
    maxWidth: "100vw",
    overflowX: "hidden",
    overflowY: "auto",
    padding: "clamp(14px,3vw,24px)",
    paddingBottom: "60px",
    color: "#fff",
    fontFamily: "'Inter', sans-serif",
    position: "relative",
    boxSizing: "border-box",
    scrollBehavior: "smooth"
  },

  blur1: {
    position: "absolute",
    width: "320px",
    height: "320px",
    background: "#00d4ff",
    filter: "blur(180px)",
    top: "-120px",
    left: "-120px",
    opacity: 0.18
  },

  blur2: {
    position: "absolute",
    width: "320px",
    height: "320px",
    background: "#00ff88",
    filter: "blur(180px)",
    bottom: "-120px",
    right: "-120px",
    opacity: 0.14
  },

  blur3: {
    position: "absolute",
    width: "250px",
    height: "250px",
    background: "#8338ec",
    filter: "blur(180px)",
    top: "40%",
    left: "50%",
    opacity: 0.08
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "18px",
    marginBottom: "28px",
    position: "relative",
    zIndex: 1
  },

  title: {
    fontSize: "clamp(32px,6vw,60px)",
    fontWeight: "800",
    lineHeight: "1.2",
    paddingBottom: "8px",
    margin: 0,
    background:
      "linear-gradient(90deg,#00d4ff,#00ff88)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent"
  },

  subtitle: {
    marginTop: "8px",
    fontSize: "15px"
  },

  alert: {
    background:
      "linear-gradient(135deg,#ff4d6d,#ff006e)",
    padding: "16px",
    borderRadius: "18px",
    marginBottom: "20px",
    textAlign: "center",
    fontWeight: "700",
    boxShadow:
      "0 0 30px rgba(255,77,109,0.45)"
  },

  budgetCard: {
    borderRadius: "24px",
    padding: "22px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "20px",
    flexWrap: "wrap",
    marginBottom: "22px"
  },

  budgetValue: {
    margin: 0,
    marginTop: "8px"
  },

  grid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit,minmax(260px,1fr))",
    gap: "20px"
  },

  card: {
    borderRadius: "28px",
    padding: "28px",
    position: "relative",
    overflow: "hidden"
  },

  shine: {
    position: "absolute",
    top: "-50%",
    left: "-60%",
    width: "220px",
    height: "220px",
    background:
      "linear-gradient(to right, rgba(255,255,255,0.12), transparent)",
    transform: "rotate(25deg)",
    pointerEvents: "none"
  },

  aiCard: {
    background:
      "linear-gradient(135deg,#00d4ff,#00ff88)",
    borderRadius: "28px",
    padding: "28px",
    color: "#000",
    overflow: "hidden",
    position: "relative"
  },

  aiGlow: {
    position: "absolute",
    width: "250px",
    height: "250px",
    background: "rgba(255,255,255,0.15)",
    borderRadius: "50%",
    top: "-80px",
    right: "-80px",
    filter: "blur(50px)"
  },

  smallLabel: {
    marginBottom: "10px",
    fontSize: "14px"
  },

  cardValue: {
    fontSize: "36px",
    margin: 0,
    fontWeight: "800"
  },

  cardSub: {
    marginTop: "10px"
  },

  aiTop: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    fontWeight: "700",
    position: "relative",
    zIndex: 2
  },

  liveDot: {
    width: "10px",
    height: "10px",
    borderRadius: "50%",
    background: "#00ff00"
  },

  aiValue: {
    fontSize: "40px",
    marginTop: "18px",
    marginBottom: "10px",
    position: "relative",
    zIndex: 2
  },

  aiTrend: {
    fontWeight: "700",
    position: "relative",
    zIndex: 2
  },

  aiBottom: {
    display: "flex",
    justifyContent: "space-between",
    gap: "20px",
    marginTop: "22px",
    flexWrap: "wrap",
    position: "relative",
    zIndex: 2
  },

  aiMiniLabel: {
    fontSize: "12px",
    marginBottom: "4px"
  },

  chartGrid: {
    display: "grid",
    gridTemplateColumns:
      "repeat(auto-fit,minmax(280px,1fr))",
    gap: "20px",
    marginTop: "28px"
  },

  chartCard: {
    borderRadius: "28px",
    padding: "24px",
    position: "relative",
    overflow: "hidden"
  },

  chartHeader: {
    marginBottom: "18px"
  },

  inputCard: {
    marginTop: "30px",
    borderRadius: "26px",
    padding: "22px",
    display: "flex",
    flexWrap: "wrap",
    gap: "16px"
  },

  input: {
    flex: 1,
    width: "100%",
    minWidth: "140px",
    padding: "15px 18px",
    borderRadius: "16px",
    border: "1px solid rgba(255,255,255,0.08)",
    background: "rgba(255,255,255,0.06)",
    color: "#fff",
    outline: "none",
    fontSize: "15px",
    transition: "all 0.3s ease",
    backdropFilter: "blur(12px)"
  },

  addBtn: {
    padding: "15px 24px",
    borderRadius: "16px",
    border: "none",
    background:
      "linear-gradient(135deg,#00d4ff,#00ff88)",
    color: "#000",
    fontWeight: "800",
    cursor: "pointer",
    whiteSpace: "nowrap"
  },

  dangerBtn: {
    padding: "14px 18px",
    borderRadius: "16px",
    border: "none",
    background:
      "linear-gradient(135deg,#ff4d6d,#ff006e)",
    color: "#fff",
    fontWeight: "700",
    cursor: "pointer",
    whiteSpace: "nowrap"
  },

  pdfBtn: {
    padding: "14px 18px",
    borderRadius: "16px",
    border: "none",
    background:
      "linear-gradient(135deg,#8338ec,#3a86ff)",
    color: "#fff",
    fontWeight: "700",
    cursor: "pointer",
    whiteSpace: "nowrap"
  },

  toggleBtn: {
    padding: "14px 18px",
    borderRadius: "16px",
    border: "none",
    color: "#fff",
    fontWeight: "700",
    cursor: "pointer",
    whiteSpace: "nowrap"
  },

  transactionSection: {
    marginTop: "34px"
  },

  sectionTop: {
    marginBottom: "18px"
  },

  transactionItem: {
    borderRadius: "22px",
    padding: "18px",
    marginBottom: "14px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    flexWrap: "wrap",
    gap: "10px",
    width: "100%",
    boxSizing: "border-box"
  },

  amount: {
    margin: 0,
    fontSize: "20px"
  },

  category: {
    marginTop: "4px"
  },

  date: {
    fontSize: "14px"
  },

  empty: {
    padding: "25px",
    borderRadius: "20px",
    textAlign: "center"
  }
};