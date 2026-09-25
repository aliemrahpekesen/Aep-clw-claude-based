#!/usr/bin/env python3
"""AEP-CLW backlog kaynağı (backlog-as-code).

Bu dosya tek doğruluk kaynağıdır. Çalıştırıldığında:
  * .github/project/backlog.json  -> GitHub Actions 'backlog-sync' iş akışının girdisi
  * docs/backlog.md               -> insan tarafından okunabilir backlog
üretir.  Kullanım:  python3 tools/backlog/backlog_source.py
"""
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPRINT0_START = date(2026, 10, 5)


def sprint_dates(n):
    start = SPRINT0_START + timedelta(days=14 * n)
    return start, start + timedelta(days=11)


MILESTONES = [
    ("M0", "Inception & Architecture", [0], "Vizyon, mimari, güvenlik/uyum tasarımı, backlog, prototip ve onay."),
    ("M1", "Platform Foundation", [1, 2], "Monorepo, platform-commons, CI/CD, OpenShift dev/test, Keycloak, gateway, tenant servisi."),
    ("M2", "Core Wallet & Ledger", [3, 4], "Müşteri & KYC Tier0/1, çift kayıtlı ledger, cüzdan, gözlemlenebilirlik."),
    ("M3", "Funding & Payments", [5, 6], "Kartla yükleme, QR ödeme, pre-auth, iade, işyeri/POS, limitler, mobil uygulama, bildirim."),
    ("M4", "Admin, Reporting & Audit - MVP v1.0", [7, 8], "Tenant Admin Portalı, Platform Admin, raporlar, audit/teftiş, UAT ve MVP sürümü."),
    ("M5", "Loyalty, Campaigns & Gift Cards", [9, 10], "Puan/tier, kampanya kural motoru, cashback, kupon, hediye kartı."),
    ("M6", "Risk, AML & Compliance", [11, 12], "Gelişmiş fraud motoru, vaka yönetimi, AML/yaptırım taraması, MASAK raporlama, KYC Tier2/3."),
    ("M7", "Settlement, Accounting & Banking", [13, 14], "Takas & mutabakat, muhasebe/GL/e-Fatura/ERP, banka & açık bankacılık, ClickHouse BI."),
    ("M8", "Production Hardening & GA v2.0", [15, 16], "Performans, chaos, DR, pentest, PCI/SOC2 hazırlık, çoklu tenant pilot ve GA."),
]

