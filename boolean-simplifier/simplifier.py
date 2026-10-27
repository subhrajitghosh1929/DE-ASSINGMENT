#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI-Assisted Boolean Expression Simplifier
==========================================
DE Assignment -- 4-Variable SOP Simplification
  * Truth table generation
  * K-map (4-variable) display
  * SymPy-based minimal SOP derivation
  * Google Gemini AI explanation & verification
  * Gate-count comparison (canonical vs minimised)

Function: F(A,B,C,D) = Sm(0,2,3,4,6,7,8,10,11,12)
Minimised: F = A'C + B'C + C'D'
"""

import os
import sys
import io
from typing import List

# ── Try optional imports ─────────────────────────────────────────────────────
try:
    from sympy.logic.boolalg import SOPform, POSform, simplify_logic
    from sympy import symbols as _sym
    SYMPY_OK = True
except ImportError:
    SYMPY_OK = False
    print("[WARN] SymPy not found - install with: pip install sympy")

try:
    import google.generativeai as genai
    GENAI_OK = True
except ImportError:
    GENAI_OK = False
    print("[WARN] google-generativeai not found - install with: pip install google-generativeai")

try:
    from tabulate import tabulate
    TABULATE_OK = True
except ImportError:
    TABULATE_OK = False

# ─────────────────────────────────────────────────────────────────────────────
# Problem Definition
# ─────────────────────────────────────────────────────────────────────────────
VARS        = ["A", "B", "C", "D"]
NUM_VARS    = 4
NUM_ROWS    = 2 ** NUM_VARS
MINTERMS    = [0, 2, 3, 4, 6, 7, 8, 10, 11, 12]   # F = 1 here
MAXTERMS    = [m for m in range(NUM_ROWS) if m not in MINTERMS]

SEP  = "=" * 70
SSEP = "-" * 70
# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def minterm_to_bits(minterm: int, n: int = NUM_VARS) -> List[int]:
    """Convert minterm number to list of bit values (MSB first)."""
    return [(minterm >> (n - 1 - i)) & 1 for i in range(n)]


def eval_f(bits: List[int]) -> int:
    """Evaluate original F(A,B,C,D) from bit list [A,B,C,D]."""
    minterm_num = sum(b << (NUM_VARS - 1 - i) for i, b in enumerate(bits))
    return 1 if minterm_num in MINTERMS else 0


def eval_simplified(bits: List[int]) -> int:
    """Evaluate minimised F = A'C + B'C + C'D'."""
    a, b, c, d = bits
    term1 = (1 - a) & c           # A'C
    term2 = (1 - b) & c           # B'C
    term3 = (1 - c) & (1 - d)     # C'D'
    return 1 if (term1 | term2 | term3) else 0


# ─────────────────────────────────────────────────────────────────────────────
# 1. Truth Table
# ─────────────────────────────────────────────────────────────────────────────
def print_truth_table():
    print(f"\n{SEP}")
    print("  TRUTH TABLE   F(A,B,C,D) = Σm(0,2,3,4,6,7,8,10,11,12)")
    print(SEP)

    rows = []
    for m in range(NUM_ROWS):
        bits = minterm_to_bits(m)
        f_val = eval_f(bits)
        f_min = eval_simplified(bits)
        match = "✓" if f_val == f_min else "✗ MISMATCH"
        rows.append([m, *bits, f_val, f_min, match])

    headers = ["m#", "A", "B", "C", "D", "F (orig)", "F (min)", "Match"]

    if TABULATE_OK:
        print(tabulate(rows, headers=headers, tablefmt="rounded_grid"))
    else:
        print(f"{'m#':>3} | A | B | C | D | F(orig) | F(min) | Match")
        print(SSEP)
        for r in rows:
            print(f"{r[0]:>3} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |    {r[5]}    |    {r[6]}   | {r[7]}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. Canonical SOP (unsimplified)
# ─────────────────────────────────────────────────────────────────────────────
def minterm_to_product(m: int) -> str:
    bits = minterm_to_bits(m)
    terms = []
    for i, (var, bit) in enumerate(zip(VARS, bits)):
        terms.append(var if bit else f"{var}'")
    return "".join(terms)


def print_canonical_sop():
    print(f"\n{SEP}")
    print("  CANONICAL SOP (unsimplified)")
    print(SEP)
    products = [minterm_to_product(m) for m in MINTERMS]
    print("F = " + " + ".join(products))
    literals = sum(NUM_VARS for _ in MINTERMS)
    print(f"\n  → {len(MINTERMS)} product terms, {literals} literals")
    print(f"  → Requires {len(MINTERMS)} AND gates + 1 OR gate + {NUM_VARS} NOT gates")


# ─────────────────────────────────────────────────────────────────────────────
# 3. K-Map (4-variable, Gray-code order)
# ─────────────────────────────────────────────────────────────────────────────
GRAY = [0, 1, 3, 2]   # Gray-code column/row order for CD and AB

def kmap_value(ab_idx: int, cd_idx: int) -> int:
    ab = GRAY[ab_idx]
    cd = GRAY[cd_idx]
    minterm = (ab << 2) | cd
    return eval_f(minterm_to_bits(minterm))


def kmap_minterm(ab_idx: int, cd_idx: int) -> int:
    ab = GRAY[ab_idx]
    cd = GRAY[cd_idx]
    return (ab << 2) | cd


def print_kmap():
    print(f"\n{SEP}")
    print("  4-VARIABLE K-MAP  (Gray-code order)")
    print(SEP)
    col_labels = ["CD=00", "CD=01", "CD=11", "CD=10"]
    row_labels  = ["AB=00", "AB=01", "AB=11", "AB=10"]

    print(f"{'':>8}", end="")
    for cl in col_labels:
        print(f"  {cl}", end="")
    print()
    print(f"{'':>8}" + "  " + "------  " * 4)

    for ri in range(4):
        print(f"{row_labels[ri]:>8} |", end="")
        for ci in range(4):
            v = kmap_value(ri, ci)
            m = kmap_minterm(ri, ci)
            cell = f" {v}(m{m:02d}) "
            print(f"{cell}|", end="")
        print()

    print()
    print("  Groups identified:")
    print("  +----------------------------------------------------------+")
    print("  |  Group 1 -> m(2,3,6,7)      -- A'C  (A=0, C=1)         |")
    print("  |  Group 2 -> m(2,3,10,11)    -- B'C  (B=0, C=1)         |")
    print("  |  Group 3 -> m(0,4,8,12)     -- C'D' (C=0, D=0)         |")
    print("  +----------------------------------------------------------+")
    print()
    print("  => Minimised SOP: F = A'C + B'C + C'D'")
    print()
    print("  Algebraic check:")
    print("    A'C + B'C = C(A' + B')")
    print("              = C*(AB)'       (De Morgan)")
    print("    F = C*(AB)' + C'D'  (equivalent 2-term form)")


# ─────────────────────────────────────────────────────────────────────────────
# 4. SymPy Minimisation
# ─────────────────────────────────────────────────────────────────────────────
def print_sympy_result():
    print(f"\n{SEP}")
    print("  SYMPY BOOLEAN MINIMISATION")
    print(SEP)

    if not SYMPY_OK:
        print("  [SKIP] SymPy not available.")
        return

    minterms_list = [[int(b) for b in minterm_to_bits(m)] for m in MINTERMS]
    sop = SOPform(list("ABCD"), minterms_list)
    pos = POSform(list("ABCD"), minterms_list)

    print(f"  Minimised SOP (via Quine-McCluskey): {sop}")
    print(f"  Minimised POS (via Quine-McCluskey): {pos}")
    simplified = simplify_logic(sop, form="dnf")
    print(f"  Further simplified DNF:              {simplified}")


# ─────────────────────────────────────────────────────────────────────────────
# 5. AI Explanation (Google Gemini)
# ─────────────────────────────────────────────────────────────────────────────
AI_PROMPT = """
You are an expert in digital electronics and Boolean algebra.

