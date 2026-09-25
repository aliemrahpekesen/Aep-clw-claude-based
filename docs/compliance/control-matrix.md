# AEP-CLW — Audit (Kontrol) Matrisi

| Alan | Değer |
|---|---|
| Doküman sahibi | `AUD` (Internal Audit Liaison) + `CMP` |
| Katkı | `SEC`, `OPS`, `QA`, `SA`, `DATA`, `BE` |
| Sürüm | v1.0 — Sprint 0 (başlangıç içeriği) |
| Güncelleme | **Her sprint review'da** güncellenir (Tüzük §6 — Sprint review paketi) |
| Kontrol sayısı | **60** (CTL-001 … CTL-060) |

---

## 1. Kullanım Kılavuzu

### 1.1 Sütun Tanımları

| Sütun | Açıklama |
|---|---|
| **ID** | `CTL-xxx` — kalıcıdır, yeniden kullanılmaz; emekliye ayrılan kontrol `Retired` olarak kalır |
| **Alan** | `ERİŞİM`, `DEĞİŞİKLİK`, `FİNANSAL`, `VERİ`, `OPERASYON`, `AML`, `SÜREKLİLİK` |
| **Kontrol tanımı** | Kontrolün ne yaptığı — test edilebilir ifade |
| **Risk** | Azaltılan risk; tehdit modeli ID'si (`T-xx`) varsa belirtilir |
| **Tip** | `Ö` = Önleyici, `T` = Tespit edici, `D` = Düzeltici · `O` = Otomatik, `M` = Manuel, `Y` = Yarı otomatik (IT-dependent manual) |
| **Regülasyon** | İlgili mevzuat/standart (R-xx: [regulatory-framework.md](regulatory-framework.md) §11) |
| **Servis/Bileşen** | Kontrolü uygulayan servis/araç |
| **Kanıt** | Denetçiye sunulacak delil |
| **Test yöntemi** | `Inq` = sorgulama, `Obs` = gözlem, `Insp` = inceleme, `Reperf` = yeniden performans, `Auto` = otomatik test/CI kanıtı |
| **Sorumlu** | Kontrol sahibi (rol kodu) |
| **Sprint / MS** | Kontrolün `Implemented` olması hedeflenen sprint ve milestone — [yol haritası](../product/roadmap.md) ile hizalı: M1 Platform Foundation (S1–S2), M2 Core Wallet & Ledger (S3–S4), M3 Funding & Payments (S5–S6), M4 Admin, Reporting & Audit → **MVP v1.0** (S7–S8), M5 Loyalty & Gift (S9–S10), M6 Risk, AML & Compliance (S11–S12), M7 Settlement & Accounting (S13–S14), M8 Hardening & **GA v2.0** (S15–S16) |
| **Durum** | `Planned` → `Implemented` (kod/süreç devrede) → `Tested` (tasarım + işletim testi yapıldı) → `Effective` (en az bir periyot boyunca istisnasız çalıştı, AUD onaylı) · `Deficient` (test başarısız, aksiyon planı var) |

### 1.2 Sprint Review Güncelleme Prosedürü

1. Sprint sonunda ilgili takımlar, kontrol durumu değişikliklerini PR ile önerir (kanıt linkleri dahil: CI run, PR, dashboard, rapor).
2. `AUD` kanıtı inceler; `Tested`/`Effective` geçişleri yalnızca `AUD` onayıyla yapılır (CODEOWNERS).
3. `Deficient` kontroller için aksiyon planı (sahip + tarih) §4'e eklenir.
4. §3 özet tablosu güncellenir ve Sprint Review paketine eklenir.
5. Yeni tehdit/regülasyon → yeni kontrol ID'si; değişiklik geçmişi §5'e.

---

## 2. Kontrol Matrisi