# Epic: (id, milestone, title, area, summary, stories)
# Story: (id, title, sprint, area, points, priority, description, [acceptance criteria])
EPICS = [
    ("E01", "M0", "Inception, Governance & Architecture Baseline", "architecture",
     "Proje tüzüğü, mimari, güvenlik/uyum tasarımı, backlog ve tıklanabilir prototip; kullanıcı onayı ile kodlamaya geçiş.", [
        ("S001", "Proje tüzüğü, ekip ve RACI", 0, "governance", 2, "P0", "Vizyon, kapsam, ekip rolleri, RACI ve çalışma anlaşmasının yazılması.",
         ["docs/00-project-charter.md ve docs/product/raci.md yayınlandı", "DoR/DoD tanımlı"]),
        ("S002", "Mimari dokümantasyon ve ADR seti", 0, "architecture", 8, "P0", "C4 diyagramları, servis kataloğu, ledger tasarımı, akışlar, ADR-001..012.",
         ["docs/architecture altında tüm dokümanlar mevcut", "ADR'ler Proposed durumunda ve CA onayına hazır"]),
        ("S003", "Güvenlik mimarisi ve tehdit modeli (STRIDE)", 0, "security", 5, "P0", "Zero-trust mimari, STRIDE tehdit modeli, secure SDLC.",
         ["En az 30 tehdit ve kontrolü tanımlı", "Güvenlik kapıları CI tasarımına eşlendi"]),
        ("S004", "Regülasyon çerçevesi, AML/KYC politikası ve kontrol matrisi", 0, "compliance", 5, "P0", "6493, MASAK, KVKK, PCI-DSS, PSD2 eşlemesi; Audit (Kontrol) Matrisi v1.",
         ["docs/compliance/control-matrix.md en az 40 kontrol içerir", "Her kontrol bir milestone'a eşlenmiş"]),
        ("S005", "Gereksinimler, fonksiyon matrisi ve MVP kapsamı", 0, "analysis", 5, "P0", "FR/NFR kataloğu, Fonksiyon Matrisi v1, MVP tanımı, yol haritası.",
         ["FR ≥ 120, NFR ≥ 30, FN ≥ 80", "MVP kapsamı ve başarı kriterleri onaya hazır"]),
        ("S006", "Test stratejisi, performans planı ve DevOps tasarımı", 0, "qa", 5, "P0", "Test piramidi, kalite kapıları, CI/CD ve OpenShift platform tasarımı.",
         ["docs/quality ve docs/devops yayınlandı"]),
        ("S007", "Tıklanabilir prototip ve proje sunumu", 0, "ux", 5, "P0", "Mobil, Tenant Admin, POS, Platform Admin ekranlarının HTML prototipi ve yönetici sunumu.",
         ["Prototip ve sunum paylaşıldı", "Kullanıcı geri bildirimi toplandı"]),
        ("S008", "Backlog-as-code ve GitHub proje otomasyonu", 0, "devops", 3, "P0", "Label, milestone, epic/story issue'larının JSON kaynaktan otomatik oluşturulması.",
         ["backlog-sync workflow'u idempotent çalışır", "Tüm epic/story'ler milestone ve label'larıyla GitHub'da"]),
        ("S009", "Sprint 0 review ve kodlama onayı", 0, "governance", 1, "P0", "Plan, prototip ve sunumun kullanıcıya sunulup onay alınması.",
         ["Kullanıcı onayı kayıt altına alındı (issue yorumu)"]),
    ]),
    ("E02", "M1", "Engineering Foundation", "backend",
     "Monorepo, build sistemi, ortak platform kütüphaneleri ve yerel geliştirme ortamı.", [
        ("S010", "Monorepo iskeleti (Gradle multi-module + pnpm workspace)", 1, "backend", 3, "P0", "backend/, frontend/, mobile/, deploy/, docs/ yapısı; Gradle version catalog; Java 21 toolchain.",
         ["./gradlew build yeşil", "pnpm -r build yeşil", "Kod stili (Spotless, ESLint, Prettier) zorunlu"]),
        ("S011", "platform-commons: tenant context, hata modeli, Money tipi", 1, "backend", 5, "P0", "TenantContext propagation (HTTP/Kafka/async), RFC 7807 hata modeli, Money/Currency value object (minor units).",
         ["Tenant context thread/reactive/Kafka boyunca taşınır (testli)", "Money aritmetiği property-based test ile doğrulanır"]),
        ("S012", "platform-commons: idempotency ve transactional outbox", 1, "backend", 5, "P0", "Idempotency-Key filtre + Redis/Postgres store; outbox tablosu ve yayınlayıcı.",
         ["Aynı Idempotency-Key ile tekrar istek aynı yanıtı döner", "Outbox kaydı iş transaction'ı ile atomik yazılır"]),
        ("S013", "Servis şablonu (hexagonal) ve ArchUnit kuralları", 1, "backend", 3, "P0", "Yeni servis üretmek için şablon; katman bağımlılık kuralları ArchUnit ile.",
         ["Domain katmanı Spring'e bağımlı değil (ArchUnit)", "Şablondan servis 5 dk içinde üretilebilir"]),
        ("S014", "Yerel geliştirme ortamı (docker-compose)", 1, "devops", 3, "P0", "Postgres, Kafka (KRaft), Schema Registry, Keycloak, Redis, Mailpit, WireMock.",
         ["make up ile tüm bağımlılıklar ayağa kalkar", "README'de 10 dakikada kurulum"]),
        ("S015", "PostgreSQL standartları: Flyway, RLS, tenant politikaları", 2, "data", 5, "P0", "Flyway konvansiyonları, RLS politikası şablonu, app_user/owner rol ayrımı.",
         ["RLS olmadan tenant verisine erişim testi başarısız olur", "Migration'lar expand-contract uyumlu"]),
        ("S016", "Kafka event standartları (CloudEvents, Avro, Schema Registry)", 2, "backend", 3, "P1", "Event zarfı, topic isimlendirme, uyumluluk kuralları, DLQ ve retry.",
         ["Schema uyumluluk kontrolü CI'da", "DLQ akışı entegrasyon testli"]),
    ]),
    ("E03", "M1", "CI/CD & DevSecOps Pipeline", "devops",
     "PR ve main pipeline'ları, güvenlik taramaları, imaj üretimi, SBOM ve imzalama.", [
        ("S017", "PR pipeline: build, test, lint, ArchUnit", 1, "devops", 3, "P0", "GitHub Actions ile her PR'da derleme ve testler.",
         ["PR'da zorunlu status check", "Ortalama süre < 10 dk"]),
        ("S018", "Güvenlik kapıları: SAST, SCA, secret scan, IaC scan", 1, "security", 5, "P0", "Semgrep/CodeQL, OWASP Dependency-Check, Gitleaks, Checkov.",
         ["Critical bulgu PR'ı bloklar", "Raporlar artifact olarak saklanır"]),
        ("S019", "Kalite kapısı: coverage ve SonarQube", 2, "qa", 3, "P1", "JaCoCo, Sonar quality gate.",
         ["Domain coverage ≥ %80", "0 blocker/critical"]),
        ("S020", "Konteyner imajı, Trivy, SBOM (CycloneDX), Cosign imza", 2, "devops", 5, "P0", "Jib ile distroless imaj, zafiyet taraması, SBOM ve imzalama.",
         ["Imzasız imaj cluster'a deploy edilemez", "SBOM her release'e eklenir"]),
        ("S021", "Release otomasyonu (SemVer, Conventional Commits, changelog)", 2, "devops", 2, "P2", "release-please ile sürüm ve changelog.",
         ["Tag'ten otomatik release notları"]),
    ]),
    ("E04", "M1", "OpenShift Platform & GitOps", "devops",
     "Dev/test ortamları, Helm library chart, ArgoCD, veri servisleri operatörleri.", [
        ("S022", "Helm library chart ve servis chart standardı", 1, "devops", 5, "P0", "Deployment, Service, Route, HPA, PDB, NetworkPolicy, ServiceMonitor şablonları.",
         ["Tüm servisler aynı library chart'ı kullanır", "helm lint + kubeconform CI'da"]),
        ("S023", "ArgoCD app-of-apps ve ortam promotion", 2, "devops", 5, "P0", "deploy/ gitops repo yapısı; dev→test otomatik, üst ortamlar PR ile.",
         ["main merge sonrası dev'e otomatik deploy", "Rollback tek commit revert ile"]),
        ("S024", "Veri platformu: CloudNativePG, Strimzi Kafka, Redis, Vault", 2, "devops", 8, "P0", "Operatörlerle yönetilen veri servisleri; Vault dinamik DB kimlikleri.",
         ["PITR yedekleme aktif", "Servisler statik parola kullanmaz"]),
        ("S025", "NetworkPolicy default-deny ve service mesh mTLS", 2, "security", 3, "P0", "Namespace bazlı default deny; mesh ile mTLS STRICT.",
         ["Yetkisiz pod-pod trafiği engellenir (test)"]),
    ]),
    ("E05", "M1", "Identity & Access Management", "backend",
     "Keycloak, API Gateway, OTP, cihaz bağlama, RBAC.", [
        ("S026", "Keycloak kurulumu: realm, organization-per-tenant, roller", 1, "security", 5, "P0", "Platform realm, tenant organizasyonları, rol modeli (docs/security).",
         ["Realm konfigürasyonu kod olarak (export/import)", "MFA admin kullanıcılar için zorunlu"]),
        ("S027", "api-gateway: JWT doğrulama, tenant çözümleme, rate limit", 2, "backend", 5, "P0", "Spring Cloud Gateway; tenant header/subdomain/claim çözümleme; Redis rate limit.",
         ["Tenant uyuşmazlığında 403", "Rate limit tenant planına göre"]),
        ("S028", "identity-service: telefon OTP kayıt/giriş", 2, "backend", 5, "P0", "OTP üretimi/doğrulama, deneme limiti, SMS sağlayıcı portu (mock).",
         ["OTP 3 hatalı denemede kilitlenir", "OTP loglarda maskelenir"]),
        ("S029", "Cihaz bağlama ve step-up authentication", 2, "security", 5, "P1", "Cihaz anahtarı kaydı, hassas işlemlerde biyometrik/PIN step-up.",
         ["Yeni cihazdan yüksek tutarlı işlem step-up ister"]),
    ]),
    ("E06", "M1", "Tenant Management & Configuration", "backend",
     "Tenant onboarding, konfigürasyon, sektör presetleri, feature flag, marka.", [
        ("S030", "tenant-service: tenant CRUD ve yaşam döngüsü", 1, "backend", 5, "P0", "Tenant oluşturma, askıya alma, kapatma; plan bilgisi.",
         ["Yaşam döngüsü event'leri yayınlanır", "Tüm değişiklikler audit'e düşer"]),
        ("S031", "Tenant konfigürasyon şeması ve versiyonlama", 2, "backend", 5, "P0", "JSON Schema ile doğrulanan, versiyonlu konfigürasyon (limit, ücret, cüzdan tipleri, KYC tier).",
         ["Geçersiz konfigürasyon reddedilir", "Konfigürasyon değişikliği maker-checker gerektirir"]),
        ("S032", "Sektör presetleri (Kahve, EV, Otopark, Eğlence, Kampüs)", 2, "backend", 3, "P1", "Onboarding'de preset seçimi ile hazır konfigürasyon.",
         ["5 preset şema ile doğrulanır"]),
        ("S033", "Feature flag ve marka/tema servisi", 2, "backend", 3, "P1", "Tenant bazlı feature flag; logo, renk, dil ayarları.",
         ["Mobil ve portal temayı çalışma zamanında çeker"]),
        ("S034", "Otomatik tenant provisioning", 2, "devops", 5, "P1", "Keycloak org, DB şeması/politikalar, Kafka ACL, varsayılan roller otomatik.",
         ["Yeni tenant < 2 dk'da kullanıma hazır"]),
    ]),
    ("E07", "M2", "Customer & KYC (Tier 0/1)", "backend",
     "Müşteri profili, onaylar, KYC seviyeleri.", [
        ("S035", "customer-service: profil ve yaşam döngüsü", 3, "backend", 5, "P0", "Müşteri oluşturma (OTP sonrası), güncelleme, kapatma, bloke.",
         ["PII alanları field-level şifreli", "Bloke müşteri işlem yapamaz"]),
        ("S036", "KVKK/GDPR onay yönetimi", 3, "compliance", 3, "P0", "Aydınlatma metni versiyonları, açık rıza, pazarlama izni.",
         ["Onay geçmişi değiştirilemez şekilde saklanır"]),
        ("S037", "KYC Tier 0/1 ve limit profili bağlama", 4, "backend", 3, "P0", "Tier'a göre limit profili; tier yükseltme event'i.",
         ["Tier limitleri wallet-service tarafından uygulanır"]),
        ("S038", "Veri sahibi talepleri (erişim/silme) ve crypto-shredding", 4, "compliance", 5, "P1", "KVKK başvuruları; finansal kayıt saklama ile uyumlu anonimleştirme.",
         ["Silme sonrası PII okunamaz, ledger bütünlüğü korunur"]),
    ]),
    ("E08", "M2", "Double-Entry Ledger", "backend",
     "Değiştirilemez, çift kayıtlı defter; sistemin finansal doğruluk kaynağı.", [
        ("S039", "ledger-service: hesap planı ve hesap açma", 3, "backend", 5, "P0", "Hesap tipleri (müşteri yükümlülük, işyeri borç, PSP clearing, gelir, breakage, promo gider, suspense).",
         ["Her tenant için varsayılan hesap planı otomatik oluşur"]),
        ("S040", "Journal posting API (atomik, idempotent, dengeli)", 3, "backend", 8, "P0", "Borç=alacak zorunlu, append-only, idempotent posting.",
         ["Dengesiz journal reddedilir", "Aynı referans ikinci kez post edilemez", "UPDATE/DELETE DB seviyesinde yasak"]),
        ("S041", "Bakiye hesaplama, snapshot ve eşzamanlılık", 4, "backend", 8, "P0", "Running balance, hot-account stratejisi, negatif bakiye koruması.",
         ["1000 eşzamanlı harcamada çifte harcama yok (test)", "p99 posting < 50ms"]),
        ("S042", "Hold (provizyon) ve release/capture", 4, "backend", 5, "P0", "Pre-auth için hold hesapları; süre aşımı ile otomatik release.",
         ["Kısmi capture ve fazla tutarın serbest bırakılması"]),
        ("S043", "Ledger invariant testleri ve günlük bütünlük kontrolü", 4, "qa", 5, "P0", "jqwik property test; günlük trial balance job + alarm.",
         ["Trial balance ≠ 0 ise kritik alarm", "Mutation score ≥ %60"]),
    ]),
    ("E09", "M2", "Wallet", "backend",
     "Cüzdan hesapları, çoklu cüzdan, limit kontrolü, işlem geçmişi.", [
        ("S044", "wallet-service: cüzdan açma (ana + bonus) ve durum yönetimi", 3, "backend", 5, "P0", "Tenant konfigürasyonuna göre cüzdan tipleri; aktif/dondurulmuş/kapalı.",
         ["Kayıtta varsayılan cüzdanlar otomatik açılır"]),
        ("S045", "Bakiye sorgulama ve harcama önceliği (bonus → ana)", 4, "backend", 3, "P0", "Tenant kuralına göre harcama sırası.",
         ["Harcama sırası konfigürasyondan okunur (test)"]),
        ("S046", "Limit motoru (tek işlem, günlük, aylık, bakiye tavanı)", 4, "backend", 5, "P0", "KYC tier ve tenant limitleri; regülasyon tavanları.",
         ["Limit aşımında açıklayıcı hata kodu"]),
        ("S047", "İşlem geçmişi okuma modeli (CQRS)", 4, "backend", 3, "P0", "Event'lerden beslenen sorgu modeli; cursor pagination.",
         ["p95 < 150ms, 12 aylık geçmiş"]),
    ]),
    ("E10", "M2", "Observability", "devops",
     "OpenTelemetry, metrik, log, trace, SLO ve alarmlar.", [
        ("S048", "OpenTelemetry enstrümantasyonu ve trace yayılımı", 3, "devops", 3, "P0", "HTTP, Kafka, JDBC trace; correlation-id.",
         ["Uçtan uca trace Tempo'da görünür"]),
        ("S049", "Loki log standardı ve PII maskeleme", 3, "security", 3, "P0", "JSON log, maskeleme filtreleri.",
         ["PAN/telefon/TCKN loglarda maskeli (test)"]),
        ("S050", "Grafana dashboard'ları, SLO ve alarm kuralları", 4, "devops", 5, "P1", "RED metrikleri, iş metrikleri, error budget.",
         ["Her servis için SLO dashboard'ı"]),
    ]),
    ("E11", "M3", "Funding (Top-up)", "backend",
     "Kartla yükleme, kayıtlı kart, otomatik yükleme, PSP adaptörleri.", [
        ("S051", "funding-service: yükleme sagası ve PSP portu", 5, "backend", 8, "P0", "Başlat → 3DS → PSP callback → ledger posting; compensation.",
         ["PSP timeout'unda durum sorgulama ile kesinleşir", "Çift webhook çift yükleme yaratmaz"]),
        ("S052", "PSP adaptörü #1 (iyzico) + mock PSP", 5, "backend", 5, "P0", "Anti-corruption layer; HMAC webhook doğrulama.",
         ["Sandbox ile E2E test", "Kart verisi sistemimize girmez"]),
        ("S053", "Kayıtlı kart (tokenization) ve otomatik yükleme", 6, "backend", 5, "P1", "PSP token saklama; eşik altına inince otomatik yükleme.",
         ["Otomatik yükleme günlük limitli ve iptal edilebilir"]),
        ("S054", "Kasada nakit yükleme (POS üzerinden)", 6, "backend", 3, "P2", "Kasiyer ile yükleme; kasa mutabakatı için kayıt.",
         ["Kasiyer günlük yükleme limiti uygulanır"]),
    ]),
    ("E12", "M3", "Payments", "backend",
     "QR/token ile ödeme, pre-auth/capture, iade, iptal.", [
        ("S055", "Dinamik müşteri QR token (TOTP tabanlı)", 5, "security", 5, "P0", "Cihaz anahtarıyla üretilen, 30 sn geçerli, tek kullanımlık token.",
         ["Replay edilen token reddedilir", "Offline üretim desteklenir"]),
        ("S056", "payment-service: authorize/capture (tek adım ödeme)", 5, "backend", 8, "P0", "Ödeme sagası: token doğrulama → limit/risk → ledger.",
         ["p99 < 300ms", "Idempotent"]),
        ("S057", "Pre-auth (EV şarj/otopark): hold → final capture", 6, "backend", 5, "P0", "Tutar belirsiz işlemler için provizyon ve kapanış.",
         ["Kısmi capture, süre aşımında otomatik iptal"]),
        ("S058", "İade (tam/kısmi) ve iptal (reversal)", 6, "backend", 5, "P0", "Orijinal işleme referanslı iade; gün içi iptal.",
         ["İade toplamı orijinal tutarı aşamaz"]),
        ("S059", "Basit risk: velocity ve limit kuralları (MVP)", 6, "backend", 5, "P0", "Konfigüre edilebilir velocity kuralları; blok/uyarı.",
         ["Kural değişikliği yeniden deploy gerektirmez"]),
    ]),
    ("E13", "M3", "Merchant, Store & POS", "backend",
     "İşyeri hiyerarşisi, terminaller, POS API ve Web POS.", [
        ("S060", "merchant-service: işyeri → mağaza → terminal", 5, "backend", 5, "P0", "Hiyerarşi, durumlar, mağaza bazlı ayarlar.",
         ["Terminal API anahtarı hash'li saklanır"]),
        ("S061", "POS REST API ve webhook'lar (OpenAPI)", 6, "backend", 5, "P0", "Ödeme, iade, pre-auth, durum sorgu uçları; HMAC imzalı webhook.",
         ["OpenAPI dokümanı ve Postman koleksiyonu"]),
        ("S062", "Web POS terminali (React PWA)", 6, "frontend", 8, "P0", "Tutar gir, QR okut, onay, fiş, iade, provizyon akışları.",
         ["Tablet ve dokunmatik uyumlu", "Playwright E2E"]),
    ]),
    ("E14", "M3", "Customer Mobile App (White-label)", "mobile",
     "React Native (Expo) white-label müşteri uygulaması.", [
        ("S063", "Mobil uygulama iskeleti, tema motoru, i18n", 5, "mobile", 5, "P0", "Tenant temasını çalışma zamanında yükleme; TR/EN.",
         ["Tek kod tabanından tenant bazlı build"]),
        ("S064", "Kayıt/giriş (OTP), cihaz bağlama, biyometrik", 5, "mobile", 5, "P0", "Güvenli depolama, sertifika pinleme.",
         ["OWASP MASVS L2 kontrolleri"]),
        ("S065", "Ana sayfa, bakiye, işlem geçmişi", 6, "mobile", 5, "P0", "Bakiye kartları, son işlemler, filtreleme.",
         ["Erişilebilirlik: ekran okuyucu etiketleri"]),
        ("S066", "Yükleme ve QR ile ödeme ekranları", 6, "mobile", 8, "P0", "3DS webview, kayıtlı kart, dinamik QR, pre-auth durumu.",
         ["Detox/Maestro E2E"]),
    ]),
    ("E15", "M3", "Notifications", "backend",
     "Push, SMS, e-posta; tenant şablonları.", [
        ("S067", "notification-service: kanal adaptörleri ve şablonlar", 5, "backend", 5, "P1", "FCM/APNs, SMS, e-posta; tenant bazlı şablon ve dil.",
         ["Event'lerden tetiklenen bildirimler", "Başarısız gönderim retry + DLQ"]),
        ("S068", "Bildirim tercihleri ve sessiz saatler", 6, "backend", 2, "P2", "Müşteri tercih yönetimi.",
         ["Pazarlama bildirimi onaysız gönderilmez"]),
    ]),
    ("E16", "M4", "Tenant Admin Portal", "frontend",
     "Tenant yöneticileri için web portal (React).", [
        ("S069", "Portal iskeleti, design system, RBAC menü", 7, "frontend", 5, "P0", "Tema, layout, rol bazlı menü, i18n.",
         ["WCAG 2.2 AA (axe) hatasız"]),
        ("S070", "Dashboard (KPI ve grafikler)", 7, "frontend", 5, "P0", "Yükümlülük, günlük yükleme/harcama, aktif cüzdan, başarı oranı.",
         ["Veriler reporting-service'ten, 1 dk gecikme"]),
        ("S071", "Müşteri yönetimi ve müşteri 360", 7, "frontend", 5, "P0", "Arama, detay, cüzdanlar, işlemler, bloke/aç (maker-checker).",
         ["Hassas alanlar role göre maskeli"]),
        ("S072", "İşlem arama, detay ve iade başlatma", 7, "frontend", 5, "P0", "Filtreler, export, iade talebi.",
         ["İade maker-checker ile onaylanır"]),
        ("S073", "İşyeri/mağaza/terminal yönetimi", 8, "frontend", 3, "P0", "CRUD, API anahtarı üretimi.",
         ["API anahtarı yalnızca bir kez gösterilir"]),
        ("S074", "Kullanıcı & rol yönetimi, maker-checker kuyruğu", 8, "frontend", 5, "P0", "Tenant kullanıcıları, roller, onay bekleyenler.",
         ["Kendi talebini onaylayamaz (SoD)"]),
        ("S075", "Tenant ayarları ekranı (konfigürasyon)", 8, "frontend", 3, "P1", "Limitler, ücretler, marka, feature flag.",
         ["Değişiklikler versiyonlanır ve onaylanır"]),
    ]),
    ("E17", "M4", "Platform Admin Console", "frontend",
     "SaaS operatörü için tenant ve sistem yönetimi.", [
        ("S076", "Tenant listesi ve onboarding sihirbazı", 7, "frontend", 5, "P0", "Tenant oluşturma, preset seçimi, marka.",
         ["Sihirbaz provisioning'i tetikler"]),
        ("S077", "Plan/abonelik ve kullanım ölçümü (metering)", 8, "backend", 5, "P1", "İşlem sayısı/hacim ölçümü, plan limitleri.",
         ["Aylık kullanım raporu"]),
        ("S078", "Sistem sağlığı görünümü", 8, "frontend", 2, "P2", "Servis durumları, temel metrikler.",
         ["Grafana'ya derin bağlantılar"]),
    ]),
    ("E18", "M4", "Operational Reporting", "backend",
     "Operasyonel ve finansal raporlar, planlı raporlar, export.", [
        ("S079", "reporting-service: okuma modelleri ve rapor API", 7, "backend", 5, "P0", "Günlük özet, mağaza bazlı, müşteri bazlı raporlar.",
         ["Rapor sonuçları ledger ile tutarlı (mutabakat testi)"]),
        ("S080", "Yükümlülük (float) raporu ve günlük finansal özet", 8, "backend", 5, "P0", "Toplam müşteri bakiyesi, hareket özeti.",
         ["Ledger trial balance ile birebir"]),
        ("S081", "Export (CSV/XLSX/PDF) ve planlı raporlar", 8, "backend", 3, "P1", "Asenkron export, e-posta ile gönderim.",
         ["Büyük exportlar arka planda, imzalı link"]),
    ]),
    ("E19", "M4", "Audit & Inspection", "security",
     "Değiştirilemez audit log, teftiş ekranı, delil paketi.", [
        ("S082", "audit-service: hash-zincirli audit log", 7, "security", 8, "P0", "Tüm servislerden audit event toplama; hash zinciri; WORM arşiv.",
         ["Zincir kırılması tespit edilir ve alarm üretir"]),
        ("S083", "Teftiş (müfettiş) ekranı ve sorgular", 8, "frontend", 5, "P0", "Read-only müfettiş rolü; kullanıcı/varlık/zaman bazlı sorgu.",
         ["Müfettiş hiçbir veriyi değiştiremez"]),
        ("S084", "Delil paketi (evidence pack) export", 8, "security", 3, "P1", "İmzalı, hash'li denetim paketi.",
         ["Paket bütünlüğü bağımsız doğrulanabilir"]),
    ]),
    ("E20", "M4", "MVP Release Readiness", "qa",
     "UAT, performans baz çizgisi, güvenlik incelemesi, dokümantasyon, pilot.", [
        ("S085", "E2E regresyon paketi ve UAT", 8, "qa", 5, "P0", "Kritik yolculukların otomasyonu; pilot tenant ile UAT.",
         ["Kritik senaryolar %100 geçer"]),
        ("S086", "Performans baz çizgisi (1.000 TPS)", 8, "perf", 5, "P0", "Gatling ile ödeme/yükleme yük testi.",
         ["1.000 TPS'de p99 < 300ms"]),
        ("S087", "MVP güvenlik incelemesi ve DAST", 8, "security", 3, "P0", "OWASP ZAP, tehdit modeli güncellemesi.",
         ["High/Critical açık yok"]),
        ("S088", "Kullanıcı ve API dokümantasyonu, runbook'lar", 8, "docs", 3, "P0", "Admin kılavuzu, POS API portal, operasyon runbook'ları.",
         ["Dokümanlar yayında"]),
        ("S089", "MVP v1.0 sürümü ve pilot canlıya geçiş", 8, "devops", 3, "P0", "Release, go-live checklist, hypercare planı.",
         ["Go/No-Go onayı alındı"]),
    ]),
    ("E21", "M5", "Loyalty & Campaigns", "backend",
     "Puan/yıldız, tier, kampanya kural motoru, cashback, kupon.", [
        ("S090", "loyalty-service: puan hesabı ve tier yönetimi", 9, "backend", 8, "P1", "Harcama başına puan, tier atlama, puan son kullanma.",
         ["Puan hareketleri ledger'dan ayrı ama mutabık"]),
        ("S091", "Kampanya kural motoru (koşul → ödül DSL)", 9, "backend", 8, "P1", "Zaman, mağaza, ürün kategorisi, segment koşulları.",
         ["Kural simülasyonu (dry-run)"]),
        ("S092", "Cashback ve bonus yükleme kampanyaları", 10, "backend", 5, "P1", "Yüklemeye bonus, harcamaya cashback; promo gider muhasebesi.",
         ["Bütçe tavanı aşılamaz"]),
        ("S093", "Kupon ve kod yönetimi", 10, "backend", 3, "P2", "Tek/çok kullanımlık kuponlar.",
         ["Kupon kullanımı idempotent"]),
        ("S094", "Kampanya ekranları (portal + mobil)", 10, "frontend", 5, "P1", "Kampanya oluşturma, raporlama; mobilde ödüller.",
         ["Kampanya performans raporu"]),
    ]),
    ("E22", "M5", "Gift Cards & Vouchers", "backend",
     "Dijital/fiziksel hediye kartları ve e-kodlar.", [
        ("S095", "voucher-service: hediye kartı üretimi ve aktivasyon", 9, "backend", 5, "P1", "Toplu üretim, aktivasyon, bakiye, son kullanma.",
         ["Kart kodları tahmin edilemez (entropi ≥ 64 bit)"]),
        ("S096", "Hediye kartını cüzdana aktarma ve hediye gönderme", 10, "backend", 3, "P1", "Bakiye birleştirme, arkadaşa hediye.",
         ["Aktarım ledger'da izlenebilir"]),
        ("S097", "Breakage hesaplama ve muhasebeleştirme", 10, "backend", 5, "P1", "Süresi dolan bakiyelerin gelir kaydı (tenant kuralı).",
         ["Tüketici mevzuatına uygun süre konfigürasyonu"]),
    ]),
    ("E23", "M6", "Advanced Risk & Fraud", "backend",
     "Gerçek zamanlı fraud motoru, skor, vaka yönetimi.", [
        ("S098", "risk-service: gerçek zamanlı kural motoru ve skor", 11, "backend", 8, "P1", "Streaming özellikler (Kafka Streams), kural + skor.",
         ["Karar süresi p99 < 50ms"]),
        ("S099", "Cihaz parmak izi ve hesap ele geçirme tespiti", 11, "security", 5, "P1", "Cihaz/IP/konum sinyalleri.",
         ["Şüpheli oturumda step-up"]),
        ("S100", "Vaka yönetimi (case management)", 12, "frontend", 5, "P1", "Alarm kuyruğu, atama, karar, not.",
         ["Kararlar audit'e düşer"]),
    ]),
    ("E24", "M6", "AML & Compliance", "compliance",
     "Yaptırım/PEP taraması, işlem izleme, MASAK raporları, KYC Tier 2/3.", [
        ("S101", "compliance-service: yaptırım/PEP tarama entegrasyonu", 11, "compliance", 5, "P1", "Onboarding ve periyodik tarama; fuzzy eşleşme.",
         ["Eşleşme vakası uyum kuyruğuna düşer"]),
        ("S102", "İşlem izleme senaryoları (structuring vb.)", 12, "compliance", 8, "P1", "Batch + streaming senaryolar.",
         ["Senaryo parametreleri tenant bazlı"]),
        ("S103", "Şüpheli işlem bildirimi (STR) hazırlama ve regülatif raporlar", 12, "compliance", 5, "P1", "MASAK formatına uygun rapor taslağı.",
         ["Rapor oluşturma audit'lenir"]),
        ("S104", "KYC Tier 2/3: kimlik doğrulama sağlayıcısı entegrasyonu", 12, "backend", 5, "P1", "e-Devlet/NFC çip okuma sağlayıcı adaptörü.",
         ["Başarılı doğrulama ile tier yükselir ve limitler güncellenir"]),
    ]),
    ("E25", "M7", "Settlement & Reconciliation", "backend",
     "İşyeri takası, PSP/banka mutabakatı.", [
        ("S105", "settlement-service: günlük takas hesaplama", 13, "backend", 8, "P1", "İşyeri bazında net tutar, ücret kesintisi.",
         ["Takas toplamı ledger ile birebir"]),
        ("S106", "PSP ve banka dosyası mutabakatı", 13, "backend", 8, "P1", "Dosya parse, otomatik eşleşme, istisna kuyruğu.",
         ["Otomatik eşleşme oranı ≥ %98"]),
        ("S107", "Mutabakat istisna ekranı", 14, "frontend", 3, "P1", "Eşleşmeyen kayıtların çözümü.",
         ["Çözümler maker-checker ile"]),
    ]),
    ("E26", "M7", "Accounting & ERP", "backend",
     "GL eşleme, yevmiye export, e-Fatura, ERP adaptörleri.", [
        ("S108", "accounting-service: GL eşleme ve yevmiye üretimi", 13, "backend", 5, "P1", "Ledger hesaplarından tenant hesap planına eşleme.",
         ["Günlük yevmiye dengeli"]),
        ("S109", "e-Fatura/e-Arşiv entegrasyonu (ücret faturaları)", 14, "backend", 5, "P2", "Entegratör adaptörü.",
         ["Fatura durumları izlenir"]),
        ("S110", "ERP adaptörleri (SAP, Logo)", 14, "backend", 5, "P2", "Yevmiye aktarımı.",
         ["Aktarım idempotent ve mutabık"]),
    ]),
    ("E27", "M7", "Bank & Open Banking Integrations", "backend",
     "Havale/EFT, sanal IBAN, açık bankacılık ile yükleme.", [
        ("S111", "Sanal IBAN ile havale/EFT yükleme", 13, "backend", 5, "P2", "Banka bildirimi ile otomatik cüzdana yansıma.",
         ["Eşleşmeyen havale istisna kuyruğuna düşer"]),
        ("S112", "Açık bankacılık (ÖHVPS/PSD2) ödeme başlatma", 14, "backend", 8, "P2", "Hesaptan yükleme.",
         ["Sandbox ile E2E"]),
        ("S113", "PSP adaptörü #2 (Stripe/Adyen) ve akıllı yönlendirme", 14, "backend", 5, "P2", "Çoklu PSP, failover.",
         ["PSP arızasında otomatik geçiş"]),
    ]),
    ("E28", "M7", "Analytics & BI", "data",
     "CDC → ClickHouse analitik hattı ve gelişmiş raporlar.", [
        ("S114", "CDC hattı: Debezium → Kafka → ClickHouse", 13, "data", 8, "P1", "Gerçek zamanlıya yakın analitik veri ambarı.",
         ["Uçtan uca gecikme < 1 dk"]),
        ("S115", "Gelişmiş BI dashboard'ları ve kohort analizi", 14, "data", 5, "P2", "Müşteri segmentleri, tutunma, yükleme davranışı.",
         ["Tenant izolasyonu analitikte de korunur"]),
    ]),
    ("E29", "M8", "Production Hardening", "devops",
     "Performans, chaos, DR ve operasyonel olgunluk.", [
        ("S116", "Performans: 5.000 TPS ve 24 saat soak testi", 15, "perf", 8, "P0", "Kapasite planı, darboğaz giderme.",
         ["5.000 TPS'de p99 < 300ms, hata < %0.01"]),
        ("S117", "Chaos engineering tatbikatları", 15, "devops", 5, "P1", "Pod/node/Kafka/DB arıza senaryoları.",
         ["Finansal tutarlılık bozulmaz"]),
        ("S118", "DR tatbikatı (RPO ≤ 1 dk, RTO ≤ 15 dk)", 16, "devops", 5, "P0", "Bölge kaybı senaryosu.",
         ["Tatbikat raporu"]),
        ("S119", "Argo Rollouts canary ve otomatik analiz", 15, "devops", 3, "P1", "Metrik bazlı otomatik geri alma.",
         ["Hatalı sürüm otomatik geri alınır"]),
    ]),
    ("E30", "M8", "Security Certification & Compliance Readiness", "security",
     "Bağımsız pentest, PCI-DSS SAQ, SOC 2/ISO 27001 hazırlığı.", [
        ("S120", "Bağımsız penetrasyon testi ve kapanış", 15, "security", 5, "P0", "Web, mobil, API, altyapı.",
         ["Critical/High bulgu kalmadı"]),
        ("S121", "PCI-DSS SAQ A ve kontrol kanıtları", 16, "compliance", 3, "P0", "Kapsam daraltma kanıtları.",
         ["SAQ tamamlandı"]),
        ("S122", "SOC 2 / ISO 27001 kontrol kanıt otomasyonu", 16, "compliance", 5, "P1", "Kontrol matrisi → kanıt toplama.",
         ["Kontrol matrisi 'Effective' oranı ≥ %90"]),
    ]),
    ("E31", "M8", "GA Launch & Multi-tenant Rollout", "governance",
     "Çoklu tenant pilotu, GA sürümü, destek organizasyonu.", [
        ("S123", "Çoklu sektör pilotu (EV şarj + otopark)", 16, "governance", 5, "P0", "İki yeni sektör tenant'ının canlıya alınması.",
         ["Pilot KPI'ları hedefte"]),
        ("S124", "Destek süreçleri, SLA ve status page", 16, "docs", 3, "P1", "L1/L2/L3 destek, olay iletişimi.",
         ["SLA dokümanı yayında"]),
        ("S125", "GA v2.0 sürümü", 16, "devops", 2, "P0", "Release ve lansman.",
         ["Go/No-Go onayı alındı"]),
    ]),
]

