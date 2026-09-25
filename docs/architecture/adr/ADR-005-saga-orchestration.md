# ADR-005: Dağıtık İşlemler için Saga (Orchestration) + Idempotency + Compensation

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `SA`, Backend Tech Lead
- **İlgili:** [flows.md](../flows.md), [ADR-004](ADR-004-kafka-transactional-outbox.md)

## Context and Problem Statement

Kart yükleme (PSP → ledger), pre-auth (hold → increment → capture), P2P, iade, merchant takası, tenant onboarding gibi işlemler
birden fazla servis ve harici sistemi kapsar. Database-per-service nedeniyle 2PC/XA kullanılamaz. Çok adımlı işlemlerin
tutarlılığı, hata durumunda geri alınması ve görünürlüğü nasıl sağlanacak?

## Decision Drivers

- Para kaybı / çift yükleme = 0
- Her işlemin anlık durumunun **sorgulanabilir** olması (müşteri desteği, denetim)
- Timeout ve belirsiz sonuç (PSP) yönetimi
- Karmaşık akışların okunabilirliği ve test edilebilirliği

## Considered Options

1. **Orchestration** — iş sahibi servis içinde saga orkestratörü (`platform-commons-saga`), kalıcı durum makinesi
2. Choreography — yalnız event'lerle, merkezi koordinatör yok
3. Harici workflow motoru — Temporal / Camunda 8 (Zeebe)
4. 2PC / XA

## Decision Outcome

**Seçilen: Seçenek 1 — orchestration**, orkestratör işin sahibi olan servistedir:

| Saga | Orkestratör |
|---|---|
| TopUp, AutoTopUp, Payout, Chargeback | funding-service |
| Payment, PreAuth, Refund, P2P | payment-service |
| TenantOnboarding | tenant-service |
| SettlementBatch | settlement-service |
| VoucherBatchActivation | voucher-service |

Tasarım:
- `saga_instance (saga_id, type, tenant_id, state, data jsonb, version, deadline_at)` + `saga_step (saga_id, step, status, attempt, request_hash, response, error)`; durum geçişi + outbox aynı TX.
- Adım çağrıları: sıcak yolda **senkron REST** (düşük gecikme), uzun süren adımlarda **Kafka command/reply** topic'leri.
- Her adım **deterministik Idempotency-Key** (`{sagaId}:{step}`) → retry güvenli.
- Her ileri adımın tanımlı **kompanzasyonu** vardır (ör. PSP capture ↔ PSP refund, HOLD_PLACE ↔ HOLD_RELEASE, journal ↔ reversal journal). Kompanzasyonlar da idempotent ve sonsuz retry'a uygun; başarısızlık → `MANUAL_REVIEW` + istisna kuyruğu.
- **Pivot adım** kavramı: geri alınamaz adım (ör. merchant'a banka ödemesi gönderildi) sonrası saga yalnız ileri gider (retry), kompanze etmez.
- Timeout: `deadline_at` + zamanlayıcı (ShedLock); belirsiz sonuçta önce **sorgu (inquiry)**, sonra karar.
- Choreography yalnız **yan etkiler** için (loyalty, notification, reporting) — iş sonucunu etkilemeyen tepkiler.

### Consequences

- **Olumlu:** Akış tek yerde okunur/test edilir; durum sorgulanabilir; kompanzasyon mantığı açık; harici motor bağımlılığı yok.
- **Olumsuz:** Orkestratör servis diğerlerine bağımlı (bağımlılık grafı kurallarıyla sınırlanır); saga kütüphanesinin bakımı ekibe ait; görselleştirme için ek araç (admin konsolunda saga görüntüleyici).
- **Yeniden değerlendirme:** Saga tipi > 15 veya insan-onaylı uzun süreçler (günler) çoğalırsa Temporal değerlendirilir (ayrı ADR).

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Orchestration (in-service)** | Görünürlük, test, düşük gecikme, bağımlılık yok | Kütüphane bakımı |
| Choreography | Gevşek bağlılık | Akış dağınık, döngüsel event riski, "işlem nerede?" sorusu zor, kompanzasyon izlemesi zor |
| Temporal / Camunda | Güçlü motor, görselleştirme, dayanıklı zamanlayıcılar | Ek kritik altyapı (Tier-0 yolunda), gecikme, lisans/operasyon, ekip öğrenme eğrisi |
| 2PC / XA | Güçlü tutarlılık | Database-per-service ve harici sistemlerle uygulanamaz, kilitlenme, ölçeklenmez |
