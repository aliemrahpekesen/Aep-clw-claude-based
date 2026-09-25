# AEP-CLW — Definition of Ready ve Definition of Done (Kalite Görünümü)

| Alan | Değer |
|---|---|
| Doküman sahibi | `QA` (QA Lead) |
| Katkı | `PO`, `DM`, `SEC`, `CMP`, `AUD`, `OPS`, `PERF`, `UX` |
| Sürüm | v1.0 — Sprint 0 |
| İlişki | Ekip çalışma sözleşmesi [../governance/working-agreement.md](../governance/working-agreement.md) DoR/DoD'nin **yönetişim** özetini içerir; bu doküman aynı kriterlerin **kalite, güvenlik ve uyum** detayını tanımlar. Çelişki durumunda daha sıkı olan kriter geçerlidir. |

---

## 1. Definition of Ready (DoR) — Story

Bir story sprint'e ancak aşağıdakilerin tamamı sağlanmışsa alınır:

| # | Kriter |
|---|---|
| R1 | Kullanıcı hikâyesi formatında (Rol / İhtiyaç / Fayda), ilgili Epic'e bağlı, GitHub Issue'da |
| R2 | Kabul kriterleri test edilebilir, tercihen **Gherkin** (Given/When/Then); mutlu yol + hata yolları + sınır değerleri |
| R3 | **Finansal etki** işaretlendi (`fin-impact: yes/no`); evet ise ledger posting şeması (hangi hesaplar, borç/alacak) tanımlı ve SA onaylı |
| R4 | **Güvenlik AC** bölümü: yetki (hangi roller), tenant kapsamı, step-up/maker-checker gereksinimi, veri sınıfı (C1–C4), ilgili tehdit (`T-xx`) |
| R5 | **Uyum/audit**: üretilecek audit event'ler, KVKK etkisi (yeni kişisel veri?), ilgili kontrol (`CTL-xxx`) |
| R6 | API sözleşmesi taslağı (OpenAPI/AsyncAPI) veya UI tasarımı (Figma, tenant tema varyantı, erişilebilirlik notları) hazır |
| R7 | Bağımlılıklar tanımlı ve engelleyici değil (dış API sandbox erişimi, başka takım işi) |
| R8 | NFR etkisi belirtildi (performans bütçesi, ör. "ödeme yolunda +5 ms'den fazla ekleme") |
| R9 | Tahminlendi (story point), tek sprint'e sığıyor (≤ 8 SP), gerekirse bölündü |
| R10 | Test verisi / fixture ihtiyacı belirtildi |

---

## 2. Definition of Done (DoD) — Story

### 2.1 Kod ve Test

| # | Kriter | Doğrulama |
|---|---|---|
| D1 | Kod `main`'e merge edildi; PR en az 2 onay (güvenlik/ledger yollarında CODEOWNER) | GitHub |
| D2 | Tüm kabul kriterleri otomatik testlerle kapsandı (uygun seviyede: unit/integration/API/E2E) | PR'da test linki |
| D3 | Kalite kapıları yeşil: coverage domain ≥ %80 / genel ≥ %70 (new code), SonarQube 0 Blocker/Critical, ArchUnit, lint | CI |
| D4 | Ledger/wallet/payment değişikliklerinde: property-based testler (jqwik) güncel, mutation ≥ %60 (ledger), eşzamanlılık testi | CI |
| D5 | Güvenlik kapıları yeşil (SAST, SCA, secret, IaC); yeni High/Critical yok | CI |
| D6 | Contract testleri (Pact) yayınlandı/doğrulandı; şema uyumluluğu sağlandı | Pact Broker |
| D7 | Cross-tenant negatif test (yeni endpoint için) ve yetki matrisi testi eklendi | CI |
| D8 | UI değişikliğinde: axe 0 kritik/ciddi ihlal (WCAG 2.2 AA), responsive, tenant tema testi, i18n (TR/EN) anahtarları | CI + UX review |

### 2.2 Operasyonel Hazırlık

| # | Kriter |
|---|---|
| D9 | Audit event'leri üretiliyor ve katalogda tanımlı ([audit-and-inspection.md](../compliance/audit-and-inspection.md)) |
| D10 | Loglar yapılandırılmış (JSON), PII maskeli (maskeleme testi); trace span'leri ve iş metrikleri eklendi |
| D11 | Feature flag arkasında (riskli/tamamlanmamış özellik) ve varsayılan durumu belgelendi |
| D12 | DB migration expand-contract uyumlu, geri alma planı var |
| D13 | Konfigürasyon/Helm değerleri güncellendi; yeni sır Vault'ta |
| D14 | Dev ve test ortamına deploy edildi; smoke yeşil |

