# ADR-004: Apache Kafka + Transactional Outbox (Debezium CDC) + Avro/Schema Registry

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `SA`, `DATA`, `OPS`
- **İlgili:** [architecture-overview.md §6](../architecture-overview.md), [api-guidelines.md §10](../api-guidelines.md), [data-architecture.md §4](../data-architecture.md)

## Context and Problem Statement

Servisler durum değişikliklerini birbirine duyurmalı (ödeme → sadakat, bildirim, takas, uyum, raporlama, audit). Bir servisin
DB'sine yazıp ardından mesaj yayınlaması **dual-write** problemidir: DB commit olup mesaj kaybolabilir veya tersi —
finansal sistemde kabul edilemez. Mesajlaşma altyapısı ve güvenilir yayın deseni seçilmelidir.

## Decision Drivers

- Event kaybı = 0 (ör. `payment.captured` kaybolursa takas eksik olur)
- Yüksek throughput (~30k msg/s), sıralama (aggregate bazında), replay
- CDC → ClickHouse raporlama hattıyla ortak altyapı
- OpenShift üzerinde operator (Strimzi / AMQ Streams)
- Şema evrimi yönetimi

## Considered Options

1. **Kafka + Transactional Outbox + Debezium Outbox Event Router**
2. Kafka + uygulama içi outbox poller (polling publisher)
3. Kafka transactions (DB + Kafka dual-write, `chainedTransactionManager`)
4. RabbitMQ + outbox
5. Event sourcing (event store = source of truth)

## Decision Outcome

**Seçilen: Seçenek 1.**

- Servis iş verisi + `outbox_event` satırını **aynı DB transaction**'ında yazar (`platform-commons-outbox`).
- Debezium PostgreSQL connector (Kafka Connect, Strimzi `KafkaConnector` CR) WAL'dan outbox insert'lerini okur, **Outbox Event Router SMT** ile hedef topic'e (`aggregatetype` → topic), key = aggregate id, header = CloudEvents attribute'ları.
- `outbox_event` günlük partition, 7 gün sonra `DROP PARTITION` (DELETE yok).
- Tüketiciler **at-least-once** + `inbox_event` dedupe → effectively-once.
- Payload **Avro**, Confluent-uyumlu Schema Registry (Apicurio Registry — Red Hat ekosistemi — veya Confluent SR; Sprint 1 PoC), uyumluluk `BACKWARD_TRANSITIVE`.
- Kafka: Strimzi / AMQ Streams, KRaft, 3 AZ, RF=3, `min.insync.replicas=2`, producer `acks=all` + idempotent producer.
- Retry topic'leri (`.retry.1m`, `.retry.10m`) + DLQ; DLQ replay aracı operasyon konsolunda.
- `KafkaTemplate.send` doğrudan kullanımı ArchUnit ile yasak (outbox relay ve DLQ replay hariç).

### Consequences

- **Olumlu:** Atomik yayın garantisi; uygulama kodu Kafka erişilebilirliğinden bağımsız (Kafka kesintisinde yazma devam eder, event'ler birikir); aynı Debezium altyapısı raporlama CDC'sinde kullanılır; replay/yeniden işlem kolay.
- **Olumsuz:** Ek bileşen (Kafka Connect + Debezium) operasyonu; replication slot yönetimi (WAL birikmesi riski → `max_slot_wal_keep_size`, lag alarmı); uçtan uca gecikme (+50–200 ms); PG 16'da failover sonrası slot yeniden oluşturma (data-architecture §4.2).
- **Kabul edilen:** Tüketiciler sırasız/tekrarlı mesaja karşı dayanıklı yazılmalıdır.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Outbox + Debezium** | Atomik, polling yükü yok, düşük gecikme, WAL sıralı | Connect/slot operasyonu |
| Outbox + poller | Basit, ek bileşen yok | DB'ye polling yükü, sıralama/çoklu instance kilidi, gecikme |
| Kafka transactions | Tek API | DB ile gerçek atomiklik yok (best-effort 1PC), karmaşık hata durumları |
| RabbitMQ | Basit routing | Replay/retention yok, CDC hattı için ayrı Kafka gerekir, throughput |
| Event sourcing | Tam tarihçe | Ekip deneyimi, sorgu karmaşıklığı; ledger zaten append-only tarihçe sağlıyor |