SPRINT_OF_MS = {m[0]: m[2] for m in MILESTONES}


def build():
    milestones = []
    for code, title, sprints, desc in MILESTONES:
        _, due = sprint_dates(sprints[-1])
        s0, _ = sprint_dates(sprints[0])
        milestones.append({
            "code": code,
            "title": f"{code} - {title}",
            "description": f"{desc} Sprintler: {', '.join('S%d' % s for s in sprints)} ({s0.isoformat()} → {due.isoformat()})",
            "due_on": due.isoformat() + "T23:59:59Z",
        })

    epics = []
    for eid, ms, title, area, summary, stories in EPICS:
        st = []
        for sid, stitle, sprint, sarea, pts, prio, desc, ac in stories:
            s_start, s_end = sprint_dates(sprint)
            st.append({
                "id": sid, "title": f"[{sid}] {stitle}", "sprint": sprint, "area": sarea,
                "points": pts, "priority": prio, "description": desc, "acceptance": ac,
                "labels": ["type:story", f"ms:{ms}", f"sprint:S{sprint:02d}", f"area:{sarea}", f"priority:{prio}"]
                + (["mvp"] if ms in ("M0", "M1", "M2", "M3", "M4") else []),
                "sprint_window": f"{s_start.isoformat()} → {s_end.isoformat()}",
            })
        epics.append({
            "id": eid, "milestone": ms, "title": f"[{eid}] Epic: {title}", "area": area, "summary": summary,
            "labels": ["type:epic", f"ms:{ms}", f"area:{area}"] + (["mvp"] if ms in ("M0", "M1", "M2", "M3", "M4") else []),
            "stories": st,
        })

    labels = [
        {"name": "type:epic", "color": "5319e7", "description": "Epic (sub-issue'lar içerir)"},
        {"name": "type:story", "color": "1d76db", "description": "Kullanıcı hikayesi / iş kalemi"},
        {"name": "type:bug", "color": "d73a4a", "description": "Hata"},
        {"name": "type:spike", "color": "c5def5", "description": "Araştırma"},
        {"name": "mvp", "color": "0e8a16", "description": "MVP kapsamında (M0–M4)"},
        {"name": "sprint-review", "color": "fbca04", "description": "Sprint review paketi ve onay kaydı"},
        {"name": "status:blocked", "color": "b60205", "description": "Bloke"},
        {"name": "needs-approval", "color": "e99695", "description": "Kullanıcı onayı bekliyor"},
    ]
    for p, c in (("P0", "b60205"), ("P1", "d93f0b"), ("P2", "fbca04")):
        labels.append({"name": f"priority:{p}", "color": c, "description": f"Öncelik {p}"})
    for m in MILESTONES:
        labels.append({"name": f"ms:{m[0]}", "color": "bfdadc", "description": m[1]})
    for s in range(0, 17):
        labels.append({"name": f"sprint:S{s:02d}", "color": "ededed", "description": "Sprint %d" % s})
    areas = sorted({e["area"] for e in epics} | {s["area"] for e in epics for s in e["stories"]})
    for a in areas:
        labels.append({"name": f"area:{a}", "color": "c2e0c6", "description": f"Alan: {a}"})

    return {"version": 1, "labels": labels, "milestones": milestones, "epics": epics}


