# AEP-CLW — Sektör Konfigürasyon Presetleri

| Alan | Değer |
|---|---|
| Doküman | Sektör bazlı tenant konfigürasyon presetleri |
| Sahibi | Product Owner (`PO`) + Business Analyst (`BA`) |
| Gözden geçiren | `SA` (ödeme/hold), `CMP` (limitler, son kullanma), `SEC` |
| Sürüm | v1.0 — Sprint 0 |
| İlgili FR | FR-005 (preset uygulama), FR-006 (feature flag), FR-009 (son kullanma), FR-036/FR-106 (limitler), FR-062–FR-065 (pre-auth) |

---

## 1. Preset Kavramı

Preset, tenant onboarding'inde (FR-005) seçilen ve **varsayılan konfigürasyonu tek adımda uygulayan** şablondur.

- Preset **kod değil, veridir**: `tenant-service` içinde versiyonlu JSON/YAML olarak tutulur (ör. `preset:coffee:v1`).
- Preset uygulandıktan sonra her değer tenant tarafından değiştirilebilir (plan izin verdiği ölçüde); tenant hangi preset versiyonundan türediğini ve sapmalarını (diff) görür.
- **Regülasyon limitleri presetten bağımsızdır**: tenant limitleri hiçbir zaman regülasyon limitlerini (FR-106) aşamaz; çakışmada düşük olan geçerlidir.
- Tabloda verilen tutarlar **gösterge (varsayılan) değerlerdir**; TRY cinsindendir ve `CMP` onayı ile kesinleşir. MENA tenant'larında para birimine göre yeniden ölçeklenir.
- MVP'de desteklenmeyen özellikler (ör. bileklik) presette `flag=false` + "M5" notuyla yer alır; ilgili milestone'da açılır.

Lejant: **●** varsayılan açık · **○** mevcut, varsayılan kapalı · **–** uygulanmaz · *(Mx)* özellik o milestone'da kullanılabilir

---

## 2. Genel Karşılaştırma

| Boyut | Kahve zinciri | EV şarj | Otopark | Eğlence / oyun parkı | Kampüs / yemekhane |
|---|---|---|---|---|---|
| Preset kodu | `coffee` | `ev_charging` | `parking` | `amusement` | `campus` |
| Tipik işlem tutarı | 80–250 TL | 150–1.500 TL | 30–400 TL | 50–500 TL | 40–150 TL |
| İşlem sıklığı / müşteri | Yüksek (günlük) | Orta (haftalık) | Orta–yüksek | Düşük (ziyaret bazlı), ziyaret içi çok yüksek | Çok yüksek (günlük öğün) |
| Tutar ne zaman belli? | Ödeme anında | **Oturum sonunda** | **Çıkışta** | Ödeme anında | Ödeme anında |
| Birincil akış | Sale | **Pre-auth → capture** | **Pre-auth → capture** / abonelik | Sale (bileklik) | Sale (kısıtlı cüzdan) |
| Temel değer | Hız + sadakat + MDR tasarrufu | Tahsilat güvencesi | Sürtünmesiz geçiş | Nakitsiz park + aile kontrolü | Kurumsal sübvansiyon yönetimi |

---

## 3. Cüzdan Tipleri