### 2.1 ERİŞİM (Access)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-002 | Tüm workforce ve platform kullanıcıları için MFA zorunludur (workforce: TOTP/WebAuthn; platform: FIDO2 donanım anahtarı); MFA'sız oturum açılamaz | Hesap ele geçirme (T-04) | Ö/O | ISO 27001 A.8.5, SOC2 CC6.1, BS ilkeleri | Keycloak `aep-workforce`, `aep-platform` | Realm konfig export, MFA kayıt raporu, başarısız giriş testi | Insp + Reperf | SEC | S2 / M1 | Planned |
| CTL-003 | Gateway her istekte JWT imza, `iss`, `aud`, `exp`, `nbf` doğrular; token `tenant_id` ile host/header tenant'ı uyuşmazsa istek reddedilir | Yetkisiz erişim, tenant karışması (T-05, T-21) | Ö/O | OWASP API2, SOC2 CC6.1 | api-gateway | Gateway konfig, negatif test sonuçları (CI) | Auto | BE | S2 / M1 | Planned |
| CTL-004 | Servisler arası trafik mTLS STRICT; yalnızca AuthorizationPolicy allowlist'indeki servisler birbirini çağırabilir; aşağı akışta token exchange + `aud` doğrulaması | Lateral movement, confused deputy | Ö/O | ISO 27001 A.8.20–8.22 | OpenShift Service Mesh | PeerAuthentication/AuthorizationPolicy manifest'leri, Kiali grafiği, izinsiz çağrı testi | Insp + Auto | OPS | S3 / M2 | Planned |
| CTL-005 | Her API metodu RBAC + ABAC (tenant, merchant, store kapsamı) ile yetkilendirilir; yetki matrisi (rol × endpoint) otomatik test edilir | BOLA/BFLA (T-21) | Ö/O | OWASP API1/API5, SOC2 CC6.3 | Tüm servisler, OPA | Yetki matrisi test raporu (CI), Semgrep `aep.authz.missing` sonucu | Auto | BE | S2 / M1 | Planned |
| CTL-006 | Hassas işlemler (cihaz bağlama, yüksek tutarlı ödeme, manuel düzeltme, rol atama, delil export) step-up authentication (`acr`, `auth_time`) gerektirir | ATO, oturum kaçırma (T-01, T-04) | Ö/O | PSD2 SCA ilkeleri, BS ilkeleri | identity-service, Keycloak, servisler | Step-up politikası, `AUTH.STEPUP.*` audit örneklemi | Reperf | SEC | S5 / M3 | Planned |
| CTL-007 | Kritik işlemler maker-checker ile yürütülür; maker≠checker (gerçek kişi eşleşmesi dahil), checker payload hash'ini onaylar, 24 saatte otomatik iptal | Insider fraud (T-18, T-28, T-29) | Ö/O | BS ilkeleri, ISO 27001 A.5.3, SOC2 CC5 | admin-bff, maker-checker modülü | Maker-checker kayıtları, "maker=checker" saved query sonucu (0 satır) | Reperf + Insp | AUD | S7 / M4 | Planned |
| CTL-008 | SoD matrisindeki toksik rol kombinasyonları atama anında sistem tarafından engellenir; geliştirici/prod-deploy/prod-veri erişimi ayrılığı | SoD aşımı (T-32) | Ö/O | ISO 27001 A.5.3, SOC2 CC5.1 | identity-service, OPA `sod-policy` | SoD politika dosyası, `IAM.SOD.VIOLATION_BLOCKED` olayları, test | Auto + Insp | CMP | S7 / M4 | Planned |
| CTL-009 | Kullanıcı erişimleri çeyreklik (ayrıcalıklı roller aylık) gözden geçirilir; gözden geçirmede onaylanmayan erişim 5 iş günü içinde kaldırılır | Aşırı yetki birikimi (T-32) | T/Y | ISO 27001 A.5.18, SOC2 CC6.2 | Admin portal erişim raporu | İmzalı erişim gözden geçirme kayıtları | Insp | TENANT_ADMIN / AUD | S8 / M4 | Planned |
| CTL-010 | Joiner-Mover-Leaver: ayrılan personelin erişimi ≤ 24 saatte kapatılır; rol değişikliğinde eski yetkiler kaldırılır; AUDITOR ataması süre sonunda otomatik düşer | Yetkisiz erişim | Ö/Y | ISO 27001 A.5.18, SOC2 CC6.2 | Keycloak + IGA süreci | HR ayrılış listesi ↔ hesap kapanış zamanı karşılaştırması | Reperf | SEC | S8 / M4 | Planned |
| CTL-019 | Sırlar yalnızca Vault'ta; DB kimlik bilgileri dinamik (TTL ≤ 24 saat); CI/CD uzun ömürlü sır kullanmaz (OIDC) | Sır sızıntısı (T-37) | Ö/O | ISO 27001 A.8.24, SOC2 CC6.1 | Vault, GitHub OIDC | Vault policy'leri, lease raporu, Gitleaks raporu | Insp + Auto | OPS | S2 / M1 | Planned |
| CTL-022 | Prod'a ayrıcalıklı erişim yalnızca break-glass (JIT ≤ 1 saat, iki onay, oturum kaydı); tüm kullanımlar 2 iş günü içinde incelenir | İçeriden tehdit (T-30) | Ö/T/Y | BS ilkeleri, ISO 27001 A.8.2 | PAM, Vault, OpenShift OAuth | Break-glass kayıtları, oturum kayıtları, inceleme notları | Insp | SEC | S6 / M3 | Planned |
| CTL-054 | Müşteri cihaz bağlama + app attestation (Play Integrity / App Attest) doğrulanır; yeni cihazda cool-down ve düşük limit uygulanır | ATO, sahte uygulama (T-01, T-02, T-03) | Ö/O | MASVS L2-R | identity-service, mobile app | Attestation doğrulama logları, cool-down test sonuçları | Auto + Reperf | MOB / SEC | S5 / M3 | Planned |

