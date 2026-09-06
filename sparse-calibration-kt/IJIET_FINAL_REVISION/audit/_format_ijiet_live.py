#!/usr/bin/env python3
"""Live IJIET format audit: template vs named Word + PDF."""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import fitz
import win32com.client as win32

HERE = Path(__file__).resolve().parent.parent
DOCX = HERE / "manuscript" / (
    "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.docx"
)
PDF = HERE / "output" / (
    "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing.pdf"
)
BLIND = HERE / "output" / (
    "Reproducible Sparse-Concept and Calibration Diagnostics for Knowledge Tracing_blind.pdf"
)
TPL_DOC = HERE.parent / "IJIET_SUBMISSION" / "source" / "template" / "IJIET_template.doc"
OUT = HERE / "audit" / "FORMAT_LIVE_20260906.md"

WD_ALIGN = {0: "left", 1: "center", 2: "right", 3: "justify"}
TPL = {
    "page_w": 595.35,
    "page_h": 841.95,
    "T": 50.45,
    "B": 50.45,
    "L": 46.80,
    "R": 46.80,
    "col_w": 243.65,
    "gutter": 14.4,
}


def font_of(rng) -> tuple[str, float, int, int]:
    f = rng.Font
    name = f.Name or ""
    sz = float(f.Size) if f.Size not in (None, 9999999) else -1
    b = int(f.Bold) if f.Bold not in (None, 9999999) else -1
    i = int(f.Italic) if f.Italic not in (None, 9999999) else -1
    return name, sz, b, i


def inner_text(doc, p) -> str:
    return doc.Range(p.Range.Start, p.Range.End - 1).Text.replace("\r", "").replace("\x07", "")


def close(v, t, tol=0.6) -> bool:
    return abs(v - t) <= tol


def measure_doc(path: Path, label: str) -> list[str]:
    word = win32.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    doc = word.Documents.Open(str(path), ReadOnly=True)
    lines = [f"## {label}", f"file={path.name}"]
    try:
        lines.append(
            f"pages={doc.ComputeStatistics(2)} words={doc.ComputeStatistics(0)} "
            f"paras={doc.Paragraphs.Count} tables={doc.Tables.Count} figs={doc.InlineShapes.Count}"
        )
        for i in range(1, doc.Sections.Count + 1):
            s = doc.Sections(i)
            ps = s.PageSetup
            hdr = (s.Headers(1).Range.Text or "").replace("\r", " ").strip()
            ftr = (s.Footers(1).Range.Text or "").replace("\r", " ").strip()
            cols = ps.TextColumns.Count
            gutter = float(ps.TextColumns.Spacing) if cols >= 2 else 0.0
            cw = None
            if cols >= 1:
                try:
                    cw = float(ps.TextColumns(1).Width)
                except Exception:
                    cw = None
            ok = (
                close(ps.PageWidth, TPL["page_w"])
                and close(ps.PageHeight, TPL["page_h"])
                and close(ps.TopMargin, TPL["T"])
                and close(ps.BottomMargin, TPL["B"])
                and close(ps.LeftMargin, TPL["L"])
                and close(ps.RightMargin, TPL["R"])
            )
            col_ok = True
            if cols >= 2:
                col_ok = (
                    cw is not None
                    and close(cw, TPL["col_w"], 1.0)
                    and close(gutter, TPL["gutter"], 0.5)
                )
            lines.append(
                f"sec{i} paper={ps.PageWidth:.2f}x{ps.PageHeight:.2f} "
                f"T={ps.TopMargin:.2f} B={ps.BottomMargin:.2f} "
                f"L={ps.LeftMargin:.2f} R={ps.RightMargin:.2f} "
                f"cols={cols} colw={cw} gutter={gutter:.2f} "
                f"geom={'OK' if ok else 'DIFF'} col={'OK' if col_ok else 'DIFF'} "
                f"header={hdr[:50]!r} footer={ftr[:50]!r}"
            )
        lines.append("### front")
        for i in range(1, 18):
            p = doc.Paragraphs(i)
            t = inner_text(doc, p).strip().replace("\x0c", "")
            if not t:
                continue
            name, sz, b, it = font_of(doc.Range(p.Range.Start, p.Range.End - 1))
            al = WD_ALIGN.get(int(p.Alignment), str(p.Alignment))
            lines.append(
                f"P{i} {p.Style.NameLocal!r} {name} {sz}pt b={b} i={it} {al} "
                f"ind={p.Format.FirstLineIndent:.1f} sa={p.Format.SpaceAfter:.1f} | {t[:90]}"
            )
        h1 = h2 = 0
        caps = []
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs(i)
            t = inner_text(doc, p).strip()
            st = p.Style.NameLocal
            name, sz, b, it = font_of(doc.Range(p.Range.Start, p.Range.End - 1))
            if st.startswith("Heading 1"):
                h1 += 1
                lines.append(f"H1 {sz}pt b={b} {name} | {t[:70]}")
            elif st.startswith("Heading 2"):
                h2 += 1
            elif t.startswith("Table ") or t.startswith("Fig."):
                caps.append((st, name, sz, t[:70]))
                if st != "figure caption" or abs(sz - 8) > 0.2:
                    lines.append(f"CAP_DIFF {st!r} {name} {sz}pt | {t[:70]}")
        lines.append(f"H1_n={h1} H2_n={h2} CAP_n={len(caps)}")
        body_sz: Counter[float] = Counter()
        body_al: Counter[str] = Counter()
        body_font: Counter[str] = Counter()
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs(i)
            try:
                if p.Range.Tables.Count:
                    continue
            except Exception:
                pass
            if p.Style.NameLocal != "Text":
                continue
            t = inner_text(doc, p).strip()
            if len(t) < 60:
                continue
            name, sz, b, it = font_of(doc.Range(p.Range.Start, p.Range.End - 1))
            body_sz[sz] += 1
            body_font[name or "(empty)"] += 1
            body_al[WD_ALIGN.get(int(p.Alignment), str(p.Alignment))] += 1
        lines.append(f"body_sz={dict(body_sz)} fonts={dict(body_font)} align={dict(body_al)}")
        for ti in range(1, doc.Tables.Count + 1):
            tbl = doc.Tables(ti)
            cell_sz: Counter[float] = Counter()
            for r in range(1, tbl.Rows.Count + 1):
                for c in range(1, tbl.Columns.Count + 1):
                    try:
                        _, sz, _, _ = font_of(tbl.Cell(r, c).Range)
                    except Exception:
                        continue
                    cell_sz[sz] += 1
            lines.append(f"T{ti} {tbl.Rows.Count}x{tbl.Columns.Count} sz={dict(cell_sz)}")
        for i in range(1, doc.InlineShapes.Count + 1):
            sh = doc.InlineShapes(i)
            lines.append(f"fig{i} {sh.Width:.1f}x{sh.Height:.1f}")
        for i in range(1, doc.Paragraphs.Count + 1):
            p = doc.Paragraphs(i)
            t = inner_text(doc, p).strip()
            if t.lower().startswith("references"):
                name, sz, b, it = font_of(doc.Range(p.Range.Start, p.Range.End - 1))
                lines.append(f"REFHEAD {p.Style.NameLocal!r} {name} {sz}pt | {t[:40]}")
                if i < doc.Paragraphs.Count:
                    q = doc.Paragraphs(i + 1)
                    qn, qs, qb, qi = font_of(doc.Range(q.Range.Start, q.Range.End - 1))
                    lines.append(
                        f"REF1 {q.Style.NameLocal!r} {qn} {qs}pt hang={q.Format.FirstLineIndent:.1f} | {inner_text(doc, q).strip()[:60]}"
                    )
                break
    finally:
        doc.Close(0)
        word.Quit()
    return lines