| Cüzdan tipi | Kahve | EV | Otopark | Eğlence | Kampüs | Açıklama |
|---|---|---|---|---|---|---|
| MAIN (ana bakiye) | ● | ● | ● | ● | ● | Gerçek parayla yüklenen, iade edilebilir bakiye |
| BONUS (promosyon) | ● | ● | ○ | ● | ○ | İade edilemez; kampanya/cashback kaynaklı |
| GIFT (hediye kartı) *(M5)* | ● | ○ | ○ | ● | – | Hediye kartından aktarılan bakiye |
| SUB (alt / çocuk cüzdanı) *(M5)* | – | – | – | ● | ○ | Ebeveyn tarafından fonlanır, limit/kategori kısıtlı |
| RESTRICTED (yemek / kısıtlı amaç) *(M5)* | – | – | – | – | ● | Sponsor (kurum) fonlu; yalnızca belirli mağaza kategorisi |
| SPONSOR (kurum hesabı) *(M5)* | – | ○ (filo) | ○ (kurumsal abonman) | ○ (okul grubu) | ● | Kurumun toplu yükleme kaynağı |
| Harcama önceliği (FR-030) | BONUS → GIFT → MAIN | BONUS → MAIN | MAIN | SUB (varsa) → BONUS → MAIN | RESTRICTED → BONUS → MAIN | Tenant değiştirebilir |

---

## 4. Ödeme Yöntemleri ve Kanallar

| Yöntem | Kahve | EV | Otopark | Eğlence | Kampüs | Not |
|---|---|---|---|---|---|---|
| Müşteri-sunar QR (FR-056) | ● | ○ | ○ | ○ | ● | MVP |
| İşyeri-sunar QR (FR-067) *(M5)* | ○ | ● (istasyon/soket QR'ı) | ● (giriş/çıkış QR'ı) | ○ | ○ | EV/otoparkta müşteri istasyonu okutur |
| Uygulamadan oturum başlatma (API) | – | ● | ○ | – | – | MVP'de CSMS POS API'yi çağırır |
| Plaka tanıma (LPR/ANPR) entegrasyonu (FR-079) *(M5)* | – | – | ● | – | – | Plaka → cüzdan eşlemesi (FR-176) |
| NFC HCE token (FR-068) *(M5)* | ○ | ○ | – | ○ | ○ | Android HCE; iOS kısıtları değerlendirilecek |
| NFC bileklik / kart (FR-068) *(M5)* | – | ○ (RFID şarj kartı) | ○ | ● | ● (kampüs kartı) | Medya kaybında bloke + bakiye taşıma |
| Web POS (FR-075) | ● | ○ (saha destek) | ○ (kasa kulübesi) | ● | ● | MVP |
| Entegre POS / harici sistem (FR-077) | ● | ● (CSMS) | ● (otopark yönetim sistemi) | ● (turnike/oyun makinesi) | ● (kafeterya POS) | MVP (genel API); adaptörler M5 |
| Kasada nakit yükleme (FR-054) *(M5)* | ○ | – | ○ | ● | ○ | |
| Otomatik yükleme (FR-048) | ● | ● | ● | ○ | ○ | |

---

## 5. Pre-auth (Hold) Kuralları

| Parametre | Kahve | EV | Otopark | Eğlence | Kampüs |
|---|---|---|---|---|---|
| Pre-auth etkin (`pre_auth.enabled`) | – | ● | ● | ○ (ör. kiralama, dolap depozitosu) | – |
| Varsayılan hold tutarı | – | 300 TL (veya istasyon tipine göre: AC 200 TL / DC 500 TL) | Günlük tavan ücret (ör. 250 TL) | Depozito tutarı (ör. 100 TL) | – |
| Hold süresi (otomatik serbest bırakma) | – | 24 saat | 72 saat (uzun süreli park için tenant ayarı ile 7 güne kadar) | Gün sonu (park kapanış + 2 saat) | – |
| Kısmi capture | – | ● | ● | ● | – |
| Çoklu capture | – | – | – | ○ | – |
| Capture toleransı (hold üstü) | – | %0 (aşım için incremental auth) | %0 | %0 | – |
| Incremental auth (FR-064) *(M5)* | – | ● | ○ | – | – |
| Bakiye yetersizse | – | Otomatik yükleme tetikle; olmazsa oturum başlamaz | Otomatik yükleme; olmazsa bilet akışına düş | Görevliye yönlendir | – |
| Capture gelmezse | – | Süre dolumunda serbest bırak + CSMS'e sorgu + operasyon alarmı | Süre dolumunda serbest bırak + "açık oturum" raporu | Gün sonu serbest bırak | – |
| Müşteri bildirimi | – | Hold, capture, serbest bırakma (her adım) | Giriş (hold), çıkış (capture + makbuz) | Hold ve iade | – |