### 2.2 DEĞİŞİKLİK YÖNETİMİ (Change Management)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-023 | `main` branch korumalı: PR + en az 2 onay (güvenlik/ledger yollarında SEC/SA CODEOWNER), CI yeşil, doğrudan push yok, force push yok | Yetkisiz/hatalı kod değişikliği | Ö/O | ISO 27001 A.8.32, SOC2 CC8.1 | GitHub branch protection / rulesets | Ruleset export, PR örneklemi | Insp + Reperf | OPS | S1 / M1 | Planned |
| CTL-024 | Her PR'da SAST (Semgrep/Sonar), SCA (Dependency-Check/Snyk), secret scan (Gitleaks), IaC scan (Checkov) çalışır; kırma kriterleri ihlalinde merge engellenir | Zafiyetli kod/bağımlılık (T-35, T-37) | Ö/O | NIST SSDF, ISO 27001 A.8.25–8.28 | GitHub Actions | Workflow run'ları, SARIF raporları, DefectDojo | Auto | SEC | S1 / M1 | Planned |
| CTL-025 | Prod imajları Trivy taramalı, CycloneDX SBOM'lu ve Cosign imzalıdır; admission controller imzasız/SBOM'suz imajı reddeder | Tedarik zinciri saldırısı (T-35, T-36) | Ö/O | SLSA L3, NIST SSDF | CI, Quay, Kyverno/policy-controller | Rekor kayıtları, admission ret logları, SBOM deposu (Dependency-Track) | Auto + Reperf | OPS | S1 / M1 | Planned |
| CTL-026 | Prod'daki tüm değişiklikler yalnızca GitOps (ArgoCD) ile; manuel `oc apply` yasak; drift tespitinde alarm + otomatik düzeltme | Kayıt dışı değişiklik | Ö/T/O | ISO 27001 A.8.32, SOC2 CC8.1 | ArgoCD, OpenShift RBAC | ArgoCD senkron geçmişi, drift alarmları, RBAC konfig | Insp + Auto | OPS | S1 / M1 | Planned |
| CTL-027 | Prod promotion PR'ı release manager + (değişiklik sınıfı yüksekse) CAB onayı gerektirir; onaylayan, değişikliği geliştirenden farklıdır; release notu ve rollback planı zorunlu | Onaysız release | Ö/Y | BS ilkeleri, SOC2 CC8.1 | GitOps repo, GitHub Environments | Promotion PR'ları, onay kayıtları, release notları | Insp | DM / OPS | S8 / M4 | Planned |
| CTL-028 | Veritabanı migration'ları Flyway ile, expand-contract deseninde; geri alınamaz (destructive) migration DBA onayı ve yedek doğrulaması gerektirir | Veri kaybı, kesinti | Ö/Y | ISO 27001 A.8.32 | Flyway, CI | Migration PR review'ları, CI migration testi | Insp + Auto | DATA | S1 / M1 | Planned |
| CTL-029 | Tenant iş konfigürasyonu (limit, ücret, breakage, P2P, regülasyon modeli, IBAN) değişiklikleri versiyonlanır, maker-checker ile onaylanır, regülasyon tavanını aşamaz | Limit manipülasyonu, istisna ihlali (T-18, T-27) | Ö/O | 6493 LNE, 6502, 5549 | tenant-service, merchant-service | Konfig geçmişi, `TENANT.CONFIG.CHANGED` olayları, tavan aşım testi | Auto + Reperf | PO / CMP | S7 / M4 | Planned |