def story_body(s, epic):
    ac = "\n".join(f"- [ ] {a}" for a in s["acceptance"])
    return (f"<!-- backlog-id: {s['id']} -->\n"
            f"**Epic:** {epic['id']} · **Milestone:** {epic['milestone']} · **Sprint:** S{s['sprint']:02d} ({s['sprint_window']})\n"
            f"**Alan:** `{s['area']}` · **Öncelik:** {s['priority']} · **Story point:** {s['points']}\n\n"
            f"### Açıklama\n{s['description']}\n\n"
            f"### Kabul kriterleri\n{ac}\n\n"
            f"### Definition of Done\n- [ ] Kod + testler (unit/integration) ve kalite kapıları yeşil\n"
            f"- [ ] Güvenlik taramaları temiz, audit/kontrol matrisi güncellendi\n"
            f"- [ ] Dokümantasyon (OpenAPI/README/runbook) güncel\n"
            f"- [ ] Fonksiyon matrisinde durum güncellendi\n")


def epic_body(e):
    rows = "\n".join(f"| {s['id']} | {s['title'][len(s['id']) + 3:]} | S{s['sprint']:02d} | {s['points']} | {s['priority']} |" for s in e["stories"])
    pts = sum(s["points"] for s in e["stories"])
    return (f"<!-- backlog-id: {e['id']} -->\n"
            f"**Milestone:** {e['milestone']} · **Alan:** `{e['area']}` · **Toplam SP:** {pts}\n\n"
            f"### Amaç\n{e['summary']}\n\n"
            f"### Story'ler\n| ID | Başlık | Sprint | SP | Öncelik |\n|---|---|---|---|---|\n{rows}\n")


