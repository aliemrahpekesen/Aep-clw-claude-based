# ADR-012: Kart Verisini Saklamama — PSP Tokenization ile PCI DSS Kapsam Daraltma

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `SEC` (CISO), `SA`, `CMP`
- **İlgili:** [integration-architecture.md §3](../integration-architecture.md), [flows.md §2](../flows.md)

## Context and Problem Statement

Müşteriler cüzdana kartla para yükler; kayıtlı kart ve otomatik yükleme gereklidir. Kart verisi (PAN, CVV, son kullanma tarihi,
manyetik şerit/çip verisi) işleyen/saklayan/ileten her sistem **PCI DSS v4.0** kapsamına girer (SAQ D / ROC — yüzlerce kontrol,
yıllık QSA denetimi, segmentasyon testleri). Kart verisini nasıl ele alacağız?

## Decision Drivers

- PCI DSS kapsamını ve maliyetini minimize etmek
- Veri ihlali etkisini (breach impact) azaltmak
- Kullanıcı deneyimi: kayıtlı kart, tek dokunuşla yükleme, otomatik yükleme
- Çoklu PSP desteği

## Considered Options

1. **Kart verisi hiç sistemimize girmez**: PSP hosted payment page / hosted fields / mobil SDK + PSP tokenization
2. Kendi kart kasamız (PCI DSS Level 1 vault, HSM ile şifreleme)
3. Üçüncü taraf bağımsız vault (VGS, Basis Theory — PSP-agnostic token)

## Decision Outcome

**Seçilen: Seçenek 1.**

- **Web/mobil kart girişi** PSP'nin hosted sayfası/iFrame'i veya PSP'nin native mobil SDK'sı ile; PAN/CVV **hiçbir zaman** AEP-CLW backend'ine, loglarına, Kafka'ya, veritabanına ulaşmaz.
- Saklanan: `pspToken` (card token / storedPaymentMethodId), `last4`, `brand`, `expMonth/expYear`, `bin` (ilk 6/8 — PCI'da hassas değil; risk için), PSP kart `fingerprint`.
- Kayıtlı kart ile yükleme: CIT ilk işlem 3DS ile; sonraki otomatik yüklemeler **MIT** işaretli (PSP ve kart şemalarının stored credential kuralları).
- Hedef PCI kapsamı: **SAQ A** (tam yönlendirme / iFrame, mobil PSP SDK). Mobil uygulama PSP SDK'sını kullandığından ve kart verisi uygulamanın kendi sunucusuna gitmediğinden kapsam minimal; uygulama bütünlüğü (script/SDK tedarik zinciri) PCI DSS v4 6.4.3 / 11.6.1 kontrolleri ile izlenir (web ödeme sayfası script envanteri, CSP, SRI).
- **DLP kontrolleri**: log masking filtresi PAN regex (Luhn doğrulamalı) tespitinde değeri maskeler + güvenlik alarmı; Kafka/DB/Loki için periyodik PAN taraması; destek kanallarında (chat/e-posta) PAN paylaşımı engelleme uyarıları.
- **v2 değerlendirmesi:** Network tokenization (Visa VTS / Mastercard MDES) — PSP'ler arası taşınabilir token ve daha yüksek onay oranı.

### Consequences

- **Olumlu:** PCI DSS kapsamı dramatik biçimde daralır (SAQ A); kart verisi ihlali riski yok denecek kadar az; güvenlik ve denetim maliyeti düşer; PSP'nin 3DS/fraud yeteneklerinden yararlanılır.
- **Olumsuz:** **PSP lock-in**: kayıtlı kart token'ları PSP'ye özgü → PSP değişimi/failover'da kayıtlı kartlar taşınamaz (PSP'den PSP'ye token migrasyonu sözleşmeye bağlı, PCI uyumlu dosya transferi ile mümkün); UI kontrolü PSP hosted bileşenleriyle sınırlı; PSP ücretleri.
- **Kural:** Hiçbir API sözleşmesinde `pan`, `cardNumber`, `cvv` alanı bulunamaz (Spectral kuralı); code review kontrol listesinde yer alır.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **PSP tokenization** | Minimal PCI kapsamı, düşük risk | PSP lock-in |
| Kendi kart kasası | PSP bağımsızlığı, tam kontrol | PCI DSS Level 1 (SAQ D/ROC), HSM, segmentasyon, yıllık QSA — maliyet ve risk çok yüksek |
| Üçüncü taraf vault | PSP bağımsız token | Ek tedarikçi, maliyet, veri yerelliği (TR), kapsam yine SAQ A-EP düzeyine çıkabilir |
