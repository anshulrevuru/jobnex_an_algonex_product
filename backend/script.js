document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = '';

    // DOM Elements
    const dbStatusPill = document.getElementById('dbStatusPill');
    const dbStatusText = document.getElementById('dbStatusText');
    const resumeForm = document.getElementById('resumeForm');
    const resumeMessage = document.getElementById('resumeMessage');
    const saveResumeBtn = document.getElementById('saveResumeBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analyzerResume = document.getElementById('analyzerResume');
    const analyzerJd = document.getElementById('analyzerJd');
    const saveAnalysisDb = document.getElementById('saveAnalysisDb');
    const analysisResult = document.getElementById('analysisResult');
    const scoreValue = document.getElementById('scoreValue');
    const scoreAnalysisSummary = document.getElementById('scoreAnalysisSummary');
    const matchedSkillsList = document.getElementById('matchedSkillsList');
    const missingSkillsList = document.getElementById('missingSkillsList');
    const suggestionsList = document.getElementById('suggestionsList');
    const resumesTableBody = document.getElementById('resumesTableBody');
    const refreshResumesBtn = document.getElementById('refreshResumesBtn');

    // 1. Check DB Health Status
    async function checkDbStatus() {
        try {
            const res = await fetch(`${API_BASE}/api/db-status`);
            const data = await res.json();
            if (data.connected) {
                dbStatusPill.className = 'db-status-pill connected';
                dbStatusText.textContent = `MySQL Connected (${data.config.database})`;
            } else {
                dbStatusPill.className = 'db-status-pill disconnected';
                dbStatusText.textContent = 'MySQL Disconnected (Check .env)';
            }
        } catch (err) {
            dbStatusPill.className = 'db-status-pill disconnected';
            dbStatusText.textContent = 'Backend Offline';
        }
    }

    // 2. Load Resumes Table
    async function loadResumes() {
        try {
            const res = await fetch(`${API_BASE}/api/resumes`);
            const data = await res.json();
            if (data.status === 'success' && data.resumes) {
                if (data.resumes.length === 0) {
                    resumesTableBody.innerHTML = '<tr><td colspan="6" class="text-center">No resumes found in database. Create one above!</td></tr>';
                    return;
                }
                resumesTableBody.innerHTML = data.resumes.map(r => `
                    <tr>
                        <td><strong>#${r.id}</strong></td>
                        <td>${escapeHtml(r.name || 'N/A')}</td>
                        <td>${escapeHtml(r.email || 'N/A')}</td>
                        <td>${escapeHtml(r.phone || '-')}</td>
                        <td><small>${escapeHtml(r.skills || '-')}</small></td>
                        <td><small>${r.created_at || '-'}</small></td>
                    </tr>
                `).join('');
            }
        } catch (err) {
            resumesTableBody.innerHTML = '<tr><td colspan="6" class="text-center" style="color:var(--danger)">Failed to load resumes. Check DB connection.</td></tr>';
        }
    }

    // 3. Handle Resume Creation
    resumeForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        saveResumeBtn.disabled = true;
        saveResumeBtn.textContent = 'Saving...';
        resumeMessage.className = 'alert-box';
        resumeMessage.style.display = 'none';

        const payload = {
            name: document.getElementById('name').value.trim(),
            email: document.getElementById('email').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            skills: document.getElementById('skills').value.split(',').map(s => s.trim()).filter(Boolean),
            education: document.getElementById('education').value.trim(),
            experience: document.getElementById('experience').value.trim(),
            summary: document.getElementById('summary').value.trim()
        };

        try {
            const res = await fetch(`${API_BASE}/api/resume`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (res.ok && data.status === 'success') {
                resumeMessage.className = 'alert-box success';
                resumeMessage.textContent = `✅ Resume created successfully (ID #${data.resume_id}) in MySQL!`;
                resumeForm.reset();
                loadResumes();
            } else {
                resumeMessage.className = 'alert-box error';
                resumeMessage.textContent = `❌ ${data.detail || 'Failed to save resume'}`;
            }
        } catch (err) {
            resumeMessage.className = 'alert-box error';
            resumeMessage.textContent = `❌ Network/Server error: ${err.message}`;
        } finally {
            saveResumeBtn.disabled = false;
            saveResumeBtn.textContent = '💾 Save Resume to MySQL';
        }
    });

    // 4. Handle Resume Analysis
    analyzeBtn.addEventListener('click', async () => {
        const resumeText = analyzerResume.value.trim();
        const jdText = analyzerJd.value.trim();

        if (!resumeText || !jdText) {
            alert('Please enter both Resume Text and Job Description to analyze.');
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';

        try {
            const res = await fetch(`${API_BASE}/api/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume: resumeText,
                    job_description: jdText,
                    save_to_db: saveAnalysisDb.checked
                })
            });

            const data = await res.json();

            if (res.ok && data.status === 'success') {
                scoreValue.textContent = `${data.score}%`;
                scoreAnalysisSummary.textContent = `${data.matched_skills.length} matched skills, ${data.missing_skills.length} missing skill(s).`;

                matchedSkillsList.innerHTML = data.matched_skills.length > 0
                    ? data.matched_skills.map(s => `<span class="tag matched">${escapeHtml(s)}</span>`).join('')
                    : '<span style="font-size:12px;color:var(--text-muted)">No matching skills found</span>';

                missingSkillsList.innerHTML = data.missing_skills.length > 0
                    ? data.missing_skills.map(s => `<span class="tag missing">${escapeHtml(s)}</span>`).join('')
                    : '<span style="font-size:12px;color:var(--success)">No missing skills! Full match!</span>';

                suggestionsList.innerHTML = data.suggestions.map(s => `<li>${escapeHtml(s)}</li>`).join('');

                analysisResult.style.display = 'flex';
            } else {
                alert(`Analysis failed: ${data.detail || 'Unknown error'}`);
            }
        } catch (err) {
            alert(`Error during analysis: ${err.message}`);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🔍 Analyze Match';
        }
    });

    // Refresh Button
    refreshResumesBtn.addEventListener('click', () => {
        loadResumes();
        checkDbStatus();
    });

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // Initial load
    checkDbStatus();
    loadResumes();
});
