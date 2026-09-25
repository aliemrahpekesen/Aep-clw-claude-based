# AEP-CLW Ürün Backlog'u

> Bu dosya `tools/backlog/backlog_source.py` tarafından üretilir; elle düzenlemeyin. GitHub Issues ile `backlog-sync` iş akışı üzerinden senkronize edilir.

**Özet:** 9 milestone · 31 epic · 125 story · 600 story point (MVP: 408 SP)

## Milestone'lar

| Kod | Başlık | Bitiş | Açıklama |
|---|---|---|---|
| M0 | M0 - Inception & Architecture | 2026-10-16 | Vizyon, mimari, güvenlik/uyum tasarımı, backlog, prototip ve onay. Sprintler: S0 (2026-10-05 → 2026-10-16) |
| M1 | M1 - Platform Foundation | 2026-11-13 | Monorepo, platform-commons, CI/CD, OpenShift dev/test, Keycloak, gateway, tenant servisi. Sprintler: S1, S2 (2026-10-19 → 2026-11-13) |
| M2 | M2 - Core Wallet & Ledger | 2026-12-11 | Müşteri & KYC Tier0/1, çift kayıtlı ledger, cüzdan, gözlemlenebilirlik. Sprintler: S3, S4 (2026-11-16 → 2026-12-11) |
| M3 | M3 - Funding & Payments | 2027-01-08 | Kartla yükleme, QR ödeme, pre-auth, iade, işyeri/POS, limitler, mobil uygulama, bildirim. Sprintler: S5, S6 (2026-12-14 → 2027-01-08) |
| M4 | M4 - Admin, Reporting & Audit - MVP v1.0 | 2027-02-05 | Tenant Admin Portalı, Platform Admin, raporlar, audit/teftiş, UAT ve MVP sürümü. Sprintler: S7, S8 (2027-01-11 → 2027-02-05) |
| M5 | M5 - Loyalty, Campaigns & Gift Cards | 2027-03-05 | Puan/tier, kampanya kural motoru, cashback, kupon, hediye kartı. Sprintler: S9, S10 (2027-02-08 → 2027-03-05) |
| M6 | M6 - Risk, AML & Compliance | 2027-04-02 | Gelişmiş fraud motoru, vaka yönetimi, AML/yaptırım taraması, MASAK raporlama, KYC Tier2/3. Sprintler: S11, S12 (2027-03-08 → 2027-04-02) |
| M7 | M7 - Settlement, Accounting & Banking | 2027-04-30 | Takas & mutabakat, muhasebe/GL/e-Fatura/ERP, banka & açık bankacılık, ClickHouse BI. Sprintler: S13, S14 (2027-04-05 → 2027-04-30) |
| M8 | M8 - Production Hardening & GA v2.0 | 2027-05-28 | Performans, chaos, DR, pentest, PCI/SOC2 hazırlık, çoklu tenant pilot ve GA. Sprintler: S15, S16 (2027-05-03 → 2027-05-28) |

## Sprint kapasite özeti

| Sprint | Pencere | Story | SP |
|---|---|---|---|
| S00 | 2026-10-05 → 2026-10-16 | 9 | 39 |
| S01 | 2026-10-19 → 2026-10-30 | 10 | 42 |
| S02 | 2026-11-02 → 2026-11-13 | 15 | 65 |
| S03 | 2026-11-16 → 2026-11-27 | 7 | 32 |
| S04 | 2026-11-30 → 2026-12-11 | 9 | 42 |
| S05 | 2026-12-14 → 2026-12-25 | 8 | 46 |
| S06 | 2026-12-28 → 2027-01-08 | 10 | 51 |
| S07 | 2027-01-11 → 2027-01-22 | 7 | 38 |
| S08 | 2027-01-25 → 2027-02-05 | 14 | 53 |
| S09 | 2027-02-08 → 2027-02-19 | 3 | 21 |
| S10 | 2027-02-22 → 2027-03-05 | 5 | 21 |
| S11 | 2027-03-08 → 2027-03-19 | 3 | 18 |
| S12 | 2027-03-22 → 2027-04-02 | 4 | 23 |
| S13 | 2027-04-05 → 2027-04-16 | 5 | 34 |
| S14 | 2027-04-19 → 2027-04-30 | 6 | 31 |
| S15 | 2027-05-03 → 2027-05-14 | 4 | 21 |
| S16 | 2027-05-17 → 2027-05-28 | 6 | 23 |