### 2.3 FİNANSAL DOĞRULUK (Financial Integrity)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-030 | Her journal Σ(borç) = Σ(alacak) (para birimi bazında) — DB deferrable constraint ile zorlanır; property-based testler (jqwik) CI'da | Dengesiz defter (T-12) | Ö/O | SOC2 PI1, TFRS | ledger-service | Constraint DDL, jqwik raporu, mutation skoru ≥ %60 | Auto + Insp | SA | S3 / M2 | Planned |
| CTL-031 | Bakiye değiştiren tüm API'ler `Idempotency-Key` zorunlu kılar; aynı key + farklı payload reddedilir; sonuç 24 saat önbelleklenir | Mükerrer işlem (T-09) | Ö/O | SOC2 PI1 | payment, funding, wallet | API sözleşmesi, entegrasyon testi, Semgrep kuralı | Auto | BE | S3 / M2 | Planned |
| CTL-032 | Çifte harcama ve yarış koşulu koruması: atomik koşullu debit, `CHECK (available >= 0)`, hold durum makinesi, QR counter tek kullanım | Çifte harcama, replay (T-07, T-08, T-10) | Ö/O | SOC2 PI1 | wallet, ledger, payment, Redis | Eşzamanlılık testleri (jqwik + Testcontainers), yük testi sonuçları, DB constraint | Auto + Reperf | SA | S4 / M2 | Planned |
| CTL-033 | Ledger dengesizliği (`ledger_imbalance_total`) ve negatif bakiye için gerçek zamanlı alarm; ≠ 0 → P1 sayfa (page) + PB-02 | Tespit edilmeyen finansal hata (T-12) | T/O | SOC2 PI1, CC7 | ledger, Prometheus/Alertmanager | Alarm kuralı, tatbikat kaydı, alarm geçmişi | Reperf | OPS / SA | S5 / M3 | Planned |
| CTL-034 | PSP/banka işlemleri günlük otomatik mutabakat; istisnalar 1 iş günü içinde sınıflandırılır, 5 iş günü içinde çözülür | Mutabakatsızlık, kayıp (T-19, T-20) | T/Y | SOC2 PI1, 6493 | settlement-service | Günlük mutabakat raporları, istisna yaşlandırma raporu | Reperf + Insp | FINANCE | S13 / M7 | Planned |
| CTL-035 | Müşteri fonu mutabakatı: ledger'daki toplam müşteri yükümlülüğü ↔ tenant fon hesap(lar)ı bakiyesi günlük karşılaştırılır; fark eşiği aşarsa alarm | Fon açığı (safeguarding) | T/Y | 6493 (fon koruma), TFRS | settlement, ledger, reporting | Günlük fon mutabakat raporu, imzalı onay | Reperf | FINANCE / CMP | S13 / M7 | Planned |
| CTL-036 | Ledger append-only: journal kayıtları güncellenemez/silinemez; düzeltme yalnızca ters kayıt (reversal) + maker-checker ile | Kayıt manipülasyonu (T-11, T-28) | Ö/O | BS ilkeleri, SOC2 PI1 | ledger-service, PostgreSQL grants | DB yetki listesi, trigger, Semgrep `aep.ledger.no-update-delete` | Auto + Insp | SA / DATA | S3 / M2 | Planned |
| CTL-037 | GL/yevmiye export'u ledger deneme mizanı ile mutabık; e-Fatura/e-Arşiv belgeleri işlemlerle eşleşir; breakage hesaplaması onaylı politika ile | Mali tablo hatası | T/Y | VUK, TFRS 15 | accounting-service | Export ↔ mizan mutabakat raporu, e-belge eşleşme raporu | Reperf | FINANCE | S14 / M7 | Planned |
| CTL-038 | Gelen webhook'lar imza + zaman damgası + event ID tekilliği ile doğrulanır; funding credit'i yalnızca PSP S2S geri sorgulama teyidi sonrası yazılır; ödeme tutarı yalnızca sunucu tarafı payment intent'ten | Webhook sahteciliği, tutar manipülasyonu (T-13, T-16) | Ö/O | PCI-DSS, SOC2 PI1 | funding, payment | Entegrasyon testleri (sahte webhook), kod review | Auto + Reperf | BE / SEC | S5 / M3 | Planned |

