// --- Анализ одного человека ---
async function analyzeSingle() {
    const date = document.getElementById("date_single").value;
    if (!date) return alert("Введите дату!");
  
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date })
    });
  
    const data = await res.json();
    document.getElementById("result").innerHTML = `
      <h3>📅 ${date}</h3>
      <p>${data.interpretation}</p>
    `;
  }
  
  // --- Анализ совместимости ---
  async function analyzeCompat() {
    const d1 = document.getElementById("date_female").value;
    const d2 = document.getElementById("date_male").value;
    if (!d1 || !d2) return alert("Введите обе даты!");
  
    const res = await fetch("http://127.0.0.1:8000/compat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date1: d1, date2: d2 })
    });
  
    const data = await res.json();
    document.getElementById("result").innerHTML = `
      <h3>👩 ${d1} + 👨 ${d2}</h3>
      <p>${data.interpretation}</p>
    `;
  }
  