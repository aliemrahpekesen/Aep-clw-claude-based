# AEP-CLW — Ekip Rolleri ve RACI Matrisi

| Alan | Değer |
|---|---|
| Doküman | Ekip Rolleri & RACI |
| Sahibi | Delivery Manager (`DM`) |
| Onay | Product Owner (`PO`), Chief Architect (`CA`) |
| Sürüm | v1.0 — Sprint 0 |
| Kaynak | [Proje Tüzüğü §5](../00-project-charter.md) |

---

## 1. Ekip Rolleri

| Kod | Rol | Kişi sayısı | Ana sorumluluk | Karar yetkisi |
|---|---|---|---|---|
| `DM` | Program Direktörü / Delivery Manager | 1 | Plan, kapasite, risk, sprint review, paydaş iletişimi | Takvim, kaynak, eskalasyon |
| `PO` | Product Owner (Fintech/Payments) | 1 | Vizyon, backlog önceliği, kabul kriterleri, kabul (Accepted) | Kapsam ve öncelik, fonksiyon kabulü |
| `CA` | Chief Architect | 1 | Mimari bütünlük, ADR onayı, teknik standartlar | Mimari kararlar |
| `SA` | Solution Architect – Payments | 1 | Ödeme, ledger, takas, entegrasyon tasarımı | Ödeme/ledger tasarım detayları |
| `SEC` | CISO / Security Architect | 1 | Tehdit modeli, secure SDLC, PCI DSS, pentest | Güvenlik kapısı (veto) |
| `CMP` | Compliance & Risk Officer | 1 | 6493, MASAK, KVKK/GDPR, PSD2; limit tabloları | Uyum kapısı (veto) |
| `AUD` | Internal Audit Liaison (Teftiş) | 1 | Audit (Kontrol) Matrisi, kontrol testleri, delil gereksinimleri | Kontrol etkinliği görüşü |
| `BA` | Business Analyst | 2 | Süreç analizi, FR/NFR, use-case, Fonksiyon Matrisi | Gereksinim detayları (PO onayıyla) |
| `BE` | Backend Tech Lead + Engineers | 1 + 6 | Java/Spring mikroservisler | Uygulama tasarımı (CA standartları içinde) |
| `FE` | Frontend Tech Lead + Engineers | 1 + 2 | React portallar, Web POS | UI uygulama detayları |
| `MOB` | Mobile Lead + Engineer | 1 + 1 | React Native white-label app | Mobil uygulama detayları |
| `UX` | UX/UI Lead | 1 | Design system, prototip, araştırma, erişilebilirlik | UX kararları (PO onayıyla) |
| `QA` | QA Lead + SDET | 1 + 2 | Test stratejisi, otomasyon, kalite kapıları | Kalite kapısı (Done teyidi) |
| `PERF` | Performance Engineer | 1 | Yük/stres/soak, kapasite planı | Performans kabulü |
| `OPS` | DevOps/SRE Lead + Engineer | 1 + 1 | CI/CD, OpenShift, GitOps, gözlemlenebilirlik, DR | Üretim değişiklik onayı |
| `DATA` | DBA / Data Engineer | 1 | PostgreSQL, CDC, ClickHouse, veri modeli | Veritabanı standartları |
| `DOC` | Technical Writer | 1 | Dokümantasyon, API portalı, runbook, kılavuzlar | Doküman standartları |
| | **Toplam** | **~33** | | |

---

## 2. RACI Lejantı

| Kod | Anlam | Kural |
|---|---|---|
| **R** | Responsible — işi yapan | Her faaliyette en az bir R |
| **A** | Accountable — nihai hesap veren / onaylayan | Her faaliyette **tam olarak bir** A |
| **A/R** | Hem hesap veren hem yapan | |
| **C** | Consulted — görüşü alınan (iki yönlü) | Karar öncesi danışılır |
| **I** | Informed — bilgilendirilen (tek yönlü) | Karar sonrası bilgilendirilir |
| · | Dahil değil | |

> **Veto kapıları:** `SEC` (güvenlik) ve `CMP` (uyum) C olarak yer aldıkları faaliyetlerde de kritik bulgu
> durumunda release'i durdurabilir; bu durum `DM` tarafından eskalasyon sürecine alınır.

---

## 3. RACI Matrisi