### 2.4 VERİ KORUMA (Data Protection)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-011 | Tenant izolasyonu: PostgreSQL RLS (`FORCE`), TenantContext yalnızca token'dan, ClickHouse row policy, Redis prefix; cross-tenant negatif test seti her build'de | Tenant veri sızıntısı (T-21, T-22, T-23) | Ö/O | KVKK md.12, 6493 LNE, SOC2 C1 | Tüm servisler, DB | RLS politika DDL, cross-tenant test raporu, ArchUnit raporu | Auto + Reperf | SA / DATA | S2 / M1 | Planned |
| CTL-012 | PII alanları (ad, telefon, e-posta, TCKN, adres) uygulama seviyesinde AES-256-GCM ile şifrelenir (envelope, tenant KEK); arama blind index ile | PII ifşası (T-30) | Ö/O | KVKK md.12, GDPR Art.32 | customer-service, Vault Transit | Şema incelemesi (şifreli kolonlar), kripto birim testleri | Insp + Auto | SEC | S3 / M2 | Planned |
| CTL-013 | Transit TLS 1.3 (dış) / mTLS (iç); at-rest AES-256 (DB volume, backup, object storage, Kafka) | Dinleme, medya çalınması (T-25) | Ö/O | PCI-DSS 4.2, ISO 27001 A.8.24 | Edge, mesh, storage | TLS tarama raporu (testssl.sh), storage şifreleme konfig | Insp + Auto | OPS | S2 / M1 | Planned |
| CTL-014 | Anahtar hiyerarşisi HSM/KMS kökü; KEK yıllık, imza anahtarları politika bazlı rotasyon; anahtar erişimi Vault audit ile izlenir | Anahtar kompromizi | Ö/Y | PCI-DSS 3.6, ISO 27001 A.8.24 | Vault, HSM | Rotasyon kayıtları, Vault audit örneklemi | Insp | SEC | S4 / M2 | Planned |
| CTL-015 | Log/trace'lerde PII ve sır maskeleme (Logback + OTel redaction); haftalık otomatik PII sızıntı taraması | Log üzerinden ifşa (T-24) | Ö/T/O | KVKK md.12, GDPR Art.32 | Logging kütüphanesi, OTel Collector, Loki | Maskeleme birim testleri, DLP tarama raporları | Auto + Reperf | SEC / OPS | S2 / M1 | Planned |
| CTL-016 | Saklama süresi dolan kişisel veriler periyodik imha edilir (crypto-shredding dahil); imha tutanağı üretilir | Aşırı saklama | Ö/Y | KVKK md.7, Silme/İmha Yönetmeliği, GDPR Art.17 | customer-service, Vault | İmha job logları, `KEY.SHREDDED` olayları, imha tutanakları | Reperf | CMP / DATA | S8 / M4 | Planned |
| CTL-017 | Aydınlatma metni ve açık rıza versiyonlu kaydedilir (metin versiyonu, zaman, kanal); geri çekme anında uygulanır; İYS ile senkron | Hukuka aykırı işleme | Ö/O | KVKK md.5, 10; GDPR Art.7; 6563 (İYS) | customer-service, notification-service | Onay kayıtları örneklemi, İYS senkron raporu | Reperf | CMP | S3 / M2 | Planned |
| CTL-018 | Kart verisi (PAN/CVV) sistemlere girmez; PSP hosted page/iframe/SDK kullanılır; ödeme sayfalarında CSP + SRI | PCI kapsam genişlemesi | Ö/O | PCI-DSS v4.0 SAQ A | funding-service, web/mobil | Veri akış diyagramı, DLP taraması (PAN regex), CSP başlıkları, SAQ A | Insp + Auto | SEC | S5 / M3 | Planned |