---

## 6. Sadakat Mekaniği *(M5)*

| Parametre | Kahve | EV | Otopark | Eğlence | Kampüs |
|---|---|---|---|---|---|
| Birim | **Yıldız** | kWh bonusu / puan | Puan | Puan / jeton | Puan (opsiyonel) |
| Kazanım kuralı | 1 yıldız / 10 TL (cüzdanla ödemede 2×) | 1 puan / 1 kWh | 1 puan / 10 TL | 1 puan / 5 TL | 1 puan / öğün |
| Ödül | 150 yıldız = ücretsiz içecek; 400 = ücretsiz yiyecek | 100 puan = 10 kWh ücretsiz | 10. giriş ücretsiz | Ücretsiz oyun / hediyelik indirimi | Ücretsiz tatlı / içecek |
| Tier | Green → Gold (yıllık 300 yıldız) | Standart → Premium (aylık 200 kWh) | – (abonelik ile) | Sezon kartı sahibi | – |
| Olay tetikli ödüller | Hoş geldin, doğum günü içeceği, ilk yükleme bonusu | İlk şarj bonusu | İlk abonelik indirimi | Doğum günü partisi paketi | Dönem başı bonusu |
| Cashback | ○ | ● (off-peak şarj cashback) | ○ | ○ | – |
| Kupon | ● | ○ | ● (AVM harcama validation) | ● | ○ |
| Puan son kullanma | 12 ay hareketsizlik | 12 ay | 12 ay | Sezon sonu | Akademik yıl sonu |

---

## 7. Limitler (Gösterge Varsayılanlar)

> Regülasyon limitleri (FR-106) her zaman önceliklidir. Aşağıdaki değerler **tenant limitleri**dir.

| Limit | Kahve | EV | Otopark | Eğlence | Kampüs |
|---|---|---|---|---|---|
| Maks. bakiye — Tier0 | 1.000 TL | 2.000 TL | 1.500 TL | 2.000 TL | 1.000 TL |
| Maks. bakiye — Tier1 | 5.000 TL | 10.000 TL | 5.000 TL | 5.000 TL | 3.000 TL |
| Tek yükleme min / maks | 50 / 2.000 TL | 100 / 5.000 TL | 50 / 2.000 TL | 100 / 3.000 TL | 25 / 1.000 TL |
| Önerilen yükleme tutarları | 150 / 250 / 500 | 500 / 1.000 / 2.000 | 200 / 500 / 1.000 | 300 / 500 / 1.000 | 100 / 200 / 500 |
| Aylık yükleme tavanı (Tier1) | 10.000 TL | 20.000 TL | 10.000 TL | 10.000 TL | 5.000 TL |
| Tek ödeme maks. | 1.000 TL | 2.500 TL | 1.000 TL | 1.500 TL | 300 TL |
| Günlük ödeme adedi | 20 | 10 | 20 | 100 | 10 |
| Otomatik yükleme eşiği / tutarı (öneri) | 50 / 250 TL | 300 / 1.000 TL | 100 / 500 TL | – | – |
| Alt cüzdan günlük limit *(M5)* | – | – | – | 400 TL (ebeveyn ayarlar) | ○ |
| Kısıtlı cüzdan günlük öğün limiti *(M5)* | – | – | – | – | 2 öğün / 250 TL |
| Velocity: 10 dk içinde farklı kart ile yükleme | ≤ 2 | ≤ 2 | ≤ 2 | ≤ 3 | ≤ 2 |
| Velocity: 1 saatte başarısız yükleme | ≤ 5 | ≤ 5 | ≤ 5 | ≤ 5 | ≤ 5 |
| İade eşiği (StoreMgr onayı gerektiren) | 250 TL | 500 TL (operasyon ekibi) | 250 TL | 300 TL | 150 TL |

