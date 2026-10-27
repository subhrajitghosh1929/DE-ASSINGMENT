# K-Map Analysis & Algebraic Simplification

## 4-Variable K-Map (Gray-Code Order)

```
              CD
         ╔═══╤═══╤═══╤═══╗
    AB   ║ 00│ 01│ 11│ 10║
    ═════╬═══╪═══╪═══╪═══╣
    00   ║ 1 │ 0 │ 1 │ 1 ║   m0, m1, m3, m2
    ─────╫───┼───┼───┼───╢
    01   ║ 1 │ 0 │ 1 │ 1 ║   m4, m5, m7, m6
    ─────╫───┼───┼───┼───╢
    11   ║ 1 │ 0 │ 0 │ 0 ║   m12,m13,m15,m14
    ─────╫───┼───┼───┼───╢
    10   ║ 1 │ 0 │ 1 │ 1 ║   m8, m9, m11,m10
         ╚═══╧═══╧═══╧═══╝
```

## Prime Implicant Groups

| Group | Minterms Covered | Simplified Term | Size |
|-------|-----------------|-----------------|------|
| **Group 1** | m2, m3, m6, m7 | **A'C** | Quad |
| **Group 2** | m2, m3, m10, m11 | **B'C** | Quad |
| **Group 3** | m0, m4, m8, m12 | **C'D'** | Quad |

> **Note:** m2 and m3 are shared between Group 1 and Group 2 (allowed in K-map — we pick largest groups).

## Minimised SOP

```
F = A'C + B'C + C'D'
```

- **3 product terms**, 6 literals
- Requires: 3 AND gates + 1 (3-in) OR gate + 4 NOT gates = **8 gates**
- **47% reduction** in gate count vs canonical SOP

## Algebraic Verification

### Step 1 — Verify each term covers its minterms

| Term | Condition | Minterms |
|------|-----------|----------|
| A'C  | A=0, C=1  | 2,3,6,7 ✓ |
| B'C  | B=0, C=1  | 2,3,10,11 ✓ |
| C'D' | C=0, D=0  | 0,4,8,12 ✓ |

Union = {0,2,3,4,6,7,8,10,11,12} = Σm ✓

### Step 2 — Algebraic Simplification

```
F = A'C + B'C + C'D'
  = C(A' + B') + C'D'         [factor out C]
  = C·(AB)'   + C'D'          [De Morgan: A'+B' = (AB)']
```

This gives an equivalent **2-term** expression using NAND logic.

### Step 3 — POS Form (bonus)

```
F = (A' + B' + C')(A + B + C')(C + D')... 
```
(Full POS derivation via maxterms 1,5,9,13,14,15)

## Gate-Count Comparison

| Implementation | AND Gates | OR Gate | NOT Gates | Total |
|----------------|-----------|---------|-----------|-------|
| Canonical SOP  | 10 × 4-in | 1 × 10-in | 4 | **15** |
| Minimised SOP  | 3 × 2-in  | 1 × 3-in  | 4 | **8** |
| Savings        | −7        | simpler   | 0 | **−7 (47%)** |

## Circuit Implementation (Logisim)

```
Inputs              NOT stage           AND stage           OR stage
  A ──────────────┬─[NOT]─ A' ─────────┬─[AND]─ A'C ──────┐
                  │                    │                    │
  B ──────────────┼─[NOT]─ B' ─────────┼─[AND]─ B'C ──────┤─[OR]── F
                  │                    │                    │
  C ──────────────┼─[NOT]─ C' ─────────┼─[AND]─ C'D' ─────┘
                  │                    │
  D ──────────────┴─[NOT]─ D' ─────────┘
```
