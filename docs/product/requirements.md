# AEP-CLW — Gereksinimler (Fonksiyonel & Fonksiyonel Olmayan)

| Alan | Değer |
|---|---|
| Doküman | Gereksinim Spesifikasyonu |
| Sahibi | Product Owner (`PO`) |
| Hazırlayan | Business Analyst ×2 (`BA`) |
| Gözden geçiren | `CA`, `SA`, `SEC`, `CMP`, `AUD`, `QA` |
| Sürüm | v1.0 — Sprint 0 |
| Kapsam | 185 fonksiyonel gereksinim (FR-001 … FR-185), 50 fonksiyonel olmayan gereksinim (NFR-001 … NFR-050) |

---

## 0. Okuma Kılavuzu

### 0.1 Kimlik ve izlenebilirlik

- **FR-xxx**: Fonksiyonel gereksinim. Numara **kalıcıdır**; silinen gereksinim numarası yeniden kullanılmaz, durumu `Deprecated` olarak işaretlenir.
- **NFR-xxx**: Fonksiyonel olmayan gereksinim.
- Her FR, [Fonksiyon Matrisi](function-matrix.md) içinde bir veya daha fazla **FN-xxx** fonksiyonuna, GitHub Issues'ta bir **Story**'ye eşlenir (`fr:FR-xxx` etiketi).
- Kabul kriterleri burada **özet** düzeydedir; tam Gherkin senaryoları Story seviyesinde yazılır (Definition of Ready şartı).

### 0.2 Öncelik (MoSCoW)

| Kod | Anlam | Kural |
|---|---|---|
| **M** | Must | Hedef milestone'un çıkış kriteri; eksikse milestone kapanmaz |
| **S** | Should | Güçlü beklenti; kapasite sıkışırsa bir sonraki milestone'a kayabilir (PO onayı ile) |
| **C** | Could | Kapasite olursa; değer/efor oranına göre |
| **W** | Won't (bu sürümde) | v2.0 GA kapsamı dışı; kayıt amaçlı tutulur |

> Öncelik **hedef milestone'a göredir**: M5'e atanmış bir "M", MVP için zorunlu değildir, M5 için zorunludur.

### 0.3 Milestone referansı

| MS | Ad | Sprintler |
|---|---|---|
| M1 | Platform Foundation | S1–S2 |
| M2 | Core Wallet & Ledger | S3–S4 |
| M3 | Funding & Payments | S5–S6 |
| M4 | Admin Portal, Reporting & Audit → **MVP v1.0** | S7–S8 |
| M5 | Loyalty, Campaigns & Gift Cards | S9–S10 |
| M6 | Risk, AML & Compliance | S11–S12 |
| M7 | Settlement, Accounting & Bank Integrations | S13–S14 |
| M8 | Production Hardening & **GA v2.0** | S15–S16 |

### 0.4 Ortak terimler

| Terim | Tanım |
|---|---|
| Tenant | Platformu kullanan marka/kurum (ör. kahve zinciri) |
| Cüzdan (wallet) | Bir müşteriye ait, ledger'da bir veya daha fazla hesapla temsil edilen bakiye kabı |
| Hold | Kullanılabilir bakiyeden geçici olarak ayrılan tutar (pre-auth) |
| Capture | Hold'un kesin tahsilata dönüşmesi |
| Maker-checker | Bir kullanıcının başlattığı kritik işlemin farklı bir yetkili tarafından onaylanması |
| Breakage | Kullanılmayacağı öngörülen / süresi dolan bakiye |
| Tier0 / Tier1 / Tier2 | KYC seviyeleri: Tier0 = doğrulanmış telefon; Tier1 = ad-soyad + doğum tarihi + e-posta beyanı; Tier2 = kimlik numarası doğrulaması (eKYC) |

---

## 1. Fonksiyonel Gereksinimler

### 1.1 Tenant Yönetimi (`tenant-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-001 | Platform Admin yeni bir tenant oluşturabilmeli (ad, ticari unvan, vergi no, ülke, bölge, plan, izolasyon modu). | Tenant benzersiz `tenant_id` ve slug alır; Keycloak organizasyonu otomatik oluşur; işlem audit log'a yazılır. | M | M1 |
| FR-002 | Tenant yaşam döngüsü yönetilebilmeli: `Draft → Onboarding → Active → Suspended → Terminated`. | Suspended tenant'ta finansal işlemler reddedilir, bakiye sorgusu çalışır; geçişler maker-checker ile yapılır. | M | M1 |
| FR-003 | Tenant temel konfigürasyonu: para birimi (ISO 4217), saat dilimi, varsayılan dil, desteklenen diller, hafta başlangıcı. | Konfigürasyon versiyonlanır; geçmiş versiyonlar görüntülenebilir; aktif tenant'ta para birimi değiştirilemez. | M | M1 |
| FR-004 | Tenant marka/tema tanımı: logo, renk paleti, tipografi, uygulama adı, e-posta alt bilgisi. | Tema değişikliği Admin Portal ve e-posta şablonlarına 5 dk içinde yansır; kontrast oranı WCAG AA altındaysa uyarı verilir. | M | M1 |
| FR-005 | Onboarding sırasında sektör preseti (Kahve / EV / Otopark / Eğlence / Kampüs) seçilebilmeli ve varsayılan konfigürasyonu uygulamalı. | Preset uygulandıktan sonra tüm değerler tek tek düzenlenebilir; hangi presetin uygulandığı kayıt altındadır. | S | M1 |
| FR-006 | Tenant bazlı feature flag yönetimi (ör. `pre_auth.enabled`, `auto_topup.enabled`, `p2p.enabled`). | Flag değişiklikleri çalışma zamanında (yeniden deploy olmadan) ≤ 60 sn içinde etkin olur; plan dışı özellik açılamaz. | M | M1 |
| FR-007 | Plan/abonelik ve kota tanımı (aktif cüzdan, mağaza, terminal, API çağrı kotası). | Kota %80 ve %100 eşiklerinde TenantAdmin ve PlatformAdmin'e bildirim; kota aşımı ödeme yolunu **bloklamaz**, faturalamaya yansır. | S | M1 |
| FR-008 | Tenant ücret tanımları: yükleme ücreti, işlem ücreti, hesap bakım ücreti (varsayılan kapalı). | Ücretler ledger'da ayrı gelir hesaplarına kaydolur; ücret değişikliği ileri tarihli yürürlükle ve maker-checker ile yapılır. | S | M3 |
| FR-009 | Son kullanma ve breakage kuralları konfigürasyonu (cüzdan tipi bazında: süresiz, X ay hareketsizlik, sabit tarih). | Kural değişikliği yalnızca ileriye dönük uygulanır; müşteri bildirimi için ön-süre (ör. 30 gün) tanımlanır. | S | M2 |
| FR-010 | Tenant veri izolasyon modu: paylaşılan DB + Row Level Security (varsayılan) veya dedicated DB. | Hiçbir API çağrısı başka bir tenant'ın verisini döndüremez (otomatik çapraz-tenant testleri CI'da); dedicated DB M8'de devreye alınır. | M | M1 |

### 1.2 Kimlik & Erişim (`identity-service`, Keycloak)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-011 | Son müşteri telefon numarası + SMS OTP ile kayıt olabilmeli ve giriş yapabilmeli. | OTP 6 hane, 180 sn geçerli, tek kullanımlık; E.164 formatı doğrulanır; aynı telefon aynı tenant'ta tek hesap. | M | M1 |
| FR-012 | Cihaz bağlama (device binding): hesap güvenilir cihaza bağlanır, yeni cihazda ek doğrulama istenir. | Cihaz anahtarı cihazın güvenli deposunda (Keychain/Keystore) tutulur; bir hesapta en fazla N (varsayılan 2) aktif cihaz. | M | M1 |
| FR-013 | Uygulama kilidi: PIN ve/veya biyometrik doğrulama; finansal işlem öncesi step-up doğrulama. | Tenant eşiği (ör. 1.000 TL üzeri yükleme) üzerinde biyometri/PIN zorunlu; 5 hatalı PIN'de geçici kilit. | S | M4 |
| FR-014 | Oturum yönetimi: kısa ömürlü access token, refresh token rotasyonu, uzaktan oturum sonlandırma. | Access token ≤ 5 dk, refresh token rotasyonlu; müşteri/destek "tüm cihazlardan çıkış" yapabilir. | M | M1 |
| FR-015 | Personel (Admin Portal, Web POS) kullanıcıları için kimlik doğrulama ve zorunlu MFA (TOTP/WebAuthn). | Admin rolleri için MFA zorunlu; kasiyer için mağaza cihazına bağlı PIN girişi desteklenir. | M | M1 |
| FR-016 | E-posta ile kayıt ve sosyal giriş (Apple, Google) — tenant tercihiyle açılır. | Sosyal giriş sonrası telefon doğrulaması finansal işlem için yine zorunludur. | C | M5 |
| FR-017 | Hesap kurtarma / cihaz değişimi: yeni cihazda OTP + ek bilgi (doğum tarihi veya e-posta kodu) ile doğrulama. | Cihaz değişiminden sonra 24 saat boyunca düşük limit uygulanır (risk kuralı ile birlikte). | M | M2 |
| FR-018 | OTP ve giriş uç noktaları için kötüye kullanım koruması (rate limit, SMS pumping koruması, CAPTCHA). | Telefon/IP/cihaz başına dakikalık ve günlük sınırlar; ülke kodu izin listesi; olay metriği ve alarm. | M | M1 |