A student has the following 4-variable Boolean function:
  F(A,B,C,D) = Σm(0,2,3,4,6,7,8,10,11,12)

The AI-simplified result is: F = A'C + B'C + C'D'

Please:
1. Confirm this is correct (verify by listing covered minterms for each term).
2. Show the K-map groupings that led to this result.
3. Explain the algebraic equivalence: A'C + B'C = C(A' + B') = C·(AB)'
4. Compare gate counts:  
   • Canonical SOP: 10 AND gates + 1 ten-input OR gate + 4 NOT gates  
   • Minimised SOP: 3 AND gates + 1 three-input OR gate + 4 NOT gates  
5. State what the Logisim circuit should look like (inputs → NOT → AND → OR → output).
6. Give a one-paragraph summary suitable for a Digital Electronics assignment.

Keep the response concise, structured, and educational.
"""


def print_ai_explanation():
    print(f"\n{SEP}")
    print("  AI EXPLANATION (Google Gemini)")
    print(SEP)

    if not GENAI_OK:
        print("  [SKIP] google-generativeai not installed.")
        print("  Install: pip install google-generativeai")
        print("  Then set: GEMINI_API_KEY environment variable")
        _print_static_explanation()
        return

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("  [SKIP] GEMINI_API_KEY environment variable not set.")
        _print_static_explanation()
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(AI_PROMPT)
        print(response.text)
    except Exception as e:
        print(f"  [ERROR] Gemini API call failed: {e}")
        _print_static_explanation()


def _print_static_explanation():
    """Fallback built-in explanation when Gemini API is unavailable."""
    print("""
  ━━━ Built-in AI-Style Explanation ━━━

  Step 1 — Minterm Verification
  ─────────────────────────────
  • A'C covers minterms where A=0 & C=1  →  m2,m3,m6,m7
  • B'C covers minterms where B=0 & C=1  →  m2,m3,m10,m11
  • C'D' covers minterms where C=0 & D=0 →  m0,m4,m8,m12
  Union = {0,2,3,4,6,7,8,10,11,12} = Σm  ✓

  Step 2 — K-Map Groupings
  ─────────────────────────
  The 4-variable K-map reveals three prime implicant groups:
    • Quad A'C   : top-half rows (AB=00,01) × right-half cols (CD=10,11)
    • Quad B'C   : left & right halves (AB=00,10) × right-half cols
    • Quad C'D'  : entire leftmost column (CD=00) wrapping AB=00→11→10→01

  Step 3 — Algebraic Simplification
  ────────────────────────────────────
    A'C + B'C  =  C(A' + B')          [factorise C]
               =  C · (AB)'            [De Morgan]
    ∴ F = C(AB)' + C'D'              [2-term POS-like form]

  Step 4 — Gate Count Comparison
  ────────────────────────────────
    Canonical SOP : 10 AND (4-input) + 1 OR (10-input) + 4 NOT = 15 gates
    Minimised SOP :  3 AND (2-input) + 1 OR  (3-input)  + 4 NOT =  8 gates
    Savings       : ~47% fewer gates, simpler PCB layout, lower propagation delay

  Step 5 — Assignment Summary
  ────────────────────────────
  The Boolean function F(A,B,C,D) = Σm(0,2,3,4,6,7,8,10,11,12) was
  simplified using Karnaugh-map grouping. Three prime implicants—A'C,
  B'C, and C'D'—collectively cover all minterms with no redundancy.
  The minimised expression F = A'C + B'C + C'D' requires only 8 logic
  gates (vs 15 in canonical form), reducing hardware complexity by 47%.
  The circuit was implemented and verified in Logisim 2.7.1.
