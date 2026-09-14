/* ========================================
   STUDENT PERFORMANCE MANAGEMENT SYSTEM
   Frontend JavaScript Application
   ======================================== */

// ---- Configuration ----
const API_BASE = '/api';

// ---- State ----
let allStudents = [];
let currentView = 'dashboard';

// ========================== INITIALIZATION ==========================

document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});

// ========================== VIEW SWITCHING ==========================

function switchView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));

    // Show target view
    const target = document.getElementById('view-' + viewName);
    if (target) {
        target.classList.add('active');
    }

    // Update nav active state
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-view') === viewName) {
            item.classList.add('active');
        }
    });

    currentView = viewName;

    // Load data for the view
    switch(viewName) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'students':
            loadStudents();
            break;
        case 'add-student':
            // Reset form if switching to add (not edit)
            if (document.getElementById('editMode').value === 'add') {
                resetForm();
            }
            break;
        case 'analytics':
            loadAnalytics();
            break;
        case 'numpy':
            loadNumpyAnalysis();
            break;
        case 'pandas':
            loadPandasAnalysis();
            break;
    }

    // Close sidebar on mobile
    document.getElementById('sidebar').classList.remove('open');
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
}

// ========================== API HELPER ==========================

async function apiFetch(endpoint, options = {}) {
    try {
        const response = await fetch(API_BASE + endpoint, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showToast('Connection error. Is the server running?', 'error');
        return { success: false, message: 'Connection error' };
    }
}

// ========================== DASHBOARD ==========================

async function loadDashboard() {
    // Load statistics
    const statsResult = await apiFetch('/statistics');
    const analyticsResult = await apiFetch('/analytics');

    if (statsResult.success) {
        renderStatsCards(statsResult.data);
        renderGradeChart(statsResult.data.grade_distribution);
    }

    if (analyticsResult.success && analyticsResult.data.top_students) {
        renderTopStudents(analyticsResult.data.top_students);
    }
}

function renderStatsCards(stats) {
    const grid = document.getElementById('statsGrid');
    grid.innerHTML = `
        <div class="stat-card purple">
            <div class="stat-icon">👥</div>
            <div class="stat-value">${stats.total_students}</div>
            <div class="stat-label">Total Students</div>
        </div>
        <div class="stat-card green">
            <div class="stat-icon">📊</div>
            <div class="stat-value">${stats.class_average || 0}</div>
            <div class="stat-label">Class Average</div>
        </div>
        <div class="stat-card orange">
            <div class="stat-icon">🏆</div>
            <div class="stat-value">${stats.highest_average || 0}</div>
            <div class="stat-label">Highest Average</div>
        </div>
        <div class="stat-card pink">
            <div class="stat-icon">📉</div>
            <div class="stat-value">${stats.lowest_average || 0}</div>
            <div class="stat-label">Lowest Average</div>
        </div>
    `;
}

function renderGradeChart(distribution) {
    const container = document.getElementById('gradeChart');
    if (!distribution || Object.keys(distribution).length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="icon">📊</div><p>No data yet</p></div>';
        return;
    }

    const grades = ['A+', 'A', 'B', 'C', 'D', 'F'];
    const maxCount = Math.max(...Object.values(distribution), 1);

    let html = '';
    for (const grade of grades) {
        const count = distribution[grade] || 0;
        const width = (count / maxCount) * 100;
        const gradeClass = 'grade-' + grade.toLowerCase().replace('+', '-plus');

        html += `
            <div class="chart-bar-row">
                <span class="chart-bar-label">${grade}</span>
                <div class="chart-bar-track">
                    <div class="chart-bar-fill ${gradeClass}" style="width: ${width}%">
                        ${count > 0 ? count : ''}
                    </div>
                </div>
                <span class="chart-bar-count">${count}</span>
            </div>
        `;
    }

    container.innerHTML = html;

    // Animate bars (trigger reflow)
    setTimeout(() => {
        container.querySelectorAll('.chart-bar-fill').forEach(bar => {
            bar.style.width = bar.style.width; // re-trigger
        });
    }, 50);
}

function renderTopStudents(topStudents) {
    const container = document.getElementById('topStudentsList');
    if (!topStudents || topStudents.length === 0) {
        container.innerHTML = '<div class="empty-state"><div class="icon">🏆</div><p>No students yet</p></div>';
        return;
    }

    let html = '';
    topStudents.forEach((student, index) => {
        const rankClass = index < 3 ? `rank-${index + 1}` : 'rank-other';
        html += `
            <div class="top-student-item">
                <div class="top-rank ${rankClass}">${index + 1}</div>
                <div class="top-student-info">
                    <div class="name">${student.name}</div>
                    <div class="dept">${student.department} • Year ${student.year}</div>
                </div>
                <div class="top-student-avg">${student.average}</div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// ========================== STUDENTS LIST ==========================

async function loadStudents() {
    const result = await apiFetch('/students');
    if (result.success) {
        allStudents = result.data;
        renderStudentsTable(allStudents);
    }
}

function renderStudentsTable(students) {
    const tbody = document.getElementById('studentsTableBody');

    if (!students || students.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8">
                    <div class="empty-state">
                        <div class="icon">👥</div>
                        <p>No students found. Add your first student!</p>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    let html = '';
    for (const student of students) {
        const gradeClass = getGradeClass(student.grade);
        html += `
            <tr>
                <td><strong>${student.student_id}</strong></td>
                <td>${student.name}</td>
                <td>${student.department}</td>
                <td>${student.year}</td>
                <td>${student.total}</td>
                <td>${student.average}</td>
                <td><span class="grade-badge ${gradeClass}">${student.grade}</span></td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn view-btn" onclick="viewStudent('${student.student_id}')">👁</button>
                        <button class="action-btn edit-btn" onclick="editStudent('${student.student_id}')">✏️</button>
                        <button class="action-btn delete-btn" onclick="deleteStudent('${student.student_id}', '${student.name}')">🗑</button>
                    </div>
                </td>
            </tr>
        `;
    }

    tbody.innerHTML = html;
}

function getGradeClass(grade) {
    const map = {
        'A+': 'grade-a-plus',
        'A': 'grade-a',
        'B': 'grade-b',
        'C': 'grade-c',
        'D': 'grade-d',
        'F': 'grade-f'
    };
    return map[grade] || '';
}

function filterStudents() {
    const query = document.getElementById('studentSearch').value.toLowerCase().trim();
    if (query === '') {
        renderStudentsTable(allStudents);
        return;
    }
    const filtered = allStudents.filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.student_id.toLowerCase().includes(query) ||
        s.department.toLowerCase().includes(query)
    );
    renderStudentsTable(filtered);
}

// ========================== VIEW STUDENT (MODAL) ==========================

async function viewStudent(studentId) {
    const result = await apiFetch('/students/' + studentId);
    if (!result.success) {
        showToast('Student not found.', 'error');
        return;
    }

    const s = result.data;
    const gradeClass = getGradeClass(s.grade);

    let marksHtml = '';
    if (s.subjects && s.marks) {
        for (let i = 0; i < s.subjects.length; i++) {
            marksHtml += `
                <div class="detail-row">
                    <span class="label">${s.subjects[i]}</span>
                    <span class="value">${s.marks[i]}</span>
                </div>
            `;
        }
    }

    document.getElementById('modalTitle').textContent = s.name;
    document.getElementById('modalBody').innerHTML = `
        <div class="detail-row">
            <span class="label">Student ID</span>
            <span class="value">${s.student_id}</span>
        </div>
        <div class="detail-row">
            <span class="label">Age</span>
            <span class="value">${s.age}</span>
        </div>
        <div class="detail-row">
            <span class="label">Department</span>
            <span class="value">${s.department}</span>
        </div>
        <div class="detail-row">
            <span class="label">Year</span>
            <span class="value">${s.year}</span>
        </div>
        <div class="detail-row">
            <span class="label">Total Marks</span>
            <span class="value">${s.total}</span>
        </div>
        <div class="detail-row">
            <span class="label">Average</span>
            <span class="value">${s.average}</span>
        </div>
        <div class="detail-row">
            <span class="label">Highest Mark</span>
            <span class="value">${s.highest}</span>
        </div>
        <div class="detail-row">
            <span class="label">Lowest Mark</span>
            <span class="value">${s.lowest}</span>
        </div>
        <div class="detail-row">
            <span class="label">Grade</span>
            <span class="value"><span class="grade-badge ${gradeClass}">${s.grade}</span></span>
        </div>
        <div class="modal-marks-section">
            <h4>Subject-wise Marks</h4>
            ${marksHtml}
        </div>
    `;

    document.getElementById('modalOverlay').classList.add('active');
}

function closeModal() {
    document.getElementById('modalOverlay').classList.remove('active');
}

// ========================== ADD / EDIT STUDENT ==========================

async function handleFormSubmit(event) {
    event.preventDefault();

    const editMode = document.getElementById('editMode').value;
    const studentId = document.getElementById('studentId').value.trim();
    const name = document.getElementById('studentName').value.trim();
    const age = parseInt(document.getElementById('studentAge').value);
    const department = document.getElementById('studentDept').value;
    const year = parseInt(document.getElementById('studentYear').value);

    const marks = [
        parseInt(document.getElementById('markMath').value),
        parseInt(document.getElementById('markPhysics').value),
        parseInt(document.getElementById('markChemistry').value),
        parseInt(document.getElementById('markEnglish').value),
        parseInt(document.getElementById('markCS').value)
    ];

    // Basic client-side validation
    if (!studentId || !name || !department) {
        showToast('Please fill all required fields.', 'error');
        return;
    }

    for (let i = 0; i < marks.length; i++) {
        if (isNaN(marks[i]) || marks[i] < 0 || marks[i] > 100) {
            showToast('All marks must be between 0 and 100.', 'error');
            return;
        }
    }

    const payload = {
        student_id: studentId,
        name: name,
        age: age,
        department: department,
        year: year,
        marks: marks
    };

    let result;

    if (editMode === 'edit') {
        result = await apiFetch('/students/' + studentId, {
            method: 'PUT',
            body: JSON.stringify(payload)
        });
    } else {
        result = await apiFetch('/students', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
    }

    if (result.success) {
        showToast(result.message, 'success');
        resetForm();
        switchView('students');
    } else {
        showToast(result.message, 'error');
    }
}

async function editStudent(studentId) {
    const result = await apiFetch('/students/' + studentId);
    if (!result.success) {
        showToast('Student not found.', 'error');
        return;
    }

    const s = result.data;

    // Switch to form view and populate
    document.getElementById('editMode').value = 'edit';
    document.getElementById('formTitle').textContent = 'Edit Student';
    document.getElementById('formSubtitle').textContent = 'Modify student details and marks';
    document.getElementById('submitBtn').textContent = 'Update Student';

    document.getElementById('studentId').value = s.student_id;
    document.getElementById('studentId').disabled = true; // Can't change ID
    document.getElementById('studentName').value = s.name;
    document.getElementById('studentAge').value = s.age;
    document.getElementById('studentDept').value = s.department;
    document.getElementById('studentYear').value = s.year;

    if (s.marks && s.marks.length >= 5) {
        document.getElementById('markMath').value = s.marks[0];
        document.getElementById('markPhysics').value = s.marks[1];
        document.getElementById('markChemistry').value = s.marks[2];
        document.getElementById('markEnglish').value = s.marks[3];
        document.getElementById('markCS').value = s.marks[4];
    }

    switchView('add-student');
}

function resetForm() {
    document.getElementById('studentForm').reset();
    document.getElementById('editMode').value = 'add';
    document.getElementById('formTitle').textContent = 'Add New Student';
    document.getElementById('formSubtitle').textContent = 'Enter student details and marks';
    document.getElementById('submitBtn').textContent = 'Add Student';
    document.getElementById('studentId').disabled = false;
}

// ========================== DELETE STUDENT ==========================

async function deleteStudent(studentId, name) {
    if (!confirm(`Are you sure you want to delete "${name}" (${studentId})?`)) {
        return;
    }

    const result = await apiFetch('/students/' + studentId, {
        method: 'DELETE'
    });

    if (result.success) {
        showToast(result.message, 'success');
        loadStudents(); // Refresh table
        // Also refresh dashboard if it's visible
        if (currentView === 'dashboard') {
            loadDashboard();
        }
    } else {
        showToast(result.message, 'error');
    }
}

// ========================== GLOBAL SEARCH ==========================

async function handleGlobalSearch(event) {
    if (event.key !== 'Enter') return;

    const query = document.getElementById('globalSearch').value.trim();
    if (!query) return;

    const result = await apiFetch('/students?search=' + encodeURIComponent(query));
    if (result.success) {
        allStudents = result.data;
        switchView('students');
        renderStudentsTable(result.data);
        showToast(`Found ${result.count} student(s)`, 'info');
    }
}

// ========================== ANALYTICS ==========================

async function loadAnalytics() {
    const container = document.getElementById('analyticsContent');
    container.innerHTML = '<div class="loading"><div class="spinner"></div>Loading analytics...</div>';

    const result = await apiFetch('/analytics');
    if (!result.success) {
        container.innerHTML = '<div class="empty-state"><div class="icon">📈</div><p>Failed to load analytics</p></div>';
        return;
    }

    const data = result.data;
    let html = '';

    // Subject Averages
    if (data.subject_averages && Object.keys(data.subject_averages).length > 0) {
        const maxSubjAvg = Math.max(...Object.values(data.subject_averages), 1);
        let barsHtml = '';
        for (const [subject, avg] of Object.entries(data.subject_averages)) {
            const width = (avg / 100) * 100;
            barsHtml += `
                <div class="h-bar-item">
                    <span class="label">${subject}</span>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${width}%"></div>
                    </div>
                    <span class="value">${avg}</span>
                </div>
            `;
        }
        html += `
            <div class="analytics-card">
                <h3>📚 Subject Averages</h3>
                <div class="h-bar-chart">${barsHtml}</div>
            </div>
        `;
    }

    // Department Averages
    if (data.department_averages && Object.keys(data.department_averages).length > 0) {
        let barsHtml = '';
        for (const [dept, avg] of Object.entries(data.department_averages)) {
            const width = (avg / 100) * 100;
            barsHtml += `
                <div class="h-bar-item">
                    <span class="label">${dept}</span>
                    <div class="bar-track">
                        <div class="bar-fill" style="width: ${width}%; background: var(--gradient-warm)"></div>
                    </div>
                    <span class="value">${avg}</span>
                </div>
            `;
        }
        html += `
            <div class="analytics-card">
                <h3>🏛 Department Averages</h3>
                <div class="h-bar-chart">${barsHtml}</div>
            </div>
        `;
    }

    // Department Count
    if (data.department_count && Object.keys(data.department_count).length > 0) {
        let rowsHtml = '';
        for (const [dept, count] of Object.entries(data.department_count)) {
            rowsHtml += `
                <div class="stat-row">
                    <span class="key">${dept}</span>
                    <span class="val">${count} student(s)</span>
                </div>
            `;
        }
        html += `
            <div class="analytics-card">
                <h3>👥 Department Strength</h3>
                ${rowsHtml}
            </div>
        `;
    }

    // Year Distribution
    if (data.year_distribution && Object.keys(data.year_distribution).length > 0) {
        let rowsHtml = '';
        for (const [year, count] of Object.entries(data.year_distribution)) {
            rowsHtml += `
                <div class="stat-row">
                    <span class="key">Year ${year}</span>
                    <span class="val">${count} student(s)</span>
                </div>
            `;
        }
        html += `
            <div class="analytics-card">
                <h3>📅 Year Distribution</h3>
                ${rowsHtml}
            </div>
        `;
    }

    container.innerHTML = html || '<div class="empty-state"><div class="icon">📈</div><p>No analytics data available. Add students first.</p></div>';
}

// ========================== NUMPY ANALYSIS ==========================

async function loadNumpyAnalysis() {
    const container = document.getElementById('numpyContent');
    container.innerHTML = '<div class="loading"><div class="spinner"></div>Loading NumPy analysis...</div>';

    const result = await apiFetch('/analytics');
    if (!result.success) {
        container.innerHTML = '<div class="empty-state"><div class="icon">🔢</div><p>Failed to load analysis</p></div>';
        return;
    }

    const data = result.data;
    let html = '<div class="numpy-grid">';

    // Overall NumPy Stats
    if (data.numpy_stats && !data.numpy_stats.error) {
        const stats = data.numpy_stats;
        html += `
            <div class="stat-block">
                <h3>🔢 Overall NumPy Statistics</h3>
                <div class="stat-row">
                    <span class="key">Mean</span>
                    <span class="val">${stats.mean}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Median</span>
                    <span class="val">${stats.median}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Std Deviation</span>
                    <span class="val">${stats.std_deviation}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Variance</span>
                    <span class="val">${stats.variance}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Maximum</span>
                    <span class="val">${stats.max}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Minimum</span>
                    <span class="val">${stats.min}</span>
                </div>
                <div class="stat-row">
                    <span class="key">Marks Analysed</span>
                    <span class="val">${stats.total_marks_analysed}</span>
                </div>
            </div>
        `;
    } else {
        html += `
            <div class="stat-block">
                <h3>🔢 NumPy Statistics</h3>
                <div class="empty-state">
                    <p>NumPy not installed on server.<br>Run: pip install numpy</p>
                </div>
            </div>
        `;
    }

    // Per-Subject NumPy Stats
    if (data.subject_numpy && Object.keys(data.subject_numpy).length > 0) {
        let subjectHtml = '';
        for (const [subject, stats] of Object.entries(data.subject_numpy)) {
            subjectHtml += `
                <div class="stat-row">
                    <span class="key">${subject}</span>
                    <span class="val">μ=${stats.mean} σ=${stats.std} ↑${stats.max} ↓${stats.min}</span>
                </div>
            `;
        }
        html += `
            <div class="stat-block">
                <h3>📊 Per-Subject NumPy Analysis</h3>
                ${subjectHtml}
            </div>
        `;
    }

    html += '</div>';
    container.innerHTML = html;
}

// ========================== PANDAS ANALYSIS ==========================

async function loadPandasAnalysis() {
    const container = document.getElementById('pandasContent');
    container.innerHTML = '<div class="loading"><div class="spinner"></div>Loading Pandas analysis...</div>';

    const result = await apiFetch('/analytics');
    if (!result.success) {
        container.innerHTML = '<div class="empty-state"><div class="icon">🐼</div><p>Failed to load analysis</p></div>';
        return;
    }

    const data = result.data;
    let html = '<div class="pandas-grid">';

    // Pandas head() preview
    if (data.pandas_head && data.pandas_head.length > 0) {
        const columns = Object.keys(data.pandas_head[0]);
        let tableHtml = '<table class="pandas-table"><thead><tr>';
        for (const col of columns) {
            tableHtml += `<th>${col}</th>`;
        }
        tableHtml += '</tr></thead><tbody>';
        for (const row of data.pandas_head) {
            tableHtml += '<tr>';
            for (const col of columns) {
                let val = row[col];
                if (typeof val === 'number' && !Number.isInteger(val)) {
                    val = val.toFixed(2);
                }
                tableHtml += `<td>${val}</td>`;
            }
            tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table>';

        html += `
            <div class="stat-block" style="grid-column: 1 / -1">
                <h3>🐼 DataFrame — head()</h3>
                <p style="color: var(--text-muted); font-size: 0.82rem; margin-bottom: 12px">
                    First 5 rows of the student DataFrame
                </p>
                <div class="pandas-table-wrapper">${tableHtml}</div>
            </div>
        `;
    } else if (data.pandas_summary && data.pandas_summary.error) {
        html += `
            <div class="stat-block">
                <h3>🐼 Pandas</h3>
                <div class="empty-state">
                    <p>Pandas not installed on server.<br>Run: pip install pandas</p>
                </div>
            </div>
        `;
    }

    // Pandas describe()
    if (data.pandas_summary && !data.pandas_summary.error && Object.keys(data.pandas_summary).length > 0) {
        const describeCols = Object.keys(data.pandas_summary);
        const describeRows = Object.keys(data.pandas_summary[describeCols[0]] || {});

        let tableHtml = '<table class="pandas-table"><thead><tr><th>Statistic</th>';
        for (const col of describeCols) {
            tableHtml += `<th>${col}</th>`;
        }
        tableHtml += '</tr></thead><tbody>';

        for (const row of describeRows) {
            tableHtml += `<tr><td><strong>${row}</strong></td>`;
            for (const col of describeCols) {
                const val = data.pandas_summary[col][row];
                tableHtml += `<td>${typeof val === 'number' ? val.toFixed(2) : val}</td>`;
            }
            tableHtml += '</tr>';
        }
        tableHtml += '</tbody></table>';

        html += `
            <div class="stat-block" style="grid-column: 1 / -1">
                <h3>📋 DataFrame — describe()</h3>
                <p style="color: var(--text-muted); font-size: 0.82rem; margin-bottom: 12px">
                    Statistical summary of numeric columns
                </p>
                <div class="pandas-table-wrapper">${tableHtml}</div>
            </div>
        `;
    }

    html += '</div>';
    container.innerHTML = html || '<div class="empty-state"><div class="icon">🐼</div><p>No Pandas data available. Add students first.</p></div>';
}

// ========================== TOAST NOTIFICATIONS ==========================

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');

    const icons = {
        success: '✓',
        error: '✗',
        info: 'ℹ'
    };

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${icons[type] || 'ℹ'}</span> ${message}`;

    container.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// ========================== KEYBOARD SHORTCUTS ==========================

document.addEventListener('keydown', (e) => {
    // Escape to close modal
    if (e.key === 'Escape') {
        closeModal();
    }
});
