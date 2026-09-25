# ADR-009: CQRS ve ClickHouse ile Raporlama

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `DATA`, `PERF`
- **İlgili:** [data-architecture.md §4](../data-architecture.md), [service-catalog.md §16](../service-catalog.md)

## Context and Problem Statement

Tenant admin dashboard'ları, merchant raporları, finansal raporlar, kampanya simülasyonu ve uyum işlem izleme senaryoları
milyarlarca satır üzerinde agregasyon gerektirir. Bu sorguların OLTP veritabanlarında (özellikle ledger/payment) çalışması
ödeme gecikmesini bozar ve database-per-service nedeniyle servisler arası join mümkün değildir.

## Decision Drivers

- OLTP'yi (Tier-0) raporlama yükünden tamamen ayırmak
- Servisler arası birleşik görünüm (payment + loyalty + merchant)
- Saniye altı agregasyon, yüksek sıkıştırma, uygun maliyet
- Self-hosted (veri yerelliği), OpenShift üzerinde işletilebilir
- Veri tazeliği < 60 sn

## Considered Options

1. **CQRS: CDC/event → Kafka → ClickHouse**, reporting-service sorgu API'si
2. PostgreSQL read replica'ları üzerinde raporlama
3. Ayrı PostgreSQL raporlama DB'si (+ TimescaleDB / Citus)
4. Apache Druid / Apache Pinot
5. Bulut DWH (BigQuery, Snowflake)

## Decision Outcome

**Seçilen: Seçenek 1.**

- Kaynak: domain event'leri (outbox) + seçili tablo CDC'si (PII kolonları hariç).
- ClickHouse: Kafka engine → materialized view → `ReplicatedReplacingMergeTree` fact tabloları, `AggregatingMergeTree` özetler; `ORDER BY (tenant_id, ...)`, aylık partition, soğuk veri S3 tiered storage.
- Tenant izolasyonu: ClickHouse row policy + reporting-service'in zorunlu tenant predicate'i + kullanıcı başı quota.
- **Resmi finansal raporlar** (mizan, emanet/safeguarding, regülatör raporları) **ledger'dan** (read replica) üretilir; ClickHouse operasyonel/analitik raporlar içindir. Günlük karşılaştırma job'u farkları alarmlar.
- Servis-içi basit okuma modelleri (ör. müşteri işlem listesi) servisin kendi DB'sinde projection tabloları olarak kalabilir (CQRS "light").
- Operatör: Altinity ClickHouse Operator; 2 shard × 2 replica başlangıç, ClickHouse Keeper.

### Consequences

- **Olumlu:** OLTP korunur; çok hızlı agregasyon; kampanya simülasyonu/işlem izleme için güçlü motor; yüksek sıkıştırma (~10x).
- **Olumsuz:** Nihai tutarlılık (≤ 60 sn gecikme) — UI'da "veri X sn önce güncellendi" gösterimi; ClickHouse operasyon yetkinliği gerekir; `ReplacingMergeTree` tekrarları sorgu anında `FINAL`/`argMax` ile ele alınmalı; şema evrimi (event versiyonları) MV'lerde yönetilmeli.
- **Kural:** ClickHouse'ta PII yok; müşteri anahtarı tenant-salt'lı hash.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **ClickHouse (CQRS)** | Performans, maliyet, self-hosted, olgun Kafka entegrasyonu | Nihai tutarlılık, yeni teknoloji operasyonu |
| PG read replica | Basit | Cross-service join yok, analitik sorgular replica'yı yorar, replikasyon gecikmesi, satır bazlı depolama verimsiz |
| PG raporlama DB (+Timescale/Citus) | Tanıdık SQL | Milyar satır agregasyonda ClickHouse'tan belirgin yavaş, ölçek maliyeti |
| Druid / Pinot | Gerçek zamanlı OLAP | Operasyon karmaşıklığı daha yüksek, SQL/join desteği ClickHouse'a göre kısıtlı |
| Bulut DWH | Yönetilen | Veri yerelliği (TR), maliyet belirsizliği, gecikme |
