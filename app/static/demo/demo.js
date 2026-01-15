/**
 * AIDE Frame Demo page JavaScript
 */

// DEMOS config - uses i18n keys
const DEMO_CONFIG = {
    http_call: { titleKey: 'demo_http', descKey: 'demo_http_desc' },
    config: { titleKey: 'demo_config', descKey: 'demo_config_desc' },
    logging: { titleKey: 'demo_logging', descKey: 'demo_logging_desc' },
    qrcode: { titleKey: 'demo_qrcode', descKey: 'demo_qrcode_desc' },
    i18n: { titleKey: 'demo_i18n', descKey: 'demo_i18n_desc' },
    markdown: { titleKey: 'demo_markdown', descKey: 'demo_markdown_desc', link: '/sample_docs?doc=markdown-demo.md' }
};

let activeDemo = null;

function initDemoGrid() {
    const grid = document.getElementById('demo-grid');
    for (const [key, cfg] of Object.entries(DEMO_CONFIG)) {
        const title = i18n.t(cfg.titleKey);
        const desc = i18n.t(cfg.descKey);

        if (cfg.link) {
            // Link-based demo - navigate to page
            const a = document.createElement('a');
            a.className = 'demo-btn notranslate';
            a.href = cfg.link;
            a.innerHTML = `<h3>${title}</h3><p>${desc}</p>`;
            grid.appendChild(a);
        } else {
            // Panel-based demo
            const btn = document.createElement('button');
            btn.className = 'demo-btn notranslate';
            btn.id = `btn-${key}`;
            btn.innerHTML = `<h3>${title}</h3><p>${desc}</p>`;
            btn.onclick = () => selectDemo(key);
            grid.appendChild(btn);
        }
    }
}

function selectDemo(key) {
    // Update buttons
    document.querySelectorAll('.demo-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`btn-${key}`).classList.add('active');

    // Hide placeholder, show selected panel
    const placeholder = document.getElementById('demo-placeholder');
    if (placeholder) placeholder.classList.add('hidden');

    document.querySelectorAll('.demo-panel').forEach(p => p.classList.remove('active'));
    document.getElementById(`panel-${key}`).classList.add('active');

    activeDemo = key;
}

async function callDemo(demoName, data) {
    const res = await fetch(`/api/demo/${demoName}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });
    return res.json();
}

function showResult(elementId, data) {
    const el = document.getElementById(elementId);
    el.textContent = JSON.stringify(data, null, 2);
    el.classList.add('show');
}

async function runHttpDemo() {
    const name = document.getElementById('http-name').value.trim();
    if (!name) { alert(i18n.t('please_enter_name')); return; }
    const result = await callDemo('http_call', { name });
    showResult('http-result', result);
}

async function runConfigDemo(action) {
    const result = await callDemo('config', { action });
    showResult('config-result', result);
}

async function runLoggingDemo(action) {
    const level = document.getElementById('log-level').value;
    const data = { action, level };
    if (action === 'log') {
        data.message = `Test ${level} message from demo UI`;
    }
    const result = await callDemo('logging', data);
    showResult('logging-result', result);
}

async function runQrDemo() {
    const text = document.getElementById('qr-text').value.trim();
    if (!text) { alert(i18n.t('please_enter_text')); return; }
    const result = await callDemo('qrcode', { text });
    if (result.image) {
        document.getElementById('qr-image').src = result.image;
        document.getElementById('qr-result').style.display = 'block';
    } else if (result.error) {
        alert(result.error);
    }
}

function switchLanguage(lang) {
    i18n.setLanguage(lang);
}

function updateI18nPanel() {
    const currentEl = document.getElementById('i18n-current');
    if (currentEl) {
        currentEl.textContent = i18n.t('i18n_current', { lang: i18n.lang.toUpperCase() });
        currentEl.classList.add('notranslate');
    }
    // Highlight active flag button
    const langMap = { en: 'english', de: 'deutsch', es: 'español' };
    document.querySelectorAll('.flag-btn').forEach(btn => {
        btn.classList.toggle('active', btn.title.toLowerCase() === langMap[i18n.lang]);
    });
}

// Initialize
(async () => {
    await i18n.init();
    document.title = i18n.t('app_title');
    const subtitle = document.getElementById('app-subtitle');
    subtitle.textContent = i18n.t('app_subtitle');
    subtitle.classList.add('notranslate');
    i18n.applyToDOM();
    initDemoGrid();
    updateI18nPanel();
    HeaderWidget.init('#app-header', { appName: i18n.t('app_title'), showGoogleTranslate: true });
    StatusWidget.init('#status-widget', { showRestart: false });
})();