## M0 - Inception & Architecture

### [E01] Epic: Inception, Governance & Architecture Baseline

Proje tüzüğü, mimari, güvenlik/uyum tasarımı, backlog ve tıklanabilir prototip; kullanıcı onayı ile kodlamaya geçiş.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S001 | Proje tüzüğü, ekip ve RACI | S00 | governance | 2 | P0 | docs/00-project-charter.md ve docs/product/raci.md yayınlandı<br>DoR/DoD tanımlı |
| S002 | Mimari dokümantasyon ve ADR seti | S00 | architecture | 8 | P0 | docs/architecture altında tüm dokümanlar mevcut<br>ADR'ler Proposed durumunda ve CA onayına hazır |
| S003 | Güvenlik mimarisi ve tehdit modeli (STRIDE) | S00 | security | 5 | P0 | En az 30 tehdit ve kontrolü tanımlı<br>Güvenlik kapıları CI tasarımına eşlendi |
| S004 | Regülasyon çerçevesi, AML/KYC politikası ve kontrol matrisi | S00 | compliance | 5 | P0 | docs/compliance/control-matrix.md en az 40 kontrol içerir<br>Her kontrol bir milestone'a eşlenmiş |
| S005 | Gereksinimler, fonksiyon matrisi ve MVP kapsamı | S00 | analysis | 5 | P0 | FR ≥ 120, NFR ≥ 30, FN ≥ 80<br>MVP kapsamı ve başarı kriterleri onaya hazır |
| S006 | Test stratejisi, performans planı ve DevOps tasarımı | S00 | qa | 5 | P0 | docs/quality ve docs/devops yayınlandı |
| S007 | Tıklanabilir prototip ve proje sunumu | S00 | ux | 5 | P0 | Prototip ve sunum paylaşıldı<br>Kullanıcı geri bildirimi toplandı |
| S008 | Backlog-as-code ve GitHub proje otomasyonu | S00 | devops | 3 | P0 | backlog-sync workflow'u idempotent çalışır<br>Tüm epic/story'ler milestone ve label'larıyla GitHub'da |
| S009 | Sprint 0 review ve kodlama onayı | S00 | governance | 1 | P0 | Kullanıcı onayı kayıt altına alındı (issue yorumu) |


## M1 - Platform Foundation

### [E02] Epic: Engineering Foundation

Monorepo, build sistemi, ortak platform kütüphaneleri ve yerel geliştirme ortamı.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S010 | Monorepo iskeleti (Gradle multi-module + pnpm workspace) | S01 | backend | 3 | P0 | ./gradlew build yeşil<br>pnpm -r build yeşil<br>Kod stili (Spotless, ESLint, Prettier) zorunlu |
| S011 | platform-commons: tenant context, hata modeli, Money tipi | S01 | backend | 5 | P0 | Tenant context thread/reactive/Kafka boyunca taşınır (testli)<br>Money aritmetiği property-based test ile doğrulanır |
| S012 | platform-commons: idempotency ve transactional outbox | S01 | backend | 5 | P0 | Aynı Idempotency-Key ile tekrar istek aynı yanıtı döner<br>Outbox kaydı iş transaction'ı ile atomik yazılır |
| S013 | Servis şablonu (hexagonal) ve ArchUnit kuralları | S01 | backend | 3 | P0 | Domain katmanı Spring'e bağımlı değil (ArchUnit)<br>Şablondan servis 5 dk içinde üretilebilir |
| S014 | Yerel geliştirme ortamı (docker-compose) | S01 | devops | 3 | P0 | make up ile tüm bağımlılıklar ayağa kalkar<br>README'de 10 dakikada kurulum |
| S015 | PostgreSQL standartları: Flyway, RLS, tenant politikaları | S02 | data | 5 | P0 | RLS olmadan tenant verisine erişim testi başarısız olur<br>Migration'lar expand-contract uyumlu |
| S016 | Kafka event standartları (CloudEvents, Avro, Schema Registry) | S02 | backend | 3 | P1 | Schema uyumluluk kontrolü CI'da<br>DLQ akışı entegrasyon testli |

### [E03] Epic: CI/CD & DevSecOps Pipeline

