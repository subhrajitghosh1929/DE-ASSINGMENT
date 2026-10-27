# 🔬 AI-Assisted Boolean Expression Simplifier

> **Digital Electronics Assignment**  
> 4-Variable Boolean Function — SOP Minimisation using K-Map, Algebraic Method & AI (Google Gemini)  
> Circuit verified in **Logisim 2.7.1**

---

## 📌 Problem Statement

Simplify the following 4-variable Boolean function and implement the minimised circuit in Logisim:

```
F(A, B, C, D) = Σm(0, 2, 3, 4, 6, 7, 8, 10, 11, 12)
```

---

## 📐 Truth Table

| m# | A | B | C | D | **F** |
|:--:|:-:|:-:|:-:|:-:|:-----:|
|  0 | 0 | 0 | 0 | 0 | **1** |
|  1 | 0 | 0 | 0 | 1 |   0   |
|  2 | 0 | 0 | 1 | 0 | **1** |
|  3 | 0 | 0 | 1 | 1 | **1** |
|  4 | 0 | 1 | 0 | 0 | **1** |
|  5 | 0 | 1 | 0 | 1 |   0   |
|  6 | 0 | 1 | 1 | 0 | **1** |
|  7 | 0 | 1 | 1 | 1 | **1** |
|  8 | 1 | 0 | 0 | 0 | **1** |
|  9 | 1 | 0 | 0 | 1 |   0   |
| 10 | 1 | 0 | 1 | 0 | **1** |
| 11 | 1 | 0 | 1 | 1 | **1** |
| 12 | 1 | 1 | 0 | 0 | **1** |
| 13 | 1 | 1 | 0 | 1 |   0   |
| 14 | 1 | 1 | 1 | 0 |   0   |
| 15 | 1 | 1 | 1 | 1 |   0   |

---

## 🗺️ K-Map (4-Variable)

```
                    CD
           ┌────┬────┬────┬────┐
      AB   │ 00 │ 01 │ 11 │ 10 │
    ════════╪════╪════╪════╪════╡
      00    │  1 │  0 │  1 │  1 │  ← m0, m1, m3, m2
    ────────┼────┼────┼────┼────┤
      01    │  1 │  0 │  1 │  1 │  ← m4, m5, m7, m6
    ────────┼────┼────┼────┼────┤
      11    │  1 │  0 │  0 │  0 │  ← m12,m13,m15,m14
    ────────┼────┼────┼────┼────┤
      10    │  1 │  0 │  1 │  1 │  ← m8, m9, m11,m10
           └────┴────┴────┴────┘
```

### Prime Implicant Groups

| Group | Cells | Simplified | Explanation |
|-------|-------|-----------|-------------|
| 🟦 **Group 1** | m2, m3, m6, m7 | **A'C** | A=0 (rows 00,01) & C=1 (cols 10,11) |
| 🟩 **Group 2** | m2, m3, m10, m11 | **B'C** | B=0 (rows 00,10) & C=1 (cols 10,11) |
| 🟥 **Group 3** | m0, m4, m8, m12 | **C'D'** | C=0 & D=0 (entire col 00) |

---

## ✅ Minimised Expression

```
F = A'C + B'C + C'D'
```

### Algebraic Equivalence

```
F = A'C + B'C + C'D'
  = C(A' + B') + C'D'      ← factor C
  = C·(AB)'   + C'D'       ← De Morgan's theorem
```

### Gate Count Comparison

| | Canonical SOP | **Minimised SOP** | Savings |
|--|:---:|:---:|:---:|
| AND gates | 10 (4-input) | **3 (2-input)** | −7 gates |
| OR gate   | 1 (10-input) | **1 (3-input)** | simpler |
| NOT gates | 4 | **4** | — |
| **Total** | **15 gates** | **8 gates** | **−47%** |

---

## 🤖 AI Assistance (Google Gemini)

