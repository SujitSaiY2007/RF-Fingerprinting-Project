const D = {
  a: { accuracy: 87.3899, known: 94.90, unknown: 29.49 },
  b: { accuracy: 87.3899, known: 94.90, unknown: 29.49, adapt: 37.9704, replay: 1.0, replayHold: 99.0, gain: 94.6809, disp: 0.969641 },
  frozen: 28.6629,
  always: { adapt: 38.1705, replay: 100, gain: 100, disp: 0.995174 },
  updates: 4799,
  holds: 151,
  total: 4950,
  targetLike: 100
};

const pct = (v, d = 2) => `${v.toFixed(d)}%`;
const pp = (v, d = 2) => `${v >= 0 ? '+' : ''}${v.toFixed(d)} pp`;
const app = document.querySelector('#app');

const navIcon = (label) => `<span class="mini-icon">${label}</span>`;
const bar = (value, cls = '') => `<div class="bar-track"><span class="bar-fill ${cls}" style="width:${Math.max(0, Math.min(100, value))}%"></span></div>`;

const views = {
  overview: `
    <section class="page-head command-head">
      <div>
        <span class="eyebrow">TRACK-A · COMMAND CENTER</span>
        <h1>RF identity, adaptation<br><em>and update security.</em></h1>
        <p class="lede">A controlled research demonstrator built around the frozen RF recognizer and Version-B adaptive profile-security layer.</p>
      </div>
      <div class="stage-card">
        <span class="stage-label">CURRENT STAGE</span>
        <strong>Track A</strong>
        <div class="stage-status"><span class="status-dot"></span> Demonstrator complete</div>
        <small>Track B remains the broader validation direction.</small>
      </div>
    </section>

    <section class="kpi-grid">
      <article class="kpi kpi-main"><div class="kpi-top"><span>RF recognition</span><span class="kpi-code">V-A / V-B</span></div><strong>${pct(D.a.accuracy,2)}</strong><small>closed-set accuracy · frozen control</small></article>
      <article class="kpi"><div class="kpi-top"><span>Profile adaptation</span><span class="kpi-code">D8</span></div><strong>${pct(D.b.adapt,2)}</strong><small>post-update profile test accuracy</small><div class="kpi-delta positive">${pp(D.b.adapt - D.frozen)} vs frozen profile</div></article>
      <article class="kpi"><div class="kpi-top"><span>Replay hold</span><span class="kpi-code">D9</span></div><strong>${pct(D.b.replayHold,0)}</strong><small>controlled replay scenario</small><div class="kpi-delta positive">${pp(D.b.replayHold)} absolute gain</div></article>
      <article class="kpi kpi-alert"><div class="kpi-top"><span>Target-like contamination</span><span class="kpi-code">LIMIT</span></div><strong>${pct(D.targetLike,0)}</strong><small>accepted in tested scenario</small><div class="kpi-delta negative">unresolved security boundary</div></article>
    </section>

    <section class="dashboard-grid">
      <div class="panel span-8">
        <div class="panel-head"><div><span class="eyebrow">SYSTEM PATH</span><h2>From RF observation to persistent identity</h2></div><span class="source-chip">IMPLEMENTED</span></div>
        <div class="flow">
          <div class="flow-step"><span>01</span><strong>Observe</strong><small>Canonical I/Q</small></div><div class="flow-arrow">→</div>
          <div class="flow-step"><span>02</span><strong>Recognize</strong><small>16 RF features</small></div><div class="flow-arrow">→</div>
          <div class="flow-step"><span>03</span><strong>Evaluate</strong><small>Open-set evidence</small></div><div class="flow-arrow">→</div>
          <div class="flow-step emphasis"><span>04</span><strong>Authorize</strong><small>Update safety</small></div><div class="flow-arrow">→</div>
          <div class="flow-step"><span>05</span><strong>Evolve</strong><small>Persistent profile</small></div><div class="flow-arrow">→</div>
          <div class="flow-step"><span>06</span><strong>Audit</strong><small>Decision trace</small></div>
        </div>
      </div>

      <div class="panel span-4 evidence-panel">
        <div class="panel-head"><div><span class="eyebrow">EVIDENCE STATUS</span><h2>What is established</h2></div></div>
        <ul class="status-list">
          <li><span class="check">✓</span><div><strong>Recognition control</strong><small>Frozen and retained in V-B</small></div></li>
          <li><span class="check">✓</span><div><strong>Adaptive profile</strong><small>D8 demonstrated</small></div></li>
          <li><span class="check">✓</span><div><strong>Replay quarantine</strong><small>D9 demonstrated</small></div></li>
          <li><span class="check">✓</span><div><strong>Integrated lifecycle</strong><small>D10 demonstrated</small></div></li>
          <li class="warning-row"><span class="warn">!</span><div><strong>Target-like unknown</strong><small>100% contamination remains</small></div></li>
        </ul>
      </div>

      <div class="panel span-7">
        <div class="panel-head"><div><span class="eyebrow">RECOGNITION CONTROL</span><h2>Known / unknown behaviour</h2></div><span class="source-chip">SMoRFFI</span></div>
        <div class="metric-rows">
          <div class="metric-row"><div><strong>Closed-set accuracy</strong><small>Version A = Version B</small></div><b>${pct(D.a.accuracy,4)}</b></div>
          ${bar(D.a.accuracy)}
          <div class="metric-row"><div><strong>Known acceptance</strong><small>Frozen open-set control</small></div><b>${pct(D.a.known)}</b></div>
          ${bar(D.a.known)}
          <div class="metric-row"><div><strong>Unknown rejection</strong><small>Frozen open-set control</small></div><b>${pct(D.a.unknown)}</b></div>
          ${bar(D.a.unknown)}
        </div>
      </div>

      <div class="panel span-5">
        <div class="panel-head"><div><span class="eyebrow">UPDATE STREAM</span><h2>Profile decisions</h2></div><span class="source-chip">D8</span></div>
        <div class="donut-wrap">
          <div class="donut"><div><strong>${pct(D.updates / D.total * 100,1)}</strong><span>accepted</span></div></div>
          <div class="donut-legend"><div><i class="legend-dot accepted"></i><span>Accepted updates</span><b>${D.updates}</b></div><div><i class="legend-dot held"></i><span>Held updates</span><b>${D.holds}</b></div><div class="legend-total">${D.total} observations in update stream</div></div>
        </div>
      </div>

      <div class="panel span-12 boundary-panel">
        <div class="boundary-icon">!</div>
        <div><span class="eyebrow">SCIENTIFIC BOUNDARY</span><h2>Target-like unknown contamination remains unresolved</h2><p>The tested controlled scenario produced 100% contamination for both versions. The dashboard keeps this falsifying case visible; Version B is not presented as universally secure or universally superior.</p></div>
        <button class="text-link" data-view="d9">Inspect D9 ${navIcon('→')}</button>
      </div>
    </section>`,

  comparison: `
    <section class="page-head compact"><div><span class="eyebrow">FROZEN EVIDENCE · CONTROL COMPARISON</span><h1>Version A <em>vs</em> Version B</h1><p class="lede">The RF recognition backbone is held constant. The measured difference is concentrated in adaptation and security-oriented profile management.</p></div></section>
    <section class="panel comparison-panel">
      <div class="panel-head"><div><span class="eyebrow">MEASURED RESULTS</span><h2>Track-A evidence matrix</h2></div><span class="source-chip">FROZEN</span></div>
      <div class="table-scroll"><table class="evidence-table"><thead><tr><th>Metric</th><th>Version A</th><th>Version B</th><th>Observed change</th><th>Interpretation</th></tr></thead><tbody>
        <tr><td>Closed-set RF accuracy</td><td>${pct(D.a.accuracy,4)}</td><td>${pct(D.b.accuracy,4)}</td><td>—</td><td>Same frozen recognizer</td></tr>
        <tr><td>Known acceptance</td><td>${pct(D.a.known)}</td><td>${pct(D.b.known)}</td><td>—</td><td>Same open-set control</td></tr>
        <tr><td>Unknown rejection</td><td>${pct(D.a.unknown)}</td><td>${pct(D.b.unknown)}</td><td>—</td><td>Same open-set control</td></tr>
        <tr class="row-positive"><td>Profile test accuracy after adaptation</td><td>${pct(D.frozen,4)}</td><td>${pct(D.b.adapt,4)}</td><td>${pp(D.b.adapt - D.frozen,2)}</td><td>Adaptation improvement</td></tr>
        <tr class="row-positive"><td>Replay acceptance</td><td>${pct(D.always.replay,0)}</td><td>${pct(D.b.replay,0)}</td><td>−99.00 pp</td><td>Strong controlled replay result</td></tr>
        <tr class="row-positive"><td>Replay hold</td><td>0%</td><td>${pct(D.b.replayHold,0)}</td><td>+99.00 pp</td><td>Repeated evidence quarantined</td></tr>
        <tr><td>Gain-drift acceptance</td><td>${pct(D.always.gain,0)}</td><td>${pct(D.b.gain,4)}</td><td>−5.32 pp</td><td>More conservative authorization</td></tr>
        <tr><td>Mean profile displacement (L2)</td><td>${D.always.disp.toFixed(6)}</td><td>${D.b.disp.toFixed(6)}</td><td>−2.56%</td><td>Lower measured profile movement</td></tr>
        <tr class="row-danger"><td>Target-like unknown contamination</td><td>${pct(D.targetLike,0)}</td><td>${pct(D.targetLike,0)}</td><td>0 pp</td><td>Unresolved falsifying case</td></tr>
      </tbody></table></div>
    </section>
    <section class="two-col">
      <div class="panel interpretation"><span class="eyebrow">READ THIS AS</span><h2>What Version B actually changes</h2><div class="statement"><b>Recognition</b><span>remains the same frozen RF control.</span></div><div class="statement accent"><b>Authorization</b><span>becomes an independent decision before persistent profile modification.</span></div><div class="statement"><b>Security evidence</b><span>is measured at the profile-update pathway rather than claimed from classifier accuracy.</span></div></div>
      <div class="panel interpretation"><span class="eyebrow">DO NOT OVERCLAIM</span><h2>Evidence boundary</h2><ul class="plain-list"><li>Not universal Version-B superiority.</li><li>Not complete poisoning resistance.</li><li>Not cross-dataset or cross-frequency validation.</li><li>Not a formal novelty proof.</li></ul></div>
    </section>`,

  d8: `
    <section class="page-head compact"><div><span class="eyebrow">D8 · PROFILE EVOLUTION</span><h1>Adaptation with <em>authorization.</em></h1><p class="lede">D8 demonstrates that persistent RF identity profiles can evolve through a controlled update stream while separating recognition from permission to modify stored identity state.</p></div></section>
    <section class="hero-metric"><div><span>FROZEN PROFILE</span><strong>${pct(D.frozen,4)}</strong><small>profile test accuracy</small></div><div class="hero-arrow">→</div><div class="hero-metric-highlight"><span>V-B MULTI-EVIDENCE</span><strong>${pct(D.b.adapt,4)}</strong><small>profile test accuracy</small></div><div class="hero-delta">${pp(D.b.adapt - D.frozen)}<small>absolute improvement</small></div></section>
    <section class="two-col">
      <div class="panel"><div class="panel-head"><div><span class="eyebrow">UPDATE STREAM</span><h2>Decision distribution</h2></div><span class="source-chip">4,950 observations</span></div><div class="decision-stat"><div><strong>${D.updates}</strong><span>Accepted</span></div><div><strong>${D.holds}</strong><span>Held</span></div></div><div class="stacked-bar"><span style="width:96.95%"></span><i style="width:3.05%"></i></div><div class="legend-inline"><span><i class="legend-dot accepted"></i>96.95% accepted</span><span><i class="legend-dot held"></i>3.05% held</span></div></div>
      <div class="panel"><div class="panel-head"><div><span class="eyebrow">PROTOCOL</span><h2>Chronological evaluation</h2></div></div><div class="protocol-grid"><div><b>50</b><span>enrollment observations / device</span></div><div><b>150</b><span>update observations / device</span></div><div><b>33</b><span>known devices</span></div><div><b>frozen</b><span>test set protected from updates</span></div></div></div>
    </section>
    <section class="panel wide-panel"><div class="panel-head"><div><span class="eyebrow">CONCEPTUAL SEPARATION</span><h2>Recognition ≠ authorization</h2></div><span class="source-chip">CORE IDEA</span></div><div class="separation"><div><span>Operational decision</span><strong>Device A</strong><small>RF recognition result</small></div><div class="separation-line">≠</div><div class="authorize-box"><span>Persistent-state decision</span><strong>ACCEPT / HOLD / REJECT</strong><small>independent update authorization</small></div></div></section>`,

  d9: `
    <section class="page-head compact"><div><span class="eyebrow">D9 · SECURITY EVALUATION</span><h1>Security at the <em>update pathway.</em></h1><p class="lede">Controlled and derived scenarios test whether suspicious evidence can be prevented from silently modifying persistent RF identity profiles.</p></div><span class="scenario-badge">CONTROLLED / DERIVED SCENARIOS</span></section>
    <section class="security-grid-new">
      <article class="attack-card strong"><div class="attack-top"><span class="scenario-label">REPLAY</span><span class="result-chip good">DEMONSTRATED</span></div><h2>Repeated evidence is held</h2><div class="attack-numbers"><div><small>V-A</small><strong>${pct(D.always.replay,0)}</strong><span>accepted</span></div><div class="attack-arrow">→</div><div class="highlight"><small>V-B</small><strong>${pct(D.b.replay,0)}</strong><span>accepted</span></div></div>${bar(D.b.replay,'good')}<p>Acceptance fell by 99 percentage points; replay hold reached 99% in the tested scenario.</p></article>
      <article class="attack-card"><div class="attack-top"><span class="scenario-label">GAIN DRIFT</span><span class="result-chip neutral">TESTED</span></div><h2>Authorization becomes more conservative</h2><div class="attack-numbers"><div><small>V-A</small><strong>${pct(D.always.gain,0)}</strong><span>accepted</span></div><div class="attack-arrow">→</div><div class="highlight"><small>V-B</small><strong>${pct(D.b.gain,4)}</strong><span>accepted</span></div></div>${bar(D.b.gain,'neutral')}<p>Acceptance decreases by 5.32 pp under the controlled amplitude-variation scenario.</p></article>
      <article class="attack-card danger-card"><div class="attack-top"><span class="scenario-label">TARGET-LIKE UNKNOWN</span><span class="result-chip danger">UNRESOLVED</span></div><h2>Current mechanism does not contain the case</h2><div class="attack-numbers"><div><small>V-A</small><strong>${pct(D.targetLike,0)}</strong><span>contamination</span></div><div class="attack-arrow">→</div><div class="highlight"><small>V-B</small><strong>${pct(D.targetLike,0)}</strong><span>contamination</span></div></div>${bar(D.targetLike,'danger')}<p>This is the principal unresolved security limitation and is retained as a falsifying case.</p></article>
    </section>
    <section class="panel wide-panel security-note"><span class="eyebrow">SCIENTIFIC INTERPRETATION</span><h2>Strong replay evidence ≠ complete poisoning resistance</h2><p>Version B is not presented as universally secure. The current evidence supports a narrower statement: the update-authorization layer substantially improves the tested replay scenario while failing to prevent the tested target-like unknown contamination.</p></section>`,

  d10: `
    <section class="page-head compact"><div><span class="eyebrow">D10 · END-TO-END LIFECYCLE</span><h1>From observation to <em>audited identity state.</em></h1><p class="lede">D10 demonstrates the integrated Track-A lifecycle rather than treating recognition, adaptation, security and audit as isolated components.</p></div><span class="result-chip good large-chip">DEMONSTRATED</span></section>
    <section class="lifecycle-grid">
      <article><span>01</span><h2>Recognize</h2><p>RF evidence produces a candidate device identity through the frozen recognition control.</p></article>
      <article><span>02</span><h2>Evaluate</h2><p>Confidence, novelty and profile consistency contribute to update-safety assessment.</p></article>
      <article class="accent-card"><span>03</span><h2>Authorize</h2><p>ACCEPT, HOLD or REJECT controls whether persistent identity state may change.</p></article>
      <article><span>04</span><h2>Evolve</h2><p>Authorized legitimate evidence produces a new profile state.</p></article>
      <article><span>05</span><h2>Audit</h2><p>Decision, reason and profile version remain traceable in the demonstrated lifecycle.</p></article>
    </section>
    <section class="panel wide-panel lifecycle-summary"><div class="summary-icon">✓</div><div><span class="eyebrow">D10 EVIDENCE</span><h2>Lifecycle demonstrated end-to-end</h2><p>Legitimate recognition → profile evolution → suspicious repetition → replay quarantine → audit record.</p></div></section>`,

  provenance: `
    <section class="page-head compact"><div><span class="eyebrow">METHODOLOGY · PROVENANCE · BOUNDARIES</span><h1>Know what every number <em>means.</em></h1><p class="lede">The dashboard distinguishes source evidence, derived controlled scenarios, implementation status and scientific limitations.</p></div></section>
    <section class="method-grid-new">
      <article class="method-card source"><span class="method-tag source-tag">SOURCE DATA</span><h2>SMoRFFI</h2><p>The Track-A RF control and chronological engineering evaluation use the supplied SMoRFFI archive.</p><small>Raw dataset files remain outside the repository.</small></article>
      <article class="method-card derived"><span class="method-tag">DERIVED / CONTROLLED</span><h2>Security scenarios</h2><p>Replay, gain drift and target-like contamination scenarios are constructed from source observations using documented mechanisms.</p><small>They are not native SMoRFFI measurements.</small></article>
      <article class="method-card limitation"><span class="method-tag">LIMITATION</span><h2>Temporal meaning</h2><p>SMoRFFI source-row order is engineering chronology, not trustworthy temporal/session metadata.</p><small>No real-world temporal generalization claim is made.</small></article>
      <article class="method-card control"><span class="method-tag">CONTROL</span><h2>Immutable recognizer</h2><p>Version A remains the recognition control. Version B retains the same measured RF backbone.</p><small>No uncertified candidate-model accuracy is substituted.</small></article>
    </section>
    <section class="panel wide-panel"><div class="panel-head"><div><span class="eyebrow">CURRENT CLAIM BOUNDARY</span><h2>Implemented · Tested · Demonstrated</h2></div></div><div class="claim-grid"><div><b>IMPLEMENTED</b><span>RF pipeline, Version B authorization/profile layer, D8–D10 lifecycle, dashboard.</span></div><div><b>TESTED</b><span>Frozen recognition, adaptation and controlled security scenarios.</span></div><div><b>DEMONSTRATED</b><span>Profile evolution, replay improvement and integrated lifecycle.</span></div><div class="claim-muted"><b>NOT YET VALIDATED</b><span>Universal security, cross-dataset/generalization, cross-frequency behaviour and formal novelty.</span></div></div></section>`
};

function render(key = 'overview') {
  app.innerHTML = views[key] || views.overview;
  document.querySelectorAll('.nav button').forEach(btn => btn.classList.toggle('active', btn.dataset.view === key));
  document.querySelectorAll('[data-view]').forEach(el => {
    if (el.tagName === 'BUTTON') return;
    el.onclick = () => render(el.dataset.view);
  });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.querySelectorAll('.nav button').forEach(btn => btn.addEventListener('click', () => render(btn.dataset.view)));
render();
