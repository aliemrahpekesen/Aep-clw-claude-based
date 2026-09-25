# AEP-CLW — Proje Risk Kaydı (Risk Register)

| Alan | Değer |
|---|---|
| Doküman | Proje Risk Kaydı |
| Sahibi | Delivery Manager (`DM`) |
| Katkı | `PO`, `CA`, `SA`, `SEC`, `CMP`, `AUD`, `OPS`, `QA` |
| Sürüm | v1.0 — Sprint 0 baseline |
| Gözden geçirme | 2 haftada bir (Risk & uyum gözden geçirme) + her milestone çıkışı |

---

## 1. Puanlama Yöntemi

| Puan | Olasılık (O) | Etki (E) |
|---|---|---|
| 1 | Çok düşük (< %10) | İhmal edilebilir: plan içinde emilir |
| 2 | Düşük (%10–30) | Küçük: < 1 hafta gecikme veya tek fonksiyon etkisi |
| 3 | Orta (%30–50) | Orta: 1 sprint gecikme, Should kapsam kaybı |
| 4 | Yüksek (%50–70) | Büyük: milestone kayması, Must kapsam kaybı, uyum bulgusu |
| 5 | Çok yüksek (> %70) | Kritik: MVP/GA kayması, finansal kayıp, regülasyon yaptırımı, veri ihlali |

**Skor = O × E** · **15–25 Yüksek** · **8–14 Orta** · **1–7 Düşük**

Risk yanıt stratejileri: **Azalt** (olasılık/etkiyi düşür), **Kaçın** (kapsam/tasarım değişikliği), **Transfer** (sözleşme/sigorta), **Kabul** (izle).

---

## 2. Risk Kaydı

