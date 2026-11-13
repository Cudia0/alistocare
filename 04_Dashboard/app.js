/* AlistoCare Dashboard — client-side CSV upload + Plotly charts */
(function () {
  'use strict';

  // DOM references
  const fileInput = document.getElementById('fileInput');
  const skeletonOverlay = document.getElementById('skeletonOverlay');
  const filtersSection = document.getElementById('filters');
  const kpisSection = document.getElementById('kpis');
  const chartsSection = document.getElementById('charts');
  const dataNote = document.getElementById('dataNote');
  const footer = document.getElementById('footer');

  // Filter inputs
  const fromDate = document.getElementById('fromDate');
  const toDate = document.getElementById('toDate');
  const departmentSel = document.getElementById('department');
  const daySel = document.getElementById('day');
  const admissionSel = document.getElementById('admission');
  const resetBtn = document.getElementById('reset');

  // KPI elements
  const kpiCount = document.getElementById('kpiCount');
  const kpiCountNote = document.getElementById('kpiCountNote');
  const kpiAvg = document.getElementById('kpiAvg');
  const kpiMedian = document.getElementById('kpiMedian');
  const kpiLong = document.getElementById('kpiLong');
  const kpiAdmission = document.getElementById('kpiAdmission');
  const kpiSat = document.getElementById('kpiSat');

  // State
  let rawData = [];       // all parsed rows
  let filteredData = [];  // rows after applying filters

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function parseDateStr(dateStr, timeStr) {
    // admission_date like "9/9/2024" (M/D/YYYY), admission_time like "9:25:00 AM"
    if (!dateStr) return null;
    const parts = String(dateStr).trim().split('/');
    if (parts.length !== 3) return null;
    const m = parseInt(parts[0], 10);
    const d = parseInt(parts[1], 10);
    const y = parseInt(parts[2], 10);
    if (isNaN(m) || isNaN(d) || isNaN(y)) return null;
    // Per project rule: first component > 12 => DD/MM/YYYY, else MM/DD/YYYY
    let month, day;
    if (m > 12) { month = d; day = m; } else { month = m; day = d; }
    if (month < 1 || month > 12 || day < 1 || day > 31) return null;
    const date = new Date(y, month - 1, day);
    if (timeStr) {
      const t = String(timeStr).trim();
      const m2 = t.match(/^(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i);
      if (m2) {
        let h = parseInt(m2[1], 10);
        const mi = parseInt(m2[2], 10);
        const ampm = m2[4].toUpperCase();
        if (ampm === 'PM' && h !== 12) h += 12;
        if (ampm === 'AM' && h === 12) h = 0;
        if (!isNaN(h) && !isNaN(mi)) {
          date.setHours(h, mi, m2[3] ? parseInt(m2[3], 10) : 0, 0);
        }
      }
    }
    return date;
  }

  function median(vals) {
    if (!vals.length) return 0;
    const s = vals.slice().sort((a, b) => a - b);
    const mid = Math.floor(s.length / 2);
    return s.length % 2 === 0 ? (s[mid - 1] + s[mid]) / 2 : s[mid];
  }

  function fmtNum(n, decimals = 2) {
    return Number(n).toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
  }

  function fmtPct(n) {
    return Number(n).toLocaleString(undefined, { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + '%';
  }

  // ---------------------------------------------------------------------------
  // Data loading
  // ---------------------------------------------------------------------------

  fileInput.addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.csv')) {
      alert('Please select a .csv file.');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (ev) {
      const text = ev.target.result;
      Papa.parse(text, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function (results) {
          if (results.errors && results.errors.length) {
            console.warn('Parse warnings:', results.errors);
          }
          loadData(results.data);
        }
      });
    };
    reader.readAsText(file);
  });

  function loadData(rows) {
    if (!rows || !rows.length) {
      alert('The CSV file appears to be empty.');
      return;
    }

    // Normalize + enrich rows
    const processed = rows.map(function (row) {
      const r = {};
      r.patient_id = String(row.patient_id || '').trim();
      r.admission_date = String(row.admission_date || '').trim();
      r.admission_time = String(row.admission_time || '').trim();
      r.gender = String(row.gender || '').trim();
      r.age = Number(row.age) || 0;
      r.race = String(row.race || '').trim();
      r.department = String(row.department || '').trim() || null;
      r.admission_flag = String(row.admission_flag || '').trim();
      r.satisfaction_score = row.satisfaction_score != null ? Number(row.satisfaction_score) : null;
      r.wait_time_minutes = Number(row.wait_time_minutes) || 0;

      const dt = parseDateStr(r.admission_date, r.admission_time);
      r.admission_datetime = dt;
      r.date = dt ? dt.toISOString().slice(0, 10) : null;
      r.day_of_week = dt ? ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][dt.getDay()] : null;
      r.hour = dt != null ? dt.getHours() : null;
      r.month = dt ? dt.toLocaleString(undefined, { month: 'short' }) : null;

      if (r.wait_time_minutes <= 15) r.wait_category = '0–15 min';
      else if (r.wait_time_minutes <= 30) r.wait_category = '16–30 min';
      else if (r.wait_time_minutes <= 45) r.wait_category = '31–45 min';
      else if (r.wait_time_minutes <= 60) r.wait_category = '46–60 min';
      else r.wait_category = '60+ min';

      if (r.age <= 17) r.age_group = '0–17';
      else if (r.age <= 30) r.age_group = '18–30';
      else if (r.age <= 45) r.age_group = '31–45';
      else if (r.age <= 60) r.age_group = '46–60';
      else if (r.age <= 75) r.age_group = '61–75';
      else r.age_group = '76+';

      return r;
    });

    rawData = processed;
    filteredData = processed.slice();

    // Populate filter options
    const depts = [...new Set(processed.filter(d => d.department).map(d => d.department))].sort();
    depts.forEach(d => {
      const o = document.createElement('option');
      o.value = d;
      o.textContent = d;
      departmentSel.appendChild(o);
    });

    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    days.forEach(d => {
      const o = document.createElement('option');
      o.value = d;
      o.textContent = d;
      daySel.appendChild(o);
    });

    // Date range defaults
    const dates = processed.filter(d => d.date).map(d => d.date);
    if (dates.length) {
      dates.sort();
      fromDate.min = dates[0];
      fromDate.max = dates[dates.length - 1];
      toDate.min = dates[0];
      toDate.max = dates[dates.length - 1];
      fromDate.value = dates[0];
      toDate.value = dates[dates.length - 1];
    }

    document.getElementById('ctxRecords').textContent = processed.length.toLocaleString() + ' encounters';

    // Swap UI: hide skeleton+upload, show dashboard
    skeletonOverlay.style.display = 'none';
    filtersSection.style.display = 'grid';
    kpisSection.style.display = 'grid';
    chartsSection.style.display = 'grid';
    dataNote.style.display = 'block';
    footer.style.display = 'block';

    // Wire filter listeners
    [fromDate, toDate, departmentSel, daySel, admissionSel].forEach(function (el) {
      el.addEventListener('change', applyFilters);
    });
    resetBtn.addEventListener('click', function () {
      fromDate.value = fromDate.min || '';
      toDate.value = fromDate.max || '';
      departmentSel.value = 'All';
      daySel.value = 'All';
      admissionSel.value = 'All';
      applyFilters();
    });

    applyFilters();
  }

  // ---------------------------------------------------------------------------
  // Filtering + rendering
  // ---------------------------------------------------------------------------

  function applyFilters() {
    const fFrom = fromDate.value;
    const fTo = toDate.value;
    const fDept = departmentSel.value;
    const fDay = daySel.value;
    const fAdm = admissionSel.value;

    filteredData = rawData.filter(function (r) {
      if (fFrom && r.date && r.date < fFrom) return false;
      if (fTo && r.date && r.date > fTo) return false;
      if (fDept !== 'All' && r.department !== fDept) return false;
      if (fDay !== 'All' && r.day_of_week !== fDay) return false;
      if (fAdm !== 'All' && r.admission_flag !== fAdm) return false;
      return true;
    });

    render();
  }

  function render() {
    renderKPIs();
    renderVolumeChart();
    renderCategoryChart();
    renderDepartmentChart();
    renderHourChart();
    renderWeekdayChart();
    renderSatisfactionChart();
  }

  // ---------------------------------------------------------------------------
  // KPIs
  // ---------------------------------------------------------------------------

  function renderKPIs() {
    const n = filteredData.length;
    kpiCount.textContent = n.toLocaleString();
    kpiCountNote.textContent = n === rawData.length ? 'All records' : 'Filtered records';

    if (n === 0) {
      kpiAvg.textContent = '—';
      kpiMedian.textContent = '—';
      kpiLong.textContent = '—';
      kpiAdmission.textContent = '—';
      kpiSat.textContent = '—';
      return;
    }

    const waits = filteredData.map(d => d.wait_time_minutes);
    const avgWait = waits.reduce((a, b) => a + b, 0) / n;
    const medWait = median(waits);
    const over30 = waits.filter(w => w > 30).length;
    const admCount = filteredData.filter(d => d.admission_flag === 'Admission').length;
    const satScores = filteredData.filter(d => d.satisfaction_score != null).map(d => d.satisfaction_score);
    const avgSat = satScores.length ? satScores.reduce((a, b) => a + b, 0) / satScores.length : 0;

    kpiAvg.textContent = fmtNum(avgWait);
    kpiMedian.textContent = fmtNum(medWait, 0);
    kpiLong.textContent = fmtPct((over30 / n) * 100);
    kpiAdmission.textContent = fmtPct((admCount / n) * 100);
    kpiSat.textContent = satScores.length ? fmtNum(avgSat, 1) : '—';
  }

  // ---------------------------------------------------------------------------
  // Charts
  // ---------------------------------------------------------------------------

  function renderVolumeChart() {
    const counts = {};
    filteredData.forEach(d => {
      if (!d.date) return;
      const monthKey = d.date.slice(0, 7); // YYYY-MM
      counts[monthKey] = (counts[monthKey] || 0) + 1;
    }
    );
    const keys = Object.keys(counts).sort();
    Plotly.newPlot('volumeChart', [{
      x: keys,
      y: keys.map(k => counts[k]),
      type: 'bar',
      marker: { color: '#6E1C1A' }
    }], {
      margin: { t: 30, b: 50, l: 50, r: 20 },
      xaxis: { title: 'Month', tickangle: -45 },
      yaxis: { title: 'Encounters', rangemode: 'tozero' },
      showlegend: false
    }, { responsive: true });
  }

  function renderCategoryChart() {
    const order = ['0–15 min', '16–30 min', '31–45 min', '46–60 min', '60+ min'];
    const counts = {};
    order.forEach(k => counts[k] = 0);
    filteredData.forEach(d => { if (counts[d.wait_category] !== undefined) counts[d.wait_category]++; });
    const total = filteredData.length;
    Plotly.newPlot('categoryChart', [{
      labels: order,
      values: order.map(k => total ? (counts[k] / total) * 100 : 0),
      type: 'pie',
      textinfo: 'label+percent',
      insidetextorientation: 'radial',
      marker: { colors: ['#432716', '#6E1C1A', '#985829', '#BA9457', '#F1D6A5'] }
    }], {
      margin: { t: 30, b: 30, l: 30, r: 30 },
      showlegend: false
    }, { responsive: true });
  }

  function renderDepartmentChart() {
    const sums = {}, cnts = {};
    filteredData.forEach(d => {
      if (!d.department) return;
      sums[d.department] = (sums[d.department] || 0) + d.wait_time_minutes;
      cnts[d.department] = (cnts[d.department] || 0) + 1;
    });
    const depts = Object.keys(sums).sort((a, b) => sums[b] / cnts[b] - sums[a] / cnts[a]);
    Plotly.newPlot('departmentChart', [{
      x: depts.map(d => sums[d] / cnts[d]).reverse(),
      y: depts.reverse(),
      type: 'bar',
      orientation: 'h',
      marker: { color: '#6E1C1A' }
    }], {
      margin: { t: 30, b: 40, l: 90, r: 20 },
      xaxis: { title: 'Avg wait (min)', rangemode: 'tozero' },
      yaxis: { title: 'Department', automargin: true },
      showlegend: false
    }, { responsive: true });
  }

  function renderHourChart() {
    const sums = {}, cnts = {};
    filteredData.forEach(d => {
      if (d.hour == null) return;
      sums[d.hour] = (sums[d.hour] || 0) + d.wait_time_minutes;
      cnts[d.hour] = (cnts[d.hour] || 0) + 1;
    });
    const hours = [];
    for (let h = 0; h < 24; h++) hours.push(h);
    Plotly.newPlot('hourChart', [{
      x: hours,
      y: hours.map(h => cnts[h] ? sums[h] / cnts[h] : 0),
      type: 'bar',
      marker: { color: '#6E1C1A' }
    }], {
      margin: { t: 30, b: 90, l: 50, r: 20 },
      xaxis: { title: 'Hour of day', title: { standoff: 25 }, tickmode: 'array', tickvals: hours, ticktext: hours.map(h => (h % 12 || 12) + (h >= 12 ? ' PM' : ' AM')) },
      yaxis: { title: 'Avg wait (min)', rangemode: 'tozero' },
      showlegend: false
    }, { responsive: true });
  }

  function renderWeekdayChart() {
    const order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const counts = {};
    order.forEach(d => counts[d] = 0);
    filteredData.forEach(d => { if (d.day_of_week && counts[d.day_of_week] !== undefined) counts[d.day_of_week]++; });
    Plotly.newPlot('weekdayChart', [{
      x: order,
      y: order.map(d => counts[d]),
      type: 'bar',
      marker: { color: '#6E1C1A' }
    }], {
      margin: { t: 30, b: 110, l: 50, r: 20 },
      xaxis: { title: 'Day of week', title: { standoff: 25 }, tickangle: -45 },
      yaxis: { title: 'Encounters', rangemode: 'tozero' },
      showlegend: false
    }, { responsive: true });
  }

  function renderSatisfactionChart() {
    const scores = {};
    for (let i = 0; i <= 10; i++) scores[i] = 0;
    filteredData.forEach(d => {
      if (d.satisfaction_score != null) {
        const s = Math.round(d.satisfaction_score);
        if (s >= 0 && s <= 10) scores[s]++;
      }
    });
    const total = filteredData.filter(d => d.satisfaction_score != null).length;
    Plotly.newPlot('satisfactionChart', [{
      x: Object.keys(scores).map(Number),
      y: Object.keys(scores).map(s => total ? (scores[s] / total) * 100 : 0),
      type: 'bar',
      marker: { color: '#985829' }
    }], {
      margin: { t: 30, b: 50, l: 50, r: 20 },
      xaxis: { title: 'Satisfaction score (0–10)', tickmode: 'linear', tick0: 0, dtick: 1 },
      yaxis: { title: 'Share of scored encounters', rangemode: 'tozero', ticksuffix: '%' },
      showlegend: false
    }, { responsive: true });
  }

})();