### 1.3 Müşteri & KYC (`customer-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-019 | Müşteri profili oluşturma/güncelleme (ad, soyad, doğum tarihi, e-posta, dil tercihi). | Profil değişiklikleri versiyonlanır ve audit log'a yazılır; e-posta doğrulama linki gönderilir. | M | M2 |
| FR-020 | KVKK/GDPR onay yönetimi: aydınlatma metni, açık rıza, ticari ileti izni; versiyonlu metin. | Hangi metin versiyonuna, ne zaman, hangi kanaldan onay verildiği saklanır; rıza geri alınabilir. | M | M2 |
| FR-021 | KYC seviyeleri Tier0 ve Tier1 yönetimi; seviye geçişinde limitlerin otomatik güncellenmesi. | Tier0: telefon doğrulandı; Tier1: zorunlu profil alanları tamamlandı; seviye limit tablosu tenant + regülasyon kaynaklı. | M | M2 |
| FR-022 | Tier2 KYC: kimlik numarası doğrulaması ve/veya harici eKYC sağlayıcı entegrasyonu. | Doğrulama sonucu ve kanıt referansı saklanır; başarısız denemeler sınırlandırılır. | S | M6 |
| FR-023 | Müşteri durum yönetimi: `Active`, `Restricted`, `Blocked`, `Closed`; durum değişikliği gerekçe kodu ile. | Blocked müşteride ödeme/yükleme reddedilir; durum değişikliği müşteriye bildirilir (fraud durumları hariç). | M | M2 |
| FR-024 | Müşteri hesap kapatma ve kalan ana bakiyenin iadesi (karta/IBAN'a) veya tenant kuralına göre işlenmesi. | Bonus/promosyon bakiyesi iade edilmez; iade maker-checker ile; hesap kapatma sonrası PII saklama süresine göre anonimleşir. | S | M4 |
| FR-025 | Toplu müşteri aktarımı (CSV/API) — kampüs, kurumsal program ve göç senaryoları. | Satır bazında doğrulama raporu; kısmi başarı desteklenir; idempotent tekrar yükleme. | S | M5 |
| FR-026 | Veri sahibi talepleri (KVKK md. 11 / GDPR): erişim, düzeltme, silme/anonimleştirme talepleri iş akışı. | Talep 30 gün SLA sayacı ile takip edilir; yasal saklama yükümlülüğü olan veriler silinmez, kısıtlanır. | S | M6 |

### 1.4 Cüzdan (`wallet-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-027 | Müşteri kaydında ana cüzdan (MAIN) otomatik açılmalı. | Cüzdan, ledger'da müşteri yükümlülük hesabı ile 1:1 eşlenir; açılış idempotenttir. | M | M2 |
| FR-028 | Bonus/promosyon cüzdanı (BONUS): iade edilemez, ayrı son kullanma kuralı olan bakiye. | Bonus bakiye ayrı ledger hesabında; raporlarda ana bakiyeden ayrı gösterilir. | M | M2 |
| FR-029 | Bakiye sorgulama: toplam, kullanılabilir, bloke (hold), cüzdan tipi bazında. | Bakiye yanıtı p95 ≤ 100 ms; ledger ile tutarlı (bkz. NFR-026). | M | M2 |
| FR-030 | Harcama önceliği kuralı: ödeme sırasında cüzdanlardan düşüm sırası (ör. önce BONUS, sonra MAIN). | Kural tenant bazlıdır; tek ödeme birden fazla cüzdandan karşılanabilir ve ledger'da ayrıntılı gösterilir. | S | M2 |
| FR-031 | Alt cüzdan (sub-wallet): bir ana cüzdan sahibinin başka bir kullanıcı/bileklik için alt cüzdan açması. | Alt cüzdan bakiyesi ebeveyn tarafından yüklenir/geri çekilir; alt cüzdan kendi başına dış yükleme yapamaz (konfigüre edilebilir). | C | M5 |
| FR-032 | Aile cüzdanı kontrolleri: alt cüzdan için günlük/işlem limiti, kategori kısıtı, zaman penceresi, anlık bildirim. | Kural ihlalinde ödeme reddedilir ve ebeveyne bildirim gider. | C | M5 |
| FR-033 | Kısıtlı amaçlı cüzdan (ör. yemek bakiyesi): yalnızca belirli mağaza kategorisinde harcanabilir; sponsor (kurum) kaynaklı. | Kategori dışı ödemede ret; dönem sonu sıfırlama/devretme kuralı; sponsor bazlı kullanım raporu. | S | M5 |
| FR-034 | Hold yönetimi: hold oluşturma, sorgulama, süre tanımı, süre dolumunda otomatik serbest bırakma. | Hold'lar kullanılabilir bakiyeden düşer; süre dolan hold ≤ 5 dk içinde serbest kalır ve müşteri bilgilendirilir. | M | M2 |
| FR-035 | Cüzdan dondurma/çözme (müşteri talebi, destek, risk). | Donmuş cüzdanda ödeme/yükleme reddedilir; iade (credit) kabul edilir; her işlem gerekçe kodu ile loglanır. | M | M2 |
| FR-036 | Cüzdan limitleri: maksimum bakiye, tek seferde yükleme, aylık yükleme; KYC seviyesine bağlı. | Limit kontrolü senkron ve atomik; limit aşımında anlaşılır hata kodu (`LIMIT_EXCEEDED`) döner. | M | M2 |

### 1.5 Defter (Ledger) (`ledger-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-037 | Çift kayıtlı, append-only journal: her finansal olay borç = alacak olan dengeli kayıt setidir. | Dengesiz kayıt reddedilir; kayıtlar güncellenemez/silinemez (DB seviyesinde yetki ile garanti). | M | M2 |
| FR-038 | Tenant bazlı hesap planı (chart of accounts): müşteri yükümlülük, işyeri alacak, PSP takas, ücret geliri, breakage, sponsor hesapları. | Hesap planı şablonu presetten gelir; hesap tipi (asset/liability/income/expense) ve normal bakiye yönü tanımlıdır. | M | M2 |
| FR-039 | Gerçek zamanlı hesap bakiyesi hesaplama (kayıt anında güncellenen bakiye + tarihsel bakiye sorgusu). | Herhangi bir tarihteki bakiye sorgulanabilir (point-in-time); negatif bakiyeye izin verilmeyen hesaplarda kısıt. | M | M2 |
| FR-040 | Idempotent kayıt (posting): aynı iş anahtarı ile gelen tekrar istek yeni kayıt oluşturmaz. | Tekrar istek ilk sonucu döndürür; eşzamanlı çift istekte tek kayıt oluşur (yarış testleri). | M | M2 |
| FR-041 | Düzeltmeler yalnızca ters kayıt (reversal) ve düzeltme kaydı ile; manuel düzeltme maker-checker gerektirir. | Orijinal kayıt referansı zorunlu; manuel düzeltme gerekçe + ek + iki farklı yetkili. | M | M2 |
| FR-042 | Günlük/sürekli defter bütünlük kontrolü: toplam borç = toplam alacak, cüzdan görünümü = ledger bakiyesi. | Fark tespitinde P1 alarm; kontrol sonuçları raporlanır ve audit'e yazılır. | M | M2 |
| FR-043 | Çoklu para birimi desteği (tenant bazında birden fazla para birimi; kur çevrimi yok, para birimi başına ayrı hesap). | Farklı para birimleri tek journal satırında karıştırılamaz. | C | M8 |
| FR-044 | Journal sorgulama ve drill-down: rapor satırından journal kaydına, oradan kaynak işleme. | Finance rolü journal'ı işlem id, hesap, tarih aralığı ile sorgular; sonuç CSV olarak alınabilir. | S | M4 |

### 1.6 Para Yükleme (`funding-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-045 | Banka/kredi kartı ile 3DS doğrulamalı bakiye yükleme. | Kart verisi platforma girmez (PSP hosted/SDK tokenizasyon); başarılı yüklemede ledger kaydı ve bildirim; yarım kalan 3DS oturumu 15 dk sonra iptal. | M | M3 |
| FR-046 | PSP adaptör mimarisi: MVP'de 1 gerçek PSP adaptörü + test/demo için mock PSP. | Adaptör port arayüzü ile ikinci PSP kodu değişmeden eklenebilir; mock PSP başarı/red/timeout senaryolarını simüle eder. | M | M3 |
| FR-047 | Kayıtlı kart: PSP token ile kart saklama, listeleme, silme, varsayılan kart seçimi. | Yalnızca maskeli PAN (son 4), marka, son kullanma gösterilir; kart silme PSP token'ını da iptal eder. | S | M3 |
| FR-048 | Otomatik yükleme: bakiye eşik altına düştüğünde kayıtlı karttan belirlenen tutarda yükleme. | Müşteri eşik/tutar/aylık tavan belirler; başarısız 3 denemede otomatik yükleme durur ve bildirim gider. | S | M3 |
| FR-049 | Yükleme tutar kuralları: min/max, önerilen tutar butonları, KYC limit kontrolü. | Kurallar tenant konfigürasyonundan okunur; limit aşımı yükleme başlamadan reddedilir. | M | M3 |
| FR-050 | Yükleme iptali/iadesi: kullanılmamış yükleme tutarının kaynağa (karta) iadesi. | Yalnızca harcanmamış bakiye iade edilebilir; iade tutarı ledger'da ters kayıt; PSP refund referansı saklanır. | S | M3 |
| FR-051 | Banka havalesi/EFT ile yükleme (müşteriye özel referans kodu veya sanal IBAN). | Banka hareketinden referans eşleşmesi ile otomatik yükleme; eşleşmeyenler istisna kuyruğuna. | C | M7 |
| FR-052 | Açık bankacılık (ödeme başlatma) ile yükleme. | Yetkili aracı üzerinden ödeme başlatma; sonuç webhook ile teyit edilir. | C | M8 |
| FR-053 | Kurumsal/sponsor toplu yükleme (ör. kampüs yemek bakiyesi, işveren yan hakkı). | CSV/API ile toplu yükleme talebi; maker-checker; sponsor hesabından cüzdanlara transfer; satır bazında sonuç raporu. | S | M5 |
| FR-054 | Kasada nakit yükleme (cash-in): kasiyerin müşteri cüzdanına nakit karşılığı bakiye yüklemesi. | Kasiyer/mağaza bazlı günlük limit; kasa kapanış raporunda ayrı satır; mağaza nakit hesabı ledger'da. | C | M5 |
| FR-055 | Çoklu PSP yönlendirme ve failover (maliyet/başarı oranına göre). | Kural bazlı yönlendirme; birincil PSP hata oranı eşiği aşarsa ikincile geçiş. | S | M7 |

### 1.7 Ödeme (`payment-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-056 | Müşteri-sunar QR ile ödeme: uygulama dinamik, kısa ömürlü, imzalı QR token üretir; POS okutur. | Token ≤ 60 sn geçerli, tek kullanımlık, cihaza bağlı; kopyalanmış/tekrar kullanılan token reddedilir. | M | M3 |
| FR-057 | Ödeme yetkilendirme kontrolleri: cüzdan/müşteri/mağaza/terminal durumu, bakiye, limit, velocity. | Kontroller tek transaction bağlamında; red nedenleri standart kod seti ile döner. | M | M3 |
| FR-058 | Tek adımlı satış (sale = authorize + capture). | Başarılı satışta müşteri yükümlülük hesabı borç, işyeri hesabı alacak; POS'a yanıt p95 ≤ 300 ms. | M | M3 |
| FR-059 | İptal (void): aynı iş günü, takas öncesi işlemin iptali. | Void yalnızca orijinal terminal/mağaza ve yetkili rol ile; tam tutar; ledger ters kayıt. | M | M3 |
| FR-060 | İade (refund): tam veya kısmi, orijinal işleme referanslı. | Toplam iade ≤ orijinal tutar; eşik üstü iadelerde StoreMgr onayı; iade orijinal cüzdan dağılımına göre yapılır. | M | M3 |
| FR-061 | Ödeme idempotency ve durum sorgulama (timeout sonrası POS'un sonucu öğrenebilmesi). | `Idempotency-Key` başlığı zorunlu; 24 saat saklanır; durum sorgusu kesin sonucu döner. | M | M3 |
| FR-062 | Pre-auth: tahmini/tavan tutar için hold oluşturma (EV şarj, otopark). | Hold süresi tenant/sektör bazında (ör. EV 24 saat, otopark 72 saat); hold anında kullanılabilir bakiye düşer. | M | M3 |
| FR-063 | Capture: hold'a karşı tam veya kısmi tahsilat; kalan hold'un anında serbest bırakılması. | Capture tutarı ≤ hold (+ tenant toleransı); tek veya çoklu capture (konfigüre); ledger'da hold ve capture ayrıntılı. | M | M3 |
| FR-064 | Incremental authorization: aktif hold tutarının artırılması (ör. şarj süresi uzarsa). | Ek tutar için bakiye/limit kontrolü; başarısızsa mevcut hold korunur, harici sisteme bildirim. | S | M5 |
| FR-065 | Hold iptali ve süre dolumunda otomatik serbest bırakma (capture gelmezse). | İptal/serbest bırakma müşteriye bildirilir; süre dolan hold'lar için operasyon raporu ve alarm. | M | M3 |
| FR-066 | Abonelik tahsilatı: periyodik ücretin (ör. otopark aylık abonelik) cüzdandan otomatik tahsili. | Yetersiz bakiyede otomatik yükleme tetiklenir veya tolerans süresi + bildirim; abonelik durumu harici sisteme iletilir. | S | M5 |
| FR-067 | İşyeri-sunar QR ile ödeme: mağaza/terminal QR'ını müşteri uygulamayla okutur, tutarı onaylar. | Dinamik (tutar içeren) ve statik QR desteklenir; terminal onayı push/webhook ile gelir. | S | M5 |
| FR-068 | NFC (HCE token), fiziksel kart ve bileklik ile ödeme. | Medya (bileklik/kart) cüzdana bağlanır, kayıpta bloke edilir; offline limit tenant kuralına bağlı. | C | M5 |
| FR-069 | Bölünmüş ödeme: tutarın bir kısmı cüzdandan, kalanı kartla. | POS tarafında iki bacaklı işlem; iade her bacağa orantılı. | C | M8 |
| FR-070 | Müşteriler arası (P2P) bakiye transferi. | Sınırlı ağ modeli ve regülasyon nedeniyle v2.0 kapsamı dışı; flag kapalı. | W | – |

### 1.8 İşyeri & POS (`merchant-service`, `pos-bff`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-071 | İşyeri → mağaza → terminal hiyerarşisinin tanımlanması ve yönetimi. | Her seviye durum (aktif/pasif) taşır; üst seviye pasifse alt seviye işlem yapamaz; toplu CSV içe aktarım. | M | M3 |
| FR-072 | Terminal kaydı, aktivasyon kodu ile eşleme ve terminal kimlik bilgisi (API anahtarı / client credential) yönetimi. | Anahtar yalnızca oluşturulurken bir kez gösterilir; rotasyon ve iptal; terminal son görülme zamanı. | M | M3 |
| FR-073 | Kasiyer kullanıcıları ve mağaza cihazında PIN ile giriş; kasiyer bazlı işlem izleme. | Her işlem kasiyer kimliği ile ilişkilendirilir; kasiyer yalnızca atandığı mağazada işlem yapar. | M | M3 |
| FR-074 | Mağaza nitelikleri: adres, konum, çalışma saatleri, kategori (yemek, oyun, şarj, otopark vb.). | Kategori, kısıtlı cüzdan ve kampanya kurallarında kullanılabilir. | S | M3 |
| FR-075 | Web POS: tutar girişi, kamera/tarayıcı ile müşteri QR okutma ve ödeme alma. | Tarayıcıda çalışır (tablet uyumlu); büyük onay ekranı; ağ hatasında durum sorgusu ile sonuç netleştirme. | M | M3 |
| FR-076 | Web POS: iptal, iade, işlem listesi, kasiyer vardiya ve mağaza gün sonu raporu. | İade eşik üstünde müdür onayı; gün sonu raporu ledger toplamları ile uyumlu. | M | M3 |
| FR-077 | POS REST API: ödeme, pre-auth, capture, iptal, iade, durum sorgu, bakiye sorgu (müşteri izni ile). | OpenAPI 3.1 sözleşmesi; contract testleri (Pact); geriye dönük uyumlu versiyonlama. | M | M3 |
| FR-078 | POS ve harici sistemlere webhook ile işlem sonucu bildirimi. | HMAC imzalı; üstel geri çekilmeli yeniden deneme; teslim edilemeyenler için yeniden gönderim ekranı. | S | M3 |
| FR-079 | Harici sistem adaptörleri: EV CSMS, otopark LPR/bariyer, turnike/erişim kontrol entegrasyon şablonları. | Olay eşlemesi (oturum başladı/bitti, giriş/çıkış) standart API'ye; en az 1 referans entegrasyon her sektör için. | S | M5 |

### 1.9 Sadakat & Kampanya (`loyalty-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-080 | Puan/yıldız kazanım kuralları (tutar bazlı, işlem bazlı, ürün/kategori bazlı). | Kazanım ödeme capture sonrası; iade durumunda orantılı geri alınır. | M | M5 |
| FR-081 | Ödül kataloğu ve puan/yıldız harcama (ör. 150 yıldız = ücretsiz içecek). | Ödül kullanımı POS'ta kupon/indirim olarak uygulanır; puan ledger'ı ayrı (non-monetary) hesapta. | M | M5 |
| FR-082 | Seviye (tier) yönetimi: eşikler, değerlendirme dönemi, seviye avantajları. | Tier yükselişi/düşüşü bildirilir; seviyeye özel kazanım çarpanı. | S | M5 |
| FR-083 | Kampanya kural motoru: koşul (segment, mağaza, zaman, tutar, ürün) → aksiyon (bonus, çarpan, kupon, cashback). | Kural öncelik ve birleştirilebilirlik (stacking) kuralları; yayın öncesi önizleme; maker-checker. | M | M5 |
| FR-084 | Kupon üretimi (tekil/toplu), dağıtımı ve kullanımı. | Kupon tek kullanımlık/çok kullanımlık, geçerlilik tarihi, kişi başı limit. | S | M5 |
| FR-085 | Cashback: ödeme sonrası bonus cüzdana kampanya bazlı iade. | Cashback kampanya bütçe hesabından fonlanır; iade halinde geri alınır. | S | M5 |
| FR-086 | Olay tetikli ödüller: hoş geldin, doğum günü, ilk yükleme, N. ziyaret. | Tetikleyici olaylar Kafka üzerinden; müşteri başına tekil ödül garantisi. | S | M5 |
| FR-087 | Segment tanımı (kural bazlı: harcama, sıklık, son ziyaret, tier, konum). | Segment boyutu önizlenir; kampanyada hedefleme için kullanılır. | S | M5 |
| FR-088 | Kampanya bütçesi, kişi başı tavan ve kötüye kullanım sınırları. | Bütçe tükenince kampanya otomatik durur; bütçe tüketimi gerçek zamanlı izlenir. | M | M5 |
| FR-089 | Puan son kullanma kuralları ve önceden bildirim. | Süresi dolacak puanlar için X gün önce bildirim; son kullanma işlemi raporlanır. | S | M5 |

### 1.10 Hediye Kartı (`voucher-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-090 | Dijital hediye kartı satın alma ve alıcıya gönderme (uygulama içi, SMS/e-posta ile). | Kişisel mesaj ve tasarım seçimi; alıcı uygulamaya sahip değilse link ile talep. | M | M5 |
| FR-091 | Hediye kartı kodu üretimi: tekil ve toplu (B2B kurumsal sipariş), tahmin edilemez kod + PIN. | Kodlar kriptografik rastgele; toplu üretim dosyası şifreli teslim; maker-checker. | S | M5 |
| FR-092 | Hediye kartı aktivasyonu ve bakiye sorgulama (POS, uygulama, web). | Aktive edilmemiş kart harcanamaz; bakiye sorgusu rate limit ile brute-force'a karşı korunur. | M | M5 |
| FR-093 | Hediye kartını cüzdana ekleme (redeem to GIFT wallet). | Bakiye GIFT cüzdanına transfer edilir; kart tek cüzdana bağlanır. | M | M5 |
| FR-094 | Fiziksel hediye kartı POS'ta satış anında aktivasyon. | Aktivasyon ödeme ile atomik; iptal edilen satışta kart pasifleşir. | S | M5 |
| FR-095 | Hediye kartı son kullanma ve breakage kaydı. | Son kullanma yasal minimumlara uygun konfigüre edilir; süresi dolan bakiye breakage hesabına. | S | M5 |
| FR-096 | Hediye kartı bloke/iptal/yeniden basım (kayıp/çalıntı). | Bloke ve bakiye taşıma maker-checker ile; eski kod kalıcı olarak geçersiz. | S | M5 |

### 1.11 Risk & Fraud (`risk-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-097 | Temel limit kuralları: işlem başı, günlük, aylık tutar ve adet limitleri (müşteri, kart, terminal bazlı). | Limitler konfigürasyon ile değişir; kontrol ödeme ve yükleme yolunda senkron ve ≤ 20 ms ek gecikme. | M | M3 |
| FR-098 | Temel velocity kuralları: kısa zaman penceresinde yükleme/ödeme sayısı, farklı kart sayısı, başarısız deneme sayısı. | Redis tabanlı sayaçlar; tetiklenme olayı loglanır ve raporlanır. | M | M3 |
| FR-099 | Yapılandırılabilir gerçek zamanlı kural motoru (koşul-aksiyon: onay, red, inceleme, step-up). | Kurallar deploy gerektirmeden yayınlanır; versiyonlu; maker-checker. | S | M6 |
| FR-100 | İşlem risk skoru (kural + davranışsal sinyaller). | Skor her karar kaydında saklanır; eşik tenant bazlı. | S | M6 |
| FR-101 | Cihaz parmak izi ve cihaz itibarı (root/jailbreak, emülatör, cihaz başına hesap sayısı). | Sinyaller mobil SDK'dan toplanır; KVKK aydınlatma metnine uygun. | S | M6 |
| FR-102 | Kara/beyaz listeler: kart BIN/hash, cihaz, IP, telefon, müşteri. | Liste yönetimi gerekçe ve süre ile; tüm değişiklikler audit'e. | S | M6 |
| FR-103 | Risk vaka yönetimi: kuyruk, atama, not, karar, SLA, eskalasyon (uyuma). | Vaka kapanışında karar gerekçesi zorunlu; vaka geçmişi değiştirilemez. | S | M6 |
| FR-104 | Kural simülasyonu (shadow mode): yeni kuralın geçmiş/gerçek trafikte etkisini ölçme. | Shadow kural karar vermez, yalnızca loglar; isabet/yanlış pozitif raporu. | C | M6 |
| FR-105 | Promosyon suistimali tespiti (çoklu hesap, bonus avcılığı). | Aynı cihaz/kart ile çoklu hesaba ödül kısıtı; şüpheli hesaplar vaka kuyruğuna. | C | M6 |

### 1.12 Uyum (`compliance-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-106 | KYC seviyesine bağlı regülasyon limit tabloları (bakiye tavanı, aylık yükleme, işlem tutarı). | Regülasyon limitleri tenant limitlerinden bağımsız ve daha önceliklidir; yalnızca Compliance rolü değiştirebilir. | M | M2 |
| FR-107 | Yaptırım/PEP listesi taraması: kayıtta, Tier yükseltmede ve liste güncellemesinde periyodik. | Eşleşmeler inceleme kuyruğuna; kapatmada gerekçe zorunlu; liste versiyonu kaydedilir. | S | M6 |
| FR-108 | İşlem izleme (AML) senaryoları: yapılandırma (structuring), hızlı yükle-harca-iade, olağan dışı hacim. | Senaryo tetiklemeleri uyum vakası oluşturur; senaryolar parametrik. | S | M6 |
| FR-109 | Şüpheli işlem bildirimi (STR) hazırlık iş akışı ve taslak raporu. | Bildirim kararı ve gönderim kaydı saklanır; müşteriye bilgi verilmez (tipping-off koruması). | S | M6 |
| FR-110 | Uyum vaka ve karar kaydı (risk vakalarından eskalasyon dahil). | Vakalar yalnızca Compliance ve Auditor rollerince görülür. | S | M6 |
| FR-111 | Veri saklama ve imha politikalarının uygulanması (KVKK periyodik imha). | Politika tablo bazlı; imha işlemleri tutanak (rapor) üretir. | S | M6 |
| FR-112 | Regülatör ve dönemsel uyum raporları (tenant/regülasyon şablonlu). | Rapor şablonları konfigüre edilebilir; üretim kaydı ve imzalı çıktı. | C | M7 |
| FR-113 | Sınırlı ağ (kapalı devre) eşik izleme: toplam float, işlem hacmi, işyeri sayısı göstergeleri. | Tenant eşiğe yaklaştığında (%80) Compliance ve PlatformAdmin bilgilendirilir. | S | M6 |

### 1.13 Takas & Mutabakat (`settlement-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-114 | İşyeri takas hesaplaması: gün sonu batch, mağaza/işyeri bazında net tutar, komisyon kesintisi. | Takas batch'i kapandıktan sonra işlemler batch'e bağlanır; void yalnızca batch öncesi. | S | M7 |
| FR-115 | PSP settlement/clearing dosyalarının otomatik alınması (SFTP/API) ve ayrıştırılması. | Dosya bütünlük kontrolü (hash, satır sayısı); tekrar alınan dosya idempotent işlenir. | S | M7 |
| FR-116 | Otomatik eşleştirme: ledger yükleme/iade kayıtları ↔ PSP satırları ↔ banka hareketleri. | Eşleştirme kuralları (referans, tutar, tarih toleransı); eşleşme oranı hedefi ≥ %99,5. | S | M7 |
| FR-117 | Mutabakat istisna yönetimi: eksik, fazla, tutar farkı; atama, çözüm, düzeltme kaydı. | Düzeltme ledger'a maker-checker ile; istisna yaşlandırma raporu. | S | M7 |
| FR-118 | Banka ekstresi entegrasyonu (MT940 / camt.053) ile tahsilat teyidi. | Günlük ekstre alımı; hesap bazlı bakiye mutabakatı. | S | M7 |
| FR-119 | İşyeri ödeme talimatı (payout) dosyası üretimi (franchise/çok işyerli yapılarda). | Banka formatlarında dosya; maker-checker; ödeme durumu takibi. | C | M7 |
| FR-120 | Takas ve mutabakat raporları, günlük mutabakat sertifikası. | Günlük özet: yükleme, ödeme, iade, PSP, banka ve fark; imzalı PDF. | S | M7 |

### 1.14 Muhasebe (`accounting-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-121 | Ledger hesaplarının tenant genel muhasebe (GL) hesap planına eşlenmesi. | Eşleme ekranı; eşlenmemiş hesap varsa export engellenir. | S | M7 |
| FR-122 | Yevmiye (journal entry) export: günlük/aylık, CSV/XML, özet veya detay. | Export tekrar üretilebilir ve ledger ile toplam mutabık; dönem kilidi sonrası sabit. | S | M7 |
| FR-123 | ERP adaptörleri: SAP (S/4 IDoc/API), Logo, Netsis. | En az 1 ERP adaptörü GA'da; diğerleri adaptör şablonu ile. | C | M7 |
| FR-124 | e-Fatura/e-Arşiv entegrasyonu (tenant'ın müşteriye kestiği ücret faturaları ve platformun tenant'a faturası için özel entegratör üzerinden). | Fatura numarası ve durum ledger kaydına referanslanır. | C | M7 |
| FR-125 | Breakage hesaplama: süresi dolan bakiye kaydı ve (opsiyonel) tarihsel oran bazlı öngörü. | Breakage kaydı gelir hesabına ledger üzerinden; hesaplama parametreleri denetlenebilir. | S | M7 |
| FR-126 | Ertelenmiş gelir ve müşteri yükümlülüğü raporu (IFRS 15 uyumlu sunum). | Dönem sonu yükümlülük bakiyesi = ledger müşteri hesapları toplamı. | S | M7 |
| FR-127 | Muhasebe dönemi kapanışı ve kilitleme. | Kilitli döneme kayıt atılamaz; düzeltmeler açık döneme ters kayıtla. | S | M7 |

### 1.15 Raporlama (`reporting-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-128 | Tenant operasyonel dashboard: günlük yükleme, ödeme, aktif cüzdan, toplam bakiye, hata oranları. | Veri gecikmesi ≤ 5 dk; mağaza filtresi; StoreMgr yalnızca kendi mağazasını görür. | M | M4 |
| FR-129 | İşlem raporu: filtreleme (tarih, tip, mağaza, terminal, durum), CSV export. | 1 milyon satıra kadar asenkron export; export işlemi audit'e yazılır. | M | M4 |
| FR-130 | Müşteri bakiye/yükümlülük raporu (cüzdan tipine göre, günlük snapshot). | Toplamlar ledger ile birebir; tarih seçilerek geçmiş snapshot. | M | M4 |
| FR-131 | Mağaza gün sonu ve kasiyer vardiya raporları. | Web POS ve Admin Portal'dan alınabilir; PDF/CSV. | M | M4 |
| FR-132 | KPI raporu: North Star (MTAW), MAW, kayıt→ilk yükleme dönüşümü, otomatik yükleme benimseme. | Tanımlar [Ürün Vizyonu](product-vision.md) ile aynı; kohort kırılımı. | S | M4 |
| FR-133 | Planlı raporlar: günlük/haftalık/aylık, e-posta veya SFTP ile teslim. | Rapor linkleri süreli ve yetki kontrollü; ek olarak PII gönderilmez. | S | M7 |
| FR-134 | XLSX ve PDF export, tenant markalı rapor şablonu. | Büyük raporlar asenkron; hazır olduğunda bildirim. | S | M7 |
| FR-135 | Analitik veri ambarı (ClickHouse) ve self-servis BI görünümleri. | CDC gecikmesi ≤ 2 dk; tenant izolasyonu analitik katmanda da garanti. | C | M7 |

### 1.16 Audit & Teftiş (`audit-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-136 | Hash-zincirli, değiştirilemez audit log: tüm yetkili işlemler (kim, ne, ne zaman, nereden, önce/sonra). | Her kayıt bir önceki kaydın hash'ini içerir; servisler olay üretir (M1'den itibaren), zincirleme servis M2'de. | M | M2 |
| FR-137 | Maker-checker (çift onay) çerçevesi: konfigürasyon, manuel düzeltme, iade eşik üstü, rol atama. | Maker kendi talebini onaylayamaz; talep süresi dolabilir; onay/red gerekçesi zorunlu. | M | M4 |
| FR-138 | Teftiş sorgu ekranı: aktör, nesne, aksiyon, tarih aralığı, tenant filtresi; salt okunur. | Auditor rolü MFA ile; sonuçlar sayfalı ve dışa aktarılabilir; sorgu kendisi de loglanır. | M | M4 |
| FR-139 | Hash-zincir bütünlük doğrulaması (isteğe bağlı ve günlük otomatik). | Kırılma tespitinde P1 alarm; doğrulama sonucu ekranda gösterilir. | M | M4 |
| FR-140 | Delil paketi export: seçili kayıtlar + manifest + imza (imzalı ZIP). | Paket bağımsız doğrulanabilir (doğrulama aracı/talimatı ile). | S | M4 |
| FR-141 | Hassas veri erişim logu: PII görüntüleme, maskesiz görüntüleme gerekçesi, export. | Maskesiz görüntüleme gerekçe seçimi ister; rapor Compliance'a açık. | S | M4 |
| FR-142 | Audit log uzun süreli saklama ve arşiv (WORM depolama). | Saklama süresi NFR-042'ye uygun; arşivden geri getirme prosedürü. | S | M8 |

### 1.17 Bildirim (`notification-service`)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-143 | Push bildirim (FCM/APNs): işlem, yükleme, hold serbest bırakma, güvenlik olayları. | İşlem bildirimi p95 ≤ 5 sn; bildirim hatası ödeme akışını etkilemez. | M | M3 |
| FR-144 | E-posta bildirimleri: hoş geldin, makbuz, güvenlik uyarısı, personel davetleri. | SPF/DKIM/DMARC uyumlu gönderim; tenant markalı şablon. | M | M3 |
| FR-145 | SMS bildirimleri (OTP dışı işlemsel ve pazarlama). | Pazarlama SMS'i yalnızca izinli müşteriye; gönderici başlığı tenant bazlı. | S | M5 |
| FR-146 | Tenant bazlı, çok dilli bildirim şablonu yönetimi (değişkenli). | Önizleme ve test gönderimi; şablon versiyonları. | S | M4 |
| FR-147 | Bildirim tercihleri ve ticari ileti izin yönetimi (İYS entegrasyonu dahil). | İşlemsel/güvenlik bildirimleri kapatılamaz; ticari izin İYS ile senkron. | S | M4 |
| FR-148 | Uygulama içi gelen kutusu (in-app inbox). | Okundu/okunmadı; kampanya mesajları. | C | M5 |

### 1.18 Tenant Admin Portal (`admin-bff`, React)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-149 | Admin kullanıcı ve rol yönetimi (RBAC + mağaza/bölge kapsamı), davet, deaktivasyon. | Rol ataması maker-checker; kullanıcı ayrıldığında erişim anında kapanır. | M | M4 |
| FR-150 | Müşteri arama ve Müşteri 360 görünümü (profil, cüzdanlar, işlemler, cihazlar, onaylar, vakalar). | Telefon/e-posta/müşteri no ile arama; PII rol bazlı maskeli. | M | M4 |
| FR-151 | İşlem arama ve işlem detay (ledger kayıtları, durum geçmişi, ilişkili iade/void). | Detayda ilgili journal kayıtları görüntülenir (Finance/Auditor). | M | M4 |
| FR-152 | İşyeri/mağaza/terminal yönetim ekranları. | FR-071–FR-074 fonksiyonlarının UI karşılığı; toplu içe aktarım. | M | M4 |
| FR-153 | Konfigürasyon ekranları: limitler, ücretler, yükleme kuralları, hold süreleri, tema. | Kritik alanlar maker-checker; değişiklik geçmişi ve fark (diff) görünümü. | M | M4 |
| FR-154 | Onay kuyruğu (maker-checker iş listesi). | Filtre, toplu görüntüleme; onaylayıcı talebin tam bağlamını görür. | M | M4 |
| FR-155 | Destek aksiyonları: müşteri/cüzdan bloke-çöz, iade talebi oluşturma, not ekleme, oturum sonlandırma. | Support rolü finansal işlemi yalnızca **talep** olarak oluşturur; onay yetkili rolde. | M | M4 |
| FR-156 | Toplu işlemler ekranı: müşteri aktarımı, toplu yükleme, toplu kupon. | Dosya doğrulama önizlemesi; sonuç raporu indirilebilir. | S | M5 |
| FR-157 | PII maskeleme ve maskesiz görüntüleme için gerekçe akışı. | Varsayılan maskeli; maskesiz görüntüleme FR-141 ile loglanır. | M | M4 |

### 1.19 Platform Admin Konsolu

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-158 | Tenant yaşam döngüsü konsolu (FR-001, FR-002 UI) ve onboarding kontrol listesi. | Go-live kontrol listesi tamamlanmadan tenant `Active` olamaz. | M | M4 |
| FR-159 | Plan, kota ve feature flag yönetimi (platform seviyesi). | Plan değişikliği anında etkin; geçmiş saklanır. | S | M4 |
| FR-160 | Tenant sağlık ve SLO paneli (hata oranı, gecikme, kuyruk birikimi, kota kullanımı). | Tenant bazlı kırılım; Grafana panellerine derin link. | S | M4 |
| FR-161 | Break-glass erişim: tenant verisine acil erişim (gerekçe, süre, ikinci onay, otomatik sona erme). | Varsayılan olarak PlatformAdmin tenant PII'sine erişemez; break-glass oturumu tamamen loglanır ve tenant'a raporlanır. | M | M4 |
| FR-162 | Global parametreler: PSP konfigürasyonları, ülke/para birimi tabloları, global kara listeler. | Değişiklikler maker-checker ve ortam bazlı. | S | M4 |
| FR-163 | Platform faturalandırma: tenant bazlı kullanım (aktif cüzdan, işlem) ölçümü ve fatura taslağı. | Ölçüm verileri denetlenebilir; aylık kullanım raporu tenant ile paylaşılır. | S | M7 |
| FR-164 | Tenant verisinin dışa aktarımı ve sözleşme sonunda sonlandırma/imha süreci. | Standart formatta dışa aktarım; imha tutanağı; yasal saklama istisnaları. | C | M8 |

### 1.20 Mobil Uygulama (React Native, white-label)

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-165 | White-label build pipeline: tenant teması, ikon, uygulama adı, paket kimliği ile iOS/Android derlemesi. | Tek kod tabanı; tenant konfigürasyonu build-time + run-time; MVP'de 1 tema. | M | M4 |
| FR-166 | Onboarding ve kayıt akışı (telefon OTP, onaylar, profil, Tier1). | Akış ≤ 90 sn'de tamamlanabilir (kullanılabilirlik testi medyanı). | M | M4 |
| FR-167 | Ana ekran: toplam ve cüzdan bazlı bakiye, tek dokunuşla QR, son işlemler. | Uygulama açılışından QR'a ≤ 2 dokunuş. | M | M4 |
| FR-168 | QR ödeme ekranı: dinamik QR yenileme, ekran parlaklığı artırma, kısa süreli offline token. | Ağ yokken önceden alınmış tek kullanımlık token (tenant izni ile) gösterilir. | M | M4 |
| FR-169 | Yükleme ekranı: tutar seçimi, kayıtlı kart, yeni kart (PSP SDK), otomatik yükleme ayarı. | 3DS sonrası uygulamaya sorunsuz dönüş; sonuç ekranı ve bildirim. | M | M4 |
| FR-170 | İşlem geçmişi ve dijital makbuz (filtre, detay, hold durumu). | Son 24 ay; makbuz paylaşılabilir (PDF/görsel). | M | M4 |
| FR-171 | Profil, güvenlik ve cihaz yönetimi (PIN/biyometri, cihaz listesi, çıkış, hesap kapatma talebi). | Cihaz kaldırma anında oturumu düşürür. | M | M4 |
| FR-172 | Aktif oturum ekranları: EV şarj ve otopark hold/oturum durumu, tahmini tutar. | Hold ve capture adımları müşteriye şeffaf gösterilir. | S | M4 |
| FR-173 | Sadakat ekranları: yıldız/puan, tier ilerleme, ödüller, kampanyalar, kuponlar. | Ödül kullanımı QR ile birlikte uygulanabilir. | S | M5 |
| FR-174 | Aile/alt cüzdan yönetimi (alt cüzdan açma, limit, kategori, bileklik eşleme). | Ebeveyn tüm alt cüzdan hareketlerini gerçek zamanlı görür. | C | M5 |
| FR-175 | Hediye kartı gönderme/alma ve cüzdana ekleme ekranları. | Link veya kod ile ekleme; tasarım seçimi. | S | M5 |
| FR-176 | Plaka yönetimi (otopark): plaka ekle/sil, aktif abonelikler. | Plaka formatı ülkeye göre doğrulanır; bir plaka aynı tenant'ta tek cüzdana bağlı. | S | M5 |
| FR-177 | Mağaza/istasyon bulucu (harita, çalışma saatleri, uygunluk). | Konum izni olmadan da liste görünümü. | C | M5 |

### 1.21 Public API & Geliştirici Deneyimi

| ID | Gereksinim | Kabul kriteri özeti | Öncelik | MS |
|---|---|---|---|---|
| FR-178 | OpenAPI 3.1 sözleşmeleri ve geliştirici portalı (dokümantasyon, örnekler, Postman koleksiyonu, değişiklik günlüğü). | Dokümantasyon CI'da sözleşmeden üretilir; her endpoint için örnek istek/yanıt. | M | M3 |
| FR-179 | API istemci kimlik bilgisi yönetimi (OAuth2 client credentials, kapsam/scopes, rotasyon). | Kapsamlar en az yetki ilkesine göre; anahtar iptali ≤ 60 sn etkin. | M | M3 |
| FR-180 | Sandbox ortamı: test tenant'ı, test kartları, test QR üretici, mock PSP. | Sandbox verisi üretimden fiziksel olarak ayrı; self-servis sıfırlama. | M | M3 |
| FR-181 | Webhook aboneliği yönetimi: olay tipleri, uç nokta, gizli anahtar, teslim geçmişi, yeniden gönderim. | HMAC-SHA256 imza + zaman damgası (replay koruması). | S | M3 |
| FR-182 | Rate limit ve kota başlıkları (`RateLimit-*`), tenant/istemci bazlı. | 429 yanıtında `Retry-After`; limitler plan ile ilişkili. | M | M3 |
| FR-183 | Standart hata modeli (RFC 9457 problem+json) ve `Idempotency-Key` desteği tüm yazma uç noktalarında. | Hata kodu kataloğu yayınlanır; aynı key + farklı gövde = 422. | M | M3 |
| FR-184 | Resmi SDK'lar (Java, TypeScript) — OpenAPI'den üretilmiş + el yazımı yardımcılar. | Semantic versioning; örnek uygulama. | C | M8 |
| FR-185 | Tenant backend API'si: müşteri oluşturma/sorgu, bakiye sorgu, sunucu taraflı yükleme (sponsor), olay aboneliği. | Tenant'ın kendi CRM/uygulamasıyla entegrasyonu için; kapsamlar ayrık. | S | M5 |

### 1.22 FR Özet İstatistikleri

| Modül | FR aralığı | Adet | M | S | C | W |
|---|---|---|---|---|---|---|
| Tenant | 001–010 | 10 | 6 | 4 | 0 | 0 |
| Kimlik | 011–018 | 8 | 6 | 1 | 1 | 0 |
| Müşteri/KYC | 019–026 | 8 | 4 | 4 | 0 | 0 |
| Cüzdan | 027–036 | 10 | 6 | 2 | 2 | 0 |
| Ledger | 037–044 | 8 | 6 | 1 | 1 | 0 |
| Yükleme | 045–055 | 11 | 3 | 5 | 3 | 0 |
| Ödeme | 056–070 | 15 | 9 | 3 | 2 | 1 |
| İşyeri/POS | 071–079 | 9 | 6 | 3 | 0 | 0 |
| Sadakat/Kampanya | 080–089 | 10 | 4 | 6 | 0 | 0 |
| Hediye kartı | 090–096 | 7 | 3 | 4 | 0 | 0 |
| Risk | 097–105 | 9 | 2 | 5 | 2 | 0 |
| Uyum | 106–113 | 8 | 1 | 6 | 1 | 0 |
| Takas/Mutabakat | 114–120 | 7 | 0 | 6 | 1 | 0 |
| Muhasebe | 121–127 | 7 | 0 | 5 | 2 | 0 |
| Raporlama | 128–135 | 8 | 4 | 3 | 1 | 0 |
| Audit/Teftiş | 136–142 | 7 | 4 | 3 | 0 | 0 |
| Bildirim | 143–148 | 6 | 2 | 3 | 1 | 0 |
| Admin Portal | 149–157 | 9 | 8 | 1 | 0 | 0 |
| Platform Admin | 158–164 | 7 | 2 | 4 | 1 | 0 |
| Mobil App | 165–177 | 13 | 7 | 4 | 2 | 0 |
| Public API | 178–185 | 8 | 5 | 2 | 1 | 0 |
| **Toplam** | | **185** | **88** | **75** | **21** | **1** |

---

## 2. Fonksiyonel Olmayan Gereksinimler (NFR)

> Ölçüm yöntemi her NFR için belirtilmiştir; performans NFR'leri [Yol Haritası](roadmap.md) M3, M4 ve M8'de
> Gatling/k6 ile doğrulanır. "MVP" hedefleri M4 çıkışında, "GA" hedefleri M8 çıkışında zorunludur.

### 2.1 Performans

| ID | Gereksinim | Hedef (MVP → GA) | Doğrulama |
|---|---|---|---|
| NFR-001 | Ödeme API (sale/capture) sunucu tarafı gecikmesi | p95 ≤ 300 ms, p99 ≤ 800 ms (her iki fazda) | k6/Gatling, gateway ölçümü |
| NFR-002 | Kasada QR okutma → onay uçtan uca süre | p95 ≤ 1,5 sn (4G ağ koşulunda) | Saha testi + sentetik izleme |
| NFR-003 | Sürekli ödeme işlem kapasitesi | 300 TPS → 2.000 TPS (tepe 3× burst 5 dk) | Yük ve stres testi |
| NFR-004 | Bakiye sorgusu gecikmesi | p95 ≤ 100 ms | Yük testi |
| NFR-005 | Admin Portal sayfa yükleme | LCP ≤ 2,5 sn, INP ≤ 200 ms (p75) | Lighthouse CI, RUM |
| NFR-006 | Rapor sorgusu (1M satır aralığında filtreli liste) | İlk sayfa ≤ 3 sn; export asenkron ≤ 5 dk | Performans testi |
| NFR-007 | Mobil uygulama soğuk açılış | ≤ 2 sn (orta segment Android) | Cihaz çiftliği ölçümü |

### 2.2 Ölçeklenebilirlik & Çok Kiracılık

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-008 | Yatay ölçeklenebilirlik: tüm servisler stateless, HPA ile ölçeklenir. | Pod sayısı 2× olduğunda throughput ≥ 1,8× | Ölçek testi |
| NFR-009 | Platform kapasitesi | MVP: 10 tenant / 1M cüzdan; GA: 100 tenant / 10M cüzdan | Kapasite planı + sentetik veri testi |
| NFR-010 | Gürültülü komşu koruması: tenant bazlı rate limit ve kaynak kotası | Bir tenant'taki 10× yük diğer tenant p95'ini %10'dan fazla bozmaz | Çok kiracılı yük testi |
| NFR-011 | Olay sıralaması: aynı cüzdana ait olaylar sıralı işlenir (Kafka key = wallet_id) | Sıra ihlali 0 | Contract + kaos testi |

### 2.3 Kullanılabilirlik (Availability) & Dayanıklılık

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-012 | Ödeme yolu (QR ödeme, pre-auth, capture) aylık SLO | MVP %99,9 → GA %99,95 | SLO panosu, hata bütçesi |
| NFR-013 | Felaket kurtarma | Ledger RPO ≤ 1 dk (GA: ~0, senkron replika), RTO ≤ 1 saat | Yılda 2 DR tatbikatı (ilki M8) |
| NFR-014 | Zarif bozulma: bildirim, sadakat, raporlama arızası ödeme yolunu durdurmaz | Bağımlılık kesintisinde ödeme başarı oranı ≥ %99 | Kaos mühendisliği testleri |
| NFR-015 | Kesintisiz dağıtım (rolling/blue-green), geriye uyumlu şema göçleri (expand/contract) | Deploy sırasında hata oranı artışı ≤ %0,1 | Canary analizi |

### 2.4 Güvenlik

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-016 | İletim güvenliği: dışarıda TLS 1.2+ (tercihen 1.3), servisler arası mTLS (Service Mesh) | %100 kapsam | Konfigürasyon taraması |
| NFR-017 | Kart verisi platformda saklanmaz, işlenmez, iletilmez (PSP tokenizasyonu) → PCI DSS kapsamı minimum (SAQ A hedefi) | PAN içeren log/DB kaydı 0 | DLP taraması, QSA ön değerlendirmesi (M8) |
| NFR-018 | Durağan veri şifreleme: disk/DB AES-256; PII alanları uygulama seviyesinde şifreli (Vault Transit/KMS) | %100 PII alanı | Kod incelemesi + veri keşif taraması |
| NFR-019 | Kimlik doğrulama: personel için MFA zorunlu; ayrıcalıklı işlemlerde step-up | %100 | IAM denetimi |
| NFR-020 | Uygulama güvenliği: OWASP ASVS Level 2 (ödeme/ledger uç noktaları Level 3 kontrolleri), OWASP MASVS L2 (mobil) | Açık kritik/yüksek bulgu 0 | SAST/DAST, pentest (M8) |
| NFR-021 | Sır yönetimi: kaynak kodda/imajda sır yok; tüm sırlar Vault'tan, otomatik rotasyon | Gitleaks bulgusu 0 | CI kapısı |
| NFR-022 | Yetkilendirme: RBAC + tenant/mağaza kapsamlı ABAC; en az yetki; görev ayrılığı (SoD) matrisi | SoD ihlali 0 | Yetki matrisi testleri, dönemsel erişim gözden geçirmesi |
| NFR-023 | Tedarik zinciri güvenliği: SBOM, imzalı imajlar, bağımlılık taraması | Kritik CVE 0 (yayın anında) | Trivy, OWASP DC, cosign doğrulama |
| NFR-024 | Oturum güvenliği: personel oturumu 15 dk hareketsizlikte kapanır; mobil access token ≤ 5 dk | %100 | Otomatik test |
| NFR-025 | API kötüye kullanım koruması: WAF, bot koruması, rate limit, OTP pompalama koruması | Kötüye kullanım alarmları ≤ 5 dk içinde | Güvenlik testleri |

### 2.5 Veri Bütünlüğü

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-026 | Ledger değişmezi: her an Σ borç = Σ alacak; cüzdan görünümü = ledger bakiyesi | Fark tolerans **0** | Sürekli invariant kontrolü + property-based test |
| NFR-027 | Idempotency: tüm yazma işlemleri idempotent; anahtar saklama ≥ 24 saat | Çift tahsilat 0 | Tekrar/yarış testleri |
| NFR-028 | Dağıtık tutarlılık: saga adımları telafi edilebilir; outbox ile olay kaybı yok | Kayıp olay 0, takılı saga ≤ 5 dk içinde alarm | Kaos testi |

### 2.6 Gözlemlenebilirlik

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-029 | Dağıtık izleme: tüm istekler OpenTelemetry trace'i taşır; `tenant_id`, `correlation_id` öznitelikleri | Trace kapsamı %100 (örnekleme politikası ile) | Tempo kontrolü |
| NFR-030 | Metrikler: RED/USE metrikleri + iş metrikleri (ödeme başarı oranı, yükleme hacmi) tenant bazında | Tüm servislerde standart dashboard | Grafana şablon denetimi |
| NFR-031 | Yapılandırılmış log (JSON), PII ve sır içermez; log seviyeleri standart | PII içeren log 0 | Log tarama kuralları |
| NFR-032 | SLO tabanlı alarm (burn-rate), runbook bağlantılı alarmlar | Her P1/P2 alarmın runbook'u var | Alarm incelemesi |
| NFR-033 | Audit zinciri bütünlük doğrulaması günlük otomatik çalışır | Başarısızlıkta ≤ 15 dk alarm | Planlı iş izleme |

### 2.7 Uluslararasılaştırma (i18n) & Yerelleştirme

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-034 | Dil desteği: TR, EN, AR — Arapça için tam **RTL** yerleşim (mobil + portal + e-posta) | 3 dilde %100 arayüz metni | Pseudo-localization + RTL görsel regresyon |
| NFR-035 | Yerel biçimlendirme: tarih/saat (tenant saat dilimi), sayı, para birimi (ISO 4217 küçük birim), telefon (E.164) | Tüm ekranlarda ICU/Intl kullanımı | Birim + görsel test |
| NFR-036 | Metinler koddan ayrık; tenant bazında metin geçersiz kılma (override) | Sabit kodlanmış metin 0 | Lint kuralı |

### 2.8 Erişilebilirlik

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-037 | Web (Admin Portal, Platform Admin, Web POS, geliştirici portalı) **WCAG 2.2 AA** uyumu | Otomatik taramada kritik ihlal 0 + manuel denetim | axe-core CI, manuel ekran okuyucu testi (NVDA/VoiceOver) |
| NFR-038 | Mobil erişilebilirlik: VoiceOver/TalkBack, dinamik yazı boyutu, ≥ 44×44 pt dokunma alanı, 4.5:1 kontrast | Kritik akışlar (kayıt, yükleme, QR ödeme) %100 erişilebilir | Manuel test + erişilebilirlik ihtiyacı olan kullanıcılarla test |
| NFR-039 | Web POS ergonomisi: yüksek kontrast modu, ≥ 48 px hedefler, ses/titreşim geri bildirimi, renk dışında durum göstergesi | Kasiyer görev başarısı ≥ %95 | Kullanılabilirlik testi |

### 2.9 Veri Saklama, Gizlilik ve Yerleşim

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-040 | Finansal kayıtlar (ledger, işlem, takas) saklama süresi | En az 10 yıl (TTK/VUK ve MASAK sürelerinin en uzunu; `CMP` teyidi) | Saklama politikası denetimi |
| NFR-041 | KVKK/GDPR: veri minimizasyonu, amaçla sınırlılık; yasal saklama bitiminde anonimleştirme | Politika tablosu + periyodik imha kaydı | Uyum denetimi |
| NFR-042 | Audit log saklama | En az 10 yıl, WORM; ilk 1 yıl sıcak sorgulanabilir | Arşiv testi |
| NFR-043 | Operasyonel log/metrik saklama | Log 90 gün sıcak + 1 yıl soğuk; metrik 13 ay | Konfigürasyon denetimi |
| NFR-044 | Veri yerleşimi: TR tenant verisi Türkiye'deki veri merkezinde; bölge bazlı dağıtım (MENA fazı) | Sınır ötesi aktarım yalnızca açık hukuki dayanakla | Mimari inceleme |
| NFR-045 | Yedekleme: günlük tam + sürekli WAL arşivi; şifreli, farklı lokasyon; aylık geri yükleme testi | Geri yükleme testi başarı %100 | Yedek geri yükleme tatbikatı |

### 2.10 Sürdürülebilirlik, Test Edilebilirlik ve Kullanılabilirlik

| ID | Gereksinim | Hedef | Doğrulama |
|---|---|---|---|
| NFR-046 | Kod kalitesi: domain katmanı test kapsamı ≥ %80, mutasyon skoru ≥ %60 (ledger/payment ≥ %75), 0 kritik Sonar bulgusu | CI kalite kapısı | SonarQube, PIT |
| NFR-047 | API geriye dönük uyumluluk: `/v1` içinde kırıcı değişiklik yok; kullanım dışı bırakma ≥ 6 ay önceden duyurulur | Kırıcı değişiklik 0 | OpenAPI diff kontrolü CI'da |
| NFR-048 | Tenant izolasyon testleri: her servis için otomatik çapraz-tenant erişim testleri | Başarısız test = pipeline kırmızı | Entegrasyon testleri |
| NFR-049 | Mobil ve portal kullanılabilirliği: SUS ≥ 80; kritik görev başarı ≥ %90 | Her major sürümde | Kullanılabilirlik testi |
| NFR-050 | Kasiyer eğitim süresi: yeni kasiyer ≤ 15 dk eğitimle QR ödeme, iade ve gün sonu işlemlerini yapabilmeli | Pilot mağazada ölçüm | Saha gözlemi |

---

## 3. Varsayımlar ve Kısıtlar

1. Pilot PSP; 3DS2, tokenizasyon, karta iade ve (tercihen) kart pre-auth desteğine sahiptir.
2. SMS sağlayıcısı ve push servisleri (FCM/APNs) tenant markası ile gönderim yapabilir.
3. EV/otopark harici sistemleri (CSMS, LPR) MVP'de POS REST API'yi (FR-077) doğrudan çağırır; özel adaptörler M5'te (FR-079).
4. Regülasyon limitleri (FR-106) `CMP` tarafından sağlanacak resmi tabloya göre konfigüre edilir; ürün sabit değer içermez.
5. Kapalı devre modeli: bakiye yalnızca tenant ağında geçerli, nakde çevrilemez (hesap kapatma iadesi hariç).