| ID | Risk (neden → olay → sonuç) | Kategori | O | E | Skor | Seviye | Strateji | Azaltma aksiyonları | Tetikleyici / erken uyarı | Sahibi | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-01 | Paydaş talepleri ve pilot beklentileri nedeniyle **kapsam genişler** → MVP tarihi kayar | Kapsam | 4 | 4 | 16 | Yüksek | Azalt | Takas kuralı ([mvp-scope.md §7](mvp-scope.md)); her Review'da Fonksiyon Matrisi ile kapsam görünürlüğü; "Should" tamponu (%20) | Sprint'e plansız Story girişi > %10 | `PO` | M1–M4 | Açık |
| R-02 | Ledger/cüzdan **veri modelindeki hatalar geç fark edilir** → M3–M5'te büyük göç ve yeniden çalışma | Teknik | 3 | 5 | 15 | Yüksek | Azalt | S0'da ledger ADR + olay modeli; M2'de property-based testler; M5 cüzdan tiplerinin (SUB, RESTRICTED, GIFT) S3'te model üzerinde "kağıt üzerinde" doğrulanması | Hesap planında plan dışı değişiklik talebi | `SA` | M2 | Açık |
| R-03 | **PSP seçimi / sözleşme / sandbox erişimi gecikir** → M3 kart yükleme ve pilot takvimi kayar | Dış bağımlılık | 4 | 4 | 16 | Yüksek | Azalt | Mock PSP ile geliştirme (FR-046); PSP kısa listesi S1'de, karar S2 sonu; adaptör portu ile PSP bağımsız çekirdek; ikinci aday PSP ile paralel görüşme | S4 sonunda sandbox yok | `SA` | M3 | Açık |
| R-04 | Popüler hesaplarda (işyeri, PSP takas) **kilit çekişmesi (hot account)** → ödeme gecikmesi ve NFR-001/003 ihlali | Teknik / performans | 3 | 4 | 12 | Orta | Azalt | Hot account için alt hesap (sharding) veya batch toplama tasarımı; M2'de erken yük testi; optimistic locking + retry politikası | S4 yük testinde p95 > 200 ms | `CA` | M2–M3 | Açık |
| R-05 | Mikroservis sayısı ve **dağıtık işlem karmaşıklığı** (saga, outbox) ekip kapasitesini aşar → kalite düşüşü, gecikme | Teknik / organizasyon | 3 | 4 | 12 | Orta | Azalt | Servis şablonu ve ortak kütüphane; MVP'de yalnızca gerekli servisler deploy; bazı bounded context'lerin başlangıçta birlikte konuşlandırılması (modüler monolit seçeneği ADR'de değerlendirilir) | Sprint velocity düşüşü > %25 | `CA` | M1–M4 | Açık |
| R-06 | **OpenShift kümesi, ağ, Vault, Kafka altyapı tahsisi gecikir** → S1 walking skeleton engellenir | Altyapı | 3 | 4 | 12 | Orta | Azalt | S0'da altyapı taleplerinin açılması; geçici olarak geliştirici kümesi / yerel Testcontainers; IaC ile hızlı kurulum | S0 sonunda dev namespace yok | `OPS` | M0–M1 | Açık |
| R-07 | **Regülasyon değişikliği veya sınırlı ağ istisnasının yorumlanması** → lisans gereksinimi, kapsam/limit değişikliği | Uyum | 3 | 5 | 15 | Yüksek | Azalt / Transfer | Erken hukuki görüş (S1); limitlerin konfigürasyon olması (FR-106); sınırlı ağ eşik izleme (FR-113); gerekirse lisanslı kuruluşla iş birliği modeli | Regülatör duyurusu, hukuki görüşte çekince | `CMP` | Tümü | Açık |
| R-08 | **Banka, ERP ve e-Fatura entegrasyonları** dış tarafların takvimine bağlı kalır → M7 kayar | Dış bağımlılık | 4 | 3 | 12 | Orta | Azalt | Dosya tabanlı (MT940, CSV) yedek yol; ERP için önce export, sonra adaptör; entegratör sözleşmelerinin M5'te başlatılması | M6 sonunda test erişimi yok | `SA` | M7 | Açık |
| R-09 | **QR token çalınması / tekrar oynatma** (ekran görüntüsü, omuz üstü) → yetkisiz harcama, itibar kaybı | Güvenlik | 3 | 4 | 12 | Orta | Azalt | Kısa ömürlü (≤ 60 sn), tek kullanımlık, cihaz anahtarıyla imzalı token; ekran görüntüsü engelleme (Android); step-up eşiği; anomali alarmı | Aynı token ile çoklu deneme | `SEC` | M3 | Açık |
| R-10 | **Mobil uygulama mağaza onayı gecikir veya reddedilir** (white-label, finansal uygulama politikaları) → MVP canlıya geçiş gecikir | Dış bağımlılık | 3 | 4 | 12 | Orta | Azalt | Tenant adına geliştirici hesaplarının S5'te açılması; S7'de TestFlight/iç test yayını; mağaza politikalarına uygunluk kontrol listesi; web tabanlı yedek (PWA) değerlendirmesi | İlk inceleme reddi | `MOB` | M4 | Açık |
| R-11 | **Keycloak organizasyon (tenant) modeli** ölçek veya özelleştirme sınırlarına takılır → kimlik mimarisi değişikliği | Teknik | 2 | 4 | 8 | Orta | Azalt | S0'da PoC (100 tenant, 1M kullanıcı sentetik); OTP ve cihaz bağlamanın identity-service'te kalması (Keycloak'a gömülmemesi) | PoC'de performans veya özellik açığı | `CA` | M1 | Açık |
| R-12 | **Pentest bulgularının kapatılması** planlanandan uzun sürer → GA kayar | Güvenlik | 3 | 4 | 12 | Orta | Azalt | Sürekli DAST ve iç güvenlik testi (M3'ten itibaren); S14'te ön pentest; M8'de düzeltme tamponu | S15'te > 3 yüksek bulgu | `SEC` | M8 | Açık |
| R-13 | **Kampanya/promosyon suistimali ve yüksek yanlış pozitifli risk kuralları** → finansal kayıp veya müşteri şikâyeti | İş / risk | 3 | 3 | 9 | Orta | Azalt | Kampanya bütçe tavanı (FR-088); shadow mode (FR-104); cihaz/kart bazlı tekil ödül; kural değişikliğinde maker-checker | Bütçe tüketim hızında sapma, red oranı artışı | `PO` | M5–M6 | Açık |
| R-14 | **SMS OTP teslim oranı düşük / SMS pumping saldırısı** → kayıt dönüşümü düşer, maliyet artar | Operasyon / güvenlik | 3 | 3 | 9 | Orta | Azalt | Çoklu SMS sağlayıcı failover; ülke izin listesi, rate limit, CAPTCHA (FR-018); teslim oranı izleme | Teslim oranı < %95 veya SMS hacminde ani artış | `OPS` | M1 | Açık |
| R-15 | Pilot tenant'ın **mevcut sadakat verisinin göçü** (yıldız bakiyeleri, tier) hatalı olur → müşteri şikâyeti | Veri | 3 | 3 | 9 | Orta | Azalt | Göç provası (dry-run) ve mutabakat raporu; müşteriye bakiye teyit ekranı; geri dönüş planı | Prova mutabakatında fark | `DATA` | M5 | Açık |
| R-16 | **Ekip oluşturma / kilit uzman erişimi** (ledger, ödeme, güvenlik) gecikir veya personel ayrılır → bilgi tek kişiye bağımlı | Kaynak | 3 | 4 | 12 | Orta | Azalt | Eşli çalışma (pairing), ADR ve runbook disiplini, kritik alanlarda en az 2 kişi kuralı; işe alım S0'da tamamlanır | Kilit rolde boşluk > 2 hafta | `DM` | Tümü | Açık |
| R-17 | **Erişilebilirlik ve RTL sorunlarının geç tespiti** → M4/M8'de yeniden çalışma | Kalite | 3 | 3 | 9 | Orta | Azalt | Design system bileşenlerinde a11y + RTL baştan; axe-core CI; her sprint pseudo-localization; S3 prototip testine erişilebilirlik ihtiyacı olan katılımcılar | Kritik a11y ihlali trendi | `UX` | M4 | Açık |
| R-18 | **Çapraz tenant veri sızıntısı** (RLS yanlış yapılandırması, önbellek anahtarı hatası) → ciddi veri ihlali, KVKK bildirimi | Güvenlik / uyum | 2 | 5 | 10 | Orta | Azalt / Kaçın | RLS zorunlu politika + otomatik çapraz-tenant testleri (NFR-048); cache anahtarlarında tenant öneki; ArchUnit kuralları; güvenlik kod incelemesi | Test başarısızlığı, anomali alarmı | `SEC` | M1 → | Açık |
| R-19 | **Yıl sonu izinleri ve resmi tatiller** (S5–S6, S1, S11) → M3 kapasitesi düşer | Takvim | 4 | 2 | 8 | Orta | Kabul / Azalt | Kapasite %80 planlama; kritik yol işlerinin (PSP) S5 başına alınması; izin planlamasının S2'de toplanması | İzin planında kilit rollerin çakışması | `DM` | M3 | Açık |
| R-20 | **GA için ikinci/üçüncü tenant'ların** (EV, otopark/eğlence) onboarding'i gecikir → çoklu tenant pilotu yapılamaz | İş | 3 | 3 | 9 | Orta | Azalt | M5'te tasarım ortaklarıyla sandbox; sektör presetleri; onboarding kontrol listesi; satış hattının M4'ten itibaren izlenmesi | M6 sonunda imzalı ikinci tenant yok | `PO` | M8 | Açık |
| R-21 | **Ledger–PSP mutabakat farkı** (timeout sonrası belirsiz durum, çift bildirim) → finansal fark, denetim bulgusu | Finansal | 3 | 5 | 15 | Yüksek | Azalt | Idempotency (FR-040, FR-061); PSP durum sorgusu ve webhook teyidi; günlük CSV mutabakatı (MVP) ve M7 otomasyonu; invariant alarmı | Açıklanamayan fark > 0 TL | `SA` | M3 → | Açık |
| R-22 | **Pilot tenant'ın POS sağlayıcısı** API entegrasyonu yapamaz/geciktirir → pilot yalnızca Web POS ile sınırlı kalır | Dış bağımlılık | 3 | 3 | 9 | Orta | Azalt | Web POS (FR-075) yedek yol; entegrasyon kiti (sandbox, Postman, örnek kod); POS firmasıyla S2'de teknik toplantı | S6 sonunda POS geliştirmesi başlamamış | `BA` | M3–M4 | Açık |
| R-23 | **Düşük müşteri benimsemesi** (sadakat MVP'de yok) → pilot başarı kriterleri tutmaz, ürün-pazar uyumu sorgulanır | İş | 3 | 4 | 12 | Orta | Azalt | Hoş geldin bonusu; kasada afiş/kasiyer teşviki; kayıt akışı optimizasyonu (UX testleri); M5 sadakatini öne çekme opsiyonu | Açık pilotun 4. haftasında aktif cüzdan < %10 | `PO` | M4–M5 | Açık |
| R-24 | **Kart verisi yanlışlıkla sisteme girer** (log, hata mesajı, destek notu) → PCI DSS kapsamı genişler | Güvenlik / uyum | 2 | 4 | 8 | Orta | Kaçın | PSP hosted alanları/SDK; log maskeleme filtreleri; DLP taraması (NFR-017); destek serbest metin alanlarında PAN deseni engelleme | DLP bulgusu | `SEC` | M3 → | Açık |
| R-25 | **Gözlemlenebilirlik veya olay yönetimi olgunluğu** canlıya geçişte yetersiz → uzun kesinti, SLO ihlali | Operasyon | 2 | 4 | 8 | Orta | Azalt | Gözlemlenebilirlik M1'den itibaren; runbook'lu alarmlar; S8'de oyun günü (game day) tatbikatı; hypercare planı | Alarmın runbook'suz olması, MTTR > 1 saat | `OPS` | M4 | Açık |

---

## 3. Isı Haritası (Baseline)

| Olasılık ↓ / Etki → | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **5** | | | | | |
| **4** | | R-19 | R-08 | R-01, R-03 | |
| **3** | | | R-13, R-14, R-15, R-17, R-20, R-22 | R-04, R-05, R-06, R-09, R-10, R-12, R-16, R-23 | R-02, R-07, R-21 |
| **2** | | | | R-11, R-24, R-25 | R-18 |
| **1** | | | | | |

**Özet:** 25 risk · **Yüksek: 5** (R-01 ve R-03: 16; R-02, R-07, R-21: 15) · **Orta: 20** (skor 12 olan 8 risk üst bantta, yakından izlenir) · Düşük: 0.

---

## 4. Yüksek Riskler için Eylem Planı (S0–S4)

| Risk | Eylem | Sahibi | Hedef tarih |
|---|---|---|---|
| R-03 | PSP kısa listesi (3DS2, tokenizasyon, pre-auth, karta iade, sandbox kalitesi kriterleriyle) ve RFI | `SA` | 2026-10-30 (S1) |
| R-03 | PSP seçimi ve sandbox erişimi | `SA` + `PO` | 2026-11-13 (S2) |
| R-01 | MVP kapsamının Sprint 0 Review'da imzalanması; takas kuralının tüzüğe eklenmesi | `PO` | 2026-10-16 (S0) |
| R-07 | Sınırlı ağ istisnası ve pilot limitleri için hukuki görüş | `CMP` | 2026-10-30 (S1) |
| R-02 | Ledger ADR + hesap planı şablonu + M5 cüzdan tiplerinin model doğrulaması | `SA` | 2026-11-27 (S3) |
| R-21 | Mutabakat tasarımı: timeout/belirsiz durum senaryoları için durum makinesi ve telafi sagaları | `SA` + `QA` | 2026-12-11 (S4) |

---

## 5. Kapanmış / Gerçekleşmiş Riskler

| ID | Tarih | Sonuç | Öğrenim |
|---|---|---|---|
| — | — | Baseline; kapanmış risk yok | — |