""")


# ─────────────────────────────────────────────────────────────────────────────
# 6. Gate Count Summary
# ─────────────────────────────────────────────────────────────────────────────
def print_gate_summary():
    print(f"\n{SEP}")
    print("  GATE COUNT COMPARISON")
    print(SEP)
    data = [
        ["Canonical SOP",  "10 × 4-in AND", "1 × 10-in OR", "4 NOT",  "15 gates"],
        ["Minimised SOP",  " 3 × 2-in AND", "1 × 3-in OR",  "4 NOT",  " 8 gates"],
        ["Savings",         "−7 AND gates",  "simpler OR",   "same",  "~47% fewer"],
    ]
    headers = ["Form", "AND gates", "OR gates", "NOT gates", "Total"]
    if TABULATE_OK:
        print(tabulate(data, headers=headers, tablefmt="rounded_outline"))
    else:
        for row in data:
            print("  " + " | ".join(f"{c:20}" for c in row))


# ─────────────────────────────────────────────────────────────────────────────
# 7. Verification
# ─────────────────────────────────────────────────────────────────────────────
def verify():
    print(f"\n{SEP}")
    print("  VERIFICATION — F_original vs F_minimised")
    print(SEP)
    mismatches = []
    for m in range(NUM_ROWS):
        bits = minterm_to_bits(m)
        if eval_f(bits) != eval_simplified(bits):
            mismatches.append(m)

    if mismatches:
        print(f"  [FAIL] MISMATCH at minterms: {mismatches}")
        return False
    else:
        print("  [PASS] All 16 minterm evaluations match -- simplification is CORRECT")
        return True


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    BANNER = "#" * 70
    print(f"\n{BANNER}")
    print("  AI-ASSISTED BOOLEAN EXPRESSION SIMPLIFIER")
    print("  DE Assignment | 4-Variable | SOP | K-Map & Algebraic")
    print(BANNER)
    print(f"  Function : F(A,B,C,D) = Sm({', '.join(map(str, MINTERMS))})")
    print(f"  Variables: {', '.join(VARS)}")

    print_truth_table()
    print_canonical_sop()
    print_kmap()
    print_sympy_result()
    print_ai_explanation()
    print_gate_summary()
    ok = verify()

    print(f"\n{SEP}")
    print("  FINAL RESULT")
    print(SEP)
    print("  F(A,B,C,D) = A'C + B'C + C'D'")
    print()
    print("  Logisim circuit : circuit/boolean_simplifier.circ")
    print("  Documentation   : docs/")
    print("  Screenshots     : screenshots/")
    print(f"\n{BANNER}\n")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