### 2.5 OPERASYON (Operations & Security Operations)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-001 | Bilgi güvenliği politika seti (erişim, kripto, kabul edilebilir kullanım, IR, BCM, tedarikçi) yönetimce onaylı ve yıllık gözden geçirilir | Yönetişim eksikliği | Ö/M | ISO 27001 5.2, A.5.1; SOC2 CC1 | ISMS | Onaylı politika seti, gözden geçirme tutanağı | Insp | SEC | S1 / M1 | Planned |
| CTL-020 | Edge'de CDN + DDoS + WAF (OWASP CRS) aktif; WAF kural değişiklikleri GitOps ile | DDoS, web saldırıları (T-38) | Ö/O | OWASP, SOC2 A1 | Edge/WAF | WAF konfig, blok raporları | Insp + Reperf | OPS | S6 / M3 | Planned |
| CTL-021 | Katmanlı rate limit (IP, kullanıcı, terminal, tenant); OTP, voucher, login için brute-force limitleri | Kaynak tüketimi, brute force (T-02, T-33, T-38) | Ö/O | OWASP API4/API6 | api-gateway, Redis | Rate limit konfig, yük testi sonuçları (429) | Auto | BE | S2 / M1 | Planned |
| CTL-039 | Platform hardening: SCC `restricted-v2`, non-root, read-only FS, NetworkPolicy default-deny, egress allowlist, Kyverno politikaları, CIS benchmark | Konteyner kaçışı, SSRF (T-40, T-41) | Ö/O | CIS, ISO 27001 A.8.9 | OpenShift, Kyverno | Kyverno policy raporları, CIS (compliance-operator) sonuçları | Auto + Insp | OPS | S2 / M1 | Planned |
| CTL-040 | Güvenlik logları (Keycloak, gateway, Vault, K8s audit, audit-service) merkezi SIEM'e aktarılır; korelasyon kuralları ve UEBA; alarm triyajı SLA'lı | Tespit edilmeyen saldırı | T/O | ISO 27001 A.8.15–8.16, SOC2 CC7.2 | SIEM, Loki | Log kaynak envanteri, alarm örneklemi, triyaj kayıtları | Insp + Reperf | SEC | S8 / M4 | Planned |
| CTL-041 | Audit log hash-zincirli, HSM imzalı checkpoint'li ve WORM'da (10 yıl); günlük otomatik bütünlük doğrulaması | Delil manipülasyonu (T-31) | Ö/T/O | BS ilkeleri, 5549, SOC2 CC7 | audit-service, WORM storage | Bütünlük doğrulama raporları, Object Lock konfig, tahrifat testi | Auto + Reperf | AUD / SA | S4 / M2 | Planned |
| CTL-042 | Zafiyetler DefectDojo'da izlenir; SLA: Critical 72 saat, High 7 gün, Medium 30 gün, Low 90 gün; ihlaller eskale edilir | İstismar edilebilir zafiyet | D/Y | ISO 27001 A.8.8, SOC2 CC7.1 | DefectDojo, CI | SLA uyum raporu | Insp | SEC | S2 / M1 | Planned |
| CTL-043 | Olay müdahale planı onaylı; 6 ayda bir tabletop, yılda bir KVKK 72 saat bildirim provası; postmortem aksiyonları izlenir | Etkisiz olay yönetimi | D/M | KVKK md.12, GDPR Art.33, ISO 27001 A.5.24–5.28 | CSIRT | IR planı, tatbikat raporları, postmortem'ler | Insp | SEC / CMP | S8 / M4 | Planned |
| CTL-044 | Bağımsız pentest (web/API, mobil, multi-tenant, iş mantığı) MVP öncesi ve yılda bir; Critical/High bulgular release öncesi kapatılır, retest yapılır | Tespit edilmemiş zafiyet | T/M | BS ilkeleri, PCI-DSS 11.4, ISO 27001 A.8.8 | Harici firma | Pentest raporu, retest raporu | Insp | SEC | S8 / M4 | Planned |
| CTL-045 | Tüm personele yıllık güvenlik + KVKK + AML farkındalık eğitimi; geliştiricilere güvenli kodlama eğitimi; tamamlama ≥ %95 | İnsan kaynaklı hata | Ö/M | ISO 27001 A.6.3, 5549 (eğitim), SOC2 CC1.4 | LMS | Eğitim tamamlama raporu | Insp | SEC / CMP | S7 / M4 | Planned |
| CTL-046 | Kritik yolculuklar için SLO/SLI tanımlı; error budget politikası; 7/24 on-call ve eskalasyon; SLO ihlali postmortem gerektirir | Kullanılabilirlik kaybı | T/Y | SOC2 A1.1 | Prometheus, Grafana, Alertmanager | SLO dashboard, on-call çizelgesi, postmortem'ler | Insp | OPS | S6 / M3 | Planned |
| CTL-047 | Kapasite yönetimi: her release öncesi performans regresyon testi; çeyreklik kapasite planı; tenant kotaları (noisy neighbor) | Kapasite yetersizliği (T-14, T-39) | Ö/Y | SOC2 A1.1 | Gatling/k6, KEDA/HPA | Performans test raporları, kapasite planı | Insp + Reperf | PERF | S8 / M4 | Planned |
| CTL-059 | Kritik tedarikçiler (bulut/hosting, PSP, SMS, KYC sağlayıcı, HSM) için risk değerlendirmesi, sözleşmede güvenlik/denetim/veri yerelliği hükümleri, yıllık gözden geçirme; alt işleyen listesi | Tedarikçi riski (T-42) | Ö/M | ISO 27001 A.5.19–5.22, KVKK md.9, BS dış hizmet ilkeleri | CMP süreci | Tedarikçi envanteri, değerlendirme formları, DPA'lar | Insp | CMP | S6 / M3 | Planned |