def markdown(data):
    out = ["# AEP-CLW Ürün Backlog'u", "",
           "> Bu dosya `tools/backlog/backlog_source.py` tarafından üretilir; elle düzenlemeyin. "
           "GitHub Issues ile `backlog-sync` iş akışı üzerinden senkronize edilir.", ""]
    total = sum(s["points"] for e in data["epics"] for s in e["stories"])
    n_st = sum(len(e["stories"]) for e in data["epics"])
    mvp = sum(s["points"] for e in data["epics"] if "mvp" in e["labels"] for s in e["stories"])
    out += [f"**Özet:** {len(data['milestones'])} milestone · {len(data['epics'])} epic · {n_st} story · "
            f"{total} story point (MVP: {mvp} SP)", "", "## Milestone'lar", "",
            "| Kod | Başlık | Bitiş | Açıklama |", "|---|---|---|---|"]
    for m in data["milestones"]:
        out.append(f"| {m['code']} | {m['title']} | {m['due_on'][:10]} | {m['description']} |")
    out += ["", "## Sprint kapasite özeti", "", "| Sprint | Pencere | Story | SP |", "|---|---|---|---|"]
    for sp in range(17):
        items = [s for e in data["epics"] for s in e["stories"] if s["sprint"] == sp]
        a, b = sprint_dates(sp)
        out.append(f"| S{sp:02d} | {a} → {b} | {len(items)} | {sum(i['points'] for i in items)} |")
    for m in data["milestones"]:
        out += ["", f"## {m['title']}", ""]
        for e in [e for e in data["epics"] if e["milestone"] == m["code"]]:
            out += [f"### {e['title']}", "", e["summary"], "",
                    "| ID | Story | Sprint | Alan | SP | Öncelik | Kabul kriterleri |", "|---|---|---|---|---|---|---|"]
            for s in e["stories"]:
                out.append(f"| {s['id']} | {s['title'][len(s['id']) + 3:]} | S{s['sprint']:02d} | {s['area']} | "
                           f"{s['points']} | {s['priority']} | {'<br>'.join(s['acceptance'])} |")
            out.append("")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    data = build()
    for e in data["epics"]:
        e["body"] = epic_body(e)
        for s in e["stories"]:
            s["body"] = story_body(s, e)
    (ROOT / ".github/project").mkdir(parents=True, exist_ok=True)
    (ROOT / ".github/project/backlog.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "docs/backlog.md").write_text(markdown(data), encoding="utf-8")
    n = sum(len(e["stories"]) for e in data["epics"])
    print(f"epics={len(data['epics'])} stories={n} labels={len(data['labels'])} milestones={len(data['milestones'])}")
