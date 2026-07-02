# BKT Training Config Audit

- Config location: `configs/bkt_debug.yaml` (and defaults in code).
- Training: BKT is trained per KC (skill).
- Smoothing prior: Originally NO smoothing prior. Adding one causes parameter saturation anyway due to a bug in the M-step of pyBKT 1.4.1.
- Probability clipping: Not explicitly implemented before NLL computation, leading to large NLL.
