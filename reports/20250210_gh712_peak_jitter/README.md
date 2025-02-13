# TEST GROUP `20250210_gh712_peak_jitter`

**Description:** Testing peak jitter calculation.

**Issue:**
[roc-streaming/roc-toolkit#712](https://github.com/roc-streaming/roc-toolkit/issues/712)

**Tests:**

| **Test** | **Description** |
|----|----|
| [`01--5ghz--no_load`](01--5ghz--no_load/README.md) | 5GHz Wi-Fi link, no external load. |
| [`02--5ghz--with_load`](02--5ghz--with_load/README.md) | 5GHz Wi-Fi link, simulated network load. |
| [`03--5+2ghz--no_load`](03--5+2ghz--no_load/README.md) | 5Ghz and 2.5Ghz Wi-Fi SSIDs (same AP), no external load. |
| [`04--5+2ghz--with_load`](04--5+2ghz--with_load/README.md) | 5Ghz and 2.5Ghz Wi-Fi SSIDs (same AP), simulated network load. |
| [`05--2ghz--no_load--low_res`](05--2ghz--no_load--low_res/README.md) | 2.5GHz Wi-Fi link, no external load. Low-resolution dump. |
| [`06--2ghz--with_load--low_res`](06--2ghz--with_load--low_res/README.md) | 2.5GHz Wi-Fi link, simulated network load. Low-resolution dump. |
| [`07--ether--spikes`](07--ether--spikes/README.md) | Ethernet, short simulated load spikes. |