PR ve main pipeline'ları, güvenlik taramaları, imaj üretimi, SBOM ve imzalama.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S017 | PR pipeline: build, test, lint, ArchUnit | S01 | devops | 3 | P0 | PR'da zorunlu status check<br>Ortalama süre < 10 dk |
| S018 | Güvenlik kapıları: SAST, SCA, secret scan, IaC scan | S01 | security | 5 | P0 | Critical bulgu PR'ı bloklar<br>Raporlar artifact olarak saklanır |
| S019 | Kalite kapısı: coverage ve SonarQube | S02 | qa | 3 | P1 | Domain coverage ≥ %80<br>0 blocker/critical |
| S020 | Konteyner imajı, Trivy, SBOM (CycloneDX), Cosign imza | S02 | devops | 5 | P0 | Imzasız imaj cluster'a deploy edilemez<br>SBOM her release'e eklenir |
| S021 | Release otomasyonu (SemVer, Conventional Commits, changelog) | S02 | devops | 2 | P2 | Tag'ten otomatik release notları |

### [E04] Epic: OpenShift Platform & GitOps

Dev/test ortamları, Helm library chart, ArgoCD, veri servisleri operatörleri.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S022 | Helm library chart ve servis chart standardı | S01 | devops | 5 | P0 | Tüm servisler aynı library chart'ı kullanır<br>helm lint + kubeconform CI'da |
| S023 | ArgoCD app-of-apps ve ortam promotion | S02 | devops | 5 | P0 | main merge sonrası dev'e otomatik deploy<br>Rollback tek commit revert ile |
| S024 | Veri platformu: CloudNativePG, Strimzi Kafka, Redis, Vault | S02 | devops | 8 | P0 | PITR yedekleme aktif<br>Servisler statik parola kullanmaz |
| S025 | NetworkPolicy default-deny ve service mesh mTLS | S02 | security | 3 | P0 | Yetkisiz pod-pod trafiği engellenir (test) |

### [E05] Epic: Identity & Access Management

Keycloak, API Gateway, OTP, cihaz bağlama, RBAC.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S026 | Keycloak kurulumu: realm, organization-per-tenant, roller | S01 | security | 5 | P0 | Realm konfigürasyonu kod olarak (export/import)<br>MFA admin kullanıcılar için zorunlu |
| S027 | api-gateway: JWT doğrulama, tenant çözümleme, rate limit | S02 | backend | 5 | P0 | Tenant uyuşmazlığında 403<br>Rate limit tenant planına göre |
| S028 | identity-service: telefon OTP kayıt/giriş | S02 | backend | 5 | P0 | OTP 3 hatalı denemede kilitlenir<br>OTP loglarda maskelenir |
| S029 | Cihaz bağlama ve step-up authentication | S02 | security | 5 | P1 | Yeni cihazdan yüksek tutarlı işlem step-up ister |

### [E06] Epic: Tenant Management & Configuration

Tenant onboarding, konfigürasyon, sektör presetleri, feature flag, marka.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S030 | tenant-service: tenant CRUD ve yaşam döngüsü | S01 | backend | 5 | P0 | Yaşam döngüsü event'leri yayınlanır<br>Tüm değişiklikler audit'e düşer |
| S031 | Tenant konfigürasyon şeması ve versiyonlama | S02 | backend | 5 | P0 | Geçersiz konfigürasyon reddedilir<br>Konfigürasyon değişikliği maker-checker gerektirir |
| S032 | Sektör presetleri (Kahve, EV, Otopark, Eğlence, Kampüs) | S02 | backend | 3 | P1 | 5 preset şema ile doğrulanır |
| S033 | Feature flag ve marka/tema servisi | S02 | backend | 3 | P1 | Mobil ve portal temayı çalışma zamanında çeker |
| S034 | Otomatik tenant provisioning | S02 | devops | 5 | P1 | Yeni tenant < 2 dk'da kullanıma hazır |


## M2 - Core Wallet & Ledger

### [E07] Epic: Customer & KYC (Tier 0/1)

Müşteri profili, onaylar, KYC seviyeleri.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S035 | customer-service: profil ve yaşam döngüsü | S03 | backend | 5 | P0 | PII alanları field-level şifreli<br>Bloke müşteri işlem yapamaz |
| S036 | KVKK/GDPR onay yönetimi | S03 | compliance | 3 | P0 | Onay geçmişi değiştirilemez şekilde saklanır |
| S037 | KYC Tier 0/1 ve limit profili bağlama | S04 | backend | 3 | P0 | Tier limitleri wallet-service tarafından uygulanır |
| S038 | Veri sahibi talepleri (erişim/silme) ve crypto-shredding | S04 | compliance | 5 | P1 | Silme sonrası PII okunamaz, ledger bütünlüğü korunur |