### Yönetişim & Planlama

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Proje planı, sprint takvimi, kapasite | A/R | C | C | · | · | · | · | C | · | · | · | · | C | · | I | · | · |
| 2 | Risk kaydı yönetimi | A/R | C | C | · | C | C | I | · | · | · | · | · | C | · | C | · | · |
| 3 | Paydaş iletişimi ve durum raporu | A/R | R | I | · | · | · | · | C | · | · | · | · | · | · | · | · | · |
| 4 | Sprint Review paketi (doküman, ilerleme raporu, sunum) | A | R | · | · | · | · | C | R | · | · | · | · | C | · | · | · | R |
| 5 | Milestone go/no-go kararı (MVP, GA) | R | A | C | · | C | C | C | · | · | · | · | · | C | · | C | · | · |

### Ürün & Analiz

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 6 | Ürün vizyonu ve yol haritası | C | A/R | C | · | · | C | · | R | · | · | · | C | · | · | · | · | · |
| 7 | Backlog önceliklendirme (MoSCoW) | C | A/R | C | C | · | · | · | R | · | · | · | · | · | · | · | · | · |
| 8 | Gereksinim analizi (FR/NFR), use-case | · | A | C | C | C | C | · | R | · | · | · | C | C | · | · | · | · |
| 9 | Kabul kriterleri (Gherkin) ve Definition of Ready | · | A | · | · | · | · | · | R | C | C | C | · | R | · | · | · | · |
| 10 | Fonksiyon Matrisi bakımı (her sprint) | I | A | · | · | C | · | C | R | · | · | · | · | C | · | · | · | · |
| 11 | Sektör presetleri | · | A | · | C | · | C | · | R | C | · | · | · | · | · | · | · | · |
| 12 | Kullanıcı araştırması ve kullanılabilirlik testi | · | C | · | · | · | · | · | C | · | I | I | A/R | C | · | · | · | · |

### Mimari & Tasarım

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 13 | Mimari genel bakış ve ADR onayı | I | C | A/R | R | C | · | · | · | C | · | · | · | · | · | C | C | · |
| 14 | Ledger / ödeme / takas tasarımı | · | C | A | R | C | C | C | · | C | · | · | · | · | · | · | C | · |
| 15 | Veri modeli, migrasyon, CDC tasarımı | · | · | A | C | · | · | · | · | C | · | · | · | · | · | C | R | · |
| 16 | API sözleşmeleri (OpenAPI/AsyncAPI) | · | · | A | R | · | · | · | C | R | C | C | · | C | · | · | · | C |
| 17 | Design system ve UI prototipleri | · | C | · | · | · | · | · | C | · | R | C | A/R | I | · | · | · | · |

### Güvenlik, Uyum & Denetim

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 18 | Tehdit modeli ve güvenlik gereksinimleri | · | · | C | C | A/R | · | · | · | C | · | · | · | C | · | C | · | · |
| 19 | Secure SDLC kapıları (SAST, SCA, imaj, sır taraması) | · | · | C | · | A | · | · | · | C | · | · | · | C | · | R | · | · |
| 20 | Pentest ve bulgu kapatma | I | · | C | · | A/R | · | · | · | R | R | R | · | C | · | R | · | · |
| 21 | PCI DSS kapsam minimizasyonu ve SOC 2 hazırlık | C | · | C | · | A/R | C | C | · | · | · | · | · | · | · | R | · | C |
| 22 | Regülasyon uyumu (6493, MASAK, KVKK/GDPR) ve limit tabloları | · | C | · | C | C | A/R | C | C | · | · | · | · | · | · | · | · | · |
| 23 | Audit (Kontrol) Matrisi ve kontrol testleri | I | I | · | · | C | C | A/R | C | · | · | · | · | R | · | · | · | · |
| 24 | Rol / yetki (RBAC, SoD) modeli | · | C | C | · | A | C | C | R | R | · | · | · | · | · | · | · | · |

### Geliştirme

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | Backend mikroservis geliştirme | · | · | C | C | · | · | · | C | A/R | · | · | · | C | · | · | C | · |
| 26 | Web portallar ve Web POS geliştirme | · | · | C | · | · | · | · | C | · | A/R | · | C | C | · | · | · | · |
| 27 | White-label mobil uygulama geliştirme ve mağaza yayını | · | C | · | · | C | · | · | C | · | · | A/R | C | C | · | C | · | · |
| 28 | PSP / banka / ERP / harici sistem entegrasyonları | · | C | · | A | C | · | · | R | R | · | · | · | C | · | · | · | · |
| 29 | Kod inceleme ve teknik borç yönetimi | · | · | A | C | · | · | · | · | R | R | R | · | · | · | · | · | · |