### 2.6 AML / Fraud

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-048 | KYC seviyesine bağlı limitler `min(tenant, regülasyon tavanı, risk)` olarak gerçek zamanlı uygulanır; LNE hacim izleme raporu (PSD2 Art.37(2)) | Limit aşımı, aklama (T-27) | Ö/O | 5549, 6493, PSD2 | wallet, compliance, tenant | Limit testleri, limit aşım red logları, hacim raporu | Auto + Reperf | CMP | S3 / M2 | Planned |
| CTL-049 | Yaptırım/PEP taraması: onboarding, seviye yükseltme ve günlük delta yeniden tarama; olası eşleşme 24 saatte incelenir | Yaptırımlı kişiye hizmet | Ö/T/O | 6415, 7262, 5549 | compliance-service | Tarama logları (liste versiyonu), inceleme SLA raporu | Reperf | CMP | S11 / M6 | Planned |
| CTL-050 | İşlem izleme senaryoları (TM-01…TM-12) aktif; senaryo değişiklikleri backtest + gölge mod + maker-checker; çeyreklik etkinlik gözden geçirme | Aklama, fraud, insider (T-17, T-29, T-34) | T/O | 5549, MASAK rehberleri | compliance, risk | Senaryo kataloğu, uyarı istatistikleri, gözden geçirme tutanağı | Insp + Reperf | CMP | S11 / M6 | Planned |
| CTL-051 | AML vaka yönetimi SLA'lı; STR şüphe tarihinden ≤ 10 iş günü içinde maker-checker ile gönderilir; vaka bilgisi yalnızca yetkili rollerce görülür (tipping-off) | STR gecikmesi, ifşa (T-26) | Ö/T/Y | 5549 md.4, Tedbirler Yönetmeliği | compliance-service | Vaka yaşlandırma raporu, STR zaman çizelgesi, erişim testi | Reperf + Insp | CMP (MLRO) | S12 / M6 | Planned |
| CTL-052 | KYC, işlem, AML ve audit kayıtları yasal süreler boyunca (8/10 yıl) saklanır; retention politikası otomatik uygulanır; saklama süresinden önce silme engellidir | Kayıt kaybı | Ö/O | 5549 md.8, VUK md.253, TTK md.82 | audit, ledger, compliance, WORM | Retention konfig, WORM lock ayarları, örneklem geri getirme | Insp + Reperf | CMP / DATA | S6 / M3 | Planned |
| CTL-053 | Gerçek zamanlı fraud kural motoru (velocity, cihaz parmak izi, attestation, geofence) ödeme ve yükleme yolunda; karar < 50 ms; kural değişiklikleri maker-checker | Kart fraud, kampanya istismarı, quishing (T-15, T-17, T-34) | Ö/O | PSD2 ilkeleri, SOC2 PI1 | risk-service | Kural kataloğu, karar logları, fraud KPI raporu | Auto + Reperf | RISK_ANALYST / SA | S11 / M6 | Planned |

### 2.7 SÜREKLİLİK (Business Continuity & DR)

| ID | Kontrol tanımı | Risk | Tip | Regülasyon | Servis/Bileşen | Kanıt | Test | Sorumlu | Sprint / MS | Durum |
|---|---|---|---|---|---|---|---|---|---|---|
| CTL-055 | PostgreSQL sürekli WAL arşivleme (PITR) + günlük tam yedek; yedekler şifreli, immutable (Object Lock), ayrı bölge/hesapta | Veri kaybı, fidye yazılımı (T-25) | Ö/O | BS ilkeleri, ISO 27001 A.8.13, SOC2 A1.2 | CloudNativePG/Crunchy, object storage | Yedek job raporları, Object Lock konfig | Auto + Insp | DATA / OPS | S3 / M2 | Planned |
| CTL-056 | Çeyreklik restore tatbikatı (rastgele servis + PITR noktası); restore süresi ve veri bütünlüğü (ledger denge + hash zinciri) doğrulanır | Kullanılamaz yedek | T/Y | ISO 27001 A.8.13, SOC2 A1.3 | OPS runbook | Restore tatbikat raporları | Reperf | OPS | S8 / M4 | Planned |
| CTL-057 | DR: cross-region replika; RPO ≤ 1 dk, RTO ≤ 15 dk; yılda en az bir tam DR failover tatbikatı; lisanslı/banka tenant'ları için yurt içi ikincil sistem | Bölgesel felaket | D/Y | BS ilkeleri (yurt içi birincil/ikincil), ISO 22301, SOC2 A1.3 | OpenShift, DB replikasyonu, Kafka MirrorMaker 2 | DR tatbikat raporu (ölçülen RPO/RTO) | Reperf | OPS | S15 / M8 | Planned |
| CTL-058 | Multi-AZ yüksek erişilebilirlik: her kritik servis ≥ 3 replika, AZ'lere yayılım (topology spread), PodDisruptionBudget, DB senkron standby | AZ kaybı, bakım kesintisi | Ö/O | SOC2 A1.2 | OpenShift, Helm library chart | Helm değerleri, chaos test raporu (AZ kaybı) | Auto + Reperf | OPS | S4 / M2 | Planned |
| CTL-060 | İş etki analizi (BIA) ve iş sürekliliği planı (kasada ödeme alınamaması, PSP kesintisi senaryoları dahil); yıllık gözden geçirme ve tatbikat | Uzun süreli hizmet kesintisi | D/M | ISO 22301, BS ilkeleri, SOC2 A1 | BCM süreci | BIA, BCP, tatbikat raporu | Insp | DM / OPS | S15 / M8 | Planned |

---

