# AEP-CLW — Proje Tüzüğü (Project Charter)

> **AEP-CLW** (Closed-Loop Wallet): Kahve zincirleri, EV şarj ağları, otopark, eğlence/oyun parkları,
> kampüs, stadyum, yemekhane gibi sektörlerde çalışan, **multitenant SaaS**, **kapalı devre (closed-loop)
> dijital cüzdan** platformu.

| Alan | Değer |
|---|---|
| Proje kodu | AEP-CLW |
| Sürüm | Planlama v1.0 (Sprint 0 / Inception) |
| Durum | **Onay bekliyor** — kodlama onaydan sonra başlar |
| Repo | `aliemrahpekesen/aep-clw-claude-based` |
| Issue tracking | GitHub Issues (Epic → Story/Task hiyerarşisi, label & milestone) |
| Sprint uzunluğu | 2 hafta · her sprint sonunda Review + onay kapısı |

## 1. Vizyon

Bir markanın (tenant) kendi müşterilerine **kendi markasıyla** ön ödemeli cüzdan, hediye kartı,
sadakat puanı ve kampanya sunabilmesi; tüm finansal hareketlerin **çift kayıtlı (double-entry) defter**
üzerinde, denetlenebilir, uyumlu ve banka/ödeme sistemleriyle mutabık şekilde yönetilmesi.

Örnek kullanım: Kahve zinciri müşterisi uygulamaya 500 TL yükler, kasada QR okutarak öder, her
alışverişte yıldız kazanır; EV şarj müşterisi şarj başında ön provizyon (hold) alınır, şarj bitince
gerçek tutar tahsil edilir; otoparkta plaka/QR ile giriş-çıkış ücreti cüzdandan düşülür.

## 2. Kapsam (Yüksek seviye yetenekler)

1. **Tenant yönetimi (SaaS)**: onboarding, plan/abonelik, konfigürasyon (para birimi, limitler, ücretler,
   son kullanma/breakage kuralları, özellik bayrakları, marka/tema, dil), tenant izolasyonu.
2. **Müşteri & kimlik**: kayıt (telefon OTP / e-posta / sosyal), KYC seviyeleri, cihaz bağlama, onaylar (KVKK/GDPR).
3. **Cüzdan**: çoklu cüzdan (ana bakiye, bonus/promosyon, hediye), bakiye, provizyon (hold), limitler.
4. **Defter (Ledger)**: çift kayıtlı, değiştirilemez (append-only) journal, gerçek zamanlı bakiye.
5. **Para yükleme (Funding)**: kart (3DS), kayıtlı kart, otomatik yükleme, havale/EFT, açık bankacılık, kasada nakit yükleme.
6. **Ödeme**: müşteri QR / işyeri QR / NFC-HCE token / barkod; authorize-capture, pre-auth (EV şarj, otopark), iade, iptal.
7. **İşyeri yönetimi**: işyeri → mağaza → terminal hiyerarşisi, POS entegrasyon API/SDK, web POS terminali.
8. **Sadakat & kampanya**: puan/yıldız, seviye (tier), cashback, kupon, hediye kartı, kural motoru.
9. **Risk & fraud**: gerçek zamanlı kural motoru, velocity, cihaz parmak izi, skor, vaka yönetimi.
10. **Uyum (Compliance)**: AML/yaptırım/PEP taraması, işlem izleme, şüpheli işlem bildirimi (MASAK), limit regülasyonları.
11. **Takas & mutabakat**: işyeri takası, PSP/banka mutabakatı, istisna yönetimi.
12. **Muhasebe**: hesap planı eşleme, yevmiye/GL export, e-Fatura/e-Arşiv, ERP (SAP/Logo/Netsis) entegrasyonu, breakage & ertelenmiş gelir.
13. **Raporlama & BI**: operasyonel dashboard, finansal raporlar, planlı rapor, export (CSV/XLSX/PDF).
14. **Denetim & teftiş**: hash-zincirli değiştirilemez audit log, maker-checker, teftiş sorgu ekranı, delil paketi.
15. **Bildirim**: push, SMS, e-posta, in-app; tenant bazlı şablon.
16. **Kanallar**: white-label müşteri mobil uygulaması, Tenant Admin Portalı, Platform Admin Konsolu, Web POS, Public API + SDK.

## 3. Temel Teknik Kararlar (özet — detay ADR'lerde)

