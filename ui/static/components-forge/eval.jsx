// Forge-styled Eval screen — 120-question benchmark dashboard

const EvalScreen = () => {
  const r = (window.SENTINEL_DATA && window.SENTINEL_DATA.evalResults) || null;
  if (!r || !r.naive || !r.agentic || !r.openai) {
    return (
      <div style={{ padding: "60px 32px", textAlign: "center" }}>
        <span className="f-kicker-light">Loading evaluation results…</span>
      </div>
    );
  }
  const modes = [r.naive, r.agentic, r.openai];

  return (
    <div style={{ padding: "28px 32px", display: "flex", flexDirection: "column", gap: 28 }}>

      {/* ─── HERO SLAB ─── */}
      <Slab padding={36}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.05fr", gap: 40 }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 28 }}>
              <span className="f-kicker">120-question evaluation · 2026-05-21</span>
            </div>
            <h1 style={{ margin: 0, font: "700 60px/1.02 var(--forge-font)", letterSpacing: "-0.025em", color: "var(--forge-on-dark-strong)" }}>
              Naive RAG vs<br/>the agentic stack
            </h1>
            <p style={{
              margin: "22px 0 0", font: "400 16px/24px var(--forge-font)",
              color: "var(--forge-on-dark-mute)", maxWidth: 480,
            }}>
              Same dataset, same prompts, same Pinecone index. The two agentic configurations differ
              only in the underlying chat model. Naive RAG is the baseline: one retrieval, one LLM
              call, no tools.
            </p>
          </div>

          {/* Right: 2×2 stat grid */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
            <StatCard
              kicker="Questions"
              value="120"
              body="Curated test set: 6 categories spanning factual retrieval, synthesis, edition-aware, web-grounded and gap detection."
            />
            <StatCard
              kicker="Agentic recall"
              value="1.00"
              valueColor="var(--forge-lime)"
              body="Non-compliant recall. Both agentic configs caught every real compliance issue (0 / 25 false negatives)."
            />
            <StatCard
              kicker="Nebius cost"
              value="$12.92"
              valueColor="var(--forge-lime)"
              body="Total spend for the full 120-question run on DeepSeek-V4-Pro. 3.4× cheaper than the OpenAI run at identical recall."
            />
            <StatCard
              kicker="Agentic gain"
              value="+1.16"
              valueColor="var(--forge-lime)"
              body="Mean correctness improvement over naive RAG (LLM-as-judge, scale 0–2) across the 4 freeform categories."
            />
          </div>
        </div>
      </Slab>

      {/* ─── HEADLINE STRIP ─── */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 20 }}>
        <HeadlineSlab
          accent="var(--forge-mint-warm)"
          kicker="Audit safety"
          headline="The agentic stack never misses a real issue."
          tagline="Non-compliant recall = 1.00 · 0 false negatives in 35 SOPs"
          chart={<RecallChart modes={modes}/>}
          caption="Naive RAG misses 12% of real compliance issues — 5 of them catastrophically calling 'gap' SOPs compliant. The agentic stack catches every one."
        />
        <HeadlineSlab
          accent="var(--forge-lime)"
          kicker="Cost · quality"
          headline="Nebius matches OpenAI quality at 3.4× lower cost."
          tagline="$12.92  vs  $44.11 · same recall, same accuracy"
          chart={<CostQualityChart modes={modes}/>}
          caption="Across 120 questions, Nebius DeepSeek-V4-Pro reaches the same 1.00 non-compliant recall as GPT-5.5 while spending one third as much. Model choice is a cost-quality knob."
        />
        <HeadlineSlab
          accent="var(--forge-amber)"
          kicker="Where agents matter"
          headline="The agentic stack dominates every freeform category."
          tagline="+0.86 to +1.35 correctness pts (out of 2)"
          chart={<CategoryWinsChart r={r}/>}
          caption="On multi-regulation synthesis, edition-aware questions and web-grounded queries — anything that needs more than one retrieval — the agentic stack pulls ahead by a full LLM-judge grade."
        />
      </div>

      {/* ─── PER-CATEGORY — light bg paper card ─── */}
      <div style={{ paddingTop: 12 }}>
        <SectionTitle
          kicker="LLM-as-judge correctness · 0–2 · shared grader"
          action={<OutlinePill tone="muteLight">Freeform · 96 / 120 Qs</OutlinePill>}>
          Where the gap shows up
        </SectionTitle>
        <PaperCard>
          <CategoryTable r={r}/>
        </PaperCard>
      </div>

      {/* ─── CONFUSION MATRICES ─── */}
      <div>
        <SectionTitle
          kicker="SOP compliance · binary classification"
          action={<OutlinePill tone="muteLight">35 SOPs scored</OutlinePill>}>
          Did the agent catch the gap?
        </SectionTitle>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
          {modes.map(m => <ConfusionSlab key={m.label} mode={m}/>)}
        </div>
      </div>

      {/* ─── COST / LATENCY ─── */}
      <div>
        <SectionTitle kicker="Per 120-question run · includes grader calls">
          Cost · latency · tokens
        </SectionTitle>
        <PaperCard>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <Th>Configuration</Th>
                <Th>Model</Th>
                <Th align="right">Cost</Th>
                <Th align="right">Tokens</Th>
                <Th align="right">Avg / Q</Th>
                <Th align="right">Wall time</Th>
              </tr>
            </thead>
            <tbody>
              {modes.map(m => {
                const isNebius = m.label.includes("Nebius");
                return (
                  <tr key={m.label} style={{ borderTop: "1px solid rgba(7,26,48,0.08)" }}>
                    <Td>
                      <div style={{ font: "600 14px/19px var(--forge-font)", color: "var(--forge-on-light)" }}>{m.label}</div>
                      <div style={{ font: "400 11.5px/14px var(--forge-font)", color: "var(--forge-on-light-mute)" }}>{m.sublabel}</div>
                    </Td>
                    <Td muted style={{ font: "500 12px/16px var(--forge-mono)" }}>{m.model}</Td>
                    <Td align="right">
                      <span style={{ font: "700 16px/1 var(--forge-mono)", color: isNebius ? "rgb(60,140,40)" : "var(--forge-on-light)" }}>${m.totalCost.toFixed(2)}</span>
                    </Td>
                    <Td align="right">
                      <span style={{ font: "600 14px/1 var(--forge-mono)" }}>{((m.inputTokens + m.outputTokens) / 1e6).toFixed(2)}M</span>
                    </Td>
                    <Td align="right">
                      <span style={{ font: "600 14px/1 var(--forge-mono)" }}>{m.latencyAvg.toFixed(1)}s</span>
                    </Td>
                    <Td align="right">
                      <span style={{ font: "600 14px/1 var(--forge-mono)" }}>{(m.latencyTotal / 60).toFixed(1)} min</span>
                    </Td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <div style={{ padding: "18px 24px", borderTop: "1px solid rgba(7,26,48,0.08)", background: "rgba(212,250,80,0.10)", display: "flex", gap: 32 }}>
            <CostRatio label="Agentic Nebius vs naive" value="8.7×"/>
            <CostRatio label="Agentic OpenAI vs naive" value="29.8×"/>
            <CostRatio label="Nebius vs OpenAI" value="−71%" highlight/>
          </div>
        </PaperCard>
      </div>

      {/* ─── READ THE NUMBERS ─── */}
      <div>
        <SectionTitle kicker="How to weigh each metric">Read the numbers</SectionTitle>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 16 }}>
          <Note title="Recall is the audit-safety metric">
            For a compliance auditor, missing a real gap (false negative) is the catastrophic failure mode. False alarms are recoverable: a human reviews and dismisses them. Use <M>recall_non_compliant</M> as the primary metric.
          </Note>
          <Note title="Three-class is harder than binary">
            Both agentic configs hit 1.00 binary recall but only ~0.40 three-class accuracy. Most three-class misses are "partial → gap" — the agent over-flags. That over-flagging is what keeps binary recall perfect.
          </Note>
          <Note title="Naive has its uses">
            For <M>factual_single_hop</M> questions the cost-quality math favors naive RAG. Use the agent only where retrieval-and-synthesis or web-grounding matter — the Sentinel router picks per-question.
          </Note>
        </div>
      </div>
    </div>
  );
};

// ─── Headline slab ───
const HeadlineSlab = ({ accent, kicker, headline, tagline, chart, caption }) => (
  <Slab padding={0} style={{ display: "flex", flexDirection: "column", position: "relative", overflow: "hidden" }}>
    <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 3, background: accent }}/>
    <div style={{ padding: "26px 28px 16px" }}>
      <div style={{ font: "700 11px/1 var(--forge-font)", letterSpacing: "0.14em", textTransform: "uppercase", color: accent, marginBottom: 14 }}>
        {kicker}
      </div>
      <div style={{ font: "700 22px/1.25 var(--forge-font)", letterSpacing: "-0.01em", color: "var(--forge-on-dark-strong)" }}>
        {headline}
      </div>
      <div style={{ font: "500 12px/18px var(--forge-mono)", color: "var(--forge-on-dark-mute)", marginTop: 10 }}>
        {tagline}
      </div>
    </div>
    <div style={{ flex: 1, padding: "8px 28px 18px" }}>{chart}</div>
    <div style={{ padding: "16px 28px 22px", borderTop: "1px solid var(--forge-border-dark)", font: "400 12px/18px var(--forge-font)", color: "var(--forge-on-dark-mute)" }}>
      {caption}
    </div>
  </Slab>
);

