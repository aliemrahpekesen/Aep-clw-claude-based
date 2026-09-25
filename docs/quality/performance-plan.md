# AEP-CLW — Performans ve Kapasite Planı

| Alan | Değer |
|---|---|
| Doküman sahibi | `PERF` (Performance Engineer) |
| Katkı | `SA`, `OPS`, `DATA`, `BE`, `QA` |
| Sürüm | v1.0 — Sprint 0 |
| Araçlar | Gatling (Java DSL) — ana yük; k6 — CI smoke ve hafif senaryolar; Prometheus/Grafana/Tempo — ölçüm |
| İlgili kontrol | CTL-047 (kapasite yönetimi), CTL-032 (çifte harcama — yük altında) |

---

## 1. NFR Hedefleri

| ID | Metrik | Hedef | Kapsam / Not |
|---|---|---|---|
| NFR-P1 | Ödeme throughput | **5.000 TPS** sürdürülebilir (platform geneli), 7.500 TPS pik (15 dk) | authorize+capture (tek adım) QR ödeme |
| NFR-P2 | Ödeme gecikmesi | **p99 < 300 ms**, p95 < 150 ms, p50 < 60 ms | Gateway giriş → yanıt (edge hariç), sunucu tarafı |
| NFR-P3 | Yükleme (top-up) gecikmesi | p99 < 800 ms (PSP hariç iç süre); PSP dahil p95 < 3 sn | PSP sandbox/stub ile ayrıştırılmış ölçüm |
| NFR-P4 | Bakiye sorgusu | p99 < 100 ms, 15.000 RPS | Okuma yolu (cache/replica) |
| NFR-P5 | Cüzdan ölçeği | **1M aktif cüzdan / tenant** (büyük tenant), toplam 50M+ cüzdan | Aktif = son 90 günde işlem |
| NFR-P6 | Tenant ölçeği | **500 tenant** | Karma tier: ~20 büyük (dedicated DB), ~480 paylaşımlı |
| NFR-P7 | Hata oranı | < %0,1 (5xx + timeout) yük altında | İş reddi (yetersiz bakiye) hariç |
| NFR-P8 | Tek tenant hot spot | Tek tenant 1.500 TPS (kahve zinciri sabah piki) diğer tenant'ların p99'unu > %10 bozmaz | Noisy neighbor izolasyonu |
| NFR-P9 | Tek işyeri hot account | Tek işyeri alacak hesabına 500 TPS | Hot account |
| NFR-P10 | Event gecikmesi | Ledger → Kafka → reporting read model p99 < 5 sn; audit event < 10 sn | CDC/Outbox |
| NFR-P11 | Soak kararlılığı | 24 saat boyunca bellek sızıntısı yok, p99 sapması < %10, GC pause p99 < 50 ms | — |
| NFR-P12 | Ölçeklenme | Spike'ta 2 dk içinde otomatik ölçeklenme, kuyruk birikmeden | HPA/KEDA |
| NFR-P13 | Finansal tutarlılık | Tüm yük testleri sonunda ledger dengesizliği = 0, çifte harcama = 0 | Zorunlu kabul kriteri |

---

## 2. Test Senaryoları

### 2.1 İş Yükü Modeli (Workload Mix — tepe saat)

| İşlem | Oran | 5.000 TPS'de | Not |
|---|---|---|---|
| QR ödeme (authorize+capture) | %55 | 2.750 | Kahve, otopark çıkış, kantin |
| Bakiye/işlem geçmişi sorgusu | %25 (ayrı RPS bütçesi) | — | Okuma yolu |
| Pre-auth hold (EV şarj, otopark giriş) | %6 | 300 | |
| Hold capture/release | %6 | 300 | |
| Top-up (kayıtlı kart, otomatik yükleme) | %5 | 250 | PSP stub |
| İade / iptal | %1 | 50 | |
| Sadakat puan/kampanya değerlendirme (senkron) | ödeme içinde | — | Ödeme yolunda kural değerlendirmesi |
| Kayıt / KYC / diğer | %2 | 100 | |

### 2.2 Senaryo Kataloğu

