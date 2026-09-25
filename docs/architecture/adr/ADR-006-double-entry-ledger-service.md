# ADR-006: Çift Kayıtlı (Double-Entry) Ledger Servisi — Parasal Gerçeğin Tek Kaynağı

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `SA`, `DATA`, `CMP`, `AUD`
- **İlgili:** [ledger-design.md](../ledger-design.md)

## Context and Problem Statement

Cüzdan bakiyeleri müşteri fonlarıdır (elektronik para / ön ödemeli değer). Bakiyelerin doğruluğu, denetlenebilirliği,
PSP/banka ile mutabakatı ve muhasebeye aktarımı zorunludur. Bakiye nerede ve nasıl tutulacak?

## Decision Drivers

- Her kuruşun kaynağı ve hedefi izlenebilir olmalı (denetim, 6493 fon koruma, MASAK)
- Negatif bakiye / çift harcama imkânsız olmalı (eşzamanlılık altında)
- Değiştirilemez tarihçe, düzeltme yalnız ters kayıtla
- 5.000 TPS altında düşük gecikme
- Takas, mutabakat, muhasebe, breakage için ortak model

## Considered Options

1. **Ayrı `ledger-service`, çift kayıtlı, append-only journal/posting, PostgreSQL**
2. Wallet tablosunda `balance` kolonu + işlem (transaction) log'u (tek kayıtlı)
3. Hazır ledger ürünü / DB — TigerBeetle, Formance Ledger, Modern Treasury (SaaS)
4. Event sourcing ile bakiye türetme

## Decision Outcome

**Seçilen: Seçenek 1.**

- `ledger-service` **yaprak servis**; tüm para hareketleri `POST /v1/journals` üzerinden.
- Journal ≥ 2 posting, para birimi başına Σ D = Σ C (uygulama + DB statement-level trigger).
- Append-only: `UPDATE/DELETE/TRUNCATE` trigger ile engelli, yetki REVOKE; düzeltme = reversal/adjustment journal.
- Tutarlar `bigint` minor units; `Money` value object.
- Negatif bakiye: `SELECT ... FOR UPDATE` (sıralı kilit) + `CHECK (allow_negative OR balance_minor >= 0)`.
- **Hold ledger'da temsil edilir** (`CUST_WALLET_HELD` alt hesabı) → yarış durumları DB'de çözülür.
- Hot account'lar (merchant payable, PSP clearing, fee income): `DEFERRED` bakiye modu + N shard alt hesap.
- Idempotency: `(tenant_id, idempotency_key)` PK, deterministik key'ler.
- Ölçek: tenant-hash bazlı ledger shard'ları (journal tek tenant → tek shard, dağıtık TX yok).
- Sürekli invariant doğrulama job'ları; sapma = P1 olay.

### Consequences

- **Olumlu:** Muhasebe standartlarına doğal uyum (mizan, GL export); denetçi için net model; tüm iş senaryoları (breakage, promo, takas, chargeback) aynı dille ifade edilir; bakiye tutarlılığı DB constraint'leriyle garanti.
- **Olumsuz:** Her ödeme için senkron ledger çağrısı (gecikme bütçesinde ~40 ms); ledger DB en yüksek yazma yükü (shard planlaması gerekli); ekip için çift kayıt eğitimi; hot account tasarımı dikkat ister.
- **Açık madde:** Promosyon fonlaması ve breakage muhasebe politikası `CMP` + mali müşavir onayı (ledger-design §12.2).

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Double-entry ledger servisi** | Denetlenebilir, tutarlı, muhasebe uyumlu | Geliştirme eforu, gecikme |
| Tek kayıtlı balance kolonu | Basit, hızlı | Karşı taraf izlenmez; merchant payable, PSP clearing, gelir hesapları ayrı ve tutarsız; mutabakat zor; denetimde zayıf |
| TigerBeetle | Çok yüksek performans, double-entry native | Operasyonel olgunluk/ekosistem, OpenShift'te işletim deneyimi, multitenancy ve RLS eşleniği yok, tenant tiering zor; v2'de hot path için değerlendirilebilir |
| Formance / SaaS ledger | Hızlı başlangıç | Veri yerelliği (TR), vendor lock-in, SaaS ise regülasyon/dış hizmet alımı onayı |
| Event sourcing | Tarihçe | Bakiye kontrolü (negatif önleme) için yine tutarlı okuma modeli gerekir; karmaşıklık |