## 3. Özet (Sprint Review Paketi İçin)

### 3.1 Alan × Durum

| Alan | Toplam | Planned | Implemented | Tested | Effective | Deficient |
|---|---|---|---|---|---|---|
| ERİŞİM | 12 | 12 | 0 | 0 | 0 | 0 |
| DEĞİŞİKLİK | 7 | 7 | 0 | 0 | 0 | 0 |
| FİNANSAL | 9 | 9 | 0 | 0 | 0 | 0 |
| VERİ | 8 | 8 | 0 | 0 | 0 | 0 |
| OPERASYON | 13 | 13 | 0 | 0 | 0 | 0 |
| AML | 6 | 6 | 0 | 0 | 0 | 0 |
| SÜREKLİLİK | 5 | 5 | 0 | 0 | 0 | 0 |
| **Toplam** | **60** | **60** | **0** | **0** | **0** | **0** |

### 3.2 Tip Dağılımı

Otomatik (O): 38 · Yarı otomatik (Y): 16 · Manuel (M): 6 — hedef: kritik finansal ve erişim kontrollerinin tamamı otomatik.

### 3.3 Milestone Hedefi

| Milestone | Adet | Bu milestone'da `Implemented` olacak kontroller |
|---|---|---|
| M1 Platform Foundation | 16 | CTL-001, 002, 003, 005, 011, 013, 015, 019, 021, 023, 024, 025, 026, 028, 039, 042 |
| M2 Core Wallet & Ledger | 12 | CTL-004, 012, 014, 017, 030, 031, 032, 036, 041, 048, 055, 058 |
| M3 Funding & Payments | 10 | CTL-006, 018, 020, 022, 033, 038, 046, 052, 054, 059 |
| M4 Admin, Reporting & Audit — **MVP v1.0** | 13 | CTL-007, 008, 009, 010, 016, 027, 029, 040, 043, 044, 045, 047, 056 |
| M6 Risk, AML & Compliance | 4 | CTL-049, 050, 051, 053 |
| M7 Settlement & Accounting | 3 | CTL-034, 035, 037 |
| M8 Hardening & **GA v2.0** | 2 | CTL-057, 060 |

Ek hedefler: MVP (M4) çıkışında M1–M3 kontrolleri en az `Tested`; GA (M8) çıkışında tüm kontroller en az `Tested`, kritik finansal ve erişim kontrolleri `Effective`.

### 3.4 MVP Pilotu İçin Telafi Edici Kontroller (CMP/AUD önerisi)

Yol haritası AML (M6) ve takas/mutabakat (M7) yeteneklerini MVP sonrasına koymaktadır. Gerçek para ile çalışan MVP pilotu
(M4) için aşağıdaki **telafi edici kontroller** önerilir; aksi halde ilgili kontrollerin öne çekilmesi gerekir:

| Boşluk | Risk | Telafi edici kontrol (M4'e kadar) | Sahip |
|---|---|---|---|
| CTL-049 yaptırım/PEP taraması M6'da | Yaptırımlı kişiye hizmet | Pilot yalnızca Tier 0/Tier 1 düşük limitlerle; onboarding'de minimum ulusal liste taraması (basit ad eşleşmesi) **veya** CTL-049'un S8'e çekilmesi | CMP |
| CTL-050/053 işlem izleme ve fraud motoru M6'da | Yükle-harca, kart fraud | CTL-048 limitleri + gateway velocity limitleri (CTL-021) + 3DS2 zorunlu + günlük manuel fraud raporu incelemesi | RISK / CMP |
| CTL-034/035 otomatik mutabakat M7'de | Tespit edilmeyen PSP/fon farkı | Günlük **manuel** PSP ve fon mutabakatı (rapor + FINANCE imzası) — kanıt kontrol matrisine eklenir | FINANCE |
| CTL-057 DR tatbikatı M8'de | Bölge kaybında uzun kesinti | Pilot SLA'sında DR kapsamı açıkça sınırlı; yedek + restore tatbikatı (CTL-055/056) M4'te zorunlu | OPS |

---

## 4. Eksiklik (Deficiency) ve Aksiyon Kaydı

| Kontrol | Tespit tarihi | Bulgu | Etki | Aksiyon | Sahip | Hedef tarih | Durum |
|---|---|---|---|---|---|---|---|
| — | — | (Sprint 0: henüz test yapılmadı) | — | — | — | — | — |

---

## 5. Değişiklik Geçmişi

| Tarih | Sprint | Değişiklik | Onaylayan |
|---|---|---|---|
| 2026-09-25 | Sprint 0 | İlk sürüm — 60 kontrol, tümü `Planned` | AUD, CMP (onay bekliyor) |
