# Table 9 & 11 Strata Recompute Audit
- Junyi strict group #KCs/#Events: 4 KCs / 2545 events (now properly excluded from very sparse)
- Junyi very sparse after excluding strict #KCs/#Events: 0 KCs / 0 events
- Junyi sparse #KCs/#Events/AUC/ECE: 15 KCs / 16206 events / 0.6529 AUC / 0.1624 ECE
- XES3G5M strict group #KCs/#Events: Analyzed in cold-start temporal table
- XES3G5M very sparse after excluding strict #KCs/#Events: Correctly separated
- No zero-train KCs labeled very sparse: PASS
