# AEP-CLW — Closed-Loop Wallet SaaS Platformu

Kahve zincirleri, EV şarj ağları, otoparklar, eğlence parkları ve kampüsler için **multitenant, white-label,
kapalı devre dijital cüzdan** platformu: ön ödemeli bakiye, QR/NFC ödeme, pre-auth (provizyon), sadakat ve
kampanya, hediye kartı; çift kayıtlı defter, risk & uyum, takas & mutabakat, muhasebe ve teftiş.

> **Durum:** Sprint 0 (Inception) — plan, mimari, backlog ve prototip **onay bekliyor**. Kodlama onaydan sonra başlar.

## Teknoloji
Java 21 · Spring Boot 3 · Spring Cloud Gateway · PostgreSQL 16 · Kafka (Strimzi) · Redis · Keycloak · Vault ·
React + TypeScript · React Native (Expo) · Docker · OpenShift · Helm · ArgoCD · GitHub Actions · OpenTelemetry

## Dokümantasyon haritası
| Alan | Doküman |
|---|---|
| Proje tüzüğü, ekip, kararlar | [docs/00-project-charter.md](docs/00-project-charter.md) |
| Ürün: vizyon, gereksinimler, MVP, yol haritası, fonksiyon matrisi | [docs/product/](docs/product/) |
| Backlog (milestone → epic → story) | [docs/backlog.md](docs/backlog.md) · GitHub Issues |
| Mimari: C4, servis kataloğu, multitenancy, ledger, akışlar, ADR | [docs/architecture/](docs/architecture/) |
| Güvenlik: mimari, tehdit modeli, secure SDLC | [docs/security/](docs/security/) |
| Uyum: regülasyon, AML/KYC, denetim, **kontrol (audit) matrisi** | [docs/compliance/](docs/compliance/) |
| Kalite: test stratejisi, performans, DoD | [docs/quality/](docs/quality/) |
| DevOps: CI/CD, OpenShift, gözlemlenebilirlik, DR | [docs/devops/](docs/devops/) |
| Yönetişim: sprint review süreci ve şablonlar | [docs/governance/](docs/governance/) |
| Sprint paketleri (review, ilerleme raporu) | [docs/sprints/](docs/sprints/) |
| Tıklanabilir prototip | [prototype/index.html](prototype/index.html) |

## Backlog-as-code
Backlog'un tek kaynağı `tools/backlog/backlog_source.py`'dir:

```bash
python3 tools/backlog/backlog_source.py   # .github/project/backlog.json + docs/backlog.md üretir
```

`backlog.json` değiştiğinde `.github/workflows/backlog-sync.yml` label, milestone, epic ve story issue'larını
(sub-issue hiyerarşisiyle) idempotent şekilde GitHub'a senkronize eder.

## Planlanan repo yapısı (kodlama fazı)
```
backend/            Gradle multi-module: platform-commons + 18 mikroservis + BFF'ler
frontend/           pnpm workspace: tenant-admin, platform-admin, web-pos, design-system
mobile/             React Native (Expo) white-label müşteri uygulaması
deploy/             Helm charts, ArgoCD app-of-apps, OpenShift manifestleri
local/              docker-compose yerel geliştirme ortamı
docs/               Tüm dokümantasyon
```
