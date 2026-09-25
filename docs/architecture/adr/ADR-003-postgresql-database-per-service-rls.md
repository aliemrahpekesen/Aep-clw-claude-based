# ADR-003: PostgreSQL 16, Database-per-Service ve RLS ile Multitenancy (Tenant Tiering)

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `DATA`, `SEC`, `CMP`
- **İlgili:** [multitenancy.md](../multitenancy.md), [data-architecture.md](../data-architecture.md)

## Context and Problem Statement

Platform çok sayıda tenant'a (küçük kafe zincirinden büyük EV şarj operatörüne) hizmet verecek. Finansal veriler ACID,
denetlenebilir ve tenant'lar arası kesin izolasyonlu olmalı. Bazı büyük/regüle tenant'lar sözleşmesel olarak fiziksel
izolasyon talep edecek. Hangi veritabanı ve hangi izolasyon modeli?

## Decision Drivers

- ACID, güçlü tutarlılık (ledger), olgun replikasyon/PITR
- Tenant izolasyonunun **uygulama hatasına karşı dayanıklı** olması (defense in depth)
- Maliyet: binlerce küçük tenant için tenant başına DB ekonomik değil
- Büyük tenant'lar için performans ve restore izolasyonu
- OpenShift üzerinde operator desteği

## Considered Options

- **DB motoru:** PostgreSQL 16 · MySQL 8 · CockroachDB/YugabyteDB (dağıtık SQL) · Oracle
- **Servis-veri ilişkisi:** Database-per-service · Shared database
- **Tenant izolasyonu:** (a) yalnız `tenant_id` kolonu + uygulama filtresi · (b) `tenant_id` + **RLS** · (c) schema-per-tenant · (d) DB-per-tenant · (e) **hibrit tiering** (b varsayılan, büyükler için d)

## Decision Outcome

**Seçilen:** PostgreSQL 16 + **database-per-service** + **hibrit tenant tiering**:

| Tier | Model |
|---|---|
| POOL (varsayılan) | Paylaşımlı servis DB'si, `tenant_id` + **RLS (ENABLE + FORCE)** |
| BRIDGE | Aynı cluster'da tenant'a özel database (RLS yine aktif) |
| SILO | Tenant'a özel PostgreSQL cluster |

Kurallar:
- Uygulama rolü tablo sahibi değildir; `SET LOCAL app.tenant_id` transaction başına; tenant yoksa fonksiyon **hata fırlatır**.
- CI'da RLS kapsam testi (tenant_id'li her tabloda RLS FORCE zorunlu) ve cross-tenant okuma testleri.
- Routing: `tenant-service` placement map + `TenantRoutingDataSource`.
- Operatör: CloudNativePG (birincil), pgBackRest; Crunchy PGO alternatif (data-architecture §8.1).
- Flyway migration'ları ayrı Job + owner rolü.

### Consequences

- **Olumlu:** Tek kod yolu tüm tier'larda; RLS ile uygulama hatası bile veri sızdıramaz; küçük tenant maliyeti düşük; büyük tenant'lara izolasyon/performans satılabilir (fiyatlandırma); servis DB'leri bağımsız ölçeklenir/yedeklenir.
- **Olumsuz:** RLS predicate'lerinin plan maliyeti (index'ler `tenant_id` ile başlamalı); POOL'da tenant bazlı PITR zor (yeni cluster'a restore + çıkarım); BRIDGE/SILO'da migration orkestrasyonu karmaşık (placement map bazlı çoklu hedef); çok sayıda DB bağlantı havuzu (PgBouncer zorunlu).
- **Risk:** `BYPASSRLS` rolünün kötüye kullanımı → yalnız break-glass, Vault TTL 15 dk, audit.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| Yalnız `tenant_id` + app filtresi | Basit | Tek unutulan `WHERE` = veri sızıntısı |
| **`tenant_id` + RLS** | DB seviyesinde zorlama, ekonomik | Plan maliyeti, dikkatli rol yönetimi |
| Schema-per-tenant | Mantıksal ayrım | Binlerce şema → katalog şişmesi, migration maliyeti, bağlantı başına `search_path` |
| DB-per-tenant (herkes) | Tam izolasyon | Küçük tenant'lar için maliyet/operasyon kabul edilemez |
| **Hibrit tiering** | Maliyet + izolasyon dengesi, gelir modeli | Routing karmaşıklığı |
| CockroachDB/Yugabyte | Yatay ölçek, multi-region yazma | Operasyonel olgunluk/ekip deneyimi, `SELECT FOR UPDATE` ve gecikme davranışı, lisans; PG shard'lama ihtiyacımızı karşılıyor |
| MySQL | Yaygın | RLS yok, jsonb/partition/CDC ekosistemi PG kadar güçlü değil |