| Konu | Karar |
|---|---|
| Mimari stil | Mikroservis, DDD bounded context, Hexagonal (Ports & Adapters) |
| Backend | Java 21 (LTS), Spring Boot 3.x, Spring Cloud Gateway, Spring Security (OAuth2 RS) |
| Veritabanı | PostgreSQL 16 — **database-per-service**; tenant izolasyonu: `tenant_id` + Row Level Security (varsayılan), büyük tenantlar için dedicated DB (tenant tiering) |
| Migrasyon | Flyway |
| Mesajlaşma | Apache Kafka (Strimzi / AMQ Streams), Transactional Outbox + Debezium CDC, Avro + Schema Registry |
| Dağıtık işlem | Saga (orchestration) + idempotency key + compensating transaction |
| Okuma modeli | CQRS; raporlama için ClickHouse (CDC ile) |
| Cache / rate limit | Redis |
| Kimlik | Keycloak (OIDC/OAuth2, realm-per-platform + organization-per-tenant), MFA |
| Sır yönetimi | HashiCorp Vault; kart verisi **tutulmaz** (PSP tokenizasyonu), kriptografik anahtarlar HSM/KMS |
| Frontend (web) | React 18 + TypeScript + Vite, TanStack Query, Design System (tenant temalı) |
| Mobil | React Native (Expo) — white-label build pipeline |
| Konteyner / platform | Docker, OpenShift 4.x (Kubernetes), Helm, ArgoCD (GitOps), OpenShift Service Mesh (mTLS) |
| CI/CD | GitHub Actions (build, test, SAST, SCA, image scan, SBOM, imza) → registry → ArgoCD |
| Gözlemlenebilirlik | OpenTelemetry, Prometheus, Grafana, Loki, Tempo, Alertmanager |
| API | REST + OpenAPI 3.1 (API-first), AsyncAPI (event'ler), versiyonlama `/v1` |
| Test | JUnit 5, Testcontainers, ArchUnit, Pact (contract), REST Assured, Playwright, Gatling/k6, PIT mutation |
| Kalite kapısı | SonarQube (coverage ≥ %80 domain, 0 critical), OWASP Dependency-Check, Trivy, Gitleaks |

## 4. Mikroservis Kataloğu

| # | Servis | Sorumluluk (Bounded Context) |
|---|---|---|
| 1 | `api-gateway` | Yönlendirme, JWT doğrulama, tenant çözümleme, rate limit |
| 2 | `identity-service` | Keycloak adaptörü, OTP, cihaz bağlama, oturum |
| 3 | `tenant-service` | Tenant onboarding, konfigürasyon, feature flag, plan, marka |
| 4 | `customer-service` | Müşteri profili, KYC seviyesi, onaylar |
| 5 | `wallet-service` | Cüzdan hesapları, bakiye görünümü, hold, limit kontrolü |
| 6 | `ledger-service` | Çift kayıtlı defter, journal, hesap planı, bakiye kaynağı (source of truth) |
| 7 | `payment-service` | Ödeme orkestrasyonu (QR/token), auth/capture/refund/reversal sagaları |
| 8 | `funding-service` | Para yükleme, PSP/banka/açık bankacılık adaptörleri, otomatik yükleme |
| 9 | `merchant-service` | İşyeri, mağaza, terminal, POS API anahtarları |
| 10 | `loyalty-service` | Puan, tier, kampanya/kural motoru, kupon, cashback |
| 11 | `voucher-service` | Hediye kartı / e-kod üretimi, aktivasyon, bakiye |
| 12 | `risk-service` | Gerçek zamanlı fraud kuralları, velocity, skor, vaka |
| 13 | `compliance-service` | AML/yaptırım tarama, işlem izleme, STR, regülasyon limitleri |
| 14 | `settlement-service` | Takas, mutabakat (PSP/banka dosyaları), istisnalar |
| 15 | `accounting-service` | GL eşleme, yevmiye export, e-Fatura, ERP adaptörleri, breakage |
| 16 | `reporting-service` | CQRS okuma modelleri, dashboard, planlı rapor, export |
| 17 | `audit-service` | Hash-zincirli audit log, teftiş sorguları, delil paketi |
| 18 | `notification-service` | Push/SMS/e-posta, şablon, tercih |
| 19 | `admin-bff` / `mobile-bff` / `pos-bff` | Kanal bazlı Backend-for-Frontend |

## 5. Sanal Ekip (Dünya standartlarında uzman kadro)

| Rol | Kod | Sorumluluk |
|---|---|---|
| Program Direktörü / Delivery Manager | `DM` | Plan, risk, sprint review, paydaş iletişimi |
| Product Owner (Fintech/Payments) | `PO` | Backlog önceliklendirme, kabul kriterleri |
| Chief Architect | `CA` | Mimari bütünlük, ADR onayı |
| Solution Architect – Payments | `SA` | Ödeme/ledger/settlement tasarımı |
| CISO / Security Architect | `SEC` | Tehdit modeli, PCI-DSS, secure SDLC, pentest |
| Compliance & Risk Officer | `CMP` | 6493 / MASAK / KVKK / GDPR / PSD2 uyumu |
| Internal Audit Liaison (Teftiş) | `AUD` | Audit matrisi, kontrol testleri |
| Business Analyst ×2 | `BA` | Süreç analizi, fonksiyon matrisi, use-case |
| Backend Tech Lead + Engineers ×6 | `BE` | Java/Spring mikroservisler |
| Frontend Tech Lead + Engineers ×2 | `FE` | React portallar |
| Mobile Lead + Engineer | `MOB` | React Native white-label app |
| UX/UI Lead | `UX` | Design system, prototip, kullanılabilirlik |
| QA Lead + SDET ×2 | `QA` | Test stratejisi, otomasyon, kalite kapıları |
| Performance Engineer | `PERF` | Yük/stres/soak testleri, kapasite planı |
| DevOps/SRE Lead + Engineer | `OPS` | CI/CD, OpenShift, GitOps, gözlemlenebilirlik, DR |
| DBA / Data Engineer | `DATA` | PostgreSQL, CDC, ClickHouse, veri modeli |
| Technical Writer | `DOC` | Dokümantasyon, API portal, runbook |

## 6. Kalite ve Yönetişim

- **Definition of Ready / Done**: `docs/governance/working-agreement.md`
- **Sprint review paketi** (her sprint): Sprint Review dokümanı, İlerleme Raporu, Sunum,
  **Fonksiyon Matrisi**, **Audit (Kontrol) Matrisi** → kullanıcı onayı → sonraki sprint.
- **Mimari kararlar**: ADR (`docs/architecture/adr/`).
- **Branch stratejisi**: trunk-based, kısa ömürlü feature branch + PR, zorunlu review + CI yeşil.
