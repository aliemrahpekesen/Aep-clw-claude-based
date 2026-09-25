# AEP-CLW — Mimari Dokümantasyon

Bu klasör AEP-CLW (Closed-Loop Wallet) platformunun hedef mimarisini içerir. Kaynak kararlar
[Proje Tüzüğü](../00-project-charter.md)'nde, gerekçeli kararlar [ADR'ler](adr/README.md)'de bulunur.
Durum: **Sprint 0 — Taslak / Onay bekliyor**. Kodlama bu dokümanlar onaylandıktan sonra başlar.

## Okuma Sırası

| # | Doküman | İçerik | Birincil okuyucu |
|---|---|---|---|
| 1 | [architecture-overview.md](architecture-overview.md) | Mimari ilkeler, C4 Context/Container, katmanlar, kanal → BFF → servis akışı, senkron/asenkron kuralları, ölçeklenebilirlik (5.000 TPS, p99 < 300 ms, %99,95, RPO ≤ 1 dk, RTO ≤ 15 dk), multi-region/DR, hexagonal paket yapısı, `platform-commons` | Herkes |
| 2 | [domain-model.md](domain-model.md) | Subdomain'ler, DDD context map, ubiquitous language (TR/EN), aggregate'ler ve invariant'lar | BA, BE, PO |
| 3 | [service-catalog.md](service-catalog.md) | 19 servisin sorumluluğu, aggregate'leri, API uçları, event'leri, veri deposu, bağımlılıkları, ölçekleme ve SLO | BE, OPS, QA |
| 4 | [multitenancy.md](multitenancy.md) | Tenant çözümleme, POOL/BRIDGE/SILO tiering, RLS SQL, Kafka/cache tenant kuralları, tenant config JSON Schema, sektör presetleri, noisy-neighbor, onboarding | BE, DATA, PO |
| 5 | [ledger-design.md](ledger-design.md) | Çift kayıtlı defter: hesap tipleri, DDL, bakiye modeli, idempotency, eşzamanlılık, hot-account sharding, posting senaryoları | SA, BE, DATA, AUD, CMP |
| 6 | [flows.md](flows.md) | Sequence diyagramları: kayıt+OTP, kartla yükleme (3DS/saga), QR ödeme, EV pre-auth, iade, P2P, takas & mutabakat, cashback, fraud | BE, QA, BA |
| 7 | [data-architecture.md](data-architecture.md) | Servis DB'leri, ER özetleri, CDC → Kafka → ClickHouse, saklama/arşiv (10 yıl), KVKK crypto-shredding, partitioning, backup/PITR | DATA, SEC, CMP |
| 8 | [integration-architecture.md](integration-architecture.md) | PSP, banka, açık bankacılık, KYC, AML, SMS/push, e-Fatura, ERP, POS API/SDK/webhook, ACL, Resilience4j, webhook güvenliği | SA, BE, SEC |
| 9 | [api-guidelines.md](api-guidelines.md) | REST standartları, versiyonlama, cursor pagination, Idempotency-Key, RFC 7807, correlation-id, formatlar, OpenAPI-first, CloudEvents/AsyncAPI, event versiyonlama | BE, FE, MOB |
| 10 | [adr/](adr/README.md) | ADR-001 … ADR-012 | CA, tüm leadler |

## Temel Kararlar — Tek Bakışta

| Konu | Karar |
|---|---|
| Stil | Mikroservis + DDD + Hexagonal; 19 servis; senkron grafik DAG, derinlik ≤ 3 |
| Para gerçeği | `ledger-service` çift kayıtlı, append-only; hold ledger'da temsil edilir; minor units `bigint` |
| Multitenancy | `tenant_id` + RLS (FORCE) varsayılan; BRIDGE (tenant DB) / SILO (tenant cluster) tiering |
| Tutarlılık | Transactional Outbox + Debezium; saga orchestration; deterministik idempotency key'ler |
| Okuma | CQRS; ClickHouse (analitik), resmi finansal raporlar ledger'dan |
| Kimlik | Keycloak, realm-per-population, Organizations = tenant, DPoP + cihaz bağlama |
| Kart verisi | Tutulmaz — PSP tokenization, SAQ A hedefi |
| Platform | OpenShift + Helm + ArgoCD (pull-based GitOps), Service Mesh mTLS, Vault |
| DR | Active–warm standby, bölge içi sync replika (RPO 0), bölgeler arası async (RPO ≤ 1 dk), RTO ≤ 15 dk |

## Açık Maddeler (Sprint 1'e devreden)

| # | Konu | Sahip |
|---|---|---|
| 1 | Promosyon fonlaması ve breakage muhasebe politikası (ledger-design §12.2) | `SA` + `CMP` |
| 2 | Regülasyon limit tavanlarının güncel değerleri (6493 / ilgili yönetmelik) | `CMP` |
| 3 | Veri saklama sürelerinin hukuki onayı (data-architecture §5) | `CMP` |
| 4 | PostgreSQL operatörü ve Schema Registry PoC | `DATA`, `OPS` |
| 5 | KYC / AML sağlayıcı RFP | `CMP`, `SA` |
| 6 | Walking skeleton ile p99 gecikme bütçesi doğrulaması | `PERF`, `BE` |

## Dokümantasyon Kuralları

- Diyagramlar **Mermaid** (GitHub'da doğrudan render); C4 için `C4Context` veya `flowchart`.
- Her doküman başında sahip / durum tablosu; değişiklikler PR ile, `CA` onaylı.
- Terimler [domain-model.md §3](domain-model.md) sözlüğüne uymalı.