| ID | Tür | Profil | Süre | Başarı Kriteri | Sıklık / Ortam |
|---|---|---|---|---|---|
| PT-01 | **Smoke** (k6) | 50 TPS | 5 dk | Hata < %0,1, p99 < 300 ms | Her deploy — test |
| PT-02 | **Load (baseline)** | Rampa 0 → 5.000 TPS (10 dk), 5.000 TPS sabit | 60 dk | NFR-P1, P2, P7 | Haftalık + release — preprod |
| PT-03 | **Stress** | 5.000 → +500 TPS/5 dk adımlarla kırılma noktasına kadar | ~90 dk | Kırılma noktası ≥ 1,5× hedef (7.500 TPS); zarif bozulma (429/backpressure, kaskad yok), yük kalkınca 5 dk içinde toparlanma | Release — preprod |
| PT-04 | **Soak** | 3.000 TPS (%60) sabit + gerçekçi günlük dalga | **24 saat** | NFR-P11; bağlantı havuzu, Kafka lag, disk büyümesi stabil | Aylık + major release — preprod |
| PT-05 | **Spike — kahve zinciri sabah piki** | `tenant-alpha` 300 TPS → **1.500 TPS 60 sn içinde**, 07:30–09:30 profili (2 tepe), diğer tenant'lar 2.000 TPS arka plan | 2 saat (sıkıştırılmış 30 dk) | NFR-P8, P12; işyeri hot account p99 < 300 ms | Release — preprod |
| PT-06 | **Hot account** | Tek işyeri (tek mağaza, 20 kasa) 500 TPS | 30 dk | NFR-P9, lock bekleme p99 < 20 ms | Ledger değişikliği sonrası |
| PT-07 | **Double-spend under load** | 1.000 cüzdan × 20 eşzamanlı ödeme (bakiye yalnızca 5'ine yeter), 3.000 TPS arka plan | 20 dk | Başarılı ≤ 5/cüzdan, negatif bakiye 0, dengesizlik 0 | Release — preprod |
| PT-08 | **Scale-out (tenant)** | 500 tenant simülasyonu, Zipf dağılımı | 60 dk | Tenant başına p99 hedefte, DB bağlantı sayısı limit altında | Çeyreklik |
| PT-09 | **Failover under load** | PT-02 + DB primary failover / Kafka broker kaybı / AZ kaybı (Litmus) | 60 dk | Hata oranı failover penceresinde < %1, RTO içinde toparlanma, veri kaybı yok | Çeyreklik — preprod |
| PT-10 | **Batch window** | Gece takas + GL export + breakage (1M cüzdan × 500 tenant) + arka plan 500 TPS | Batch süresi | Batch < 2 saat, online p99 etkilenmez | Aylık |
| PT-11 | **Reporting** | Dashboard sorguları 200 eşzamanlı kullanıcı, ClickHouse | 30 dk | p95 < 2 sn | Aylık |

---

## 3. Kapasite Modeli

### 3.1 Varsayımlar

- 500 tenant, toplam ~50M kayıtlı cüzdan, ~15M aktif; günlük işlem ~60M (ortalama ~700 TPS, tepe/ortalama oranı ~7).
- Ödeme başına ~6 ledger posting satırı (müşteri debit, işyeri credit, ücret, sadakat puanı, bonus kullanımı, vergi/komisyon ayrımı — ortalama).
- Event başına ~1,5 KB (Avro), ödeme başına ~5 event (payment, ledger, loyalty, audit, notification).

### 3.2 Türetilen Kapasite (5.000 TPS ödeme için ilk tahmin — PT-02 ile doğrulanacak)

| Bileşen | Hesap | İlk Boyut |
|---|---|---|
| payment-service | ~600 TPS/pod (virtual threads, 2 vCPU) → 5.000/600 ≈ 9 + %50 headroom | 14 pod (HPA min 6, max 30) |
| wallet-service | ~800 TPS/pod | 10 pod |
| ledger-service | ~400 TPS/pod (yazma ağır) | 16 pod |
| risk-service (senkron) | < 30 ms p99, ~1.000 TPS/pod | 8 pod |
| api-gateway | ~2.500 RPS/pod (reactive) | 6 pod + HPA |
| PostgreSQL (ledger, paylaşımlı cluster) | 5.000 × 6 = 30.000 satır insert/sn + güncellemeler; WAL ~40 MB/sn | 4 shard (tenant hash) × (32 vCPU, 128 GB, NVMe) + senkron standby + async replica |
| PostgreSQL (dedicated tenant) | 1.500 TPS tepe | 16 vCPU, 64 GB |
| Kafka | 5.000 × 5 event × 1,5 KB ≈ 37,5 MB/sn giriş, RF=3 → ~112 MB/sn yazma | 6 broker (8 vCPU, 32 GB, NVMe), 3 AZ; kritik topic'lerde partition = 48 |
| Redis | Idempotency, QR counter, rate limit ~40.000 op/sn | Redis Cluster 3 primary + 3 replica |
| ClickHouse | 60M satır/gün × ~6 | 3 shard × 2 replica |
| Depolama büyümesi | Ledger ~60M × 6 × ~300 B ≈ 110 GB/gün (indeksli ~200 GB) | Aylık partition, 13 ay sıcak, sonrası arşiv (WORM) |

### 3.3 Ölçek Kolları

1. Yatay ölçekleme (stateless servisler — HPA/KEDA).
2. Tenant tiering: büyük tenant → dedicated DB (tüzük kararı).
3. Ledger sharding (tenant_id hash) + tablo partitioning (zaman).
4. Okuma yolunu ayırma (CQRS, replica, Redis cache — bakiye için yazma-sonrası invalidasyon).
5. Hot account stratejileri (§4.1).

---

## 4. Darboğaz Hipotezleri

| ID | Hipotez | Belirti | Doğrulama | Öneri / Önlem |
|---|---|---|---|---|
| H-1 | **Hot account** — işyeri alacak hesabı ve tenant gelir/ücret hesaplarında satır kilidi çekişmesi | Lock wait artışı, p99 sıçraması, PT-05/06'da tail latency | `pg_stat_activity` wait events, `pg_locks`, Tempo span'leri | (a) İşyeri/sistem hesapları için **N adet alt hesap (sharded sub-accounts)**, okuma sırasında toplama; (b) sistem hesaplarına **batched/async posting** (müşteri debit'i senkron, karşı bacak kısa pencereli batch — invariant journal düzeyinde korunur); (c) müşteri hesabında satır kilidi zaten doğal olarak dağıtık |
| H-2 | DB bağlantı havuzu tükenmesi (500 tenant × servis × pod) | `HikariPool` bekleme, 5xx | Hikari metrikleri | PgBouncer (transaction mode), havuz boyutu = çekirdek×2, tenant başına bağlantı değil paylaşımlı havuz + RLS `SET LOCAL` |
| H-3 | RLS politika maliyeti | Plan süresinde artış | `EXPLAIN ANALYZE`, `pg_stat_statements` | `tenant_id` öncelikli bileşik indeksler, basit RLS ifadesi, partition pruning |
| H-4 | Outbox → Debezium gecikmesi | Kafka lag, read model gecikmesi | Debezium metrikleri | Outbox tablosu partitioning, connector paralelliği, heartbeat |
| H-5 | Senkron risk/loyalty değerlendirmesinin ödeme yoluna eklediği gecikme | Ödeme p99'unun büyük kısmı bu span'lerde | Tempo kritik yol analizi | Kural önbelleği, bütçe (30 ms) + timeout → fail-open/closed politikası (tutar bazlı), sadakat puanı asenkron |
| H-6 | Redis tek anahtar sıcaklığı (tenant rate limit anahtarı) | Tek shard CPU | Redis `--hotkeys` | Anahtar parçalama (bucket), lokal token bucket + periyodik senkron |
| H-7 | JWT doğrulama + token exchange maliyeti | Gateway CPU | Profil (async-profiler) | JWKS cache, token exchange sonucu kısa süreli cache (aud+sub) |
| H-8 | Kafka partition skew (büyük tenant tek partition anahtarı) | Tek consumer lag | Consumer lag / partition | Anahtar: `wallet_id` (tenant değil), sıralama yalnızca cüzdan bazında gerekli |
| H-9 | GC / bellek (JSON serileştirme, büyük yanıtlar) | GC pause | JFR | Generational ZGC, nesne havuzları yok — allocation azaltma |
| H-10 | Idempotency tablosu büyümesi | Insert gecikmesi | Tablo boyutu | Redis birincil + DB TTL partition (günlük drop) |

---

## 5. Ölçüm ve Analiz

| Unsur | Yaklaşım |
|---|---|
| İstemci tarafı | Gatling/k6 metrikleri (HdrHistogram — ortalama değil persentil), coordinated omission'dan kaçınmak için **open workload model** (sabit varış oranı) |
| Sunucu tarafı | Prometheus (RED: rate, errors, duration — servis/endpoint/tenant etiketli), USE (CPU, bellek, doygunluk), JVM (GC, thread, heap), PostgreSQL (`pg_stat_statements`, wait events, WAL), Kafka (lag, ISR), Redis |
| Trace | Tempo — %1 örnekleme + hatalı/yavaş istekler için tail-based sampling %100 |
| Profil | async-profiler / JFR sürekli profil (Pyroscope — opsiyonel) |
| Finansal doğrulama | Test sonunda mutabakat job'ı: Σ bakiye, journal dengesi, beklenen vs gerçekleşen işlem sayısı |
| Karşılaştırma | Baseline (son başarılı release) ile otomatik karşılaştırma; regresyon eşiği p99 +%10, throughput −%5 |
| Raporlama | Test raporu şablonu: amaç, ortam/versiyon, iş yükü, sonuçlar (grafikler), darboğazlar, aksiyonlar, NFR karşılama tablosu → Sprint Review paketi |

### 5.1 Ortam Koşulları

- Performans testleri **preprod**'da (prod ile aynı node tipi, aynı konfig; boyut en az %50, sonuçlar lineer ölçeklenme varsayımıyla değil **doğrudan** hedef yükle — kritik testler için tam boyut).
- PSP, SMS, KYC sağlayıcıları WireMock (gerçekçi gecikme dağılımı: PSP p50 400 ms / p99 2 sn) ile.
- Veri: 500 tenant, 50M cüzdan, 6 ay işlem geçmişi (sentetik).

---

## 6. Yol Haritası

| Sprint / MS | Faaliyet |
|---|---|
| S1–S2 (M1) | Gatling/k6 iskeleti, veri üreteci, preprod gözlemlenebilirlik, PT-01 CI entegrasyonu |
| S3–S6 (M2–M3) | Ledger/wallet mikro-benchmark (JMH), PT-06 hot account spike, H-1 çözüm ADR'si, PT-07 |
| S7–S8 (M4 — MVP) | PT-02, PT-03, PT-05 tam; PT-04 ilk soak; kapasite modeli v2; MVP kapasite onayı |
| S9–S16 (M5–M8 — GA) | PT-08, PT-09, PT-10 (settlement batch M7 ile), GA kapasite onayı |