// ─── Charts ───
const RecallChart = ({ modes }) => {
  const rows = [
    { mode: modes[0], v: modes[0].binary.recallNonCompliant, color: "rgba(255,255,255,0.20)" },
    { mode: modes[1], v: modes[1].binary.recallNonCompliant, color: "var(--forge-mint-warm)" },
    { mode: modes[2], v: modes[2].binary.recallNonCompliant, color: "var(--forge-mint-warm)" },
  ];
  return (
    <div>
      {rows.map(r => (
        <div key={r.mode.label} style={{ marginBottom: 14 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <span style={{ font: "500 12px/1 var(--forge-font)", color: "var(--forge-on-dark-mute)", whiteSpace: "nowrap" }}>{r.mode.label}</span>
            <span style={{ font: "700 12px/1 var(--forge-mono)", color: r.color === "var(--forge-mint-warm)" ? "var(--forge-mint-warm)" : "var(--forge-on-dark)" }}>{r.v.toFixed(2)}</span>
          </div>
          <div style={{ height: 10, borderRadius: 999, background: "rgba(255,255,255,0.05)", overflow: "hidden" }}>
            <div style={{ height: "100%", width: (r.v * 100) + "%", background: r.color, borderRadius: 999 }}/>
          </div>
        </div>
      ))}
      <div style={{ display: "flex", gap: 18, marginTop: 12 }}>
        <Tiny label="False neg · naive"   value="3 / 22"/>
        <Tiny label="False neg · agentic" value="0 / 25" accent="var(--forge-mint-warm)"/>
      </div>
    </div>
  );
};

const CostQualityChart = ({ modes }) => {
  const max = 50;
  return (
    <div>
      {modes.map(m => {
        const isNebius = m.label.includes("Nebius");
        const isOpenAI = m.label.includes("OpenAI");
        return (
          <div key={m.label} style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
              <span style={{ font: "500 12px/1 var(--forge-font)", color: "var(--forge-on-dark-mute)", whiteSpace: "nowrap" }}>{m.label}</span>
              <span style={{ font: "700 12px/1 var(--forge-mono)", color: isNebius ? "var(--forge-lime)" : "var(--forge-on-dark)" }}>${m.totalCost.toFixed(2)}</span>
            </div>
            <div style={{ height: 10, borderRadius: 999, background: "rgba(255,255,255,0.05)", overflow: "hidden" }}>
              <div style={{
                height: "100%", width: ((m.totalCost / max) * 100) + "%",
                background: isNebius ? "var(--forge-lime)" : isOpenAI ? "rgba(255,255,255,0.40)" : "rgba(255,255,255,0.20)",
                borderRadius: 999,
              }}/>
            </div>
          </div>
        );
      })}
      <div style={{ display: "flex", gap: 18, marginTop: 12 }}>
        <Tiny label="Per-Q · Nebius" value="$0.108" accent="var(--forge-lime)"/>
        <Tiny label="Per-Q · OpenAI" value="$0.368"/>
      </div>
    </div>
  );
};

const CategoryWinsChart = ({ r }) => {
  const cats = [
    { key: "multi_regulation", label: "Multi-reg" },
    { key: "edition_aware",    label: "Edition" },
    { key: "web_grounded",     label: "Web grounded" },
    { key: "negation_gap",     label: "Negation" },
  ];
  return (
    <div>
      {cats.map(c => {
        const n = r.naive.perCategory[c.key].correctness;
        const a = r.agentic.perCategory[c.key].correctness;
        return (
          <div key={c.key} style={{ marginBottom: 10 }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6, alignItems: "baseline" }}>
              <span style={{ font: "500 12px/1 var(--forge-font)", color: "var(--forge-on-dark-mute)", whiteSpace: "nowrap" }}>{c.label}</span>
              <span style={{ font: "700 12px/1 var(--forge-mono)", color: "var(--forge-amber)" }}>+{(a - n).toFixed(2)}</span>
            </div>
            <div style={{ position: "relative", height: 14, background: "rgba(255,255,255,0.05)", borderRadius: 4, overflow: "hidden" }}>
              <div style={{ position: "absolute", inset: 0, width: (n / 2 * 100) + "%", background: "rgba(255,255,255,0.30)" }}/>
              <div style={{ position: "absolute", left: (n / 2 * 100) + "%", top: 0, bottom: 0, width: ((a - n) / 2 * 100) + "%", background: "var(--forge-amber)" }}/>
            </div>
          </div>
        );
      })}
      <div style={{ display: "flex", gap: 14, marginTop: 8, font: "500 11px/14px var(--forge-font)", color: "var(--forge-on-dark-faint)" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 5 }}><div style={{ width: 10, height: 10, background: "rgba(255,255,255,0.30)" }}/> naive</div>
        <div style={{ display: "flex", alignItems: "center", gap: 5 }}><div style={{ width: 10, height: 10, background: "var(--forge-amber)" }}/> agentic gain</div>
      </div>
    </div>
  );
};

// ─── Category table ───
const CategoryTable = ({ r }) => {
  const cats = [
    { key: "factual_single_hop", label: "Factual · single hop", expl: "Direct retrieval of one clause" },
    { key: "multi_regulation",   label: "Multi-regulation",     expl: "Synthesis across 2+ frameworks" },
    { key: "edition_aware",      label: "Edition-aware",        expl: "Distinguishing historical versions" },
    { key: "negation_gap",       label: "Negation · gap",       expl: "Identifying what's missing" },
    { key: "web_grounded",       label: "Web-grounded",         expl: "Needs live web grounding" },
  ];
  return (
    <table style={{ width: "100%", borderCollapse: "collapse" }}>
      <thead>
        <tr>
          <Th>Category</Th>
          <Th align="center">n</Th>
          <Th align="center">Naive RAG</Th>
          <Th align="center">Agentic · Nebius</Th>
          <Th align="center">Agentic · OpenAI</Th>
          <Th align="right">Agentic gain</Th>
        </tr>
      </thead>
      <tbody>
        {cats.map(c => {
          const n = r.naive.perCategory[c.key].correctness;
          const a = r.agentic.perCategory[c.key].correctness;
          const o = r.openai.perCategory[c.key].correctness;
          const gain = a - n;
          return (
            <tr key={c.key} style={{ borderTop: "1px solid rgba(7,26,48,0.08)" }}>
              <Td>
                <div style={{ font: "600 14px/19px var(--forge-font)" }}>{c.label}</div>
                <div style={{ font: "400 11.5px/15px var(--forge-font)", color: "var(--forge-on-light-mute)" }}>{c.expl}</div>
              </Td>
              <Td align="center" muted><span style={{ font: "500 12px/1 var(--forge-mono)" }}>{r.naive.perCategory[c.key].n}</span></Td>
              <ScoreCell value={n}/>
              <ScoreCell value={a} highlight={a >= o && a > n}/>
              <ScoreCell value={o} highlight={o > a}/>
              <Td align="right">
                <GainPill value={gain}/>
              </Td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
};

const ScoreCell = ({ value, highlight }) => {
  const tone = value >= 1.7 ? "rgb(60,140,40)" : value >= 1.0 ? "rgb(170,115,0)" : "rgb(180,0,40)";
  return (
    <td style={{ padding: "14px 18px", textAlign: "center" }}>
      <span style={{
        display: "inline-flex", alignItems: "center", gap: 6,
        padding: "5px 11px", borderRadius: 999,
        background: highlight ? "rgba(212,250,80,0.25)" : "transparent",
        border: highlight ? "1px solid rgba(120,160,0,0.45)" : "1px solid transparent",
      }}>
        <span style={{ width: 6, height: 6, borderRadius: 999, background: tone }}/>
        <span style={{ font: "700 13px/1 var(--forge-mono)" }}>{value.toFixed(2)}</span>
      </span>
    </td>
  );
};

const GainPill = ({ value }) => {
  const ok = value > 0.5;
  return (
    <span style={{
      display: "inline-flex", padding: "4px 11px", borderRadius: 999,
      background: ok ? "rgba(120,220,140,0.18)" : "rgba(7,26,48,0.06)",
      color: ok ? "rgb(40,120,60)" : "var(--forge-on-light-mute)",
      border: ok ? "1px solid rgba(40,120,60,0.30)" : "1px solid rgba(7,26,48,0.10)",
      font: "700 12px/1 var(--forge-mono)",
    }}>
      {value > 0 ? "+" : ""}{value.toFixed(2)}
    </span>
  );
};

// ─── Confusion matrix as Slab ───
const ConfusionSlab = ({ mode }) => {
  const b = mode.binary;
  const isAgentic = !mode.label.includes("Naive");
  return (
    <Slab padding={24}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 18 }}>
        <div>
          <div className="f-kicker">{mode.label}</div>
          <div style={{ font: "500 12px/16px var(--forge-font)", color: "var(--forge-on-dark-mute)", marginTop: 6 }}>{mode.sublabel}</div>
        </div>
        <span style={{
          display: "inline-flex", alignItems: "center", gap: 6,
          padding: "4px 11px", borderRadius: 999,
          color: isAgentic ? "var(--forge-mint-warm)" : "var(--forge-on-dark)",
          border: isAgentic ? "1px solid var(--forge-mint-warm)" : "1px solid rgba(255,255,255,0.20)",
          font: "700 11px/1 var(--forge-mono)",
        }}>recall {b.recallNonCompliant.toFixed(2)}</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "auto 1fr 1fr", gap: 5 }}>
        <div/>
        <CornerLabel>pred non-comp.</CornerLabel>
        <CornerLabel>pred compliant</CornerLabel>

        <RowLabel>actual non-comp.</RowLabel>
        <ConfCell value={b.tp} tone="success" label="TP"/>
        <ConfCell value={b.fn} tone={b.fn === 0 ? "successDim" : "danger"} label="FN"/>

        <RowLabel>actual compliant</RowLabel>
        <ConfCell value={b.fp} tone="warn" label="FP"/>
        <ConfCell value={b.tn} tone="successDim" label="TN"/>
      </div>

      <div style={{ display: "flex", gap: 18, marginTop: 16, font: "500 11px/14px var(--forge-font)", color: "var(--forge-on-dark-mute)" }}>
        <span>F1 <span style={{ font: "700 11px/1 var(--forge-mono)", color: "var(--forge-on-dark-strong)" }}>{b.f1NonCompliant.toFixed(2)}</span></span>
        <span>Prec <span style={{ font: "700 11px/1 var(--forge-mono)", color: "var(--forge-on-dark-strong)" }}>{b.precisionNonCompliant.toFixed(2)}</span></span>
        <span>Acc <span style={{ font: "700 11px/1 var(--forge-mono)", color: "var(--forge-on-dark-strong)" }}>{b.accuracy.toFixed(2)}</span></span>
      </div>
    </Slab>
  );
};

const ConfCell = ({ value, tone, label }) => {
  const styles = {
    success:    { bg: "rgba(120,220,140,0.18)", fg: "var(--forge-mint-warm)", border: "rgba(120,220,140,0.35)" },
    successDim: { bg: "rgba(120,220,140,0.06)", fg: "rgba(120,220,140,0.80)", border: "rgba(120,220,140,0.20)" },
    warn:       { bg: "rgba(255,190,92,0.14)",  fg: "var(--forge-amber)",     border: "rgba(255,190,92,0.35)" },
    danger:     { bg: "rgba(247,100,110,0.16)", fg: "var(--forge-red)",       border: "rgba(247,100,110,0.40)" },
  }[tone];
  return (
    <div style={{
      padding: "12px 8px", borderRadius: 8,
      background: styles.bg, color: styles.fg,
      border: `1px solid ${styles.border}`,
      display: "flex", flexDirection: "column", alignItems: "center", gap: 2,
    }}>
      <span style={{ font: "800 22px/1 var(--forge-font)" }}>{value}</span>
      <span style={{ font: "600 9px/1 var(--forge-font)", letterSpacing: "0.12em", opacity: 0.85 }}>{label}</span>
    </div>
  );
};

const CornerLabel = ({ children }) => (
  <div style={{
    font: "600 10px/14px var(--forge-font)", letterSpacing: "0.10em",
    color: "var(--forge-on-dark-faint)", textAlign: "center",
    textTransform: "uppercase", padding: "6px 0",
  }}>{children}</div>
);
const RowLabel = ({ children }) => (
  <div style={{
    font: "600 10px/1 var(--forge-font)", letterSpacing: "0.10em",
    color: "var(--forge-on-dark-faint)", textTransform: "uppercase",
    display: "flex", alignItems: "center", paddingRight: 8,
  }}>{children}</div>
);

const Th = ({ children, align }) => (
  <th style={{
    font: "600 11px/1 var(--forge-font)", letterSpacing: "0.12em", textTransform: "uppercase",
    color: "var(--forge-on-light-mute)", padding: "14px 18px",
    textAlign: align || "left", whiteSpace: "nowrap",
  }}>{children}</th>
);
const Td = ({ children, muted, align, style }) => (
  <td style={{
    padding: "14px 18px",
    font: "400 13px/19px var(--forge-font)",
    color: muted ? "var(--forge-on-light-mute)" : "var(--forge-on-light)",
    textAlign: align || "left",
    verticalAlign: "top", ...style,
  }}>{children}</td>
);

const Tiny = ({ label, value, accent }) => (
  <div style={{ display: "flex", flexDirection: "column", flex: 1 }}>
    <span style={{ font: "600 9px/1 var(--forge-font)", letterSpacing: "0.10em", textTransform: "uppercase", color: "var(--forge-on-dark-faint)" }}>{label}</span>
    <span style={{ font: "700 14px/1.5 var(--forge-mono)", color: accent || "var(--forge-on-dark-strong)" }}>{value}</span>
  </div>
);

const CostRatio = ({ label, value, highlight }) => (
  <div>
    <div style={{ font: "600 10px/1 var(--forge-font)", letterSpacing: "0.10em", textTransform: "uppercase", color: "var(--forge-on-light-mute)", whiteSpace: "nowrap" }}>{label}</div>
    <div style={{ font: "800 26px/1.2 var(--forge-font)", color: highlight ? "rgb(40,120,60)" : "var(--forge-on-light)", letterSpacing: "-0.01em", marginTop: 4 }}>{value}</div>
  </div>
);

const Note = ({ title, children }) => (
  <PaperCard padding={22}>
    <div style={{ font: "700 15px/20px var(--forge-font)", color: "var(--forge-on-light)", marginBottom: 8 }}>{title}</div>
    <div style={{ font: "400 13px/20px var(--forge-font)", color: "var(--forge-on-light-mute)" }}>{children}</div>
  </PaperCard>
);

Object.assign(window, { EvalScreen });
