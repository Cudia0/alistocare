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

  // Header action buttons
  const btnImportCsv = document.getElementById('btnImportCsv');
  const btnResetDefault = document.getElementById('btnResetDefault');

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

  // Insights modal
  const insightsModal = document.getElementById('insightsModal');
  const insightsTitle = document.getElementById('insightsTitle');
  const insightsChart = document.getElementById('insightsChart');
  const insightsText = document.getElementById('insightsText');
  const insightsNote = document.getElementById('insightsNote');
  const insightsClose = document.getElementById('insightsClose');

  // Default cleaned dataset bundled with the repo
  const DEFAULT_CSV_URL = 'healthcare_analytics_cleaned.csv';

  // Storage key for persisting custom CSV across refreshes
  const STORAGE_KEY = 'alistocare_custom_csv';
  const STORAGE_NAME_KEY = 'alistocare_custom_csv_name';

  // State
  let rawData = [];       // all parsed rows
  let filteredData = [];  // rows after applying filters

  // ---------------------------------------------------------------------------
  // Helpers
  // ---------------------------------------------------------------------------

  function parseDateStr(dateStr, timeStr) {
    if (!dateStr) return null;
    const parts = String(dateStr).trim().split('/');
    if (parts.length !== 3) return null;
    const m = parseInt(parts[0], 10);
    const d = parseInt(parts[1], 10);
    const y = parseInt(parts[2], 10);
    if (isNaN(m) || isNaN(d) || isNaN(y)) return null;
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
  // LocalStorage persistence for custom CSV
  // ---------------------------------------------------------------------------

  function saveCustomCsv(csvText, fileName) {
    try {
      localStorage.setItem(STORAGE_KEY, csvText);
      localStorage.setItem(STORAGE_NAME_KEY, fileName);
    } catch (e) {
      console.warn('localStorage unavailable, custom CSV will not persist:', e);
    }
  }

  function loadStoredCustomCsv() {
    try {
      const csvText = localStorage.getItem(STORAGE_KEY);
      const fileName = localStorage.getItem(STORAGE_NAME_KEY);
      if (csvText) return { csvText, fileName };
    } catch (e) {
      console.warn('localStorage read failed:', e);
    }
    return null;
  }

  function clearStoredCustomCsv() {
    try {
      localStorage.removeItem(STORAGE_KEY);
      localStorage.removeItem(STORAGE_NAME_KEY);
    } catch (e) {
      console.warn('localStorage clear failed:', e);
    }
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
          saveCustomCsv(text, file.name);
          loadData(results.data, file.name);
        }
      });
    };
    reader.readAsText(file);
  });

  function loadData(rows, sourceName = null) {
    if (!rows || !rows.length) {
      alert('The CSV file appears to be empty.');
      return;
    }

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

    skeletonOverlay.style.display = 'none';
    filtersSection.style.display = 'grid';
    kpisSection.style.display = 'grid';
    chartsSection.style.display = 'grid';
    dataNote.style.display = 'block';
    footer.style.display = 'block';

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
  // Default data loading
  // ---------------------------------------------------------------------------

  function loadDefaultData() {
    fetch(DEFAULT_CSV_URL)
      .then(function (response) {
        if (!response.ok) throw new Error('Failed to load default dataset');
        return response.text();
      })
      .then(function (text) {
        Papa.parse(text, {
          header: true,
          dynamicTyping: true,
          skipEmptyLines: true,
          complete: function (results) {
            loadData(results.data, 'healthcare_analytics_cleaned.csv');
          }
        });
      })
      .catch(function (err) {
        console.error('Default data load failed:', err);
      });
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
  // Charts (Plotly with click-to-insights)
  // ---------------------------------------------------------------------------

  function showInsights(chartId, title, label, value, ctx) {
    insightsTitle.textContent = title;
    insightsChart.innerHTML = '';
    insightsText.innerHTML = '';
    insightsNote.textContent = '';

    let html = '';
    let note = '';

    if (chartId === 'volumeChart') {
      html = `<h4>Encounter volume — ${label}</h4>
              <p>There were <strong>${fmtNum(value)}</strong> patient encounters in ${label}.</p>
              <ul>
                <li>This represents ${fmtPct((value / rawData.length) * 100)} of all ${rawData.length.toLocaleString()} encounters.</li>
                <li>Monthly volume varies by department and day of week — use the filters above to drill down.</li>
              </ul>`;
      note = 'Data: All encounters within the selected date range.';
    } else if (chartId === 'categoryChart') {
      html = `<h4>Wait-time band — ${label}</h4>
              <p>${fmtPct(value)} of encounters waited <strong>${label}</strong>.</p>
              <ul>
                <li>This wait band includes ${Math.round((value / 100) * filteredData.length)} encounters.</li>
                <li>Longer waits correlate with admission — check the department filter for patterns.</li>
              </ul>`;
      note = 'Data: Encounters with a recorded wait-time category.';
    } else if (chartId === 'departmentChart') {
      html = `<h4>Department — ${label}</h4>
              <p>Average wait: <strong>${value} minutes</strong> per encounter.</p>
              <ul>
                <li>Departments are ranked by average wait time (highest first).</li>
                <li>Use this to identify where queue management improvements would have the most impact.</li>
              </ul>`;
      note = 'Data: Only encounters with a recorded department.';
    } else if (chartId === 'hourChart') {
      html = `<h4>Wait by hour — ${label}:00</h4>
              <p>Average wait at this hour is <strong>${value} minutes</strong>.</p>
              <ul>
                <li>Peak and low hours help identify staffing and scheduling opportunities.</li>
                <li>Interpret alongside encounter volume — low-volume hours may have outlier waits.</li>
              </ul>`;
      note = 'Data: Hourly average wait across all days in range.';
    } else if (chartId === 'weekdayChart') {
      html = `<h4>Encounters by weekday — ${label}</h4>
              <p><strong>${fmtNum(value)}</strong> encounters on ${label}s.</p>
              <ul>
                <li>Weekday patterns help plan staffing rosters.</li>
                <li>Weekend vs weekday differences may reflect reduced services.</li>
              </ul>`;
      note = 'Data: Encounter counts by day of week.';
    } else if (chartId === 'satisfactionChart') {
      html = `<h4>Satisfaction score — ${label}</h4>
              <p>${fmtPct(value)} of scored encounters rated their experience <strong>${label}/10</strong>.</p>
              <ul>
                <li>Satisfaction is only recorded for a subset of encounters.</li>
                <li>Low scores may correlate with longer waits — cross-check with wait-time filters.</li>
              </ul>`;
      note = 'Data: Only encounters with a recorded satisfaction score.';
    }

    insightsText.innerHTML = html;
    insightsNote.textContent = note;

    const modalChartData = [];
    const modalLayout = {
      margin: { t: 10, b: 30, l: 40, r: 10 },
      showlegend: false,
      height: 200,
      xaxis: { title: null, tickangle: -45 },
      yaxis: { title: null, rangemode: 'tozero' },
    };

    if (chartId === 'volumeChart') {
      const keys = Object.keys(ctx.monthCounts || {}).sort();
      modalChartData.push({ x: keys, y: keys.map(k => ctx.monthCounts[k]), type: 'bar', marker: { color: '#0E7C7B' } });
      modalLayout.xaxis.title = 'Month';
      modalLayout.yaxis.title = 'Encounters';
    } else if (chartId === 'categoryChart') {
      const order = ['0–15 min', '16–30 min', '31–45 min', '46–60 min', '60+ min'];
      modalChartData.push({ labels: order, values: order.map(k => ctx.catCounts[k] || 0), type: 'pie', textinfo: 'label+percent', marker: { colors: ['#0E7C7B','#2E8B57','#985829','#E8833A','#CFE9E9'] } });
      modalLayout.showlegend = false;
    } else if (chartId === 'departmentChart') {
      modalChartData.push({ x: ctx.deptValues, y: ctx.deptLabels, type: 'bar', orientation: 'h', marker: { color: '#0E7C7B' } });
      modalLayout.xaxis.title = 'Avg wait (min)';
      modalLayout.yaxis.title = 'Department';
    } else if (chartId === 'hourChart') {
      const hours = [];
      for (let h = 0; h < 24; h++) hours.push(h);
      modalChartData.push({ x: hours, y: hours.map(h => ctx.hourValues[h] || 0), type: 'bar', marker: { color: '#0E7C7B' } });
      modalLayout.xaxis.title = 'Hour of day';
      modalLayout.yaxis.title = 'Avg wait (min)';
    } else if (chartId === 'weekdayChart') {
      const order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      modalChartData.push({ x: order, y: order.map(d => ctx.weekdayCounts[d] || 0), type: 'bar', marker: { color: '#0E7C7B' } });
      modalLayout.xaxis.title = 'Day of week';
      modalLayout.yaxis.title = 'Encounters';
    } else if (chartId === 'satisfactionChart') {
      const scores = [];
      for (let i = 0; i <= 10; i++) scores.push(i);
      modalChartData.push({ x: scores, y: scores.map(s => ctx.satCounts[s] || 0), type: 'bar', marker: { color: '#985829' } });
      modalLayout.xaxis.title = 'Satisfaction score (0–10)';
      modalLayout.yaxis.title = 'Encounters';
    }

    if (modalChartData.length) {
      Plotly.newPlot('insightsChart', modalChartData, modalLayout, { responsive: true });
    }

    insightsModal.style.display = 'flex';
  }

  function hideInsights() {
    insightsModal.style.display = 'none';
  }

  insightsClose.addEventListener('click', hideInsights);
  insightsModal.addEventListener('click', function (e) {
    if (e.target === insightsModal) hideInsights();
  });

  function renderVolumeChart() {
    const counts = {};
    filteredData.forEach(d => {
      if (!d.date) return;
      const monthKey = d.date.slice(0, 7);
      counts[monthKey] = (counts[monthKey] || 0) + 1;
    });
    const keys = Object.keys(counts).sort();
    const ctx = { monthCounts: counts };

    Plotly.newPlot('volumeChart', [{
      x: keys,
      y: keys.map(k => counts[k]),
      type: 'bar',
      marker: { color: '#0E7C7B' },
      hovertemplate: '%{x}<br>Encounters: %{y}<extra></extra>',
      customdata: keys.map(k => ({ chartId: 'volumeChart', label: k, value: counts[k] })),
    }], {
      margin: { t: 30, b: 50, l: 50, r: 20 },
      xaxis: { title: 'Month', tickangle: -45 },
      yaxis: { title: 'Encounters', rangemode: 'tozero' },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('volumeChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('volumeChart', 'Encounter Volume — ' + cd.label, cd.label, cd.value, ctx);
    });
  }

  function renderCategoryChart() {
    const order = ['0–15 min', '16–30 min', '31–45 min', '46–60 min', '60+ min'];
    const counts = {};
    order.forEach(k => counts[k] = 0);
    filteredData.forEach(d => { if (counts[d.wait_category] !== undefined) counts[d.wait_category]++; });
    const total = filteredData.length;
    const ctx = { catCounts: counts };

    Plotly.newPlot('categoryChart', [{
      labels: order,
      values: order.map(k => total ? (counts[k] / total) * 100 : 0),
      type: 'pie',
      textinfo: 'label+percent',
      insidetextorientation: 'radial',
      marker: { colors: ['#0E7C7B', '#2E8B57', '#985829', '#E8833A', '#CFE9E9'] },
      hovertemplate: '%{label}<br>%{percent}<extra></extra>',
      customdata: order.map(k => ({ chartId: 'categoryChart', label: k, value: total ? (counts[k] / total) * 100 : 0 })),
    }], {
      margin: { t: 30, b: 30, l: 30, r: 30 },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('categoryChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('categoryChart', 'Wait-Time Distribution — ' + (cd.label || pts[0].label), cd.label, cd.value, cd.ctx);
    });
  }

  function renderDepartmentChart() {
    const sums = {}, cnts = {};
    filteredData.forEach(d => {
      if (!d.department) return;
      sums[d.department] = (sums[d.department] || 0) + d.wait_time_minutes;
      cnts[d.department] = (cnts[d.department] || 0) + 1;
    });
    const depts = Object.keys(sums).sort((a, b) => sums[b] / cnts[b] - sums[a] / cnts[a]);
    const ctx = { deptValues: depts.map(d => sums[d] / cnts[d]), deptLabels: depts.slice().reverse() };

    Plotly.newPlot('departmentChart', [{
      x: depts.map(d => sums[d] / cnts[d]).reverse(),
      y: depts.reverse(),
      type: 'bar',
      orientation: 'h',
      marker: { color: '#0E7C7B' },
      hovertemplate: '%{y}<br>Avg wait: %{x:.1f} min<extra></extra>',
      customdata: depts.map(d => ({ chartId: 'departmentChart', label: d, value: sums[d] / cnts[d] })),
    }], {
      margin: { t: 30, b: 40, l: 90, r: 20 },
      xaxis: { title: 'Avg wait (min)', rangemode: 'tozero' },
      yaxis: { title: 'Department', automargin: true },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('departmentChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('departmentChart', 'Avg Wait by Department — ' + cd.label, cd.label, cd.value, ctx);
    });
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
    const hourValues = {};
    hours.forEach(h => { hourValues[h] = cnts[h] ? sums[h] / cnts[h] : 0; });
    const ctx = { hourValues };

    Plotly.newPlot('hourChart', [{
      x: hours,
      y: hours.map(h => hourValues[h]),
      type: 'bar',
      marker: { color: '#0E7C7B' },
      hovertemplate: '%{x}:00<br>Avg wait: %{y:.1f} min<extra></extra>',
      customdata: hours.map(h => ({ chartId: 'hourChart', label: h, value: hourValues[h] })),
    }], {
      margin: { t: 30, b: 90, l: 50, r: 20 },
      xaxis: { title: 'Hour of day', title: { standoff: 25 }, tickmode: 'array', tickvals: hours, ticktext: hours.map(h => (h % 12 || 12) + (h >= 12 ? ' PM' : ' AM')) },
      yaxis: { title: 'Avg wait (min)', rangemode: 'tozero' },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('hourChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('hourChart', 'Avg Wait by Hour — ' + cd.label + ':00', cd.label, cd.value, ctx);
    });
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
      marker: { color: '#0E7C7B' },
      hovertemplate: '%{x}<br>Encounters: %{y}<extra></extra>',
      customdata: order.map(d => ({ chartId: 'weekdayChart', label: d, value: counts[d], ctx: { weekdayCounts: counts } })),
    }], {
      margin: { t: 30, b: 110, l: 50, r: 20 },
      xaxis: { title: 'Day of week', title: { standoff: 25 }, tickangle: -45 },
      yaxis: { title: 'Encounters', rangemode: 'tozero' },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('weekdayChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('weekdayChart', 'Encounters by Weekday — ' + cd.label, cd.label, cd.value, cd.ctx);
    });
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
    const ctx = { satCounts: scores };

    Plotly.newPlot('satisfactionChart', [{
      x: Object.keys(scores).map(Number),
      y: Object.keys(scores).map(s => total ? (scores[s] / total) * 100 : 0),
      type: 'bar',
      marker: { color: '#985829' },
      hovertemplate: 'Score %{x}<br>%{y:.1f}%<extra></extra>',
      customdata: Object.keys(scores).map(s => ({ chartId: 'satisfactionChart', label: s, value: total ? (scores[s] / total) * 100 : 0, ctx: { satCounts: scores } })),
    }], {
      margin: { t: 30, b: 50, l: 50, r: 20 },
      xaxis: { title: 'Satisfaction score (0–10)', tickmode: 'linear', tick0: 0, dtick: 1 },
      yaxis: { title: 'Share of scored encounters', rangemode: 'tozero', ticksuffix: '%' },
      showlegend: false,
      clickmode: 'event+select',
    }, { responsive: true });

    document.getElementById('satisfactionChart').on('plotly_click', function (ev) {
      const pts = ev.points || [];
      if (!pts.length || !pts[0].customdata) return;
      const cd = pts[0].customdata;
      showInsights('satisfactionChart', 'Satisfaction Distribution — Score ' + cd.label, cd.label, cd.value, ctx);
    });
  }

  // ---------------------------------------------------------------------------
  // Header action buttons
  // ---------------------------------------------------------------------------

  btnImportCsv.addEventListener('click', function () {
    fileInput.value = '';
    fileInput.click();
  });

  btnResetDefault.addEventListener('click', function () {
    if (!confirm('Reset to the default cleaned dataset? Any custom CSV will be cleared.')) return;
    clearStoredCustomCsv();
    rawData = [];
    filteredData = [];
    departmentSel.innerHTML = '<option value="All">All departments</option>';
    daySel.innerHTML = '<option value="All">All days</option>';
    loadDefaultData();
  });

  // ---------------------------------------------------------------------------
  // Initialize
  // ---------------------------------------------------------------------------

  function init() {
    const stored = loadStoredCustomCsv();
    if (stored) {
      Papa.parse(stored.csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: function (results) {
          loadData(results.data, stored.fileName || 'Custom CSV');
        }
      });
    } else {
      loadDefaultData();
    }
  }

  init();

})();