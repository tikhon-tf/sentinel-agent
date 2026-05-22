// Forge app — single-page nav between Audit / Compare / Eval.
// Hydrates window.SENTINEL_DATA from the backend on mount.

const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "focus": "balanced"
}/*EDITMODE-END*/;

function useForgeData() {
  // version increments after each successful load → triggers re-render of screens
  // that read directly from window.SENTINEL_DATA.
  const [version, setVersion] = React.useState(0);
  const [status, setStatus] = React.useState({ kb: "loading", eval: "loading", dataset: "loading", findings: "loading" });

  React.useEffect(() => {
    let cancelled = false;
    const API = window.ForgeAPI;
    if (!API) return;

    // Fire all four endpoints in parallel. Each one updates its own slice of
    // window.SENTINEL_DATA + status the moment it returns, so a slow query
    // (e.g. cold Pinecone /api/kb-stats taking ~10s) no longer blocks the
    // others. The screen re-renders after each individual completion.
    const tasks = [
      ["kb",       API.getKbStats,     (d) => { window.SENTINEL_DATA.kbStats = d; }],
      ["eval",     API.getEvalResults, (d) => { window.SENTINEL_DATA.evalResults = mapEvalResults(d); }],
      ["dataset",  API.getDataset,     (d) => { window.SENTINEL_DATA.dataset = d.questions || []; }],
      ["findings", API.getFindings,    (d) => { window.SENTINEL_DATA.findings = d; }],
    ];
    tasks.forEach(([key, fetcher, assign]) => {
      fetcher()
        .then((data) => {
          if (cancelled) return;
          assign(data);
          setStatus(s => ({ ...s, [key]: "ok" }));
          setVersion(v => v + 1);
        })
        .catch((err) => {
          console.warn(`[forge] failed to load /api/${key}:`, err);
          if (!cancelled) setStatus(s => ({ ...s, [key]: "error" }));
        });
    });

    return () => { cancelled = true; };
  }, []);

  return { version, status };
}

// Backend returns API JSON with snake_case + flat structure (matches eval JSON).
// Convert to the shape eval.jsx expects.
function mapEvalResults(api) {
  const mapMode = (m) => m && {
    label: m.label || (m.mode || "").replace(/-/g, " "),
    sublabel: m.sublabel || "",
    tagline: m.tagline || "",
    model: m.model,
    total: m.total,
    totalCost: m.total_cost_usd,
    latencyAvg: m.latency_avg_s,
    latencyTotal: m.latency_total_s,
    inputTokens: m.input_tokens,
    outputTokens: m.output_tokens,
    binary: {
      accuracy: m.compliance_binary?.accuracy ?? 0,
      recallNonCompliant: m.compliance_binary?.recall_non_compliant ?? 0,
      precisionNonCompliant: m.compliance_binary?.precision_non_compliant ?? 0,
      f1NonCompliant: m.compliance_binary?.f1_non_compliant ?? 0,
      macroF1: m.compliance_binary?.macro_f1 ?? 0,
      tp: m.compliance_binary?.tp_non_compliant ?? 0,
      fp: m.compliance_binary?.fp_non_compliant ?? 0,
      tn: m.compliance_binary?.tn_compliant ?? 0,
      fn: m.compliance_binary?.fn_non_compliant ?? 0,
    },
    perCategory: Object.fromEntries(Object.entries(m.per_category || {}).map(([k, v]) => [k, {
      n: v.n,
      correctness: v.judge_correctness_avg,
      citations:   v.judge_citations_avg,
      binaryAcc:   v.binary_accuracy,
    }])),
  };
  const naive  = mapMode(api.naive)         || {};
  const nebius = mapMode(api.agentic)       || {};
  const openai = mapMode(api["agentic-openai"]) || {};
  // Restore labels (the API uses mode keys, not the friendly labels).
  if (!naive.label  || naive.label  === "naive")          naive.label  = "Naive RAG";
  if (!nebius.label || nebius.label === "agentic")        nebius.label = "Agentic (Nebius)";
  if (!openai.label || openai.label === "agentic openai") openai.label = "Agentic (OpenAI)";
  if (!naive.sublabel)  naive.sublabel  = "DeepSeek-V4-Pro";
  if (!nebius.sublabel) nebius.sublabel = "DeepSeek-V4-Pro + Pinecone + Tavily";
  if (!openai.sublabel) openai.sublabel = "GPT-5.5 + Pinecone + Tavily";
  if (!naive.tagline)   naive.tagline   = "1 retrieval + 1 LLM call · no tools";
  if (!nebius.tagline)  nebius.tagline  = "ReAct · Pinecone + web · sub-agent fan-out";
  if (!openai.tagline)  openai.tagline  = "ReAct · Pinecone + web · sub-agent fan-out";
  return { naive, agentic: nebius, openai };
}


function App() {
  const [scene, setScene] = React.useState("audit");
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);
  const { version, status } = useForgeData();

  return (
    <div data-screen-label={
      scene === "audit"   ? "01 Audit" :
      scene === "compare" ? "02 Compare" :
                            "03 Evaluation"
    }>
      <SpinnerStyle/>
      <Topbar scene={scene} nav={setScene}/>
      <main style={{ maxWidth: 1480, margin: "0 auto" }}>
        {/* All three screens stay mounted so in-flight streams + composer state
            survive tab switches. Inactive screens are display:none, which keeps
            React state + SSE readers alive but skips layout. */}
        <div style={{ display: scene === "audit"   ? "block" : "none" }}><AuditScreen   dataVersion={version} loadStatus={status}/></div>
        <div style={{ display: scene === "compare" ? "block" : "none" }}><CompareScreen dataVersion={version} loadStatus={status}/></div>
        <div style={{ display: scene === "eval"    ? "block" : "none" }}><EvalScreen    dataVersion={version} loadStatus={status}/></div>
      </main>

      <TweaksPanel>
        <TweakSection label="Screen">
          <TweakRadio
            label="Active screen"
            value={scene}
            onChange={v => setScene(v)}
            options={[
              { value: "audit",   label: "Audit"   },
              { value: "compare", label: "Compare" },
              { value: "eval",    label: "Eval"    },
            ]}
          />
        </TweakSection>
        <TweakSection label="Demo focus">
          <TweakSelect
            label="Story"
            value={t.focus}
            onChange={v => setTweak("focus", v)}
            options={[
              { value: "balanced", label: "Balanced — all three equal" },
              { value: "recall",   label: "100% recall vs 12% miss" },
              { value: "cost",     label: "Nebius 3.4× cheaper" },
              { value: "category", label: "Where agents matter most" },
            ]}/>
        </TweakSection>
        <TweakSection label="Data status">
          <div style={{ font: "500 11px/16px var(--forge-font)", color: "rgba(255,255,255,0.7)" }}>
            kb: {status.kb} · eval: {status.eval} · dataset: {status.dataset} · findings: {status.findings}
          </div>
        </TweakSection>
      </TweaksPanel>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
