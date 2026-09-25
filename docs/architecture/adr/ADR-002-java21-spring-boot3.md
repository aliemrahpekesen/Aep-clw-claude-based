# ADR-002: Java 21 (LTS) ve Spring Boot 3.x

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, Backend Tech Lead, `SEC`, `PERF`

## Context and Problem Statement

Backend servisleri için dil/çalışma zamanı ve uygulama çatısı seçilmelidir. Gereksinimler: finansal doğruluk, yüksek eşzamanlılık
(5.000 TPS, çok sayıda I/O bekleyen harici çağrı — PSP, banka), olgun güvenlik ekosistemi (OAuth2 RS, mTLS), uzun vadeli destek,
Türkiye pazarında yetenek bulunabilirliği, OpenShift uyumu.

## Decision Drivers

- LTS ve kurumsal destek (Red Hat build of OpenJDK / Spring commercial support opsiyonu)
- Yüksek eşzamanlılıkta basit programlama modeli
- Ekosistem: Spring Security, Spring Cloud Gateway, Resilience4j, Testcontainers, jOOQ, Flyway, Debezium, Kafka client
- Yetenek havuzu

## Considered Options

1. **Java 21 + Spring Boot 3.x** (virtual threads)
2. Kotlin + Spring Boot 3.x (coroutines)
3. Java 21 + Quarkus
4. Go
5. .NET 8

## Decision Outcome

**Seçilen: Seçenek 1 — Java 21 LTS + Spring Boot 3.x (3.3+).**

- **Virtual threads** (`spring.threads.virtual.enabled=true`) varsayılan: bloklayan (JDBC, HTTP) kod ile reaktif seviyesinde eşzamanlılık; WebFlux yalnız `api-gateway`'de (Spring Cloud Gateway gereği).
- Dil özellikleri: `record` (value object, DTO), `sealed` interface (domain sonuç tipleri: `PspOutcome`), pattern matching `switch`.
- GC: Generational ZGC; `MaxRAMPercentage=70`; AppCDS / CRaC değerlendirilir (hızlı scale-out).
- Native image (GraalVM) v1'de **kullanılmaz** (reflection yoğun kütüphaneler, derleme süresi); yeniden değerlendirme v2.
- JDK dağıtımı: Red Hat build of OpenJDK (UBI9 base image, OpenShift uyumlu, non-root).
- Java 25 LTS'ye geçiş: GA + 6 ay sonra, ayrı ADR ile.

### Consequences

- **Olumlu:** Olgun ekosistem; virtual threads ile basit imperative kod + yüksek eşzamanlılık; güçlü tip sistemi; güvenlik kütüphaneleri; geniş yetenek havuzu.
- **Olumsuz:** JVM bellek ayak izi (pod başına ~512 MB–1 GB); başlangıç süresi (AppCDS ile azaltılır); virtual thread + `synchronized` pinning riski (JDK 21'de) → kütüphane sürümleri (JDBC sürücüsü, HikariCP) kontrol edilir, `-Djdk.tracePinnedThreads` testte açık.
- **Kural:** Domain katmanı yalnız JDK + küçük yardımcılar (ör. `platform-commons-money`); Spring bağımlılığı yok.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Java 21 + Spring Boot** | Ekosistem, destek, yetenek, virtual threads | Bellek, başlangıç süresi |
| Kotlin + Spring | Kısa sözdizimi, null safety | Ekip yetkinliği, coroutines + Spring karmaşıklığı, ArchUnit/araç desteği biraz zayıf |
| Quarkus | Hızlı başlangıç, native | Ekosistem/ekip deneyimi daha dar; Spring Cloud Gateway/Security eşdeğerleri farklı |
| Go | Düşük kaynak, hızlı | Finansal domain modellemesi için tip ifade gücü, ekosistem (Debezium, jOOQ benzeri) zayıf, yetenek |
| .NET 8 | Güçlü platform | Charter ve ekip Java odaklı; OpenShift/Kafka ekosisteminde Java daha olgun |
