# TEST GROUP `20250210_gh712_peak_jitter`

**Description:** Testing peak jitter calculation.

**Issue:**
[roc-streaming/roc-toolkit#712](https://github.com/roc-streaming/roc-toolkit/issues/712)

**Tests:**

| **Test** | **Description** |
|----|----|
| [`01--5ghz--no_load`](01--5ghz--no_load/report.md) | 5GHz Wi-Fi link, no external load. |
| [`02--5ghz--with_load`](02--5ghz--with_load/report.md) | 5GHz Wi-Fi link, simulated network load. |
| [`03--5+2ghz--no_load`](03--5+2ghz--no_load/report.md) | 5Ghz and 2Ghz Wi-Fi SSIDs (same AP), no external load. |
| [`04--2ghz--no_load`](04--2ghz--no_load/report.md) | 2GHz Wi-Fi link, no external load. |
| [`05--2ghz--with_load`](05--2ghz--with_load/report.md) | 2GHz Wi-Fi link, simulated network load. |
| [`06--ether--spikes`](06--ether--spikes/report.md) | Ethernet, short simulated load spikes. |
