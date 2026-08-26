// JANSAHAY Frontend SPA Controller
const app = {
  currentUser: null,
  token: null,
  services: [],
  selectedService: null,
  currentWizardStep: 1,
  wizardAnswers: {},
  uploadedDocuments: {}, // requirement_id -> doc metadata
  currentCaseDetail: null,
  activeCategory: 'ALL',
  officerFilter: 'ALL',

  async init() {
    // Check saved persona or default to citizen_rahul
    const savedUser = localStorage.getItem('jansahay_persona') || 'citizen_rahul';
    const select = document.getElementById('persona-select');
    if (select) select.value = savedUser;
    
    await this.loginAs(savedUser);
    await this.loadServices();
    this.refreshIcons();
  },

  refreshIcons() {
    setTimeout(() => {
      if (window.lucide) {
        window.lucide.createIcons();
      }
    }, 50);
  },

  async loginAs(username) {
    try {
      const resp = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password: 'Password123!' })
      });
      if (!resp.ok) throw new Error('Login failed');
      const data = await resp.json();
      this.token = data.access_token;
      this.currentUser = data.user;
      localStorage.setItem('jansahay_token', this.token);
      localStorage.setItem('jansahay_persona', username);

      this.updateUserContextUI();
      await this.loadNotifications();

      // If officer, automatically open officer queue
      if (this.currentUser.role !== 'CITIZEN') {
        this.navigate('officer-queue');
      } else {
        this.navigate('home');
      }
    } catch (err) {
      console.error('Authentication Error:', err);
    }
  },

  async switchPersona(username) {
    await this.loginAs(username);
  },

  updateUserContextUI() {
    if (!this.currentUser) return;
    const nameEl = document.getElementById('user-display-name');
    const roleBadge = document.getElementById('user-role-badge');
    const scopeInfo = document.getElementById('user-scope-info');
    const avatar = document.getElementById('user-avatar');
    const officerNav = document.getElementById('nav-officer-queue');

    if (nameEl) nameEl.textContent = this.currentUser.full_name;
    if (roleBadge) {
      roleBadge.textContent = this.currentUser.role.replace('_', ' ');
      roleBadge.className = `px-2 py-0.5 text-xs font-semibold rounded ${
        this.currentUser.role === 'CITIZEN' ? 'bg-blue-100 text-blue-800' : 'bg-emerald-100 text-emerald-800'
      }`;
    }

    if (scopeInfo) {
      if (this.currentUser.role === 'CITIZEN') {
        scopeInfo.textContent = `Central Delhi District · Aadhaar: ****4321`;
      } else {
        scopeInfo.textContent = `Dept: ${this.currentUser.department_code || 'Revenue'} · Jur: ${this.currentUser.jurisdiction_code || 'Delhi Central'} · Desk: ${this.currentUser.designation || 'In-Charge'}`;
      }
    }

    if (avatar) {
      const initials = this.currentUser.full_name.split(' ').map(n => n[0]).join('').slice(0, 2);
      avatar.textContent = initials;
    }

    if (officerNav) {
      if (this.currentUser.role !== 'CITIZEN') {
        officerNav.classList.remove('hidden');
      } else {
        officerNav.classList.add('hidden');
      }
    }
  },

  navigate(viewName) {
    const views = ['home', 'wizard', 'my-cases', 'officer-queue'];
    views.forEach(v => {
      const el = document.getElementById(`view-${v}`);
      if (el) el.classList.add('hidden');
    });

    const activeEl = document.getElementById(`view-${viewName}`);
    if (activeEl) activeEl.classList.remove('hidden');

    if (viewName === 'my-cases') this.loadCases();
    if (viewName === 'officer-queue') this.loadOfficerQueue();

    this.refreshIcons();
  },

  async loadServices() {
    try {
      const resp = await fetch('/api/v1/services');
      this.services = await resp.json();
      this.renderServices();
    } catch (err) {
      console.error('Error loading services:', err);
    }
  },

  setCategoryFilter(cat) {
    this.activeCategory = cat;
    ['ALL', 'CERTIFICATES', 'SOCIAL_SECURITY', 'GRIEVANCES'].forEach(c => {
      const tab = document.getElementById(`tab-cat-${c}`);
      if (tab) {
        if (c === cat) {
          tab.className = 'px-4 py-2 text-xs font-bold rounded-lg bg-gov-navy text-white transition';
        } else {
          tab.className = 'px-4 py-2 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-200 transition';
        }
      }
    });
    this.renderServices();
  },

  filterServices(query) {
    this.renderServices(query.toLowerCase());
  },

  renderServices(searchQuery = '') {
    const grid = document.getElementById('services-grid');
    if (!grid) return;

    let filtered = this.services;
    if (this.activeCategory !== 'ALL') {
      filtered = filtered.filter(s => s.category === this.activeCategory);
    }
    if (searchQuery) {
      filtered = filtered.filter(s => s.title.toLowerCase().includes(searchQuery) || s.code.toLowerCase().includes(searchQuery));
    }

    grid.innerHTML = filtered.map(s => `
      <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between group">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider rounded ${
              s.category === 'CERTIFICATES' ? 'bg-amber-100 text-amber-800' :
              s.category === 'SOCIAL_SECURITY' ? 'bg-blue-100 text-blue-800' : 'bg-rose-100 text-rose-800'
            }">${s.category.replace('_', ' ')}</span>
            <span class="text-xs text-slate-500 font-medium flex items-center gap-1">
              <i data-lucide="clock" class="w-3.5 h-3.5 text-slate-400"></i> SLA: ${s.sla_days} Days
            </span>
          </div>
          <h3 class="text-base font-bold text-slate-900 group-hover:text-amber-700 transition">${s.title}</h3>
          <p class="text-xs text-slate-500 mt-2 line-clamp-2">${s.eligibility_criteria_json.description || 'Public service application'}</p>
        </div>
        
        <div class="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
          <span class="text-xs text-slate-400 font-medium">${s.requirements ? s.requirements.length : 0} Mandatory Docs</span>
          <button onclick="app.startWizard('${s.id}')" class="px-4 py-2 bg-gov-navy text-white text-xs font-semibold rounded-lg hover:bg-slate-800 transition flex items-center gap-1.5 shadow-sm">
            <span>Apply Now</span>
            <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>
    `).join('');

    this.refreshIcons();
  },

  startWizard(serviceId) {
    this.selectedService = this.services.find(s => s.id === serviceId);
    if (!this.selectedService) return;

    this.currentWizardStep = 1;
    this.wizardAnswers = {};
    this.uploadedDocuments = {};

    document.getElementById('wizard-service-badge').textContent = `${this.selectedService.title} Journey`;
    this.renderWizardStep1();
    this.navigate('wizard');
  },

  renderWizardStep1() {
    const container = document.getElementById('eligibility-questions-container');
    const questions = this.selectedService.eligibility_criteria_json.questions || [];

    container.innerHTML = questions.map((q, idx) => `
      <div class="p-4 rounded-xl bg-slate-50 border border-slate-200">
        <label class="block font-semibold text-slate-800 text-xs mb-2">Q${idx + 1}: ${q.text}</label>
        <div class="flex items-center gap-4">
          <label class="flex items-center gap-1.5 text-xs text-slate-700 cursor-pointer">
            <input type="radio" name="q_${q.id}" value="true" checked onchange="app.wizardAnswers['${q.id}']=true" class="text-amber-600">
            <span>Yes, Confirmed</span>
          </label>
          <label class="flex items-center gap-1.5 text-xs text-slate-700 cursor-pointer">
            <input type="radio" name="q_${q.id}" value="false" onchange="app.wizardAnswers['${q.id}']=false" class="text-amber-600">
            <span>No</span>
          </label>
        </div>
      </div>
    `).join('');

    questions.forEach(q => this.wizardAnswers[q.id] = true);
    this.updateWizardStepUI(1);
  },

  renderWizardStep2() {
    const container = document.getElementById('checklist-items-container');
    const reqs = this.selectedService.requirements || [];

    container.innerHTML = reqs.map((r, idx) => `
      <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 flex items-start gap-3">
        <div class="w-6 h-6 rounded-full bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-xs shrink-0 mt-0.5">
          ${idx + 1}
        </div>
        <div class="flex-1">
          <div class="flex items-center justify-between">
            <h4 class="font-bold text-slate-900 text-xs">${r.document_name}</h4>
            <span class="px-2 py-0.5 text-[10px] font-bold rounded ${r.is_mandatory ? 'bg-rose-100 text-rose-800' : 'bg-slate-200 text-slate-700'}">
              ${r.is_mandatory ? 'MANDATORY' : 'OPTIONAL'}
            </span>
          </div>
          <p class="text-[11px] text-slate-500 mt-1">Accepted: ${r.allowed_extensions} · Max Size: ${Math.round(r.max_size_kb / 1024)}MB</p>
        </div>
      </div>
    `).join('');

    this.updateWizardStepUI(2);
  },

  renderWizardStep3() {
    const container = document.getElementById('upload-dropzones-container');
    const reqs = this.selectedService.requirements || [];

    container.innerHTML = reqs.map(r => {
      const doc = this.uploadedDocuments[r.id];
      return `
        <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2" id="dropzone-${r.id}">
          <div class="flex items-center justify-between">
            <span class="font-bold text-xs text-slate-800">${r.document_name}</span>
            <span id="status-${r.id}" class="text-[10px] font-bold px-2 py-0.5 rounded ${doc ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'}">
              ${doc ? 'SCAN PASSED ✓' : 'PENDING UPLOAD'}
            </span>
          </div>
          <div class="flex items-center gap-3">
            <input type="file" id="file-${r.id}" onchange="app.handleFileUpload('${r.id}', this)" class="text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-gov-navy file:text-white hover:file:bg-slate-800 cursor-pointer">
            ${doc ? `<span class="text-xs text-emerald-700 font-medium truncate">${doc.file_name}</span>` : ''}
          </div>
        </div>
      `;
    }).join('');

    this.updateWizardStepUI(3);
  },

  async handleFileUpload(requirementId, inputEl) {
    const file = inputEl.files[0];
    if (!file) return;

    const statusBadge = document.getElementById(`status-${requirementId}`);
    if (statusBadge) {
      statusBadge.textContent = 'SCANNING & VALIDATING...';
      statusBadge.className = 'text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-800 badge-pulse';
    }

    const formData = new FormData();
    formData.append('file', file);
    formData.append('requirement_id', requirementId);
    formData.append('case_id', 'temp');

    try {
      const resp = await fetch('/api/v1/documents/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });
      if (!resp.ok) throw new Error('Upload failed');
      const doc = await resp.json();
      this.uploadedDocuments[requirementId] = doc;

      if (statusBadge) {
        statusBadge.textContent = 'SCAN PASSED ✓';
        statusBadge.className = 'text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800';
      }
    } catch (err) {
      if (statusBadge) {
        statusBadge.textContent = 'FAILED';
        statusBadge.className = 'text-[10px] font-bold px-2 py-0.5 rounded bg-rose-100 text-rose-800';
      }
    }
  },

  renderWizardStep4() {
    document.getElementById('decl-name').textContent = this.currentUser ? this.currentUser.full_name : 'Citizen';
    document.getElementById('decl-service').textContent = this.selectedService.title;
    const docCount = Object.keys(this.uploadedDocuments).length;
    document.getElementById('decl-doc-count').textContent = `${docCount} Documents Attached (Sandbox Passed)`;
    this.updateWizardStepUI(4);
  },

  wizardNext(step) {
    if (step === 2) this.renderWizardStep2();
    if (step === 3) this.renderWizardStep3();
    if (step === 4) this.renderWizardStep4();
    this.currentWizardStep = step;
  },

  wizardPrev(step) {
    this.currentWizardStep = step;
    this.updateWizardStepUI(step);
  },

  updateWizardStepUI(step) {
    [1, 2, 3, 4].forEach(s => {
      const view = document.getElementById(`wizard-step-${s}`);
      const dot = document.getElementById(`step-dot-${s}`);
      if (view) {
        if (s === step) view.classList.remove('hidden');
        else view.classList.add('hidden');
      }
      if (dot) {
        if (s === step) {
          dot.className = 'w-8 h-8 rounded-full bg-gov-navy text-white flex items-center justify-center font-bold text-xs shadow';
        } else if (s < step) {
          dot.className = 'w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-xs';
        } else {
          dot.className = 'w-8 h-8 rounded-full bg-slate-200 text-slate-600 flex items-center justify-center font-bold text-xs';
        }
      }
    });
    this.refreshIcons();
  },

  async submitApplication() {
    const declChecked = document.getElementById('decl-checkbox').checked;
    if (!declChecked) {
      alert('Please check the statutory declaration checkbox before submitting.');
      return;
    }

    const docIds = Object.values(this.uploadedDocuments).map(d => d.id);
    const payload = {
      service_id: this.selectedService.id,
      jurisdiction_id: '',
      form_data: {
        applicant_name: this.currentUser.full_name,
        declaration_accepted: true,
        eligibility_responses: this.wizardAnswers,
        annual_family_income: 180000
      },
      document_ids: docIds
    };

    try {
      const resp = await fetch('/api/v1/cases', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) throw new Error('Submission failed');
      const createdCase = await resp.json();

      alert(`Application Submitted Successfully!\nPublic Case Tracking ID: ${createdCase.public_case_id}`);
      this.navigate('my-cases');
    } catch (err) {
      alert('Error submitting application: ' + err.message);
    }
  },

  async loadCases() {
    try {
      const resp = await fetch('/api/v1/cases', {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
      if (!resp.ok) throw new Error('Failed to load cases');
      const cases = await resp.json();
      this.renderCases(cases);
    } catch (err) {
      console.error('Error loading cases:', err);
    }
  },

  renderCases(cases) {
    const container = document.getElementById('cases-list-container');
    if (!container) return;

    if (!cases || cases.length === 0) {
      container.innerHTML = `
        <div class="bg-white p-12 text-center rounded-2xl border border-slate-200 space-y-3">
          <i data-lucide="inbox" class="w-12 h-12 text-slate-300 mx-auto"></i>
          <h3 class="font-bold text-slate-800 text-base">No Active Cases Found</h3>
          <p class="text-xs text-slate-500 max-w-sm mx-auto">You haven't submitted any applications yet. Explore available public services on the home catalog.</p>
          <button onclick="app.navigate('home')" class="mt-2 px-4 py-2 bg-gov-navy text-white text-xs font-semibold rounded-lg hover:bg-slate-800">Browse Services</button>
        </div>
      `;
      this.refreshIcons();
      return;
    }

    container.innerHTML = cases.map(c => `
      <div class="bg-white rounded-xl border ${c.action_required ? 'border-amber-400 ring-2 ring-amber-400/20' : 'border-slate-200'} p-5 shadow-sm hover:shadow transition flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="space-y-1.5">
          <div class="flex items-center gap-2">
            <span class="font-mono font-bold text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">${c.public_case_id}</span>
            <span class="text-xs font-bold text-slate-900">${c.service_title}</span>
            <span class="px-2 py-0.5 text-[10px] font-bold rounded ${
              c.current_state === 'RESOLVED' ? 'bg-emerald-100 text-emerald-800' :
              c.current_state === 'ACTION_REQUIRED' ? 'bg-amber-500 text-white badge-pulse' :
              c.current_state === 'REJECTED' ? 'bg-rose-100 text-rose-800' : 'bg-blue-100 text-blue-800'
            }">${c.current_state}</span>
          </div>
          <p class="text-xs text-slate-600 font-medium">${c.citizen_status}</p>
          <p class="text-[11px] text-slate-400">Submitted: ${new Date(c.submitted_at).toLocaleDateString()} · Last Updated: ${new Date(c.updated_at).toLocaleTimeString()}</p>
        </div>

        <div class="flex items-center gap-2">
          ${c.action_required ? `
            <button onclick="app.openCaseDetail('${c.id}')" class="px-3.5 py-2 bg-amber-500 text-white text-xs font-bold rounded-lg hover:bg-amber-600 flex items-center gap-1.5 shadow-sm">
              <i data-lucide="alert-circle" class="w-4 h-4"></i> Fix Defect
            </button>
          ` : `
            <button onclick="app.openCaseDetail('${c.id}')" class="px-3.5 py-2 bg-slate-100 text-slate-700 text-xs font-semibold rounded-lg hover:bg-slate-200 flex items-center gap-1.5">
              <span>View Case & Timeline</span>
              <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
            </button>
          `}
        </div>
      </div>
    `).join('');

    this.refreshIcons();
  },

  async loadOfficerQueue() {
    try {
      let url = '/api/v1/cases';
      if (this.officerFilter !== 'ALL') {
        url += `?status_filter=${this.officerFilter}`;
      }
      const resp = await fetch(url, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
      if (!resp.ok) throw new Error('Failed to load officer queue');
      const cases = await resp.json();
      this.renderOfficerTable(cases);
    } catch (err) {
      console.error('Error loading queue:', err);
    }
  },

  setOfficerFilter(filter) {
    this.officerFilter = filter;
    ['ALL', 'VERIFICATION', 'DEPARTMENT_REVIEW', 'APPROVAL', 'RESOLVED'].forEach(f => {
      const tab = document.getElementById(`off-filter-${f}`);
      if (tab) {
        if (f === filter) tab.className = 'px-3 py-1.5 rounded-lg bg-gov-navy text-white font-semibold';
        else tab.className = 'px-3 py-1.5 rounded-lg text-slate-600 hover:bg-slate-200';
      }
    });
    this.loadOfficerQueue();
  },

  renderOfficerTable(cases) {
    const container = document.getElementById('officer-cases-table-container');
    if (!container) return;

    if (!cases || cases.length === 0) {
      container.innerHTML = `<div class="p-12 text-center text-slate-500 text-xs">No cases matching filter in your queue.</div>`;
      return;
    }

    container.innerHTML = `
      <table class="w-full text-left text-xs">
        <thead class="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-200">
          <tr>
            <th class="py-3 px-4">Case ID</th>
            <th class="py-3 px-4">Applicant</th>
            <th class="py-3 px-4">Service</th>
            <th class="py-3 px-4">Current Stage</th>
            <th class="py-3 px-4">Submitted</th>
            <th class="py-3 px-4 text-right">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          ${cases.map(c => `
            <tr class="hover:bg-slate-50 transition cursor-pointer" onclick="app.openCaseDetail('${c.id}')">
              <td class="py-3.5 px-4 font-mono font-bold text-amber-700">${c.public_case_id}</td>
              <td class="py-3.5 px-4 font-semibold text-slate-800">${c.citizen_name}</td>
              <td class="py-3.5 px-4 text-slate-600">${c.service_title}</td>
              <td class="py-3.5 px-4">
                <span class="px-2 py-0.5 text-[10px] font-bold rounded ${
                  c.current_state === 'RESOLVED' ? 'bg-emerald-100 text-emerald-800' :
                  c.current_state === 'ACTION_REQUIRED' ? 'bg-amber-100 text-amber-800' :
                  c.current_state === 'APPROVAL' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
                }">${c.current_state}</span>
              </td>
              <td class="py-3.5 px-4 text-slate-400">${new Date(c.submitted_at).toLocaleDateString()}</td>
              <td class="py-3.5 px-4 text-right">
                <button class="px-3 py-1 bg-gov-navy text-white text-xs font-semibold rounded hover:bg-slate-800">Scrutinize</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
    this.refreshIcons();
  },

  async openCaseDetail(caseId) {
    try {
      const resp = await fetch(`/api/v1/cases/${caseId}`, {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
      if (!resp.ok) throw new Error('Failed to fetch case detail');
      this.currentCaseDetail = await resp.json();
      this.renderCaseModal();
    } catch (err) {
      alert('Cannot view case: ' + err.message);
    }
  },

  renderCaseModal() {
    const c = this.currentCaseDetail;
    if (!c) return;

    document.getElementById('modal-public-id').textContent = c.public_case_id;
    document.getElementById('modal-status-badge').textContent = c.current_state;
    document.getElementById('modal-service-title').textContent = `${c.service_title} · ${c.department_name}`;
    document.getElementById('modal-citizen-status').textContent = c.citizen_status;
    document.getElementById('modal-case-version').textContent = c.version_id;

    // Action Required Banner
    const actionRequiredAlert = document.getElementById('modal-action-required-alert');
    if (c.action_required) {
      actionRequiredAlert.classList.remove('hidden');
      document.getElementById('modal-action-required-remarks').textContent = c.resolution_remarks || 'Defective document noted by verification desk.';
      
      // Citizen re-upload box
      const reuploadBox = document.getElementById('citizen-reupload-box');
      if (this.currentUser.role === 'CITIZEN') {
        const deficientDoc = c.documents.find(d => d.status === 'REPLACEMENT_REQUIRED');
        if (deficientDoc) {
          reuploadBox.innerHTML = `
            <div class="p-3 bg-white rounded-lg border border-amber-300 space-y-2 mt-2">
              <span class="font-bold text-xs text-amber-900">Upload Replacement for: ${deficientDoc.file_name}</span>
              <input type="file" id="reupload-file-input" class="text-xs text-slate-500 file:mr-2 file:py-1 file:px-2 file:rounded file:bg-amber-600 file:text-white file:border-0 cursor-pointer">
              <button onclick="app.submitReplacementDocument('${c.id}', '${deficientDoc.id}')" class="px-4 py-1.5 bg-amber-600 text-white font-bold rounded hover:bg-amber-700">Submit Replacement</button>
            </div>
          `;
        }
      } else {
        reuploadBox.innerHTML = `<span class="text-xs text-amber-800 italic">Waiting for citizen to upload replacement document.</span>`;
      }
    } else {
      actionRequiredAlert.classList.add('hidden');
    }

    // Applicant Declarations
    const appFields = document.getElementById('modal-applicant-fields');
    appFields.innerHTML = `
      <div class="flex justify-between py-1"><span class="text-slate-500">Applicant:</span><span class="font-semibold text-slate-800">${c.citizen_name}</span></div>
      <div class="flex justify-between py-1"><span class="text-slate-500">Aadhaar (Synthetic):</span><span class="font-semibold text-slate-800">****${c.citizen_aadhaar_last4}</span></div>
      <div class="flex justify-between py-1"><span class="text-slate-500">Phone:</span><span class="font-semibold text-slate-800">${c.citizen_phone}</span></div>
      <div class="flex justify-between py-1"><span class="text-slate-500">Jurisdiction:</span><span class="font-semibold text-slate-800">${c.jurisdiction_name}</span></div>
      ${Object.entries(c.form_data || {}).map(([k, v]) => `
        <div class="flex justify-between py-1"><span class="text-slate-500 capitalize">${k.replace('_', ' ')}:</span><span class="font-semibold text-slate-800">${typeof v === 'object' ? JSON.stringify(v) : v}</span></div>
      `).join('')}
    `;

    // Documents Matrix
    const docsList = document.getElementById('modal-documents-list');
    docsList.innerHTML = (c.documents || []).map(d => `
      <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 flex flex-col gap-2">
        <div class="flex items-center justify-between">
          <span class="font-semibold text-slate-800 truncate">${d.file_name}</span>
          <span class="px-2 py-0.5 text-[10px] font-bold rounded ${
            d.status === 'VERIFIED' ? 'bg-emerald-100 text-emerald-800' :
            d.status === 'REPLACEMENT_REQUIRED' ? 'bg-rose-100 text-rose-800' : 'bg-slate-200 text-slate-700'
          }">${d.status}</span>
        </div>
        ${this.currentUser.role !== 'CITIZEN' ? `
          <div class="flex items-center gap-2 pt-1 border-t border-slate-200">
            <label class="text-[11px] flex items-center gap-1 cursor-pointer">
              <input type="radio" name="doc_status_${d.id}" value="VERIFIED" ${d.status === 'VERIFIED' ? 'checked' : ''} class="text-emerald-600">
              <span>Accept</span>
            </label>
            <label class="text-[11px] flex items-center gap-1 cursor-pointer text-rose-700">
              <input type="radio" name="doc_status_${d.id}" value="REPLACEMENT_REQUIRED" ${d.status === 'REPLACEMENT_REQUIRED' ? 'checked' : ''} class="text-rose-600">
              <span>Reject/Deficient</span>
            </label>
          </div>
        ` : ''}
      </div>
    `).join('');

    // Certificate Preview if RESOLVED
    const certPreview = document.getElementById('modal-certificate-preview');
    if (c.current_state === 'RESOLVED') {
      certPreview.classList.remove('hidden');
      document.getElementById('cert-holder-name').textContent = c.citizen_name;
      document.getElementById('cert-number').textContent = `DL/INC/2026/${c.public_case_id.split('-').pop()}`;
    } else {
      certPreview.classList.add('hidden');
    }

    // SHA-256 Audit Trail
    const auditTimeline = document.getElementById('modal-audit-timeline');
    auditTimeline.innerHTML = (c.audit_events || []).map(e => `
      <div class="py-1 border-b border-slate-800 last:border-0">
        <div class="flex items-center justify-between text-slate-400">
          <span>#${e.event_sequence} · ${e.action} (${e.actor_role})</span>
          <span>${new Date(e.created_at).toLocaleTimeString()}</span>
        </div>
        <div class="text-slate-200 mt-0.5">${e.from_state} &rarr; <span class="text-amber-400 font-bold">${e.to_state}</span></div>
        ${e.remarks ? `<div class="text-slate-400 italic text-[10px]">"${e.remarks}"</div>` : ''}
        <div class="text-[9px] text-slate-500 truncate mt-0.5">Hash: ${e.event_hash}</div>
      </div>
    `).join('');

    // Action Buttons in Footer
    const actionBtns = document.getElementById('modal-action-buttons-container');
    const available = c.available_actions || [];

    if (available.length === 0) {
      actionBtns.innerHTML = `<span class="text-xs text-slate-400 italic">No workflow actions available for your role at this stage.</span>`;
    } else {
      actionBtns.innerHTML = available.map(a => `
        <button onclick="app.triggerWorkflowAction('${c.id}', '${a.action}')" class="px-4 py-2 text-xs font-bold rounded-lg shadow transition flex items-center gap-1.5 ${
          a.action === 'APPROVE' || a.action === 'VERIFY' || a.action === 'FORWARD' ? 'bg-emerald-600 text-white hover:bg-emerald-700' :
          a.action === 'REQUEST_CORRECTION' ? 'bg-amber-600 text-white hover:bg-amber-700' :
          a.action === 'REJECT' ? 'bg-rose-600 text-white hover:bg-rose-700' : 'bg-gov-navy text-white hover:bg-slate-800'
        }">
          <span>${a.label}</span>
        </button>
      `).join('');
    }

    document.getElementById('case-detail-modal').classList.remove('hidden');
    this.refreshIcons();
  },

  closeCaseModal() {
    document.getElementById('case-detail-modal').classList.add('hidden');
  },

  async triggerWorkflowAction(caseId, actionName) {
    const c = this.currentCaseDetail;
    if (!c) return;

    let remarks = prompt(`Enter officer remarks / justification for action: ${actionName}`, 'Verified according to statutory guidelines.');
    if (remarks === null) return;

    // Collect document statuses
    const docVerifs = [];
    (c.documents || []).forEach(d => {
      const selected = document.querySelector(`input[name="doc_status_${d.id}"]:checked`);
      if (selected) {
        docVerifs.push({ document_id: d.id, status: selected.value, notes: remarks });
      }
    });

    const payload = {
      version_id: c.version_id,
      remarks: remarks,
      document_verifications: docVerifs.length > 0 ? docVerifs : null
    };

    try {
      const resp = await fetch(`/api/v1/cases/${caseId}/actions/${actionName}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) {
        const errData = await resp.json();
        throw new Error(errData.detail || 'Action failed');
      }
      this.currentCaseDetail = await resp.json();
      this.renderCaseModal();
      this.loadOfficerQueue();
    } catch (err) {
      alert(`Action Error: ${err.message}`);
    }
  },

  async submitReplacementDocument(caseId, targetDocId) {
    const fileInput = document.getElementById('reupload-file-input');
    if (!fileInput || !fileInput.files[0]) {
      alert('Please choose a replacement file.');
      return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('requirement_id', targetDocId);
    formData.append('case_id', caseId);

    try {
      const uploadResp = await fetch('/api/v1/documents/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });
      if (!uploadResp.ok) throw new Error('File upload failed');
      const uploadedDoc = await uploadResp.json();

      const resubResp = await fetch(`/api/v1/cases/${caseId}/resubmit-document`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
        body: JSON.stringify({
          version_id: this.currentCaseDetail.version_id,
          replacement_document_id: uploadedDoc.id,
          target_document_id: targetDocId,
          remarks: 'Citizen uploaded clear high-resolution replacement document.'
        })
      });
      if (!resubResp.ok) throw new Error('Resubmission failed');

      alert('Replacement Document Accepted! Workflow resumed at Verification desk.');
      this.currentCaseDetail = await resubResp.json();
      this.renderCaseModal();
    } catch (err) {
      alert('Resubmission error: ' + err.message);
    }
  },

  async loadNotifications() {
    try {
      const resp = await fetch('/api/v1/notifications', {
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
      if (!resp.ok) return;
      const notifs = await resp.json();
      const badge = document.getElementById('notif-badge');
      const list = document.getElementById('notif-list');

      if (notifs.length > 0 && badge) badge.classList.remove('hidden');

      if (list) {
        if (notifs.length === 0) {
          list.innerHTML = `<p class="text-slate-500 text-center py-4">No notifications yet.</p>`;
        } else {
          list.innerHTML = notifs.map(n => `
            <div class="p-3 hover:bg-slate-50 transition">
              <div class="font-bold text-slate-800">${n.title}</div>
              <p class="text-slate-600 mt-0.5">${n.message}</p>
              <span class="text-[10px] text-slate-400">${new Date(n.created_at).toLocaleTimeString()}</span>
            </div>
          `).join('');
        }
      }
    } catch (err) {
      console.error(err);
    }
  },

  toggleNotifications() {
    const popover = document.getElementById('notif-popover');
    if (popover) popover.classList.toggle('hidden');
  },

  openAIChat() {
    const drawer = document.getElementById('ai-chat-drawer');
    if (drawer) drawer.classList.remove('hidden');
  },

  closeAIChat() {
    const drawer = document.getElementById('ai-chat-drawer');
    if (drawer) drawer.classList.add('hidden');
  },

  async sendAIMessage() {
    const input = document.getElementById('ai-input');
    const msg = input.value.trim();
    if (!msg) return;

    const container = document.getElementById('ai-messages-container');
    container.innerHTML += `
      <div class="bg-amber-50 p-3 rounded-xl text-amber-900 border border-amber-200 text-right">
        ${msg}
      </div>
    `;
    input.value = '';

    try {
      const resp = await fetch('/api/v1/ai/assist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: msg })
      });
      const data = await resp.json();
      container.innerHTML += `
        <div class="bg-slate-100 p-3 rounded-xl text-slate-800 space-y-1">
          <div class="font-bold text-gov-navy text-xs">${data.service_title || 'Assistant Advice'}:</div>
          <p>${data.explanation}</p>
        </div>
      `;
      container.scrollTop = container.scrollHeight;
    } catch (err) {
      container.innerHTML += `<div class="text-rose-600 p-2">Error connecting to assistant.</div>`;
    }
  },

  async resetDemo() {
    if (!confirm('Reset all demo databases to pristine initial seed state?')) return;
    try {
      const resp = await fetch('/api/v1/admin/reset-demo', { method: 'POST' });
      if (resp.ok) {
        alert('Demo database reset successfully!');
        window.location.reload();
      }
    } catch (err) {
      alert('Error resetting demo: ' + err.message);
    }
  }
};

window.addEventListener('DOMContentLoaded', () => {
  app.init();
});
