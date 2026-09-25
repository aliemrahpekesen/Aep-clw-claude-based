# ADR-011: Monorepo Yapısı (Gradle Multi-Module Backend + pnpm Workspace Frontend)

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, Backend Tech Lead, Frontend Tech Lead, `OPS`

## Context and Problem Statement

19 backend servisi, ortak `platform-commons` kütüphaneleri, OpenAPI/AsyncAPI sözleşmeleri, 4 frontend uygulaması ve ortak
frontend paketleri, Helm chart'ları ve dokümantasyon tek bir repo'da (`aliemrahpekesen/aep-clw-claude-based`) mı yoksa
çoklu repo'da mı yönetilmeli?

## Decision Drivers

- Sözleşme (OpenAPI) → sunucu + istemci kodunun **atomik** değişimi
- `platform-commons` değişikliklerinin tüm servislerde anında doğrulanması
- Küçük-orta ekip, trunk-based geliştirme
- CI süresinin yönetilebilir kalması (etkilenen modül tespiti)
- Tek issue tracker (GitHub Issues) ile izlenebilirlik

## Considered Options

1. **Monorepo**: Gradle multi-module (backend) + pnpm workspace (frontend) + `api/` + `deploy/` + `docs/`
2. Polyrepo (servis başına repo)
3. Hibrit: backend monorepo + ayrı frontend repo + ayrı GitOps repo

## Decision Outcome

**Seçilen: Seçenek 1 (GitOps ortam durumu için istisna notu ile).**

```text
aep-clw-claude-based/
├── api/                          # OpenAPI 3.1 + AsyncAPI 3.0 sözleşmeleri (source of truth)
│   ├── common/                   # Money, Problem, PageInfo, header bileşenleri
│   └── <service>/{openapi.yaml, asyncapi.yaml}
├── backend/
│   ├── settings.gradle.kts       # tüm modüller
│   ├── build-logic/              # convention plugin'ler (java, spring-service, testing, quality)
│   ├── platform/
│   │   ├── platform-bom/
│   │   ├── platform-commons-tenant/ ... -money/ -outbox/ -idempotency/ -audit/ -error/ -saga/ -security/ -observability/ -resilience/ -test/
│   │   └── keycloak-spi/         # custom authenticator (OTP, device binding)
│   └── services/
│       ├── api-gateway/ identity-service/ tenant-service/ customer-service/ wallet-service/ ledger-service/
│       ├── payment-service/ funding-service/ merchant-service/ loyalty-service/ voucher-service/ risk-service/
│       ├── compliance-service/ settlement-service/ accounting-service/ reporting-service/ audit-service/
│       └── notification-service/ mobile-bff/ pos-bff/ admin-bff/
├── frontend/
│   ├── pnpm-workspace.yaml
│   ├── apps/{tenant-admin, platform-console, web-pos, mobile}
│   └── packages/{design-system, design-tokens, api-client, i18n, validation, eslint-config, tsconfig}
├── sdks/                         # POS SDK'ları (java, dotnet, js, kotlin) — OpenAPI'den üretim + yardımcılar
├── deploy/
│   ├── charts/clw-service/       # ortak Helm library chart
│   └── services/<service>/values.yaml
├── infra/                        # operatör CR şablonları (CNPG, Strimzi, ClickHouse), Vault policy'leri
├── tests/                        # e2e (Playwright), performans (Gatling/k6), contract broker konfig
├── docs/
└── .github/workflows/
```

- **Gradle**: Kotlin DSL, version catalog (`libs.versions.toml`), convention plugin'ler, **configuration cache + build cache** (remote cache), `dependency-analysis` plugin'i; etkilenen modül tespiti ile CI'da yalnız değişenler + bağımlıları build/test edilir.
- **pnpm workspace** + Turborepo (veya Nx) görev önbelleği; `api-client` paketi `api/` değişince yeniden üretilir.
- **CODEOWNERS**: servis/paket bazında sahiplik; `api/` ve `platform/` değişiklikleri `CA` review zorunlu.
- Servis başına bağımsız versiyon/imaj (`ghcr.io/.../<service>:<git-sha>`); monorepo ≠ monolitik release.
- **İstisna — GitOps ortam durumu:** ortam overlay'leri (image tag'leri, ortam değerleri) ayrı `aep-clw-gitops` repo'sunda tutulabilir (ADR-008); böylece CI → PR otomasyonu uygulama kod geçmişini kirletmez ve prod erişim yetkileri ayrılır. Sprint 0 kararı: **başlangıçta monorepo `deploy/envs/`**, prod ortamı açılmadan önce ayrı repo'ya taşıma değerlendirilecek.

### Consequences

- **Olumlu:** Atomik sözleşme değişiklikleri; `platform-commons` kırılmaları anında görünür; tek PR'da uçtan uca özellik; ortak araç ve kalite kapıları; tek issue/PR izlenebilirliği (sprint audit matrisi için kolay).
- **Olumsuz:** CI süresi riski (etkilenen modül analizi + remote cache şart); repo boyutu büyür; erişim kontrolü klasör bazında yalnız CODEOWNERS ile (repo seviyesi ayrım yok).
- **Kural:** Servisler arası **derleme zamanı bağımlılığı yasak** (servis A, servis B modülünü import edemez) — yalnız `platform-*` ve `api/`'den üretilen client'lar. Gradle + ArchUnit ile zorlanır.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Monorepo** | Atomik değişim, tutarlı araçlar, görünürlük | CI optimizasyonu gerekir |
| Polyrepo | Bağımsızlık, küçük repolar | 25+ repo; commons sürüm cehennemi, sözleşme senkronizasyonu zor, küçük ekip için ağır |
| Hibrit | Orta yol | Sözleşme ↔ FE client atomikliği kaybolur |