### [E08] Epic: Double-Entry Ledger

Değiştirilemez, çift kayıtlı defter; sistemin finansal doğruluk kaynağı.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S039 | ledger-service: hesap planı ve hesap açma | S03 | backend | 5 | P0 | Her tenant için varsayılan hesap planı otomatik oluşur |
| S040 | Journal posting API (atomik, idempotent, dengeli) | S03 | backend | 8 | P0 | Dengesiz journal reddedilir<br>Aynı referans ikinci kez post edilemez<br>UPDATE/DELETE DB seviyesinde yasak |
| S041 | Bakiye hesaplama, snapshot ve eşzamanlılık | S04 | backend | 8 | P0 | 1000 eşzamanlı harcamada çifte harcama yok (test)<br>p99 posting < 50ms |
| S042 | Hold (provizyon) ve release/capture | S04 | backend | 5 | P0 | Kısmi capture ve fazla tutarın serbest bırakılması |
| S043 | Ledger invariant testleri ve günlük bütünlük kontrolü | S04 | qa | 5 | P0 | Trial balance ≠ 0 ise kritik alarm<br>Mutation score ≥ %60 |

### [E09] Epic: Wallet

Cüzdan hesapları, çoklu cüzdan, limit kontrolü, işlem geçmişi.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S044 | wallet-service: cüzdan açma (ana + bonus) ve durum yönetimi | S03 | backend | 5 | P0 | Kayıtta varsayılan cüzdanlar otomatik açılır |
| S045 | Bakiye sorgulama ve harcama önceliği (bonus → ana) | S04 | backend | 3 | P0 | Harcama sırası konfigürasyondan okunur (test) |
| S046 | Limit motoru (tek işlem, günlük, aylık, bakiye tavanı) | S04 | backend | 5 | P0 | Limit aşımında açıklayıcı hata kodu |
| S047 | İşlem geçmişi okuma modeli (CQRS) | S04 | backend | 3 | P0 | p95 < 150ms, 12 aylık geçmiş |

### [E10] Epic: Observability

OpenTelemetry, metrik, log, trace, SLO ve alarmlar.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S048 | OpenTelemetry enstrümantasyonu ve trace yayılımı | S03 | devops | 3 | P0 | Uçtan uca trace Tempo'da görünür |
| S049 | Loki log standardı ve PII maskeleme | S03 | security | 3 | P0 | PAN/telefon/TCKN loglarda maskeli (test) |
| S050 | Grafana dashboard'ları, SLO ve alarm kuralları | S04 | devops | 5 | P1 | Her servis için SLO dashboard'ı |


## M3 - Funding & Payments

### [E11] Epic: Funding (Top-up)

Kartla yükleme, kayıtlı kart, otomatik yükleme, PSP adaptörleri.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S051 | funding-service: yükleme sagası ve PSP portu | S05 | backend | 8 | P0 | PSP timeout'unda durum sorgulama ile kesinleşir<br>Çift webhook çift yükleme yaratmaz |
| S052 | PSP adaptörü #1 (iyzico) + mock PSP | S05 | backend | 5 | P0 | Sandbox ile E2E test<br>Kart verisi sistemimize girmez |
| S053 | Kayıtlı kart (tokenization) ve otomatik yükleme | S06 | backend | 5 | P1 | Otomatik yükleme günlük limitli ve iptal edilebilir |
| S054 | Kasada nakit yükleme (POS üzerinden) | S06 | backend | 3 | P2 | Kasiyer günlük yükleme limiti uygulanır |

### [E12] Epic: Payments

QR/token ile ödeme, pre-auth/capture, iade, iptal.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S055 | Dinamik müşteri QR token (TOTP tabanlı) | S05 | security | 5 | P0 | Replay edilen token reddedilir<br>Offline üretim desteklenir |
| S056 | payment-service: authorize/capture (tek adım ödeme) | S05 | backend | 8 | P0 | p99 < 300ms<br>Idempotent |
| S057 | Pre-auth (EV şarj/otopark): hold → final capture | S06 | backend | 5 | P0 | Kısmi capture, süre aşımında otomatik iptal |
| S058 | İade (tam/kısmi) ve iptal (reversal) | S06 | backend | 5 | P0 | İade toplamı orijinal tutarı aşamaz |
| S059 | Basit risk: velocity ve limit kuralları (MVP) | S06 | backend | 5 | P0 | Kural değişikliği yeniden deploy gerektirmez |

