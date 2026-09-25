# Architecture Decision Records (ADR) — İndeks

Format: [MADR](https://adr.github.io/madr/) (Context → Decision Drivers → Considered Options → Decision Outcome → Consequences → Pros/Cons).
Onay sahibi: Chief Architect (`CA`). Durumlar: `Proposed` → `Accepted` → (`Deprecated` | `Superseded by ADR-XXX`).

| # | Başlık | Durum | Etkilenen dokümanlar |
|---|---|---|---|
| [ADR-001](ADR-001-microservices-ddd.md) | Mikroservis mimarisi + DDD (Hexagonal) | Proposed | overview, domain-model, service-catalog |
| [ADR-002](ADR-002-java21-spring-boot3.md) | Java 21 (LTS) ve Spring Boot 3.x | Proposed | overview |
| [ADR-003](ADR-003-postgresql-database-per-service-rls.md) | PostgreSQL 16, database-per-service, RLS ile multitenancy, tenant tiering | Proposed | multitenancy, data-architecture |
| [ADR-004](ADR-004-kafka-transactional-outbox.md) | Kafka + Transactional Outbox (Debezium) + Avro/Schema Registry | Proposed | overview, api-guidelines, data-architecture |
| [ADR-005](ADR-005-saga-orchestration.md) | Saga orchestration + idempotency + compensation | Proposed | flows |
| [ADR-006](ADR-006-double-entry-ledger-service.md) | Çift kayıtlı ledger servisi | Proposed | ledger-design |
| [ADR-007](ADR-007-keycloak-identity.md) | Keycloak ile kimlik (Organizations = tenant) | Proposed | multitenancy, service-catalog |
| [ADR-008](ADR-008-openshift-gitops-argocd.md) | OpenShift + Helm + GitOps (ArgoCD) | Proposed | overview |
| [ADR-009](ADR-009-cqrs-clickhouse-reporting.md) | CQRS ve ClickHouse raporlama | Proposed | data-architecture |
| [ADR-010](ADR-010-react-react-native-frontend.md) | React + TS (web), React Native Expo (mobil, white-label) | Proposed | overview, multitenancy |
| [ADR-011](ADR-011-monorepo-structure.md) | Monorepo (Gradle multi-module + pnpm workspace) | Proposed | — |
| [ADR-012](ADR-012-no-card-data-storage-psp-tokenization.md) | Kart verisini saklamama, PSP tokenization, PCI kapsam daraltma | Proposed | integration-architecture, flows |

## Süreç

1. Yeni ADR: sıradaki numara, `ADR-NNN-kisa-baslik.md`, durum `Proposed`, PR açılır.
2. Review: `CA` + etkilenen rol(ler) (`SA`, `SEC`, `DATA`, `CMP`, `OPS`). Güvenlik/uyum etkisi olan ADR'lerde `SEC`/`CMP` onayı zorunlu.
3. Sprint Review'da onay → durum `Accepted`, bu indeks güncellenir.
4. Kabul edilmiş bir ADR **değiştirilmez**; yeni ADR ile `Superseded` edilir.

## Önerilen sonraki ADR'ler (backlog)

| Konu | Tetikleyici |
|---|---|
| Schema Registry seçimi (Apicurio vs. Confluent) | Sprint 1 PoC |
| PostgreSQL operatörü nihai seçimi (CNPG vs. Crunchy PGO) | Sprint 1 PoC |
| Servisler arası iletişimde gRPC (payment → ledger sıcak yol) | Walking skeleton gecikme ölçümü |
| Risk skorlamada ML modeli (ONNX in-process) | v2 |
| Network tokenization (VTS/MDES) | PSP failover ihtiyacı |
| Active-active multi-region | v2, trafik ve maliyet analizi |
| KYC / AML sağlayıcı seçimi | Sprint 1 RFP |
