# AEP-CLW — Fonksiyon Matrisi

| Alan | Değer |
|---|---|
| Doküman | Fonksiyon Matrisi (Function Matrix) |
| Sahibi | Business Analyst ×2 (`BA`) |
| Onay | Product Owner (`PO`) — her Sprint Review'da |
| Sürüm | v1.0 — Sprint 0 baseline |
| Son güncelleme | Sprint 0 (Inception) — tüm fonksiyonlar `Planned` |
| Kaynak | [requirements.md](requirements.md) (FR-001 … FR-185) |
| İlgili | [Audit (Kontrol) Matrisi](../compliance/) · [Yol Haritası](roadmap.md) · [MVP Kapsamı](mvp-scope.md) |

---

## 1. Kullanım ve Güncelleme Talimatı

> Bu matris, **Sprint Review paketinin zorunlu parçasıdır** (bkz. [Proje Tüzüğü §6](../00-project-charter.md)).
> Her sprint sonunda güncellenmeden Sprint Review onaya sunulamaz.

### 1.1 Matris ne işe yarar?

1. **Kapsam izlenebilirliği**: Her fonksiyonun (FN) hangi gereksinimleri (FR) karşıladığını gösterir.
2. **Yetki tasarımı girdisi**: Rol kolonları, Keycloak rol/izin modelinin ve görev ayrılığı (SoD) matrisinin **tek doğruluk kaynağıdır**. `SEC` ve `AUD` bu kolonları yetki testleri için kullanır.
3. **Kanal kapsamı**: Hangi fonksiyonun hangi arayüzden sunulduğunu tanımlar (BFF ve UI backlog'u buradan türetilir).
4. **Sektör uygulanabilirliği**: Sektör presetlerinin ([sector-configurations.md](sector-configurations.md)) hangi fonksiyonları açıp kapatacağını gösterir.
5. **İlerleme göstergesi**: Durum kolonu Sprint Review'da ilerleme raporunun temelidir.

### 1.2 Kolon sözlüğü

| Kolon | Değerler | Açıklama |
|---|---|---|
| **FN** | `FN-001` … | Kalıcı fonksiyon kimliği; silinmez, yeniden kullanılmaz |
| **FR** | `FR-xxx` listesi | Karşılanan gereksinimler ([requirements.md](requirements.md)) |
| **Kanal** | `MOB` Mobil app · `TA` Tenant Admin Portal · `PA` Platform Admin Konsolu · `POS` Web POS / entegre POS · `API` Public/POS API | Fonksiyonun sunulduğu kanallar |
| **Rol kolonları** | `C` Create (oluştur / başlat) · `R` Read (görüntüle) · `U` Update (güncelle / durum değiştir) · `D` Delete (sil / pasifleştir / iptal) · `A` Approve (maker-checker onayı) · `–` erişim yok | Yetki; birden fazla harf birleşik yazılır (`CRUA`) |
| **Roller** | `Cust` Customer · `Cash` Cashier · `StMgr` Store Manager · `TAdm` Tenant Admin · `Fin` Finance · `Risk` Risk Analyst · `Cmp` Compliance · `Aud` Auditor · `Sup` Support · `PAdm` Platform Admin | RBAC rolleri (persona eşlemesi: [personas-and-journeys.md](personas-and-journeys.md)) |
| **Sektör** | `●` uygulanır (preset'te açık) · `○` opsiyonel (preset'te kapalı, açılabilir) · `–` uygulanmaz | Kahve · EV · Otopark · Eğlence · Kampüs |
| **MVP** | `Evet` / `Hayır` | M1–M4 kapsamı = Evet |
| **MS** | `M1` … `M8` | Hedef milestone |
| **Durum** | `Planned` → `In Progress` → `Done` → `Accepted` (+ `Blocked`, `Descoped`) | Aşağıdaki durum kurallarına göre |

### 1.3 Yetki kuralları (tüm satırlar için geçerli)

1. **Görev ayrılığı**: Aynı satırda `C` ve `A` bulunan bir rol için, **aynı kullanıcı** kendi başlattığı talebi onaylayamaz (maker ≠ checker). Sistem bunu zorunlu kılar (FR-137).
2. **Auditor** tüm fonksiyonlarda varsayılan olarak **salt okunur** (`R`) erişime sahiptir; hiçbir finansal veya konfigürasyon işlemi başlatamaz. Tek istisna delil paketi üretimidir (FN-122).
3. **Platform Admin** varsayılan olarak tenant **PII ve işlem verisine erişemez**; erişim yalnızca break-glass (FN-133) ile, gerekçeli ve süreli olarak açılır. Rol kolonundaki `R` değerleri platform metriklerini/konfigürasyonunu ifade eder.
4. **Store Manager** ve **Cashier** yetkileri yalnızca atandıkları **mağaza kapsamında** geçerlidir (ABAC).
5. **Support** finansal düzeltme ve iadeyi yalnızca **talep** (`C`) olarak başlatır; onay `Fin` / `StMgr` rolündedir.
6. **Customer** yalnızca kendi verisine erişir. Sistem tarafından otomatik yürütülen fonksiyonlarda (ör. FN-039 posting) insan rolü `–` gösterilir.

### 1.4 Durum geçiş kuralları

| Durum | Ne zaman atanır? | Kim atar? | Kanıt |
|---|---|---|---|
| `Planned` | Fonksiyon backlog'da, hedef milestone'a atanmış | `BA` | GitHub Epic/Story bağlantısı |
| `In Progress` | Fonksiyona bağlı en az bir Story sprint'e alınmış | `BA` (sprint planning sonrası) | Sprint board |
| `Done` | Bağlı tüm Story'ler Definition of Done'ı karşılamış (kod + test + doküman + dev/test ortamında deploy) | `QA` teyidi ile `BA` | CI yeşil, test raporu |
| `Accepted` | PO, Sprint Review'da demo ve kabul kriterleri üzerinden onaylamış | `PO` | Sprint Review onay kaydı |
| `Blocked` | Dış bağımlılık / karar bekleniyor | `BA` + `DM` | Engelin issue bağlantısı |
| `Descoped` | PO kararıyla kapsamdan çıkarıldı / ertelendi (MS değişirse `Planned` kalır, MS güncellenir) | `PO` | Karar kaydı |

### 1.5 Sprint Review güncelleme prosedürü

1. **Sprint Planning sonrası (Gün 1)**: `BA`, sprint'e alınan Story'lerin bağlı olduğu FN'leri `In Progress` yapar.
2. **Sprint içinde**: Kapsam veya yetki değişikliği çıkarsa (ör. yeni rol ihtiyacı), değişiklik PR'ı açılır; `SEC` ve `AUD` gözden geçirir.
3. **Review öncesi (Gün 9)**: `BA` + `QA`, DoD'u sağlayan FN'leri `Done` yapar; kısmen tamamlananlar `In Progress` kalır ve Story bazında not düşülür.
4. **Sprint Review (Gün 10)**: `PO` demo edilen FN'leri `Accepted` yapar. Reddedilenler `Done` → `In Progress`'e döner, gerekçe §4 değişiklik günlüğüne yazılır.
5. **Özet tablo (§2)** yeniden hesaplanır; değişiklik günlüğüne (§4) sprint satırı eklenir.
6. Bu dosya, Sprint Review paketiyle birlikte `docs/sprints/sprint-XX/` altında **anlık görüntü** olarak da arşivlenir; bu dosya her zaman **güncel** hali tutar.
7. Yeni FN eklenirse bir sonraki boş numara verilir; mevcut FN'ler yeniden numaralandırılmaz.

---

## 2. Özet

### 2.1 Modül bazında

| Modül | FN aralığı | Toplam | MVP (Evet) | Post-MVP |
|---|---|---|---|---|
| Tenant | FN-001–FN-010 | 10 | 10 | 0 |
| Kimlik | FN-011–FN-018 | 8 | 7 | 1 |
| Müşteri/KYC | FN-019–FN-028 | 10 | 7 | 3 |
| Cüzdan | FN-029–FN-038 | 10 | 7 | 3 |
| Ledger | FN-039–FN-044 | 6 | 6 | 0 |
| Yükleme | FN-045–FN-055 | 11 | 6 | 5 |
| Ödeme | FN-056–FN-068 | 13 | 8 | 5 |
| İşyeri/POS | FN-069–FN-076 | 8 | 6 | 2 |
| Sadakat/Kampanya | FN-077–FN-085 | 9 | 0 | 9 |
| Hediye kartı | FN-086–FN-090 | 5 | 0 | 5 |
| Risk | FN-091–FN-095 | 5 | 1 | 4 |
| Uyum | FN-096–FN-101 | 6 | 0 | 6 |
| Takas/Mutabakat | FN-102–FN-106 | 5 | 0 | 5 |
| Muhasebe | FN-107–FN-111 | 5 | 0 | 5 |
| Raporlama | FN-112–FN-117 | 6 | 4 | 2 |
| Audit/Teftiş | FN-118–FN-123 | 6 | 5 | 1 |
| Bildirim | FN-124–FN-127 | 4 | 3 | 1 |
| Admin Portal | FN-128–FN-131 | 4 | 4 | 0 |
| Platform Admin | FN-132–FN-136 | 5 | 3 | 2 |
| Mobil App | FN-137–FN-142 | 6 | 5 | 1 |
| Public API | FN-143–FN-147 | 5 | 3 | 2 |
| **Toplam** | | **147** | **85** | **62** |

### 2.2 Milestone bazında

| Milestone | FN adedi |
|---|---|
| M1 | 13 |
| M2 | 19 |
| M3 | 26 |
| M4 | 27 |
| M5 | 29 |
| M6 | 11 |
| M7 | 16 |
| M8 | 6 |

### 2.3 Durum bazında

| Durum | Adet |
|---|---|
| Planned | 147 |
| In Progress | 0 |
| Done | 0 |
| Accepted | 0 |

---

## 3. Matris

### Tenant

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-001 | Tenant oluşturma ve onboarding kontrol listesi | FR-001, FR-158 | PA | – | – | – | R | – | – | R | R | – | CRUA | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-002 | Tenant yaşam döngüsü (aktivasyon, askıya alma, sonlandırma) | FR-002 | PA | – | – | – | R | R | – | R | R | – | UA | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-003 | Tenant temel konfigürasyonu (para birimi, dil, saat dilimi) | FR-003 | TA, PA | – | – | – | CRUA | R | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-004 | Marka / tema yönetimi | FR-004 | TA | – | – | – | CRU | – | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-005 | Sektör preseti uygulama | FR-005 | PA, TA | – | – | – | RU | – | – | – | R | – | CRU | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-006 | Feature flag yönetimi | FR-006, FR-159 | PA, TA | – | – | – | RU | – | – | – | R | – | CRUA | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-007 | Plan ve kota yönetimi | FR-007, FR-159 | PA | – | – | – | R | R | – | – | R | – | CRUA | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-008 | Tenant ücret tanımları | FR-008 | TA | – | – | – | CRU | RA | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-009 | Son kullanma / breakage kuralları | FR-009 | TA | – | – | – | CRU | RA | – | R | R | – | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-010 | Tenant veri izolasyon modu (RLS / dedicated DB) | FR-010 | PA | – | – | – | – | – | – | – | R | – | CRA | ● | ● | ● | ● | ● | Evet | M1 | Planned |

### Kimlik

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-011 | Telefon + SMS OTP ile kayıt / giriş | FR-011 | MOB | CR | – | – | – | – | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-012 | Cihaz bağlama ve cihaz listesi yönetimi | FR-012, FR-171 | MOB, TA | CRD | – | – | – | – | R | – | R | RD | – | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-013 | PIN / biyometrik kilit ve step-up doğrulama | FR-013 | MOB | CRU | – | – | RU | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-014 | Oturum yönetimi ve uzaktan oturum sonlandırma | FR-014 | MOB, TA | RD | – | – | – | – | D | – | R | RD | – | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-015 | Personel girişi ve zorunlu MFA | FR-015 | TA, PA, POS | – | U | U | CRUD | U | U | U | R | U | CRUD | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-016 | Hesap kurtarma / cihaz değişimi | FR-017 | MOB, TA | C | – | – | – | – | RA | – | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-017 | OTP ve giriş kötüye kullanım koruması yapılandırması | FR-018 | PA | – | – | – | – | – | R | – | R | – | CRU | ● | ● | ● | ● | ● | Evet | M1 | Planned |
| FN-018 | E-posta ve sosyal giriş | FR-016 | MOB | C | – | – | U | – | – | – | R | – | – | ○ | ● | ○ | ○ | ● | Hayır | M5 | Planned |

### Müşteri/KYC

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-019 | Müşteri profili yönetimi | FR-019 | MOB, TA | CRU | – | – | R | – | – | – | R | RU | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-020 | KVKK/GDPR onay ve ticari ileti izni yönetimi | FR-020 | MOB, TA | CRU | – | – | CRU | – | – | RA | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-021 | KYC Tier0 / Tier1 yükseltme | FR-021 | MOB, TA | C | – | – | – | – | – | R | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-022 | Tier2 eKYC doğrulaması | FR-022 | MOB, API | C | – | – | – | – | – | RA | R | R | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-023 | Müşteri durum yönetimi (kısıtlama, bloke, kapatma) | FR-023 | TA | – | – | – | RU | – | CUA | CUA | R | CU | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-024 | Hesap kapatma ve kalan bakiye iadesi | FR-024 | MOB, TA | C | – | – | – | A | – | R | R | C | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-025 | Toplu müşteri aktarımı (CSV/API) | FR-025, FR-156 | TA, API | – | – | – | CRA | – | – | R | R | – | – | ○ | ○ | – | ○ | ● | Hayır | M5 | Planned |
| FN-026 | Veri sahibi talepleri (erişim, düzeltme, silme) | FR-026 | MOB, TA | C | – | – | – | – | – | RUA | R | C | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-027 | Müşteri 360 görünümü | FR-150 | TA | – | – | R | R | R | R | R | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-028 | PII maskesiz görüntüleme (gerekçeli) ve erişim logu | FR-157, FR-141 | TA | – | – | – | R | – | R | R | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |

### Cüzdan

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-029 | Ana cüzdan (MAIN) otomatik açılışı | FR-027 | MOB, API | R | – | – | – | – | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-030 | Bonus / promosyon cüzdanı | FR-028 | MOB, TA | R | – | – | R | R | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-031 | Bakiye sorgulama (toplam / kullanılabilir / bloke) | FR-029 | MOB, POS, TA, API | R | R | R | R | R | R | – | R | R | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-032 | Harcama önceliği kuralı | FR-030 | TA | – | – | – | CRU | A | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-033 | Hold oluşturma, sorgulama ve otomatik serbest bırakma | FR-034, FR-065 | POS, API, MOB | R | CD | CD | – | R | – | – | R | R | – | – | ● | ● | ● | ○ | Evet | M2 | Planned |
| FN-034 | Cüzdan dondurma / çözme | FR-035 | MOB, TA | U | – | – | – | – | UA | UA | R | U | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-035 | Cüzdan, KYC ve regülasyon limitleri | FR-036, FR-106 | TA | – | – | – | CRU | – | R | CRUA | R | – | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-036 | Alt cüzdan / aile cüzdanı kontrolleri | FR-031, FR-032, FR-174 | MOB | CRUD | – | – | RU | – | – | – | R | R | – | ○ | – | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-037 | Kısıtlı amaçlı (yemek) cüzdan ve sponsor | FR-033 | TA | – | – | – | CRU | A | – | – | R | – | – | ○ | – | – | ○ | ● | Hayır | M5 | Planned |
| FN-038 | Çoklu para birimi hesapları | FR-043 | TA, PA | – | – | – | CRU | RA | – | – | R | – | U | ○ | ○ | ○ | ○ | ○ | Hayır | M8 | Planned |

### Ledger

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-039 | Çift kayıtlı, idempotent posting | FR-037, FR-040 | API | – | – | – | – | R | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-040 | Hesap planı (chart of accounts) yönetimi | FR-038 | TA, PA | – | – | – | R | CRUA | – | – | R | – | C | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-041 | Point-in-time bakiye sorgusu | FR-039 | TA | – | – | – | – | R | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-042 | Manuel düzeltme (ters kayıt, maker-checker) | FR-041 | TA | – | – | – | – | CA | – | – | R | C | – | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-043 | Defter bütünlük (invariant) kontrolü | FR-042 | TA, PA | – | – | – | – | R | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-044 | Journal sorgulama ve drill-down | FR-044 | TA | – | – | – | – | R | – | R | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |

### Yükleme

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-045 | Kartla 3DS yükleme | FR-045, FR-169 | MOB | C | – | – | – | R | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-046 | PSP adaptörü ve mock PSP yapılandırması | FR-046 | PA | – | – | – | – | – | – | – | R | – | CRU | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-047 | Kayıtlı kart yönetimi | FR-047 | MOB | CRD | – | – | – | – | – | – | R | RD | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-048 | Otomatik yükleme | FR-048 | MOB | CRUD | – | – | – | – | – | – | R | RU | – | ● | ● | ● | ○ | ○ | Evet | M3 | Planned |
| FN-049 | Yükleme tutar kuralları | FR-049 | TA | – | – | – | CRU | – | – | R | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-050 | Yükleme iadesi (karta) | FR-050 | TA | C | – | – | – | A | – | – | R | C | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-051 | Kurumsal / sponsor toplu yükleme | FR-053 | TA, API | – | – | – | C | A | – | – | R | – | – | ○ | – | ○ | – | ● | Hayır | M5 | Planned |
| FN-052 | Kasada nakit yükleme | FR-054 | POS | – | C | A | – | R | – | – | R | – | – | ○ | – | ○ | ● | ● | Hayır | M5 | Planned |
| FN-053 | Havale / EFT ile yükleme | FR-051 | MOB, TA | C | – | – | – | RA | – | – | R | – | – | ○ | ○ | ○ | ○ | ○ | Hayır | M7 | Planned |
| FN-054 | Çoklu PSP yönlendirme ve failover | FR-055 | PA | – | – | – | – | R | – | – | R | – | CRUA | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-055 | Açık bankacılık ile yükleme | FR-052 | MOB | C | – | – | – | R | – | – | R | – | – | ○ | ○ | ○ | ○ | ○ | Hayır | M8 | Planned |

### Ödeme

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-056 | Müşteri QR ile ödeme (sale) | FR-056, FR-058, FR-075 | MOB, POS, API | C | C | C | – | – | – | – | R | R | – | ● | ○ | ○ | ● | ● | Evet | M3 | Planned |
| FN-057 | Ödeme yetkilendirme kontrolleri | FR-057 | API | – | – | – | – | – | R | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-058 | İptal (void) | FR-059 | POS, API | – | C | CA | – | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-059 | İade (tam / kısmi) | FR-060 | POS, TA, API | – | C | CA | – | A | – | – | R | C | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-060 | Ödeme durum sorgulama ve idempotency | FR-061 | POS, API | – | R | R | – | – | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-061 | Pre-auth (hold) oluşturma | FR-062 | MOB, API | C | – | – | – | – | – | – | R | R | – | – | ● | ● | ○ | – | Evet | M3 | Planned |
| FN-062 | Capture (tam / kısmi) | FR-063 | API | – | – | – | – | – | – | – | R | R | – | – | ● | ● | ○ | – | Evet | M3 | Planned |
| FN-063 | Hold iptali ve süre dolumu | FR-065 | API, TA | – | – | C | – | – | – | – | R | R | – | – | ● | ● | ○ | – | Evet | M3 | Planned |
| FN-064 | Incremental authorization | FR-064 | API | – | – | – | – | – | – | – | R | R | – | – | ● | ○ | – | – | Hayır | M5 | Planned |
| FN-065 | Abonelik tahsilatı | FR-066 | MOB, API | CRUD | – | – | CRU | – | – | – | R | R | – | – | ○ | ● | – | ○ | Hayır | M5 | Planned |
| FN-066 | İşyeri QR ile ödeme | FR-067 | MOB, POS | C | C | – | – | – | – | – | R | – | – | ● | ○ | ○ | ● | ● | Hayır | M5 | Planned |
| FN-067 | NFC / bileklik / kart ile ödeme ve medya yönetimi | FR-068 | POS, MOB | CRUD | C | U | – | – | – | – | R | U | – | ○ | ○ | – | ● | ● | Hayır | M5 | Planned |
| FN-068 | Bölünmüş ödeme (cüzdan + kart) | FR-069 | POS, API | – | C | – | – | – | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M8 | Planned |

### İşyeri/POS

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-069 | İşyeri - mağaza - terminal hiyerarşisi | FR-071, FR-074, FR-152 | TA | – | – | RU | CRUD | R | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-070 | Terminal aktivasyonu ve kimlik bilgisi yönetimi | FR-072 | TA, POS | – | – | CU | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-071 | Kasiyer kullanıcı ve PIN yönetimi | FR-073 | TA, POS | – | U | CRUD | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-072 | Web POS gün sonu ve vardiya raporu | FR-076, FR-131 | POS, TA | – | R | R | R | R | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-073 | POS REST API | FR-077 | API | – | – | – | R | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-074 | Webhook abonelik yönetimi | FR-078, FR-181 | TA, API | – | – | – | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-075 | Harici sistem adaptörleri (CSMS / LPR / turnike) | FR-079 | API, PA | – | – | – | CRU | – | – | – | R | – | CRU | – | ● | ● | ● | ○ | Hayır | M5 | Planned |
| FN-076 | Plaka yönetimi | FR-176 | MOB | CRUD | – | – | – | – | – | – | R | RD | – | – | – | ● | – | – | Hayır | M5 | Planned |

### Sadakat/Kampanya

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-077 | Puan / yıldız kazanım kuralları | FR-080 | TA | – | – | – | CRUA | R | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-078 | Ödül kataloğu ve ödül kullanımı | FR-081, FR-173 | MOB, POS, TA | CR | C | – | CRUD | – | – | – | R | R | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-079 | Seviye (tier) yönetimi | FR-082 | TA | R | – | – | CRUA | – | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-080 | Kampanya kural motoru ve segmentler | FR-083, FR-087 | TA | – | – | – | CRUA | R | R | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |
| FN-081 | Kupon üretimi ve kullanımı | FR-084 | TA, POS, MOB | R | C | – | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |
| FN-082 | Cashback kampanyaları | FR-085 | TA | – | – | – | CRUA | A | – | – | R | – | – | ● | ● | ● | ○ | ○ | Hayır | M5 | Planned |
| FN-083 | Olay tetikli ödüller (hoş geldin, doğum günü) | FR-086 | TA | – | – | – | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |
| FN-084 | Kampanya bütçesi ve kötüye kullanım sınırları | FR-088 | TA | – | – | – | CRU | RA | R | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |
| FN-085 | Puan son kullanma ve bildirim | FR-089 | TA | – | – | – | CRU | R | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |

### Hediye kartı

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-086 | Dijital hediye kartı satın alma / gönderme | FR-090, FR-175 | MOB | CR | – | – | – | – | – | – | R | R | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-087 | Toplu hediye kodu üretimi (B2B) | FR-091 | TA | – | – | – | C | A | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-088 | Hediye kartı aktivasyon, bakiye, cüzdana ekleme | FR-092, FR-093, FR-094 | MOB, POS, API | CR | C | – | – | – | – | – | R | R | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-089 | Hediye kartı bloke / iptal / yeniden basım | FR-096 | TA | – | – | – | – | A | – | – | R | C | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |
| FN-090 | Hediye kartı son kullanma ve breakage | FR-095 | TA | – | – | – | CRU | RA | – | – | R | – | – | ● | ○ | ○ | ● | ○ | Hayır | M5 | Planned |

### Risk

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-091 | Temel limit ve velocity kuralları | FR-097, FR-098 | TA | – | – | – | R | – | CRUA | R | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-092 | Gerçek zamanlı kural motoru ve shadow mode | FR-099, FR-104 | TA | – | – | – | – | – | CRUA | R | R | – | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-093 | Risk skoru ve cihaz parmak izi | FR-100, FR-101 | TA, MOB | – | – | – | – | – | RU | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-094 | Kara / beyaz liste yönetimi | FR-102 | TA, PA | – | – | – | – | – | CRUDA | – | R | – | CRUD | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-095 | Risk vaka yönetimi ve promosyon suistimali | FR-103, FR-105 | TA | – | – | – | – | – | CRUA | R | R | C | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |

### Uyum

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-096 | Yaptırım / PEP taraması | FR-107 | TA | – | – | – | – | – | – | RUA | R | – | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-097 | AML işlem izleme senaryoları | FR-108 | TA | – | – | – | – | – | R | CRUA | R | – | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-098 | STR iş akışı ve uyum vaka kaydı | FR-109, FR-110 | TA | – | – | – | – | – | – | CRUA | R | – | – | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-099 | Sınırlı ağ eşik izleme | FR-113 | TA, PA | – | – | – | R | R | – | R | R | – | R | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-100 | Veri saklama ve imha politikası | FR-111 | TA, PA | – | – | – | – | – | – | CRUA | R | – | U | ● | ● | ● | ● | ● | Hayır | M6 | Planned |
| FN-101 | Regülatör raporları | FR-112 | TA | – | – | – | – | R | – | CRA | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |

### Takas/Mutabakat

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-102 | İşyeri takas batch hesaplaması | FR-114 | TA | – | – | R | – | RA | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-103 | PSP / banka dosyası alma ve otomatik eşleştirme | FR-115, FR-116, FR-118 | TA, PA | – | – | – | – | R | – | – | R | – | U | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-104 | Mutabakat istisna yönetimi | FR-117 | TA | – | – | – | – | CRUA | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-105 | İşyeri ödeme talimatı (payout) dosyası | FR-119 | TA | – | – | – | – | CA | – | – | R | – | – | ○ | ○ | ○ | ○ | ○ | Hayır | M7 | Planned |
| FN-106 | Mutabakat raporu ve günlük sertifika | FR-120 | TA | – | – | – | R | R | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |

### Muhasebe

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-107 | GL hesap eşleme | FR-121 | TA | – | – | – | – | CRUA | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-108 | Yevmiye export ve ERP adaptörü | FR-122, FR-123 | TA, API | – | – | – | – | CR | – | – | R | – | U | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-109 | e-Fatura / e-Arşiv entegrasyonu | FR-124 | TA | – | – | – | – | CR | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-110 | Breakage ve ertelenmiş gelir hesaplama | FR-125, FR-126 | TA | – | – | – | – | RA | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-111 | Muhasebe dönemi kapanışı | FR-127 | TA | – | – | – | – | UA | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |

### Raporlama

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-112 | Operasyonel dashboard | FR-128 | TA | – | – | R | R | R | R | R | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-113 | İşlem raporu ve CSV export | FR-129 | TA | – | – | R | R | R | R | R | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-114 | Müşteri bakiye / yükümlülük raporu | FR-130 | TA | – | – | – | R | R | – | R | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-115 | KPI raporu (North Star: MTAW) | FR-132 | TA, PA | – | – | – | R | R | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-116 | Planlı raporlar ve XLSX / PDF export | FR-133, FR-134 | TA | – | – | R | CRUD | CRUD | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-117 | Analitik veri ambarı (ClickHouse BI) | FR-135 | TA, PA | – | – | – | R | R | R | – | R | – | R | ● | ● | ● | ● | ● | Hayır | M7 | Planned |

### Audit/Teftiş

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-118 | Hash-zincirli audit log kaydı | FR-136 | API | – | – | – | – | – | – | R | R | – | R | ● | ● | ● | ● | ● | Evet | M2 | Planned |
| FN-119 | Maker-checker onay kuyruğu | FR-137, FR-154 | TA, PA | – | – | A | CA | CA | CA | CA | R | – | CA | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-120 | Teftiş sorgu ekranı | FR-138 | TA, PA | – | – | – | – | – | – | R | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-121 | Audit zincir bütünlük doğrulama | FR-139 | TA, PA | – | – | – | – | – | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-122 | Delil paketi export (imzalı) | FR-140 | TA, PA | – | – | – | – | – | – | R | RC | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-123 | Audit arşivi (WORM) ve geri getirme | FR-142 | PA | – | – | – | – | – | – | – | R | – | RU | ● | ● | ● | ● | ● | Hayır | M8 | Planned |

### Bildirim

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-124 | Push ve e-posta işlemsel bildirimler | FR-143, FR-144 | MOB | R | – | – | – | – | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-125 | Çok dilli bildirim şablon yönetimi | FR-146 | TA | – | – | – | CRUD | – | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-126 | Bildirim tercihleri ve İYS entegrasyonu | FR-147 | MOB, TA | RU | – | – | – | – | – | R | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-127 | SMS bildirimleri ve uygulama içi gelen kutusu | FR-145, FR-148 | MOB, TA | R | – | – | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |

### Admin Portal

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-128 | Admin kullanıcı ve rol yönetimi (RBAC + kapsam) | FR-149 | TA | – | – | R | CRUDA | – | – | R | R | – | R | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-129 | İşlem arama ve detay | FR-151 | TA | – | – | R | R | R | R | R | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-130 | Konfigürasyon ekranları (limit, ücret, hold süresi) | FR-153 | TA | – | – | – | CRUA | A | R | R | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-131 | Destek aksiyonları (bloke, iade talebi, not) | FR-155 | TA | – | – | R | – | – | R | – | R | CU | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |

### Platform Admin

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-132 | Tenant sağlık ve SLO paneli | FR-160 | PA | – | – | – | – | – | – | – | R | – | R | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-133 | Break-glass erişim | FR-161 | PA | – | – | – | – | – | – | R | R | – | CA | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-134 | Global parametreler (PSP, ülke, global listeler) | FR-162 | PA | – | – | – | – | – | – | – | R | – | CRUA | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-135 | Platform faturalandırma ve kullanım ölçümü | FR-163 | PA, TA | – | – | – | R | R | – | – | R | – | CRUA | ● | ● | ● | ● | ● | Hayır | M7 | Planned |
| FN-136 | Tenant veri dışa aktarımı ve sonlandırma | FR-164 | PA | – | – | – | R | – | – | A | R | – | CA | ● | ● | ● | ● | ● | Hayır | M8 | Planned |

### Mobil App

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-137 | White-label build ve mağaza yayını | FR-165 | PA | – | – | – | RA | – | – | – | R | – | CRU | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-138 | Mobil onboarding ve ana ekran | FR-166, FR-167 | MOB | CRU | – | – | – | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-139 | QR ödeme ekranı ve offline token | FR-168 | MOB | R | – | – | – | – | – | – | R | – | – | ● | ○ | ○ | ● | ● | Evet | M4 | Planned |
| FN-140 | İşlem geçmişi ve dijital makbuz | FR-170 | MOB | R | – | – | – | – | – | – | R | R | – | ● | ● | ● | ● | ● | Evet | M4 | Planned |
| FN-141 | Aktif oturum ekranı (EV şarj / otopark) | FR-172 | MOB | R | – | – | – | – | – | – | R | R | – | – | ● | ● | – | – | Evet | M4 | Planned |
| FN-142 | Mağaza / istasyon bulucu | FR-177 | MOB | R | – | – | CRU | – | – | – | R | – | – | ● | ● | ● | ○ | ○ | Hayır | M5 | Planned |

### Public API

| FN | Fonksiyon | FR | Kanal | Cust | Cash | StMgr | TAdm | Fin | Risk | Cmp | Aud | Sup | PAdm | Kahve | EV | Otopark | Eğlence | Kampüs | MVP | MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| FN-143 | Geliştirici portalı ve sandbox | FR-178, FR-180 | API | – | – | – | R | – | – | – | R | – | CRU | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-144 | API istemci, kapsam ve rate limit yönetimi | FR-179, FR-182 | TA, API | – | – | – | CRUDA | – | – | – | R | – | RU | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-145 | Hata modeli (RFC 9457) ve Idempotency-Key standardı | FR-183 | API | – | – | – | – | – | – | – | R | – | – | ● | ● | ● | ● | ● | Evet | M3 | Planned |
| FN-146 | Tenant backend API (müşteri, bakiye, sponsor yükleme) | FR-185 | API | – | – | – | CRUD | – | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M5 | Planned |
| FN-147 | Resmi SDK'lar (Java, TypeScript) | FR-184 | API | – | – | – | – | – | – | – | R | – | – | ● | ● | ● | ● | ● | Hayır | M8 | Planned |

> **Kapsam dışı (W):** FR-070 (P2P bakiye transferi) v2.0 kapsamı dışında olduğundan matriste FN olarak yer almaz.

---

## 4. Değişiklik Günlüğü

| Sprint | Tarih | Değişiklik | Onay |
|---|---|---|---|
| S0 | 2026-10-16 (planlanan) | Baseline: 147 fonksiyon, tümü `Planned` | PO (bekliyor) |