### [E13] Epic: Merchant, Store & POS

İşyeri hiyerarşisi, terminaller, POS API ve Web POS.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S060 | merchant-service: işyeri → mağaza → terminal | S05 | backend | 5 | P0 | Terminal API anahtarı hash'li saklanır |
| S061 | POS REST API ve webhook'lar (OpenAPI) | S06 | backend | 5 | P0 | OpenAPI dokümanı ve Postman koleksiyonu |
| S062 | Web POS terminali (React PWA) | S06 | frontend | 8 | P0 | Tablet ve dokunmatik uyumlu<br>Playwright E2E |

### [E14] Epic: Customer Mobile App (White-label)

React Native (Expo) white-label müşteri uygulaması.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S063 | Mobil uygulama iskeleti, tema motoru, i18n | S05 | mobile | 5 | P0 | Tek kod tabanından tenant bazlı build |
| S064 | Kayıt/giriş (OTP), cihaz bağlama, biyometrik | S05 | mobile | 5 | P0 | OWASP MASVS L2 kontrolleri |
| S065 | Ana sayfa, bakiye, işlem geçmişi | S06 | mobile | 5 | P0 | Erişilebilirlik: ekran okuyucu etiketleri |
| S066 | Yükleme ve QR ile ödeme ekranları | S06 | mobile | 8 | P0 | Detox/Maestro E2E |

### [E15] Epic: Notifications

Push, SMS, e-posta; tenant şablonları.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S067 | notification-service: kanal adaptörleri ve şablonlar | S05 | backend | 5 | P1 | Event'lerden tetiklenen bildirimler<br>Başarısız gönderim retry + DLQ |
| S068 | Bildirim tercihleri ve sessiz saatler | S06 | backend | 2 | P2 | Pazarlama bildirimi onaysız gönderilmez |


## M4 - Admin, Reporting & Audit - MVP v1.0

### [E16] Epic: Tenant Admin Portal

Tenant yöneticileri için web portal (React).

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S069 | Portal iskeleti, design system, RBAC menü | S07 | frontend | 5 | P0 | WCAG 2.2 AA (axe) hatasız |
| S070 | Dashboard (KPI ve grafikler) | S07 | frontend | 5 | P0 | Veriler reporting-service'ten, 1 dk gecikme |
| S071 | Müşteri yönetimi ve müşteri 360 | S07 | frontend | 5 | P0 | Hassas alanlar role göre maskeli |
| S072 | İşlem arama, detay ve iade başlatma | S07 | frontend | 5 | P0 | İade maker-checker ile onaylanır |
| S073 | İşyeri/mağaza/terminal yönetimi | S08 | frontend | 3 | P0 | API anahtarı yalnızca bir kez gösterilir |
| S074 | Kullanıcı & rol yönetimi, maker-checker kuyruğu | S08 | frontend | 5 | P0 | Kendi talebini onaylayamaz (SoD) |
| S075 | Tenant ayarları ekranı (konfigürasyon) | S08 | frontend | 3 | P1 | Değişiklikler versiyonlanır ve onaylanır |

### [E17] Epic: Platform Admin Console

SaaS operatörü için tenant ve sistem yönetimi.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S076 | Tenant listesi ve onboarding sihirbazı | S07 | frontend | 5 | P0 | Sihirbaz provisioning'i tetikler |
| S077 | Plan/abonelik ve kullanım ölçümü (metering) | S08 | backend | 5 | P1 | Aylık kullanım raporu |
| S078 | Sistem sağlığı görünümü | S08 | frontend | 2 | P2 | Grafana'ya derin bağlantılar |

### [E18] Epic: Operational Reporting

Operasyonel ve finansal raporlar, planlı raporlar, export.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S079 | reporting-service: okuma modelleri ve rapor API | S07 | backend | 5 | P0 | Rapor sonuçları ledger ile tutarlı (mutabakat testi) |
| S080 | Yükümlülük (float) raporu ve günlük finansal özet | S08 | backend | 5 | P0 | Ledger trial balance ile birebir |
| S081 | Export (CSV/XLSX/PDF) ve planlı raporlar | S08 | backend | 3 | P1 | Büyük exportlar arka planda, imzalı link |