The [`simplifier.py`](simplifier.py) script uses **Google Gemini 1.5 Flash** to:
- Verify the K-map groupings
- Explain each simplification step
- Confirm minterm coverage
- Generate a human-readable assignment summary

Run it with:

```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_key_here"   # or set in Windows env vars
python simplifier.py
```

> The script works fully offline (without the API key) using its built-in explanation fallback.

---

## ⚡ Logisim Circuit

### File
```
circuit/boolean_simplifier.circ
```

### Circuit Architecture

```
  A ──────────────────────────── NOT ── A' ──┬── AND ── A'C ──┐
                                             │                │
  B ──────────────────────────── NOT ── B' ──┼── AND ── B'C ──┤── OR ── F
                                             │                │
  C ──┬─────────────────────────────────────┘── AND ── C'D' ─┘
      └── NOT ── C' ──────────────────────────┘
  D ────── NOT ── D' ──────────────────────────┘
```

### Opening in Logisim

1. Download [Logisim 2.7.1](http://www.cburch.com/logisim/)
2. Open `circuit/boolean_simplifier.circ`
3. Use **Poke Tool (hand icon)** to toggle inputs A, B, C, D
4. Verify output F matches the truth table above

### Testing the Circuit

Click inputs to set specific minterms and verify F:

| Test Case | A | B | C | D | Expected F |
|-----------|:-:|:-:|:-:|:-:|:----------:|
| m0  | 0 | 0 | 0 | 0 | **1** |
| m5  | 0 | 1 | 0 | 1 | **0** |
| m7  | 0 | 1 | 1 | 1 | **1** |
| m12 | 1 | 1 | 0 | 0 | **1** |
| m14 | 1 | 1 | 1 | 0 | **0** |

---

## 📸 Screenshots

| Screenshot | Description |
|------------|-------------|
| `screenshots/01_full_circuit.png` | Full circuit view in Logisim |
| `screenshots/02_minterm0.png` | A=0,B=0,C=0,D=0 → F=1 (C'D') |
| `screenshots/03_minterm7.png` | A=0,B=1,C=1,D=1 → F=1 (A'C) |
| `screenshots/04_minterm11.png` | A=1,B=0,C=1,D=1 → F=1 (B'C) |
| `screenshots/05_minterm14.png` | A=1,B=1,C=1,D=0 → F=0 (verify 0) |
| `screenshots/06_kmap.png` | K-Map from simplifier.py output |

> **How to take screenshots in Logisim:**  
> `Ctrl+Shift+S` or File → Export Image → PNG

---

## 📁 Project Structure

```
boolean-simplifier/
├── README.md                         ← This file (GitHub landing page)
├── requirements.txt                  ← Python dependencies
├── simplifier.py                     ← AI-assisted simplification script
├── circuit/
│   └── boolean_simplifier.circ      ← Logisim 2.7.1 circuit file
├── screenshots/
│   ├── 01_full_circuit.png           ← (add after opening in Logisim)
│   └── ...
└── docs/
    ├── truth_table.md                ← Full truth table
    └── analysis.md                  ← K-map & algebraic analysis
```

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| **Python 3.10+** | Simplification script |
| **SymPy** | Quine-McCluskey Boolean minimisation |
| **Google Gemini 1.5 Flash** | AI explanation & verification |
| **Logisim 2.7.1** | Circuit simulation & verification |
| **GitHub** | Version control & submission |

---

## 📚 References

1. Morris Mano, *Digital Design*, 5th ed. — Chapter 3: Gate-Level Minimization
2. [Logisim Official Site](http://www.cburch.com/logisim/)
3. [SymPy Boolean Logic Docs](https://docs.sympy.org/latest/modules/logic.html)
4. [Google Gemini API](https://ai.google.dev/)

---

## 👤 Author

| Field | Details |
|-------|---------|
| **Name** | Subhrajit |
| **Assignment** | Digital Electronics — Boolean Simplifier |
| **Date** | October 2026 |

---

*Circuit verified: All 16 minterms match between original and minimised expressions.*
