# Kalite (Quality) — Doküman İndeksi

Sahip: `QA` (QA Lead) + `PERF` (Performance Engineer) · Bağlam: [Proje Tüzüğü](../00-project-charter.md)

| Doküman | İçerik |
|---|---|
| [test-strategy.md](test-strategy.md) | Test piramidi; unit, ArchUnit, Testcontainers, Pact, REST Assured, Playwright, Maestro/Detox, Gatling/k6, LitmusChaos, güvenlik, erişilebilirlik (WCAG 2.2 AA); ledger invariant property testleri (jqwik), çifte harcama eşzamanlılık testleri, PIT mutation; test verisi, ortamlar, kalite kapıları, severity tanımları, UAT |
| [performance-plan.md](performance-plan.md) | NFR hedefleri (5.000 TPS, p99 < 300 ms, 1M cüzdan/tenant, 500 tenant), load/stress/soak 24h/spike (kahve zinciri sabah piki), kapasite modeli, darboğaz hipotezleri (hot account), ölçüm |
| [definition-of-done.md](definition-of-done.md) | Story DoR, Story/Sprint/Release DoD (kalite, güvenlik, uyum detayları) |

İlgili: [Güvenlik](../security/README.md) · [Uyum](../compliance/README.md) · [DevOps](../devops/README.md)
