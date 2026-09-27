# Design System Specification (design.md)
## Digital Lifestyle Spillover Model (DLSM)
### *Visual Identity, Color Tokens, Typography & UI Component Standards*

- **Document Version:** 1.0.0
- **Status:** APPROVED & ACTIVE
- **Target Interface:** Streamlit Research Portal & Publication Figures
- **Repository Root:** `c:/Users/Lenovo/Downloads/DLSM`

---

## 1. Core Design Philosophy

The DLSM visual language adheres to **Edward Tufte's Data-Ink Maximization** and **Modern Academic Minimalism**:
1. **Academic Rigor:** Clean, professional, and publication-ready; avoids distracting visual gimmicks or toy aesthetics.
2. **High Information Scannability:** Key scientific metrics (effect sizes, $R^2$, $p$-values, bootstrap CIs) are highlighted with high visual hierarchy.
3. **Harmonious Scientific Palette:** Thoughtfully curated HSL color tokens that clearly differentiate between *Digital Disruption* (Crimson/Amber), *Biological Restoration* (Emerald/Teal), and *Latent Dimensions* (Electric Indigo/Slate).
4. **Interactive Responsiveness:** Visual elements provide hover feedback, clear legends, and reactive chart filtering.

---

## 2. Color Palette & Design Tokens

```
==================================================================================
DLSM DESIGN COLOR TOKENS
==================================================================================
Primary Slate        [ #0f172a ]  Deep Midnight Navy (Headings & Dominant UI)
Secondary Slate      [ #334155 ]  Slate Grey (Body Text & Labels)
Muted Slate          [ #64748b ]  Cool Grey (Captions, Sub-headers & Borders)
Background Neutral   [ #f8fafc ]  Alabaster Off-White (Card & Section Backgrounds)
Surface White        [ #ffffff ]  Pure White (Main Page Container)

-- Semantic Indicator Tokens --
Biological Buffer    [ #10b981 ]  Emerald Green (Restorative Sleep & Exercise)
Latent Construct     [ #3b82f6 ]  Electric Blue (PCA Loadings & Regression Fits)
Nocturnal Disruption [ #ef4444 ]  Crimson Red (Severe Sleep Debt & High Fatigue)
Cognitive Arousal    [ #f59e0b ]  Warm Amber (Late-night Screen Exposure & Caffeine)
Dual-Screen Load     [ #8b5cf6 ]  Royal Violet (AI Tools & High Digital Volume)
Border Divider       [ #e2e8f0 ]  Subtle Border Stroke
==================================================================================
```

### 2.1 Color Mapping Across Cohorts
- **Dataset A (Bedtime Telemetry):** Styled with **Electric Blue (`#3b82f6`)** and **Crimson (`#ef4444`)** to reflect nocturnal screen exposure vs circadian sleep debt.
- **Dataset B (Student Digital Life):** Styled with **Emerald Green (`#10b981`)** and **Royal Violet (`#8b5cf6`)** to represent generative AI tool engagement balanced against lifestyle physical buffers.

---

## 3. Typography Hierarchy

| Style Level | Font Family | Size | Weight | Line Height | Usage |
|:---|:---|:---:|:---:|:---:|:---|
| **Display Title** | `Inter`, sans-serif | `2.30 rem` | Bold (700) | `1.2` | Main Portal Header |
| **Section Header (H2)**| `Inter`, sans-serif | `1.50 rem` | Semi-Bold (600)| `1.3` | Research Module Sections |
| **Sub-Header (H3)** | `Inter`, sans-serif | `1.15 rem` | Semi-Bold (600)| `1.4` | Subsections & Plot Titles |
| **Body Text** | `Inter`, sans-serif | `1.00 rem` | Regular (400) | `1.6` | Narrative explanations |
| **Metric Value** | `Inter`, sans-serif | `1.80 rem` | Bold (700) | `1.1` | Quantitative KPI Cards |
| **Code / Notation** | `JetBrains Mono`, monospace | `0.90 rem` | Regular (400) | `1.4` | Mathematical formulas & features |

---

## 4. UI Component Guidelines (Streamlit Portal)

### 4.1 Quantitative Metric Cards
All primary statistics must be encapsulated within standard metric card containers:
```html
<div class="metric-card">
    <div class="card-title">LATENT DLL STABILITY (1000 RESAMPLES)</div>
    <div class="card-value">1.0000 <span style="font-size:1rem;color:#10b981;">(±0.0001)</span></div>
</div>
```
- Background: `#f8fafc`
- Border: `1px solid #e2e8f0`
- Border-radius: `8px`
- Padding: `16px`

### 4.2 Interactive Plotly Figures
- **Template:** `plotly_white`
- **Font:** `Inter`, neutral dark `#1e293b`
- **Margins:** Top: 40px, Bottom: 40px, Left: 50px, Right: 30px
- **Hovermode:** `closest` or `x unified`
- Zero background grid clutter: X and Y axis lines must use subtle `#f1f5f9` dividers.

### 4.3 Callouts & Scientific Badges
- **Success (`st.success`):** Used strictly for verified empirical milestones (e.g., successful Pandera validation, confirmed bootstrap stability).
- **Warning (`st.warning`):** Mandatory for cross-sectional methodological caveats (e.g., reminding users that mediation paths do not prove causal direction).
- **Info (`st.info`):** Used for theoretical definitions, research questions, and mathematical formula cards.