### [E19] Epic: Audit & Inspection

Değiştirilemez audit log, teftiş ekranı, delil paketi.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S082 | audit-service: hash-zincirli audit log | S07 | security | 8 | P0 | Zincir kırılması tespit edilir ve alarm üretir |
| S083 | Teftiş (müfettiş) ekranı ve sorgular | S08 | frontend | 5 | P0 | Müfettiş hiçbir veriyi değiştiremez |
| S084 | Delil paketi (evidence pack) export | S08 | security | 3 | P1 | Paket bütünlüğü bağımsız doğrulanabilir |

### [E20] Epic: MVP Release Readiness

UAT, performans baz çizgisi, güvenlik incelemesi, dokümantasyon, pilot.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S085 | E2E regresyon paketi ve UAT | S08 | qa | 5 | P0 | Kritik senaryolar %100 geçer |
| S086 | Performans baz çizgisi (1.000 TPS) | S08 | perf | 5 | P0 | 1.000 TPS'de p99 < 300ms |
| S087 | MVP güvenlik incelemesi ve DAST | S08 | security | 3 | P0 | High/Critical açık yok |
| S088 | Kullanıcı ve API dokümantasyonu, runbook'lar | S08 | docs | 3 | P0 | Dokümanlar yayında |
| S089 | MVP v1.0 sürümü ve pilot canlıya geçiş | S08 | devops | 3 | P0 | Go/No-Go onayı alındı |


## M5 - Loyalty, Campaigns & Gift Cards

### [E21] Epic: Loyalty & Campaigns

Puan/yıldız, tier, kampanya kural motoru, cashback, kupon.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S090 | loyalty-service: puan hesabı ve tier yönetimi | S09 | backend | 8 | P1 | Puan hareketleri ledger'dan ayrı ama mutabık |
| S091 | Kampanya kural motoru (koşul → ödül DSL) | S09 | backend | 8 | P1 | Kural simülasyonu (dry-run) |
| S092 | Cashback ve bonus yükleme kampanyaları | S10 | backend | 5 | P1 | Bütçe tavanı aşılamaz |
| S093 | Kupon ve kod yönetimi | S10 | backend | 3 | P2 | Kupon kullanımı idempotent |
| S094 | Kampanya ekranları (portal + mobil) | S10 | frontend | 5 | P1 | Kampanya performans raporu |

### [E22] Epic: Gift Cards & Vouchers

Dijital/fiziksel hediye kartları ve e-kodlar.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S095 | voucher-service: hediye kartı üretimi ve aktivasyon | S09 | backend | 5 | P1 | Kart kodları tahmin edilemez (entropi ≥ 64 bit) |
| S096 | Hediye kartını cüzdana aktarma ve hediye gönderme | S10 | backend | 3 | P1 | Aktarım ledger'da izlenebilir |
| S097 | Breakage hesaplama ve muhasebeleştirme | S10 | backend | 5 | P1 | Tüketici mevzuatına uygun süre konfigürasyonu |


## M6 - Risk, AML & Compliance

### [E23] Epic: Advanced Risk & Fraud

Gerçek zamanlı fraud motoru, skor, vaka yönetimi.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S098 | risk-service: gerçek zamanlı kural motoru ve skor | S11 | backend | 8 | P1 | Karar süresi p99 < 50ms |
| S099 | Cihaz parmak izi ve hesap ele geçirme tespiti | S11 | security | 5 | P1 | Şüpheli oturumda step-up |
| S100 | Vaka yönetimi (case management) | S12 | frontend | 5 | P1 | Kararlar audit'e düşer |

### [E24] Epic: AML & Compliance

Yaptırım/PEP taraması, işlem izleme, MASAK raporları, KYC Tier 2/3.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S101 | compliance-service: yaptırım/PEP tarama entegrasyonu | S11 | compliance | 5 | P1 | Eşleşme vakası uyum kuyruğuna düşer |
| S102 | İşlem izleme senaryoları (structuring vb.) | S12 | compliance | 8 | P1 | Senaryo parametreleri tenant bazlı |
| S103 | Şüpheli işlem bildirimi (STR) hazırlama ve regülatif raporlar | S12 | compliance | 5 | P1 | Rapor oluşturma audit'lenir |
| S104 | KYC Tier 2/3: kimlik doğrulama sağlayıcısı entegrasyonu | S12 | backend | 5 | P1 | Başarılı doğrulama ile tier yükselir ve limitler güncellenir |


