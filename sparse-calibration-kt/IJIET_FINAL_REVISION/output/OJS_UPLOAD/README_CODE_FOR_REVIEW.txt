Anonymous code bundle for IJIET double-blind review

This zip is the reviewer-facing code artifact. It does not contain:
- internal archive folders
- named IJIET Word sources
- multi-GB a2b data dumps or prediction files

It does contain local training/evaluation scripts, frozen table CSVs used by
the living manuscript (named 13 pages / blind 12 pages, Appendix A1–A5),
and a2b Python (no processed logs). Public benchmarks must be obtained
from the original providers (ASSISTments 2012, Junyi Academy, XES3G5M).

T-KT is a local Transformer reference used to stress-test the diagnostic
protocol. It is not published SimpleKT.

Rebuild reported tables from frozen summaries:
  scripts/rebuild_locked_tables.sh
That command does not retrain models.

Locked ASSISTments T-KT cells: ECE 0.1136 / 0.2280; FAR 0.196 / 0.268.
