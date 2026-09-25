# Çalışma Anlaşması ve Süreç

## Scrum çerçevesi
| Olay | Sıklık | Çıktı |
|---|---|---|
| Sprint Planning | Sprint başı | Sprint hedefi, seçilen issue'lar (`sprint:Sxx` label'ı) |
| Daily | Her gün | Bloke işler `status:blocked` ile işaretlenir |
| Backlog Refinement | Sprint ortası | DoR'u sağlayan story'ler |
| **Sprint Review** | Sprint sonu | Review paketi (aşağıda) + **kullanıcı onayı** |
| Retrospektif | Sprint sonu | Aksiyonlar bir sonraki sprint'e issue olarak |

## Onay kapısı (Approval Gate)
Hiçbir sprint, bir önceki sprintin review paketi kullanıcı (proje sponsoru) tarafından onaylanmadan başlamaz.
Onay, ilgili `sprint-review` label'lı GitHub issue'suna yorum olarak kaydedilir ve issue kapatılır.

## Sprint Review paketi (her sprint zorunlu)
1. `docs/sprints/sprint-XX/sprint-review.md` — hedef, tamamlanan/tamamlanamayan işler, demo notları, metrikler.
2. `docs/sprints/sprint-XX/progress-report.md` — proje geneli ilerleme (burn-up, milestone durumu, RAG, riskler, bütçe/kapasite).
3. Sprint sunumu (slayt artifact'ı) — yönetici özeti ve demo ekran görüntüleri.
4. **Fonksiyon Matrisi** güncellemesi — `docs/product/function-matrix.md` (durum kolonları).
5. **Audit (Kontrol) Matrisi** güncellemesi — `docs/compliance/control-matrix.md` (kontrol durumları ve kanıtlar).
6. Kalite raporu — test sonuçları, coverage, güvenlik taraması özeti.

Şablonlar: `docs/governance/templates/`.

## Definition of Ready (DoR)
- Kullanıcı değeri ve kabul kriterleri net, test edilebilir
- Bağımlılıklar tanımlı; UX/API taslağı hazır (gerekiyorsa)
- Güvenlik/uyum etkisi değerlendirildi (kontrol matrisinde karşılığı var)
- Tahminlendi (≤ 8 SP; büyükse bölünür)

## Definition of Done (DoD)
- Kod review edildi (en az 1 onay, kritik alanlarda 2), CI yeşil
- Unit + integration + (varsa) contract testleri; domain coverage ≥ %80
- SAST/SCA/secret/container taramaları temiz (Critical/High yok)
- OpenAPI/AsyncAPI, README, runbook güncel; ADR gerekiyorsa yazıldı
- Audit event'leri ve metrikler eklendi; PII maskeleme doğrulandı
- dev ortamına deploy edildi, demo edilebilir
- Fonksiyon ve kontrol matrisleri güncellendi

## Branch ve commit kuralları
- Trunk-based: `main` korumalı; kısa ömürlü `feat/<issue>-<slug>` branch'leri
- Conventional Commits (`feat(wallet): ...`, `fix(ledger): ...`), PR başlığında issue referansı (`Closes #123`)
- Squash merge; imzalı commit önerilir

## Issue yaşam döngüsü
`Backlog → Ready → In Progress → In Review → Done → Accepted (review'da onaylandı)`