def measure_pdf(path: Path, label: str) -> list[str]:
    d = fitz.open(str(path))
    lines = [f"## {label}", f"pages={d.page_count} rect={tuple(round(x, 2) for x in d[0].rect)}"]
    meta = d.metadata or {}
    lines.append(f"meta_title={meta.get('title')!r} meta_author={meta.get('author')!r}")
    # geometry page 1 vs later
    for i in (0, min(2, d.page_count - 1), d.page_count - 1):
        r = d[i].rect
        lines.append(f"p{i+1} {r.width:.2f}x{r.height:.2f}")
    # header-ish text at top 40pt
    top_hits = []
    for i, p in enumerate(d, 1):
        for b in p.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            if b["bbox"][1] > 48:
                continue
            t = "".join(s.get("text", "") for ln in b.get("lines", []) for s in ln.get("spans", [])).strip()
            if t:
                top_hits.append(f"p{i} y={b['bbox'][1]:.1f} {t[:60]}")
    lines.append(f"top_band_n={len(top_hits)}")
    lines.extend(top_hits[:8])
    blob = "\n".join(p.get_text("text") for p in d)
    lines.append(f"has_Month_date={'Month date, 2026' in blob}")
    lines.append(f"has_DOI_10.18178={'10.18178' in blob}")
    lines.append(f"has_CC_BY={'CC BY' in blob}")
    lines.append(f"has_IV_RESULTS={'IV. RESULTS' in blob}")
    lines.append(f"has_IV_RESULT_sing={'IV. RESULT' in blob and 'IV. RESULTS' not in blob}")
    # caption sizes
    cap_sz: Counter[float] = Counter()
    body_sz: Counter[float] = Counter()
    for p in d:
        for b in p.get_text("dict")["blocks"]:
            if b.get("type") != 0:
                continue
            for ln in b.get("lines", []):
                line = "".join(s.get("text", "") for s in ln.get("spans", [])).strip()
                sizes = [round(s["size"], 1) for s in ln.get("spans", []) if s.get("text", "").strip()]
                if not sizes:
                    continue
                if line.startswith("Table ") or line.startswith("Fig."):
                    cap_sz[sizes[0]] += 1
                elif 9.5 <= sizes[0] <= 10.5 and len(line) > 40:
                    body_sz[sizes[0]] += 1
    lines.append(f"pdf_caption_sz={dict(cap_sz)} pdf_body_sample={dict(body_sz)}")
    d.close()
    return lines


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    chunks = []
    if TPL_DOC.is_file():
        chunks.extend(measure_doc(TPL_DOC, "TEMPLATE"))
    chunks.extend(measure_doc(DOCX, "NAMED WORD"))
    chunks.extend(measure_pdf(PDF, "NAMED PDF"))
    if BLIND.is_file():
        chunks.extend(measure_pdf(BLIND, "BLIND PDF"))
    text = "\n".join(chunks) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