---

## 8. Son Kullanma ve Breakage Kuralları

| Kural | Kahve | EV | Otopark | Eğlence | Kampüs |
|---|---|---|---|---|---|
| MAIN bakiye | Süresiz (hareketsizlikte bildirim, 24 ay) | Süresiz | Süresiz | Süresiz **veya** sezonluk (tenant seçimi; sezon sonunda iade/devir seçeneği) | Süresiz (kişisel yükleme) |
| BONUS bakiye | 90 gün | 90 gün | 60 gün | Ziyaret günü sonu / 30 gün | Dönem sonu |
| GIFT bakiye *(M5)* | Yasal minimum ve tenant politikasına göre (ör. 24 ay) | ○ | ○ | 12 ay | – |
| RESTRICTED (yemek) *(M5)* | – | – | – | – | Ay sonu sıfırlama **veya** bir sonraki aya devir (sponsor kuralı); sıfırlanan tutar sponsora iade edilir |
| Hareketsiz hesap tanımı | 12 ay işlem yok | 12 ay | 12 ay | 18 ay | Mezuniyet / işten ayrılma |
| Son kullanma bildirimi | 30 ve 7 gün önce | 30 ve 7 gün önce | 30 gün önce | 14 gün önce | 7 gün önce |
| Breakage muhasebesi *(M7)* | Süresi dolan BONUS/GIFT → breakage gelir hesabı; MAIN için yasal süre sonrası politika | Aynı | Aynı | Aynı | Sponsor iadesi (breakage değil) |

---

## 9. Diğer Varsayılanlar

| Parametre | Kahve | EV | Otopark | Eğlence | Kampüs |
|---|---|---|---|---|---|
| Mağaza kategorisi (FR-074) | `cafe` | `charging_station` | `parking_lot` | `ride`, `fnb`, `retail` | `cafeteria` |
| Varsayılan KYC seviyesi (kayıt sonrası) | Tier0 | Tier1 (fatura için ad-soyad) | Tier0 (+ plaka) | Tier0 (ebeveyn Tier1) | Tier1 (kurum kimlik no ile) |
| Toplu müşteri aktarımı (FR-025) | ○ | ○ | ○ (kurumsal abone) | ○ (okul grupları) | ● |
| Abonelik (FR-066) *(M5)* | ○ (kahve aboneliği) | ○ (kWh paketi) | ● | ○ (sezon kartı) | – |
| Müşteri bildirimi — her işlemde push | ● | ● | ● | ● (ebeveyne alt cüzdan hareketi) | ○ |
| Makbuz / fatura bilgisi | Dijital makbuz | Oturum detaylı makbuz (kWh, süre, tarife) | Giriş/çıkış saati, süre, plaka | Dijital makbuz | Öğün özeti |
| Offline QR token (FR-168) | ● (bodrum kat mağazalar) | – | ○ | ● (park içi kapsama) | ● |
| Dil / RTL | TR, EN | TR, EN | TR, EN | TR, EN, AR (turistik parklar) | TR, EN |

---

## 10. Preset Doğrulama (QA)

Her preset için otomatik testler:
1. Preset uygulandığında tüm zorunlu konfigürasyon anahtarları dolu olmalı.
2. Hiçbir tenant limiti regülasyon limitini aşmamalı (aşan değer uyarı ile regülasyon limitine indirilir).
3. Preset'te açık olan flag'ler tenant planında mevcut olmalı (ör. Starter planda `amusement` preseti SUB cüzdanı açamaz → uyarı).
4. Sektöre özgü uçtan uca senaryo (ör. `ev_charging`: hold → kısmi capture → serbest bırakma) sandbox'ta yeşil olmalı.