### 2.3 Dokümantasyon ve Kabul

| # | Kriter |
|---|---|
| D15 | OpenAPI/AsyncAPI, ADR (gerekirse), runbook (yeni operasyonel prosedür varsa) güncellendi |
| D16 | Kontrol matrisi etkisi varsa `CTL-xxx` durumu güncelleme önerisi PR'ı açıldı |
| D17 | PO kabul etti (demo veya test ortamında doğrulama) |
| D18 | Açık S1/S2 hata yok; bilinen sınırlamalar issue'da not edildi |

---

## 3. Definition of Done — Sprint

| # | Kriter |
|---|---|
| SP1 | Sprint hedefi karşılandı veya sapma gerekçelendirildi |
| SP2 | Tüm "Done" story'ler DoD'yi sağlıyor; sağlamayanlar backlog'a döndü (kısmi "done" yok) |
| SP3 | `main` her zaman release edilebilir durumda; test ortamında tam regresyon (API + E2E + contract) yeşil |
| SP4 | Test Özet Raporu (coverage, mutation, hata trendi, flaky oranı) hazır |
| SP5 | Güvenlik: açık zafiyetler SLA içinde; yeni tehditler tehdit modeline işlendi |
| SP6 | **Sprint Review paketi** (Tüzük §6): Sprint Review dokümanı, İlerleme Raporu, Sunum, **Fonksiyon Matrisi**, **Audit (Kontrol) Matrisi** güncel |
| SP7 | UAT (sprint kapsamındaki kabul gerektiren özellikler için) tamamlandı ve sign-off alındı |
| SP8 | Teknik borç kaydı güncellendi; retrospektif aksiyonları atandı |
| SP9 | Kullanıcı (paydaş) onayı alındı → sonraki sprint'e geçiş kapısı |

---

## 4. Definition of Done — Release

| # | Kriter | Sahip |
|---|---|---|
| RL1 | Release adayı preprod'da; tam regresyon + E2E (web + mobil) yeşil | QA |
| RL2 | Performans: ilgili NFR testleri (en az PT-02, değişiklik kapsamına göre PT-05/06/07) baseline'a göre regresyonsuz; ledger dengesizliği 0 | PERF |
| RL3 | Güvenlik: DAST temiz (High yok), açık Critical/High zafiyet yok, imajlar imzalı + SBOM'lu; major release'te pentest bulguları kapalı | SEC |
| RL4 | Uyum: yeni işleme faaliyeti varsa KVKK envanteri/aydınlatma güncel; ilgili kontroller en az `Implemented`; regülasyon etkisi değerlendirildi | CMP |
| RL5 | Audit: kontrol matrisi güncel, AUD'un `Tested` onayları (milestone gereği) | AUD |
| RL6 | DB migration'lar preprod'da prova edildi; rollback planı test edildi | DATA / OPS |
| RL7 | Canary analiz şablonları (Argo Rollouts) ve SLO alarmları yeni metrikleri kapsıyor | OPS |
| RL8 | Runbook'lar, release notu (Conventional Commits'ten üretilen CHANGELOG + iş diliyle özet), tenant iletişimi hazır | DOC / PO |
| RL9 | UAT sign-off; pilot tenant onayı (MVP/GA) | PO |
| RL10 | Change record ve prod promotion PR onayı (maker ≠ checker — CTL-027) | DM / OPS |
| RL11 | Mobil: mağaza incelemesine uygun build'ler (white-label tenant'lar), zorunlu güncelleme politikası belirlendi | MOB |
| RL12 | DR etkisi değerlendirildi (yeni veri deposu → yedek/replika kapsamında) | OPS |

---

## 5. Epic / Milestone için Ek Kriterler

- Epic kapanışında: tehdit modeli ve kontrol matrisi ilgili bölümleri gözden geçirildi; Fonksiyon Matrisi'nde epic'in fonksiyonları "Done".
- Milestone (M1–M8, bkz. [yol haritası](../product/roadmap.md)) kapanışında: [control-matrix.md](../compliance/control-matrix.md) §3.3 hedefleri karşılandı.