## M7 - Settlement, Accounting & Banking

### [E25] Epic: Settlement & Reconciliation

İşyeri takası, PSP/banka mutabakatı.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S105 | settlement-service: günlük takas hesaplama | S13 | backend | 8 | P1 | Takas toplamı ledger ile birebir |
| S106 | PSP ve banka dosyası mutabakatı | S13 | backend | 8 | P1 | Otomatik eşleşme oranı ≥ %98 |
| S107 | Mutabakat istisna ekranı | S14 | frontend | 3 | P1 | Çözümler maker-checker ile |

### [E26] Epic: Accounting & ERP

GL eşleme, yevmiye export, e-Fatura, ERP adaptörleri.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S108 | accounting-service: GL eşleme ve yevmiye üretimi | S13 | backend | 5 | P1 | Günlük yevmiye dengeli |
| S109 | e-Fatura/e-Arşiv entegrasyonu (ücret faturaları) | S14 | backend | 5 | P2 | Fatura durumları izlenir |
| S110 | ERP adaptörleri (SAP, Logo) | S14 | backend | 5 | P2 | Aktarım idempotent ve mutabık |

### [E27] Epic: Bank & Open Banking Integrations

Havale/EFT, sanal IBAN, açık bankacılık ile yükleme.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S111 | Sanal IBAN ile havale/EFT yükleme | S13 | backend | 5 | P2 | Eşleşmeyen havale istisna kuyruğuna düşer |
| S112 | Açık bankacılık (ÖHVPS/PSD2) ödeme başlatma | S14 | backend | 8 | P2 | Sandbox ile E2E |
| S113 | PSP adaptörü #2 (Stripe/Adyen) ve akıllı yönlendirme | S14 | backend | 5 | P2 | PSP arızasında otomatik geçiş |

### [E28] Epic: Analytics & BI

CDC → ClickHouse analitik hattı ve gelişmiş raporlar.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S114 | CDC hattı: Debezium → Kafka → ClickHouse | S13 | data | 8 | P1 | Uçtan uca gecikme < 1 dk |
| S115 | Gelişmiş BI dashboard'ları ve kohort analizi | S14 | data | 5 | P2 | Tenant izolasyonu analitikte de korunur |


## M8 - Production Hardening & GA v2.0

### [E29] Epic: Production Hardening

Performans, chaos, DR ve operasyonel olgunluk.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S116 | Performans: 5.000 TPS ve 24 saat soak testi | S15 | perf | 8 | P0 | 5.000 TPS'de p99 < 300ms, hata < %0.01 |
| S117 | Chaos engineering tatbikatları | S15 | devops | 5 | P1 | Finansal tutarlılık bozulmaz |
| S118 | DR tatbikatı (RPO ≤ 1 dk, RTO ≤ 15 dk) | S16 | devops | 5 | P0 | Tatbikat raporu |
| S119 | Argo Rollouts canary ve otomatik analiz | S15 | devops | 3 | P1 | Hatalı sürüm otomatik geri alınır |

### [E30] Epic: Security Certification & Compliance Readiness

Bağımsız pentest, PCI-DSS SAQ, SOC 2/ISO 27001 hazırlığı.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S120 | Bağımsız penetrasyon testi ve kapanış | S15 | security | 5 | P0 | Critical/High bulgu kalmadı |
| S121 | PCI-DSS SAQ A ve kontrol kanıtları | S16 | compliance | 3 | P0 | SAQ tamamlandı |
| S122 | SOC 2 / ISO 27001 kontrol kanıt otomasyonu | S16 | compliance | 5 | P1 | Kontrol matrisi 'Effective' oranı ≥ %90 |

### [E31] Epic: GA Launch & Multi-tenant Rollout

Çoklu tenant pilotu, GA sürümü, destek organizasyonu.

| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |
|---|---|---|---|---|---|---|
| S123 | Çoklu sektör pilotu (EV şarj + otopark) | S16 | governance | 5 | P0 | Pilot KPI'ları hedefte |
| S124 | Destek süreçleri, SLA ve status page | S16 | docs | 3 | P1 | SLA dokümanı yayında |
| S125 | GA v2.0 sürümü | S16 | devops | 2 | P0 | Go/No-Go onayı alındı |

