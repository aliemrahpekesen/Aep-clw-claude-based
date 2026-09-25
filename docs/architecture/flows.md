# AEP-CLW — Uçtan Uca Akışlar (Sequence Diagrams)

| Alan | Değer |
|---|---|
| Sahip | Solution Architect – Payments (`SA`) |
| İlgili | [ledger-design.md](ledger-design.md) (posting karşılıkları), [service-catalog.md](service-catalog.md), [ADR-005](adr/ADR-005-saga-orchestration.md) |
| Durum | Taslak |

> Gösterim: senkron çağrılar `->>`, yanıtlar `-->>`; asenkron event'ler `K` (Kafka) katılımcısı
> üzerinden gösterilir. "Outbox" = aynı DB transaction'ında `outbox_event` insert, Debezium ile Kafka'ya.
> Tüm mutasyon çağrıları deterministik `Idempotency-Key` taşır.

## İçindekiler

1. [Müşteri kaydı + OTP](#1-müşteri-kaydı--otp--cihaz-bağlama)
2. [Kartla para yükleme (3DS, webhook, saga, compensation)](#2-kartla-para-yükleme-3ds--psp-webhook--saga--compensation)
3. [QR ile mağaza ödemesi (customer-presented dynamic QR)](#3-qr-ile-mağaza-ödemesi-customer-presented-dynamic-qr)
4. [Pre-auth — EV şarj](#4-pre-auth--ev-şarj-hold--increment--final-capture)
5. [İade](#5-iade-refund)
6. [P2P transfer](#6-p2p-transfer)
7. [Gün sonu takas & mutabakat](#7-gün-sonu-takas--mutabakat)
8. [Kampanya / cashback tetikleme](#8-kampanya--cashback-tetikleme)
9. [Fraud bloklama](#9-fraud-bloklama)

---

## 1. Müşteri Kaydı + OTP + Cihaz Bağlama

```mermaid
sequenceDiagram
    autonumber
    actor U as Müşteri
    participant APP as Mobil App
    participant GW as api-gateway
    participant BFF as mobile-bff
    participant IDS as identity-service
    participant KC as Keycloak
    participant NOT as notification-service
    participant SMS as SMS Sağlayıcı
    participant CS as customer-service
    participant RS as risk-service
    participant K as Kafka
    participant WS as wallet-service
    participant LS as ledger-service
    participant CMP as compliance-service

    U->>APP: Telefon no + KVKK aydınlatma onayı
    APP->>GW: POST /mobile/v1/auth/otp {phone, purpose=REGISTER, deviceId}
    GW->>GW: Tenant = app build tenantSlug (hint), rate limit (IP, phone hash, device)
    GW->>BFF: forward
    BFF->>IDS: POST /v1/otp/challenges
    IDS->>RS: POST /v1/risk/evaluate (context=REGISTER, device, IP)
    RS-->>IDS: ALLOW
    IDS->>IDS: 6 hane OTP üret, hash sakla (Redis TTL 180s, max 5 deneme)
    IDS->>NOT: POST /v1/notifications (OTP, priority=HIGH, sync)
    NOT->>SMS: Gönder (birincil sağlayıcı, 2 sn timeout → yedek)
    SMS-->>U: SMS "123456"
    IDS-->>APP: 201 {challengeId, expiresIn}
    U->>APP: OTP girer
    APP->>BFF: POST /mobile/v1/auth/otp/{challengeId}/verify {code, devicePublicKey, attestation}
    BFF->>IDS: verify
    IDS->>IDS: Kod karşılaştır (sabit zamanlı), deneme sayacı
    IDS->>KC: Kullanıcı oluştur (organization = tenant, attribute phone_verified)
    IDS->>IDS: Device kaydı (public key, Play Integrity / App Attest doğrulandı)
    IDS->>KC: Token exchange → access (5 dk) + refresh (DPoP-bound, cihaz anahtarı)
    IDS->>K: outbox identity.user.registered
    IDS-->>BFF: tokens + userId
    BFF->>CS: POST /v1/customers {userId, phone, consents[]}
    CS->>CS: Customer(kycTier=BASIC), Consent kayıtları (metin versiyonu)
    CS->>K: outbox customer.registered
    CS-->>BFF: 201 customer
    BFF-->>APP: 201 {tokens, customer, appConfig}
    par Asenkron tepkiler
        K-->>WS: customer.registered → tenant config'teki walletTypes için cüzdan aç
        WS->>LS: POST /v1/accounts (CUST_WALLET, CUST_WALLET_BONUS, CUST_WALLET_HELD)
        WS->>K: outbox wallet.opened
    and
        K-->>CMP: customer.registered → yaptırım/PEP ön tarama (ad soyad varsa)
    and
        K-->>NOT: Hoş geldin push/e-posta
    end
```

**Hata / güvenlik notları**

| Durum | Davranış |
|---|---|
| OTP 5 hatalı deneme | Challenge kilitlenir; telefon hash için 15 dk cooldown; risk sinyali |
| SIM swap şüphesi (operatör API, ops.) | Risk CHALLENGE → ek doğrulama (e-posta / KYC) |
| Aynı telefon tenant'ta mevcut | Kayıt değil **login** akışına yönlendir (hesap numaralandırma koruması: aynı yanıt süresi ve mesaj) |
| Cihaz attestation başarısız | Kayıt sınırlı mod (yükleme limiti düşük) veya red — tenant politikası |

---

## 2. Kartla Para Yükleme (3DS + PSP Webhook + Saga + Compensation)

### 2.1 Mutlu yol

```mermaid
sequenceDiagram
    autonumber
    actor U as Müşteri
    participant APP as Mobil App
    participant BFF as mobile-bff
    participant FS as funding-service (Saga Orchestrator)
    participant WS as wallet-service
    participant RS as risk-service
    participant PSP as PSP (iyzico/Adyen...)
    participant ACS as Kart Bankası ACS (3DS)
    participant LS as ledger-service
    participant K as Kafka

    U->>APP: 500 TRY yükle, kart seç / yeni kart
    APP->>BFF: POST /mobile/v1/top-ups {amount, method=CARD_3DS, savedCardId?} + Idempotency-Key
    BFF->>FS: POST /v1/top-ups
    FS->>FS: TopUp(INITIATED) + saga_instance kaydı (tek TX)
    FS->>WS: POST /v1/limits/check (TOP_UP, 500, kycTier)
    WS-->>FS: OK (günlük kalan 4.500, bakiye tavanı OK)
    FS->>RS: POST /v1/risk/evaluate (TOP_UP, device, BIN/token, velocity)
    RS-->>FS: ALLOW (score 12)
    FS->>FS: PSP routing (birincil iyzico, BIN ülkesi, başarı oranı)
    FS->>PSP: 3DS initialize (amount, conversationId=topUpId, callbackUrl, cardToken veya hosted form)
    PSP-->>FS: threeDSHtml / redirectUrl
    FS->>FS: TopUp(PENDING_3DS)
    FS-->>APP: 202 {topUpId, action: REDIRECT, url}
    APP->>ACS: WebView / in-app browser (kart verisi PSP hosted sayfasında — bizim sistemimize girmez)
    U->>ACS: SMS OTP / banka uygulaması onayı
    ACS->>PSP: 3DS sonucu
    PSP->>APP: Redirect callbackUrl (sonuç sayfası — yalnız UI, güvenilmez)
    PSP->>FS: Webhook POST /v1/webhooks/psp/iyzico (HMAC imzalı)
    FS->>FS: İmza + timestamp doğrula, webhook_inbox insert (provider event id UNIQUE)
    FS->>PSP: Auth/Capture (3DS auth sonrası tahsil — PSP'ye göre tek veya iki adım)
    PSP-->>FS: CAPTURED (pspPaymentId, fee bilgisi)
    FS->>FS: TopUp(PSP_CAPTURED)
    FS->>LS: POST /v1/journals TOP_UP (D PSP_CLEARING / C CUST_WALLET 500) key=TOPUP:{id}:post
    LS-->>FS: 201 journalId
    FS->>FS: TopUp(COMPLETED) + outbox funding.topup.completed (tek TX)
    FS-->>BFF: (APP polling/SSE) status COMPLETED
    BFF-->>APP: Bakiye 1.500 TRY
    K-->>K: loyalty (yükleme bonusu?), notification, compliance (işlem izleme), reporting
```

### 2.2 Saga durum makinesi ve kompanzasyon

```mermaid
stateDiagram-v2
    [*] --> INITIATED
    INITIATED --> REJECTED: limit / risk DENY
    INITIATED --> PENDING_3DS: PSP init OK
    PENDING_3DS --> FAILED: 3DS fail / timeout 15 dk
    PENDING_3DS --> PSP_CAPTURED: webhook + capture OK
    PSP_CAPTURED --> COMPLETED: ledger posting OK
    PSP_CAPTURED --> LEDGER_RETRY: ledger 5xx / timeout
    LEDGER_RETRY --> COMPLETED: retry OK (aynı idempotency key)
    LEDGER_RETRY --> COMPENSATING: kalıcı hata (ör. bakiye tavanı aşıldı, hesap FROZEN)
    COMPENSATING --> COMPENSATED: PSP refund/void OK
    COMPENSATING --> MANUAL_REVIEW: PSP refund başarısız (3 deneme)
    COMPLETED --> [*]
    COMPENSATED --> [*]
    FAILED --> [*]
    REJECTED --> [*]
```

```mermaid
sequenceDiagram
    autonumber
    participant FS as funding-service
    participant LS as ledger-service
    participant PSP as PSP
    participant K as Kafka
    participant OPS as Operasyon Konsolu

    Note over FS: PSP_CAPTURED — para karttan çekildi
    FS->>LS: POST /v1/journals (TOP_UP)
    LS-->>FS: 422 LIMIT_EXCEEDED (eşzamanlı başka yükleme tavanı doldurdu)
    FS->>FS: TopUp(COMPENSATING) + saga step log
    FS->>PSP: Refund / Cancel (pspPaymentId, idempotency=TOPUP:{id}:refund)
    alt PSP OK
        PSP-->>FS: REFUNDED
        FS->>FS: TopUp(COMPENSATED) + outbox funding.topup.compensated
        K-->>K: notification: "Yükleme iade edildi"
    else PSP hata (3 deneme, exponential backoff)
        FS->>FS: TopUp(MANUAL_REVIEW)
        FS->>OPS: reconciliation.exception (PSP_REFUND_FAILED)
        Note over FS,OPS: Para PSP_CLEARING'de değil, müşteri kartında da değil →<br/>settlement mutabakatında yakalanır, SLA 1 iş günü
    end
```

**Kritik kurallar**

| # | Kural |
|---|---|
| F-1 | Ledger posting yalnız **webhook veya PSP sorgu API'si** ile teyit edilmiş capture sonrasında. Redirect callback'ine güvenilmez. |
| F-2 | Webhook gelmezse: saga timeout (3 dk) → PSP `retrieve payment` sorgusu (pull), 15 dk'da FAILED. |
| F-3 | Webhook tekrarları `webhook_inbox (provider, provider_event_id)` UNIQUE ile dedupe. |
| F-4 | Yükleme ücretini müşteri ödüyorsa PSP'ye `amount + fee` gönderilir, posting 3 bacaklıdır (ledger senaryo 2). |
| F-5 | Kayıtlı kart (non-3DS, MIT/CIT kuralı): auto top-up **MIT** (merchant-initiated) olarak işaretlenir; PSP token + ilk işlem 3DS ile alınmış olmalı. |

---

## 3. QR ile Mağaza Ödemesi (Customer-Presented Dynamic QR)

### 3.1 Token tasarımı (TOTP tabanlı)

| Unsur | Tasarım |
|---|---|
| Seed | Cihaz bağlamada, cihaz başına 256-bit `tokenSeed` üretilir; sunucuda Vault Transit ile şifreli, cihazda Secure Enclave / Android Keystore'da |
| Token | `QR = base45(ver ‖ tenantShort ‖ walletRef (opaque, 8B) ‖ deviceKeyId ‖ timeStep ‖ TOTP(HMAC-SHA256, seed, 30s, 8 hane) ‖ sigTrunc)` — ~60 karakter, QR v4 |
| Geçerlilik | Tenant config `qr.ttlSeconds` (varsayılan 60 sn = 2 step), ±1 step saat sapma toleransı |
| Tek kullanım | Redis `SET NX clw:..:qr:nonce:{deviceKeyId}:{step}:{otp}` TTL 90 sn; kullanılmış token → `QR_ALREADY_USED` |
| Offline | Uygulama çevrimdışıyken önceden üretilen **N adet** (config `offlineTokens`) tek kullanımlık, düşük limitli token (sunucuda sayaçlı); POS çevrimdışıysa → kasada ödeme yapılamaz (v1), çevrimiçi POS zorunlu |
| Gizlilik | QR müşteri kimliği/telefonu içermez; `walletRef` opaque ve rotasyonlu |
| Ekran güvenliği | QR ekranında screenshot engelleme (Android FLAG_SECURE), 60 sn geri sayım, step-up (biyometri) tenant ayarı |

### 3.2 Akış

```mermaid
sequenceDiagram
    autonumber
    actor U as Müşteri
    participant APP as Mobil App
    participant POS as Web POS / Entegre Kasa
    participant GW as api-gateway
    participant PB as pos-bff
    participant PS as payment-service
    participant MS as merchant-service (cache)
    participant RS as risk-service
    participant WS as wallet-service
    participant LS as ledger-service
    participant K as Kafka

    U->>APP: "Öde" ekranı (biyometri opsiyonel)
    APP->>APP: TOTP token üret (offline mümkün), QR göster
    POS->>POS: Kasiyer sepeti kapatır, QR'ı okur (tutar 100 TRY)
    POS->>GW: POST /pos/v1/payments {qrToken, amount, orderRef, terminalId} + Idempotency-Key + X-Signature
    GW->>GW: Terminal token doğrula, tenant, rate limit
    GW->>PB: forward
    PB->>PS: POST /v1/payments
    PS->>PS: Idempotency (Redis hızlı yol)
    PS->>MS: GET terminal context (L1/L2 cache hit)
    PS->>PS: QR çöz → deviceKeyId → seed (cache, Vault Transit decrypt) → TOTP doğrula
    PS->>PS: Redis SET NX nonce (tek kullanım)
    par Paralel (bütçe 100 ms)
        PS->>RS: POST /v1/risk/evaluate (PAYMENT, amount, merchant, device, velocity)
        RS-->>PS: ALLOW
    and
        PS->>WS: POST /v1/wallets/{customer}/spend-plan (100 TRY)
        WS-->>PS: [BONUS 20, MAIN 80] + limit OK
    end
    PS->>PS: Payment(INITIATED→AUTHORIZED) in-memory
    PS->>LS: POST /v1/journals PAYMENT_CAPTURE (D BONUS 20, D MAIN 80 / C MERCHANT_PAYABLE 100)
    alt Yetersiz bakiye (yarış)
        LS-->>PS: 422 INSUFFICIENT_FUNDS
        PS->>PS: Payment(DECLINED) + outbox payment.declined
        PS-->>PB: 402 Problem (INSUFFICIENT_FUNDS)
    else OK
        LS-->>PS: 201 journalId, balancesAfter
        PS->>PS: Payment(CAPTURED) + outbox payment.captured (tek TX)
        PS-->>PB: 201 {paymentId, status CAPTURED, balances}
    end
    PB-->>POS: 201 → fiş yazdır
    K-->>APP: (notification push) "Mağaza X'te 100 TRY ödeme"
    K-->>K: loyalty (yıldız), settlement (merchant günlük toplam), compliance, reporting, audit
```

**Zaman bütçesi (p99 300 ms hedefi)**

| Adım | Bütçe |
|---|---|
| Gateway + BFF | 20 ms |
| Terminal context + QR doğrulama + nonce | 15 ms |
| Risk ∥ spend-plan | 80 ms |
| Ledger posting | 40 ms |
| Payment persist + outbox | 15 ms |
| Ağ + serileştirme payı | 30 ms |
| **Toplam** | **~200 ms** (p99 hedefi altında 100 ms tampon) |

**POS timeout / belirsiz sonuç:** POS 5 sn içinde yanıt alamazsa **aynı Idempotency-Key** ile tekrar sorar
(`GET /pos/v1/payments?orderRef=` veya POST retry). Kesin yanıt alınamazsa `POST /payments/{id}/reversal` (15 dk pencere).

### 3.3 Merchant-Presented QR (özet)

Müşteri, kasadaki dinamik QR'ı (tutar + `merchantQrId` + imza) okur → `POST /mobile/v1/merchant-qr/{id}/pay` →
müşteri onayı (biyometri) → aynı ödeme çekirdeği. POS, sonucu webhook veya long-poll ile alır.

---

## 4. Pre-Auth — EV Şarj (Hold → Increment → Final Capture)

```mermaid
sequenceDiagram
    autonumber
    actor U as Sürücü
    participant APP as Mobil App
    participant CPMS as Şarj Yönetim Sistemi (CPMS / OCPP)
    participant PB as pos-bff (Public API)
    participant PS as payment-service
    participant RS as risk-service
    participant WS as wallet-service
    participant LS as ledger-service
    participant FS as funding-service
    participant K as Kafka

    U->>APP: Şarj istasyonu QR'ını okut / connector seç
    APP->>CPMS: (Tenant app → CPMS API) StartSession(connectorId, customerRef)
    CPMS->>PB: POST /pos/v1/pre-auths {customerRef, amount=500, terminalId=chargerId, ttl=12h}
    PB->>PS: POST /v1/pre-authorizations
    PS->>RS: evaluate (PREAUTH)
    RS-->>PS: ALLOW
    PS->>WS: POST /v1/wallets/{id}/holds (500, ref=preAuthId, expiresAt)
    WS->>LS: POST /v1/journals HOLD_PLACE (D CUST_WALLET 500 / C CUST_WALLET_HELD 500)
    alt Bakiye yetersiz + auto top-up açık
        LS-->>WS: 422 INSUFFICIENT_FUNDS
        WS-->>PS: 402
        PS->>FS: POST /v1/auto-top-up/executions (eksik + eşik)
        FS-->>PS: COMPLETED (kayıtlı kart, MIT)
        PS->>WS: hold tekrar (aynı key değil, yeni attempt key)
    end
    LS-->>WS: 201
    WS-->>PS: holdId ACTIVE
    PS->>PS: PreAuthorization(OPEN) + outbox preauth.opened
    PS-->>CPMS: 201 {preAuthId, authorizedAmount 500}
    CPMS->>CPMS: RemoteStartTransaction (OCPP) → şarj başlar
    Note over CPMS,PS: Şarj sürerken CPMS periyodik MeterValues gönderir
    CPMS->>PB: POST /pos/v1/pre-auths/{id}/increment (+200, tüketim 480 TRY'ye yaklaştı)
    PB->>PS: increment
    PS->>WS: hold artır (+200)
    WS->>LS: HOLD_PLACE (+200)
    PS-->>CPMS: 200 authorized 700
    U->>CPMS: Şarjı durdur / kablo çıkarıldı
    CPMS->>PB: POST /pos/v1/pre-auths/{id}/complete {finalAmount 612.40, kWh 48.3, sessionId}
    PB->>PS: complete
    PS->>WS: POST /v1/holds/{holdId}/capture (612.40)
    WS->>LS: HOLD_CAPTURE (D HELD 700 / C MERCHANT_PAYABLE 612.40, C CUST_WALLET 87.60)
    LS-->>WS: 201
    WS-->>PS: CAPTURED (released 87.60)
    PS->>PS: PreAuthorization(COMPLETED) + Payment(CAPTURED) + outbox preauth.completed
    PS-->>CPMS: 200
    K-->>APP: push "Şarj tamamlandı: 48,3 kWh — 612,40 TRY"
    K-->>K: loyalty (kWh puanı), settlement, reporting
```

| İstisna | Davranış |
|---|---|
| `complete` hiç gelmez | Hold `expiresAt` (12 saat) → wallet-service `HOLD_RELEASE` + `wallet.hold.expired` → payment `preauth.expired`; CPMS geç `complete` gönderirse → **incremental charge** (yeni ödeme, müşteri bakiyesinden; yetersizse auto top-up / borç kaydı `CUST_RECEIVABLE`) |
| Final > hold | `overCaptureBps` içinde ise fark `CUST_WALLET`'tan ek posting; değilse kalan için ayrı ödeme denemesi |
| CPMS aynı `complete`'i 2 kez gönderir | Idempotency-Key = `PREAUTH:{id}:complete` → aynı yanıt |
| Otopark | Aynı model: giriş (plaka tanıma) → hold 200; çıkış → süre ücreti hesap → capture; bariyer offline ise PARCS kuyruğa alır, çevrimiçi olunca `complete` |

---

## 5. İade (Refund)

```mermaid
sequenceDiagram
    autonumber
    actor C as Kasiyer / Tenant Admin
    participant POS as Web POS / Admin Portal
    participant PB as pos-bff / admin-bff
    participant PS as payment-service
    participant LS as ledger-service
    participant K as Kafka
    participant LOY as loyalty-service
    participant SET as settlement-service

    C->>POS: Ödeme bul (fiş no / paymentId), iade tutarı 40, sebep
    POS->>PB: POST /pos/v1/payments/{id}/refunds {amount 40, reason} + Idempotency-Key
    PB->>PS: POST /v1/payments/{id}/refunds
    PS->>PS: Yetki (terminal aynı store/merchant mi, iade rolü, eşik üstü → maker-checker)
    PS->>PS: Invariant: refunded + 40 ≤ captured, refund penceresi (tenant: 30 gün)
    PS->>PS: Kaynak bacak dağılımı: allocate(40, [BONUS 20 : MAIN 80]) → BONUS 8, MAIN 32
    PS->>PS: BONUS bacağı süresi dolmuş mu? → evet ise politika (MAIN'e çevir / PROMO ters kayıt)
    PS->>LS: POST /v1/journals REFUND (D MERCHANT_PAYABLE 40 / C BONUS 8, C MAIN 32) key=REFUND:{refundId}
    LS-->>PS: 201
    opt Komisyon iadesi politikası açık
        PS->>LS: MERCHANT_FEE_REVERSAL (oransal)
    end
    PS->>PS: Refund(COMPLETED), Payment(PARTIALLY_REFUNDED) + outbox payment.refunded
    PS-->>PB: 201 Refund
    PB-->>POS: İade fişi
    K-->>LOY: payment.refunded → puan oransal geri al (40 TRY → 4 yıldız)
    K-->>SET: merchant günlük net'ten düş (takas edilmişse → MERCHANT_RECEIVABLE, sonraki batch'te netleme)
    K-->>K: notification, reporting, audit
```

| Kural | Açıklama |
|---|---|
| Refund ≠ Reversal | Reversal: teknik, 15 dk, settlement öncesi, ayna journal. Refund: iş işlemi, kısmi olabilir, pencere tenant ayarı. |
| Maker-checker | Tenant eşiği üstü iade (örn. > 1.000 TRY) → admin onayı bekler (`Refund(PENDING_APPROVAL)`). |
| Karta iade yok | Kapalı devre: iade **cüzdana**. Cüzdan bakiyesinin karta/IBAN'a iadesi ayrı `payout` akışıdır. |

---

## 6. P2P Transfer

```mermaid
sequenceDiagram
    autonumber
    actor A as Gönderen
    participant APP as Mobil App
    participant BFF as mobile-bff
    participant PS as payment-service
    participant CS as customer-service
    participant RS as risk-service
    participant WS as wallet-service
    participant LS as ledger-service
    participant K as Kafka

    A->>APP: Alıcı telefon / kişi seç, 150 TRY, not
    APP->>BFF: POST /mobile/v1/p2p {recipientPhone, amount, note} + Idempotency-Key
    BFF->>CS: Alıcı çöz (phoneHash, aynı tenant, ACTIVE) → maskeli ad "A*** Y***"
    BFF-->>APP: Onay ekranı (maskeli ad, ücret 0)
    A->>APP: Onay + biyometri (step-up token, acr=step-up)
    APP->>BFF: POST /mobile/v1/p2p/confirm
    BFF->>PS: POST /v1/p2p-transfers {sender, recipientCustomerId, 150}
    PS->>PS: Feature flag p2pTransfer, cüzdan tipi transferable, sender ≠ recipient
    par
        PS->>RS: evaluate (P2P, ağ analizi sinyalleri, yeni alıcı, velocity)
        RS-->>PS: ALLOW
    and
        PS->>WS: limits/check (sender: maxP2PMonthly, recipient: maxBalance + aylık gelen)
        WS-->>PS: OK
    end
    PS->>LS: POST /v1/journals P2P_TRANSFER (D CUST_WALLET A 150 / C CUST_WALLET B 150)
    LS-->>PS: 201
    PS->>PS: P2PTransfer(COMPLETED) + outbox p2p.transfer.completed
    PS-->>BFF: 201
    BFF-->>APP: Başarılı, yeni bakiye
    K-->>K: notification (gönderen + alıcı), compliance (P2P ağ izleme), reporting
```

**Risk CHALLENGE durumunda:** `PS` → `428 STEP_UP_REQUIRED` → uygulama PIN/biyometri + opsiyonel OTP → aynı Idempotency-Key ile tekrar.

---

## 7. Gün Sonu Takas & Mutabakat

```mermaid
sequenceDiagram
    autonumber
    participant SCH as Scheduler (ShedLock / K8s CronJob)
    participant SET as settlement-service
    participant LS as ledger-service
    participant MS as merchant-service
    participant PSPR as PSP Raporlama (SFTP/API)
    participant BANK as Banka (API / SFTP)
    participant S3 as Object Storage
    participant ADM as Admin Portal (maker-checker)
    participant K as Kafka
    participant ACC as accounting-service

    SCH->>SET: Tenant T için gün kapanışı (tenant TZ 23:59:59 cut-off)
    SET->>LS: GET MERCHANT_PAYABLE hesap ekstreleri (cut-off'a kadar, tüm shard'lar)
    LS-->>SET: postings (capture, refund, fee, adjustment)
    SET->>MS: Komisyon planı, takas takvimi (T+0/T+1/haftalık), IBAN
    SET->>SET: SettlementBatch hesapla: gross − refunds − fees − chargebacks ± adj, cash top-up netleme
    SET->>SET: Batch(CALCULATED) — eşik üstü veya ilk takas → PENDING_APPROVAL
    SET->>ADM: Onay kutusuna düşer
    ADM->>SET: Approve (checker ≠ maker)
    SET->>LS: SETTLEMENT_PAYOUT (D MERCHANT_PAYABLE / C PAYOUT_IN_TRANSIT) per merchant
    SET->>BANK: Toplu ödeme talimatı (EFT/FAST API veya dosya, imzalı)
    BANK-->>SET: Talimat alındı (ref)
    SET->>K: settlement.batch.paid (PAID)
    Note over SET,BANK: T+1 sabah
    BANK->>SET: Ekstre (camt.053 / MT940) SFTP
    PSPR->>SET: PSP settlement raporu (işlem bazlı + fee)
    SET->>S3: Ham dosyaları sakla (checksum, WORM)
    SET->>SET: Parse → normalize (ACL) → ReconciliationRun
    SET->>LS: Aynı dönem journal'ları (PSP_CLEARING, BANK_SAFEGUARDING, PAYOUT_IN_TRANSIT)
    SET->>SET: 3 yönlü eşleştirme (ledger ↔ PSP ↔ banka): anahtar pspPaymentId / bank ref, tutar, tarih toleransı
    alt Eşleşti
        SET->>LS: PSP_SETTLEMENT (D BANK_SAFEGUARDING / C PSP_CLEARING), PSP_FEE, PAYOUT_CONFIRM
    else Eşleşmedi
        SET->>LS: RECON_ADJUSTMENT → SUSPENSE
        SET->>K: reconciliation.exception.raised (tip: MISSING_IN_LEDGER / MISSING_AT_PSP / AMOUNT_MISMATCH / DUPLICATE)
        K-->>ADM: İstisna iş kuyruğu (SLA: 1 iş günü)
    end
    SET->>K: reconciliation.run.completed (eşleşme oranı)
    K-->>ACC: GL export + komisyon e-Faturaları (merchant'a)
```

**Mutabakat kontrolleri**

| Kontrol | Kaynaklar | Tolerans |
|---|---|---|
| PSP işlem eşleşmesi | `funding.top_up` ↔ PSP raporu | Tutar tam, tarih ±1 gün |
| PSP net ödeme | PSP raporu net ↔ banka ekstresi | Tam |
| Merchant payout | `PAYOUT_IN_TRANSIT` ↔ banka çıkışları | Tam |
| Safeguarding | Σ müşteri yükümlülükleri ↔ emanet banka bakiyesi + PSP in-transit | Tam; fark → P1 + CMP |
| İç tutarlılık | Trial balance, wallet ↔ ledger | Sıfır |

---

## 8. Kampanya / Cashback Tetikleme

```mermaid
sequenceDiagram
    autonumber
    participant K as Kafka
    participant LOY as loyalty-service
    participant RE as Kural Motoru (in-process)
    participant R as Redis
    participant DB as loyalty_db
    participant LS as ledger-service
    participant WS as wallet-service

    K-->>LOY: payment.captured (tenant, customer, merchant, store, amount 100, legs, time)
    LOY->>LOY: Inbox dedupe (event_id)
    LOY->>RE: Aktif kampanyalar (tenant, trigger=PAYMENT_CAPTURED) — derlenmiş cache
    RE->>RE: Koşullar: store ∈ {İstanbul}, saat 07-10, tier ≥ GREEN, min 50 TRY, müşteri başına max 3/hafta
    RE-->>LOY: Eşleşen: c_12 "Sabah %5 cashback" (5 TRY), c_1 "1 yıldız / 10 TRY" (10 yıldız)
    LOY->>R: Müşteri sayaç kontrol (c_12 bu hafta 1/3)
    LOY->>DB: BEGIN
    LOY->>DB: UPDATE campaign_budget SET spent = spent + 500 WHERE id=c_12 AND spent + 500 <= cap
    alt Bütçe yok
        DB-->>LOY: 0 satır
        LOY->>DB: Campaign c_12 EXHAUSTED + outbox campaign.budget.exhausted
    else Bütçe var
        LOY->>DB: CashbackGrant(PENDING), points_entry (+10, append-only), outbox (tek TX)
    end
    LOY->>DB: COMMIT
    LOY->>LS: POST /v1/journals CASHBACK (D PROMO_EXPENSE c_12 5 / C CUST_WALLET_BONUS 5) key=CASHBACK:{paymentId}:c_12
    LS-->>LOY: 201
    LOY->>DB: CashbackGrant(GRANTED) + outbox loyalty.cashback.granted, loyalty.points.earned
    Note over LOY,WS: BONUS lot kaydı: wallet-service ledger.journal.posted event'inden ValueLot (expiry 90 gün) oluşturur
    K-->>K: notification push "5 TRY cashback + 10 yıldız"
```

| Kural | Açıklama |
|---|---|
| Geri alma | `payment.refunded` → oransal cashback geri alma (D `CUST_WALLET_BONUS` / C `PROMO_EXPENSE`); BONUS harcanmışsa politika: MAIN'den düş veya zarar yaz (tenant ayarı) |
| Gecikme | Ödeme → cashback yansıma p95 < 5 sn |
| Simülasyon | Kampanya yayına almadan `simulate` ile geçmiş 30 gün ClickHouse verisinde maliyet tahmini |
| Kötüye kullanım | Risk sinyali (aynı cihaz çok hesap) → cashback REVIEW, grant bekletilir |

---

## 9. Fraud Bloklama

### 9.1 Gerçek zamanlı ret + vaka

```mermaid
sequenceDiagram
    autonumber
    participant PS as payment-service
    participant RS as risk-service
    participant R as Redis (velocity)
    participant K as Kafka
    participant WS as wallet-service
    participant IDS as identity-service
    participant CS as customer-service
    participant ANL as Risk Analisti (Admin)
    participant NOT as notification-service

    PS->>RS: POST /v1/risk/evaluate (PAYMENT 950 TRY, device D9, merchant m_77)
    RS->>R: Velocity: son 10 dk ödeme sayısı / tutar (sliding window, Lua)
    RS->>RS: Kurallar: yeni cihaz (< 1 saat) + gece + 3 farklı mağaza 10 dk içinde + tutar > p95
    RS->>RS: Skor 91 → DENY + otomatik aksiyon "WALLET_FREEZE"
    RS->>RS: RiskDecision kaydı (input snapshot, fired rules — açıklanabilirlik)
    RS-->>PS: DENY (reasonCode RISK_VELOCITY)
    PS-->>PS: Payment(DECLINED) → POS'a genel mesaj (sebep ifşa edilmez)
    RS->>K: outbox risk.case.opened, risk.wallet.freeze.requested
    K-->>WS: Wallet FROZEN (çıkışlar kapalı, hold'lar korunur)
    K-->>IDS: Şüpheli cihaz oturumlarını sonlandır (refresh token revoke)
    K-->>NOT: Müşteriye "hesabınız güvenlik kontrolünde" (SMS + push, tenant şablonu)
    K-->>ANL: Vaka kuyruğu (öncelik: yüksek)
    ANL->>RS: Vakayı incele (işlem geçmişi, cihaz grafı, konum)
    alt False positive
        ANL->>RS: resolve RELEASE (+ opsiyonel allowlist cihaz)
        RS->>K: risk.case.resolved, wallet unfreeze talebi
        K-->>WS: Wallet ACTIVE
    else Fraud teyit
        ANL->>RS: resolve CONFIRMED_FRAUD
        RS->>K: risk.customer.blocked, liste güncelle (cihaz, IBAN)
        K-->>CS: Customer BLOCKED
        K-->>K: compliance (STR değerlendirmesi), funding (kayıtlı kartları devre dışı)
    end
```

### 9.2 Karar matrisi

| Skor / kural | Karar | Aksiyon |
|---|---|---|
| 0–39 | ALLOW | — |
| 40–69 | CHALLENGE | Step-up (biyometri/PIN/OTP), başarılıysa ALLOW |
| 70–84 | REVIEW | İşlem tenant politikasına göre ALLOW+vaka veya hold+vaka |
| 85–100 veya kesin kural (blocklist) | DENY | Vaka + opsiyonel freeze |
| Risk servisi erişilemez | Tenant `risk.failMode` | `OPEN`: `failOpenMaxAmount` altı ALLOW + sonradan değerlendirme; `CLOSED`: DENY |

Kurallar yeni versiyonda önce **SHADOW** modda çalışır (karar etkilemez, metrik toplar); onaylı promosyon sonrası ACTIVE.
