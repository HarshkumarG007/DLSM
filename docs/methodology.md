# DLSM Methodology & Mathematical Specifications

## 1. Fundamental Methodological Paradigm

The Digital Lifestyle Spillover Model (DLSM) operates on the principle that disjoint observational datasets must never be fused row-wise without verified individual-level entity linkage (**RULE-001**).

Instead, DLSM adopts **Direction B (Cross-Dataset Latent Representation)** combined with **Direction C (Cross-Dataset Evidence Graph)**:

$$Z_A = f(X_A), \quad Z_B = f(X_B)$$

Where $Z_A$ and $Z_B$ represent independently estimated, standardized latent representations of Digital Lifestyle Load (DLL) grounded in domain-specific observables.

---

## 2. Mathematical Formulations of Engineered Features

### 2.1 Dataset A: Bedtime Optical & Cognitive Exposure
1. **Bedtime Intensity Index ($\text{BII}$):**
   $$\text{BII}_i = \left(\frac{\text{screen\_brightness\_pct}_i}{100}\right) \times \text{bedtime\_phone\_minutes}_i \times \left(1.0 - 0.30 \times \text{blue\_light\_filter\_active}_i\right)$$
2. **Screen-to-Sleep Ratio ($\text{SSR}_A$):**
   $$\text{SSR}_{A,i} = \frac{\text{bedtime\_phone\_minutes}_i / 60}{\text{total\_sleep\_hours}_i + 10^{-5}}$$
3. **Sleep Architecture Efficiency ($\text{SAE}$):**
   $$\text{SAE}_i = \frac{\text{deep\_sleep\_pct}_i + \text{rem\_sleep\_pct}_i}{100}$$
4. **App Cognitive Arousal Weighting ($\text{AW}$):**
   $$\text{Arousal Weighted Exposure}_i = \text{bedtime\_phone\_minutes}_i \times w_{\text{app}, i}$$
   Where $w_{\text{app}} \in \{1.00 \text{ (TikTok/Reels)}, 0.80 \text{ (YouTube)}, 0.75 \text{ (Instagram/Reddit)}, 0.60 \text{ (Streaming)}, 0.50 \text{ (Messaging)}, 0.30 \text{ (Reading)}\}$.

### 2.2 Dataset B: Student Digital Lifestyle & Buffering
1. **Total Digital Hours ($\text{TDH}$):**
   $$\text{TDH}_i = \text{Daily\_Social\_Media\_Hours}_i + \text{Daily\_AI\_Tool\_Usage\_Hours}_i$$
2. **Digital Composition Ratio ($\text{DCR}$):**
   $$\text{DCR}_i = \frac{\text{Daily\_AI\_Tool\_Usage\_Hours}_i}{\text{TDH}_i + 10^{-5}}$$
3. **Screen-to-Sleep Ratio ($\text{SSR}_B$):**
   $$\text{SSR}_{B,i} = \frac{\text{TDH}_i}{\text{Sleep\_Hours}_i + 10^{-5}}$$
4. **Active Buffer Ratio ($\text{ABR}$):**
   $$\text{ABR}_i = \frac{\text{Physical\_Activity\_Hours}_i}{\text{TDH}_i + 10^{-5}}$$

---

## 3. Latent Digital Lifestyle Load (DLL) Construction

For standardized feature matrix $X \in \mathbb{R}^{n \times p}$:

$$Z = X W$$

Where $W$ contains the orthonormal principal component loading vectors satisfying $\Sigma W = W \Lambda$.
Orientation harmonization enforces $\text{sign}\left(\sum_{j=1}^p w_{j1}\right) > 0$.

### Resampling Stability Analysis
Stability is evaluated across $B = 1,000$ bootstrap iterations:
$$\bar{s} = \frac{1}{B} \sum_{b=1}^B \frac{w_1 \cdot w_{1,b}}{\|w_1\|_2 \|w_{1,b}\|_2}$$

---

## 4. Statistical Mediation Specification

- **Model 1:** $M_i = a X_i + C_i \gamma_M + \epsilon_{M,i}$
- **Model 2:** $Y_i = c' X_i + b M_i + C_i \gamma_Y + \epsilon_{Y,i}$
- **Indirect Effect:** $\hat{\theta}_{ab} = \hat{a} \times \hat{b}$
- **Direct Effect:** $\hat{c}'$
- **Total Effect:** $\hat{c} = \hat{c}' + \hat{a} \times \hat{b}$
- **Proportion Mediated:** $\hat{P}_M = \frac{\hat{a} \times \hat{b}}{\hat{c}}$

Non-parametric percentile bootstrap intervals $[CI_{2.5\%}, CI_{97.5\%}]$ are computed over $B = 5,000$ resamples.
