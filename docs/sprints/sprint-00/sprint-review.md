# Sprint 00 Review — Inception & Architecture

| Alan | Değer |
|---|---|
| Sprint | S00 (planlanan pencere 2026-10-05 → 2026-10-16; çıktılar 2026-09-25'te erken tamamlandı) |
| Milestone | M0 — Inception & Architecture |
| Sprint hedefi | Kodlamaya başlamadan önce ürün, mimari, güvenlik/uyum, kalite ve DevOps tasarımını; backlog'u ve prototipi onaya hazır hale getirmek |
| Hedefe ulaşıldı mı? | **Evet** — onay kapısı bekleniyor |
| Taahhüt / Tamamlanan SP | 39 / 38 (S009 "kodlama onayı" onayınızla kapanacak) |
| Sunum | https://claude.ai/artifact/HLeG1pcicKzWVbogt2apqy |
| Tıklanabilir prototip | https://claude.ai/artifact/8UKhX5vozFKheUetcWwaRc · kaynak: [prototype/index.html](../../../prototype/index.html) |

## 1. Tamamlanan işler
| Issue | Story | SP | Çıktı |
|---|---|---|---|
| #2 S001 | Proje tüzüğü, ekip ve RACI | 2 | [Tüzük](../../00-project-charter.md), [RACI](../../product/raci.md) (43 faaliyet), [Çalışma anlaşması](../../governance/working-agreement.md) |
| #3 S002 | Mimari dokümantasyon ve ADR seti | 8 | [docs/architecture](../../architecture/) — C4, servis kataloğu, multitenancy, ledger, akışlar, veri, entegrasyon, API standartları, 12 ADR |
| #4 S003 | Güvenlik mimarisi ve tehdit modeli | 5 | [docs/security](../../security/) — 42 STRIDE tehdidi (15 kritik), secure SDLC, olay müdahale (10 playbook) |
| #5 S004 | Regülasyon, AML/KYC, kontrol matrisi | 5 | [docs/compliance](../../compliance/) — 32 regülasyon gerekliliği, **60 kontrollük Audit Matrisi** |
| #6 S005 | Gereksinimler, fonksiyon matrisi, MVP | 5 | [docs/product](../../product/) — 185 FR, 50 NFR, **147 fonksiyonluk Fonksiyon Matrisi**, MVP, yol haritası |
| #7 S006 | Test, performans, DevOps tasarımı | 5 | [docs/quality](../../quality/), [docs/devops](../../devops/) — 8 SLO, 15 dashboard, 26 runbook |
| #8 S007 | Prototip ve sunum | 5 | 4 yüzey, 25+ ekran; 23 slaytlık sunum |
| #9 S008 | Backlog-as-code ve GitHub otomasyonu | 3 | 9 milestone, 31 epic, 125 story, 51 label; `backlog-sync` iş akışı başarılı |

## 2. Açık / onaya bağlı
| Issue | Durum |
|---|---|
| #10 S009 — Sprint 0 review ve kodlama onayı | **Onayınızı bekliyor** |

## 3. Demo senaryoları (prototip)
1. **Müşteri Mobil** → Kahve Durağı: *Öde* ile dinamik QR (30 sn yenileme), *Yükle* ile 3DS akışı ve bakiye artışı.
2. Sektör değiştir → **VoltGo Şarj**: aktif şarj provizyonu kartı; **ParkPlus**: plaka oturumu; **FunLand**: aile alt cüzdanları.
3. **Tenant Admin** → Dashboard KPI'ları → Müşteriler → bloke et (gerekçe + audit kaydı) → *Onay Bekleyenler*'de kendi talebini onaylayamama (dört göz).
4. **Denetim/Teftiş** → hash zinciri doğrulama, delil paketi.
5. **Web POS** → satış, iade ve EV provizyon → gerçek tutarla kapanış.
6. **Platform Admin** → 3 adımlı yeni tenant sihirbazı, servis sağlık ızgarası.

## 4. Kalite
Bu sprint doküman sprintidir; kod kalite metrikleri Sprint 1'den itibaren raporlanır.
| Kontrol | Sonuç |
|---|---|
| Backlog senkronizasyonu | `backlog-sync` #1 başarılı; 156 issue, epic→story sub-issue bağları doğrulandı |
| Prototip | JS hatası yok; 1440px açık tema ve 400px koyu tema gezildi |
| Doküman tutarlılığı | FR→FN eşlemesi tam (FR-070 P2P bilinçli "Won't"); CTL referansları matrisle tutarlı |

## 5. Fonksiyon matrisi değişiklikleri
Baseline oluşturuldu: **147 fonksiyon** (85 MVP, 62 post-MVP), tümü `Planned`. → [function-matrix.md](../../product/function-matrix.md)

## 6. Audit (kontrol) matrisi değişiklikleri
Baseline oluşturuldu: **60 kontrol** — Erişim 12, Değişiklik 7, Finansal 9, Veri 8, Operasyon 13, AML 6, Süreklilik 5; tümü `Planned`. → [control-matrix.md](../../compliance/control-matrix.md)

## 7. Mimari kararlar (onayınıza sunulan)
ADR-001…ADR-012 (`Proposed`): mikroservis + DDD, Java 21/Spring Boot 3, PostgreSQL database-per-service + RLS, Kafka + Outbox, Saga, çift kayıtlı ledger servisi, Keycloak, OpenShift + ArgoCD, CQRS + ClickHouse, React + React Native, monorepo, kart verisi saklamama. → [adr/](../../architecture/adr/)

## 8. Karar gerektiren konular
| # | Konu | Öneri |
|---|---|---|
| K1 | MVP pilotu gerçek parayla çalışacak ama AML taraması (M6) ve otomatik mutabakat (M7) sonra geliyor | **Önerimiz:** Telafi edici kontrollerle ilerlemek (Tier 0/1 düşük limit, basit yaptırım listesi eşleşmesi, günlük manuel mutabakat) — [control-matrix §3.4](../../compliance/control-matrix.md). Alternatif: yaptırım taramasını (S101) S08'e çekmek (+5 SP). |
| K2 | Regülasyon: kapalı devre istisnasının tenant bazında sınırları | Hukuk görüşü alınana kadar pilot tenant limitleri istisna eşiğinin altında tutulur ([regulatory-framework.md](../../compliance/regulatory-framework.md) §12). |
| K3 | İlk PSP | iyzico (TR pazarı) + mock PSP; Stripe/Adyen M7'de. |
| K4 | Pilot tenant | Bir kahve zinciri (Kahve Durağı profili). |

## 9. Riskler
En yüksek 5 risk: regülasyon sınıflandırması, PSP entegrasyon süresi, ledger hot-account performansı, kapsam büyümesi, pilot tenant bulunabilirliği → [risk-register.md](../../product/risk-register.md)

## 10. Sonraki sprint önerisi — Sprint 1 (M1 Platform Foundation)
**Hedef:** Çalışan iskelet: monorepo, platform-commons, CI güvenlik kapıları, yerel ortam, Keycloak ve tenant-service.
Aday story'ler: S010–S014, S017–S018, S022, S026, S030 (42 SP).

## 11. Onay
- [ ] Proje sponsoru onayı — GitHub issue #10 üzerine yorum olarak