### Kalite & Performans

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | Test stratejisi ve otomasyon | · | · | C | · | · | · | · | C | C | C | C | · | A/R | C | · | · | · |
| 31 | Performans / yük / soak testleri ve kapasite planı | · | · | C | C | · | · | · | · | C | · | · | · | C | A/R | C | C | · |
| 32 | Erişilebilirlik (WCAG 2.2 AA) doğrulaması | · | I | · | · | · | · | · | · | · | R | R | A | R | · | · | · | · |
| 33 | UAT koordinasyonu (pilot tenant) | C | A | · | · | · | · | · | R | · | · | · | C | R | · | · | · | C |

### Operasyon & Veri

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 34 | CI/CD, GitOps, OpenShift ortamları | · | · | C | · | C | · | · | · | C | · | · | · | C | · | A/R | · | · |
| 35 | Gözlemlenebilirlik, SLO ve alarmlar | · | · | C | C | · | · | · | · | C | · | · | · | · | C | A/R | · | · |
| 36 | Yedekleme, DR planı ve tatbikatı | I | · | C | · | C | · | I | · | · | · | · | · | · | · | A/R | R | · |
| 37 | Olay yönetimi (incident) ve post-mortem | I | I | C | · | C | · | · | · | R | · | · | · | · | · | A/R | C | · |
| 38 | Veritabanı yönetimi, raporlama/BI veri hattı | · | · | C | · | · | · | · | · | C | · | · | · | · | · | C | A/R | · |
| 39 | Tenant onboarding (teknik) ve go-live kontrol listesi | C | A | · | · | C | C | · | R | · | · | · | · | · | · | R | · | C |

### Dokümantasyon & Eğitim

| # | Faaliyet | DM | PO | CA | SA | SEC | CMP | AUD | BA | BE | FE | MOB | UX | QA | PERF | OPS | DATA | DOC |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 40 | API portalı ve geliştirici dokümantasyonu | · | · | · | C | · | · | · | · | C | · | · | · | C | · | · | · | A/R |
| 41 | Runbook ve operasyon dokümanları | · | · | · | · | · | · | · | · | C | · | · | · | · | · | A | · | R |
| 42 | Kullanıcı kılavuzları ve kasiyer eğitim materyali | · | C | · | · | · | · | · | C | · | · | · | C | · | · | · | · | A/R |
| 43 | Release notları | · | A | · | · | · | · | · | C | · | · | · | · | C | · | · | · | R |

---

## 4. Eskalasyon Yolu

| Seviye | Konu | Muhatap | Süre hedefi |
|---|---|---|---|
| 1 | Takım içi teknik/iş anlaşmazlığı | İlgili Tech Lead + `BA` | 1 iş günü |
| 2 | Kapsam / öncelik çatışması | `PO` | 2 iş günü |
| 2 | Mimari çatışma | `CA` | 2 iş günü |
| 3 | Takvim / kaynak etkisi, güvenlik veya uyum vetosu | `DM` + `PO` + `CA` (+ `SEC`/`CMP`) | 3 iş günü |
| 4 | Sponsor kararı gerektiren konular | Proje sponsoru / yönlendirme kurulu | Sonraki kurul toplantısı |

## 5. Ritüeller ve Katılım

| Ritüel | Sıklık | Zorunlu | Opsiyonel |
|---|---|---|---|
| Daily stand-up (takım bazlı) | Günlük, 15 dk | BE, FE, MOB, QA, OPS, BA | PO, CA |
| Sprint Planning | Sprint başı | DM, PO, BA, tüm geliştirme ve QA | CA, SA, UX |
| Backlog refinement | Haftalık | PO, BA, CA/SA, Tech Lead'ler, QA, UX | SEC, CMP |
| Mimari kurul (ADR) | Haftalık | CA, SA, SEC, Tech Lead'ler, DATA, OPS | PERF |
| Sprint Review + onay kapısı | Sprint sonu | DM, PO, BA, QA, AUD, CMP, SEC, Tech Lead'ler | Tüm ekip, paydaşlar |
| Retrospektif | Sprint sonu | Tüm ekip | — |
| Risk & uyum gözden geçirme | 2 haftada bir | DM, PO, SEC, CMP, AUD | CA |
