# ADR-001: Mikroservis Mimarisi + Domain-Driven Design (Hexagonal)

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** Chief Architect (`CA`), Solution Architect – Payments (`SA`), Backend Tech Lead
- **İlgili:** [architecture-overview.md](../architecture-overview.md), [domain-model.md](../domain-model.md), [service-catalog.md](../service-catalog.md)

## Context and Problem Statement

AEP-CLW; cüzdan, ledger, ödeme, yükleme, sadakat, risk, uyum, takas, muhasebe gibi **farklı değişim hızına, farklı
ölçekleme profiline ve farklı regülasyon gereksinimine** sahip çok sayıda yeteneği multitenant SaaS olarak sunacaktır.
Hedefler: 5.000 TPS ödeme, %99,95 kullanılabilirlik, bağımsız ekiplerle paralel geliştirme (6 BE + FE + MOB), denetlenebilirlik.
Sistemin nasıl ayrıştırılacağına karar verilmelidir.

## Decision Drivers

- Ödeme/ledger sıcak yolunun diğer yeteneklerden **bağımsız ölçeklenmesi** ve arıza izolasyonu
- Regülasyon kapsamındaki bileşenlerin (ledger, compliance, audit) **sınırlarının net** olması (denetim kapsamı)
- Ekip özerkliği, bağımsız dağıtım
- Karmaşık iş kuralları için güçlü domain modeli (invariant'lar)
- Operasyonel karmaşıklığın yönetilebilir kalması

## Considered Options

1. **Modüler monolit** (tek dağıtım birimi, modül sınırları ArchUnit ile)
2. **Mikroservis + DDD bounded context + Hexagonal** (charter'daki 19 servis)
3. **Makro servisler** (4–5 büyük servis: Core Money, Engagement, Back-office, Platform)

## Decision Outcome

**Seçilen: Seçenek 2** — her bounded context bir mikroservis; her servis Hexagonal (Ports & Adapters) iç yapıda;
servisler arası iletişim REST (karar anı) + Kafka event'leri (durum yayılımı).

Uygulama kuralları:
- Servis sınırları = bounded context sınırları (domain-model.md context map). Yeni servis ancak yeni bounded context ile (ADR gerekir).
- Paket yapısı `com.aep.clw.<service>.{domain, application, adapter.in.*, adapter.out.*, config}`; ArchUnit ile zorlanır.
- Senkron bağımlılık grafı DAG'dır, derinlik ≤ 3; `ledger`, `risk` yaprak servislerdir.
- Paylaşılan kod yalnız `platform-commons-*` kütüphaneleri (teknik); **paylaşılan domain modeli yoktur**.

### Consequences

- **Olumlu:** Ödeme/ledger bağımsız ölçeklenir ve ayrı SLO'ya sahip; arıza izolasyonu (loyalty çökse ödeme çalışır); PCI/denetim kapsamı servis bazında daraltılabilir; ekipler paralel çalışır; teknoloji evrimi (ör. ledger'ı gRPC'ye taşımak) lokal.
- **Olumsuz:** Dağıtık işlem karmaşıklığı (→ ADR-004 Outbox, ADR-005 Saga); gözlemlenebilirlik ve test (contract test) maliyeti; ağ gecikmesi (p99 bütçesi dikkatle yönetilmeli); başlangıç altyapı maliyeti yüksek.
- **Risk azaltma:** Sprint 1–2'de "walking skeleton" (gateway → payment → wallet → ledger) ile gecikme bütçesi ölçülür; servis sayısı operasyonel olgunluğa göre kademeli açılır (ör. voucher, accounting başlangıçta daha az replica).

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| Modüler monolit | Basit operasyon, tek transaction, düşük gecikme | Tek ölçekleme birimi; loyalty batch'i ödeme gecikmesini etkiler; denetim kapsamı tüm kod; 19 context'li büyük kod tabanında sınır erozyonu; bağımsız dağıtım yok |
| **Mikroservis + DDD** | Bağımsız ölçek/dağıtım, arıza izolasyonu, net sorumluluk | Dağıtık sistem karmaşıklığı, operasyon maliyeti |
| Makro servisler | Orta karmaşıklık | Sınırlar keyfi; ledger ile ödeme aynı dağıtımda → denetim/ölçek ayrışması kaybolur; ileride bölme maliyeti |

## More Information

- Charter §3–4. Yeniden değerlendirme tetikleyicisi: walking skeleton'da p99 > 300 ms çıkması veya ekip < 4 BE'ye düşmesi.
