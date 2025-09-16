const API = "https://numbot-production.up.railway.app"; // твой Railway-домен

function showResult(html){
  const r = document.getElementById("result");
  r.innerHTML = html;
  r.classList.remove("hidden");
  r.scrollIntoView({behavior:"smooth"});
}

// --- Нумерология (один) ---
async function analyzeSingle(){
  const date = document.getElementById("date_single").value.trim();
  if(!date) return alert("Введите дату!");

  showLoader();

  try {
    const res = await fetch(`${API}/analyze`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({date})
    });
    const data = await res.json();
    showResult(`<h3>📅 ${date}</h3><p>${data.interpretation}</p>`);
  } catch (err) {
    alert("Ошибка соединения. Попробуйте позже.");
  } finally {
    hideLoader();
  }
}

// --- Совместимость ---
async function analyzeCompat() {
  const d1 = document.getElementById("date_female").value.trim();
  const d2 = document.getElementById("date_male").value.trim();
  if (!d1 || !d2) return alert("Введите обе даты!");

  showLoader();

  try {
    const res = await fetch(`${API}/compat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date1: d1, date2: d2 })
    });
    const data = await res.json();
    showResult(`<h3>👩 ${d1} + 👨 ${d2}</h3><p>${data.interpretation}</p>`);
  } catch (err) {
    alert("⚠️ Ошибка соединения. Попробуйте позже.");
    console.error(err);
  } finally {
    hideLoader();
  }
}

// --- Натальная карта ---
async function analyzeNatal() {
  const date = document.getElementById("natal_date").value.trim();
  const time = document.getElementById("natal_time").value.trim();
  const place = document.getElementById("natal_place").value.trim();
  if (!date || !time || !place) return alert("Заполните дату, время и место!");

  showLoader();

  try {
    const res = await fetch(`${API}/natal`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ date, time, place })
    });
    const data = await res.json();
    showResult(`<h3>🗺️ Натальная карта</h3><p>${data.interpretation}</p>`);
  } catch (err) {
    alert("⚠️ Ошибка при получении данных. Попробуйте позже.");
    console.error(err);
  } finally {
    hideLoader();
  }
}

// --- Гороскоп ---
async function getHoroscope() {
  const sign = document.getElementById("hs_sign").value;
  const period = document.getElementById("hs_period").value;

  showLoader();

  try {
    const res = await fetch(`${API}/horoscope`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sign, period })
    });
    const data = await res.json();
    showResult(`<h3>♈ Гороскоп для ${sign} (${period})</h3><p>${data.interpretation}</p>`);
  } catch (err) {
    alert("⚠️ Ошибка загрузки гороскопа.");
    console.error(err);
  } finally {
    hideLoader();
  }
}
// заглушки для старых кнопок (если где-то вызываются)
function showSingle(){}; function showCompat(){};

// показать крутилку
function showLoader(){
  document.getElementById("loader").classList.remove("hidden");
  document.getElementById("result").classList.add("hidden");
}

// скрыть крутилку
function hideLoader(){
  document.getElementById("loader").classList.add("hidden");
}
