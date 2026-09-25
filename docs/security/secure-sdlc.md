# AEP-CLW — Güvenli Yazılım Geliştirme Yaşam Döngüsü (Secure SDLC)

| Alan | Değer |
|---|---|
| Doküman sahibi | `SEC` |
| Katkı | `OPS`, `QA`, `BE`, `FE`, `MOB` |
| Referans çerçeveler | OWASP SAMM 2.0, NIST SSDF (SP 800-218), SLSA v1.0, OWASP ASVS 4.0.3 L2 / MASVS L2 |
| Sürüm | v1.0 — Sprint 0 |

> Pipeline'ın teknik uygulaması: [../devops/devops-pipeline.md](../devops/devops-pipeline.md). Kontrol eşlemesi:
> CTL-023 (review), CTL-024 (CI güvenlik kapıları), CTL-025 (imaj/SBOM/imza), CTL-042 (zafiyet SLA), CTL-044 (pentest).

---

## 1. SDLC Fazları ve Güvenlik Aktiviteleri

| Faz | Aktivite | Çıktı | Sorumlu | Kapı |
|---|---|---|---|---|
| Planlama / DoR | Güvenlik & gizlilik gereksinimleri (ASVS/MASVS eşlemesi), abuse case'ler, veri sınıflandırma | Story'de "Security AC" bölümü | PO + SEC şampiyonu | DoR |
| Tasarım | Tehdit modelleme (STRIDE) — yeni servis/dış entegrasyon/para akışı değişikliği | [threat-model.md](threat-model.md) güncellemesi, ADR | SEC + SA | Tasarım review |
| Geliştirme | Güvenli kodlama standardı, IDE eklentileri (Semgrep, SonarLint), pre-commit Gitleaks | Temiz commit | BE/FE/MOB | Pre-commit |
| Doğrulama (PR) | SAST, SCA, secret scan, IaC scan, lisans kontrolü, peer review (2 onay, güvenlik-hassas yollarda SEC CODEOWNER) | PR check'leri yeşil | CI + reviewer | PR merge |
| Build (main) | Container scan, SBOM, imzalama, provenance | İmzalı imaj + SBOM + attestation | CI | Registry push |
| Test | DAST (ZAP), API fuzzing, yetki matrisi testleri, cross-tenant testleri | Rapor | QA + SEC | UAT girişi |
| Release | Güvenlik release checklist, açık zafiyet kontrolü, pentest bulguları kapanışı | Release onayı | SEC | Prod promotion |
| Operasyon | Sürekli tarama (runtime), zafiyet yönetimi, bug bounty, IR | Bulgular, metrikler | SEC + OPS | — |

---

## 2. Otomatik Güvenlik Kapıları

| Kapı | Araç | Tetik | Kırma (Fail) Kriteri | Rapor Hedefi |
|---|---|---|---|---|
| **SAST** | Semgrep (OSS + özel kurallar) — hızlı; SonarQube (kalite + güvenlik hotspot) | Her PR | Yeni *High/Critical* bulgu; Sonar Quality Gate fail | PR yorumu, SARIF → GitHub Code Scanning |
| **SCA** | OWASP Dependency-Check (NVD) + Snyk (reachability, fix PR) | Her PR + günlük gece | CVSS ≥ 7.0 ve fix mevcut (yeni eklenen bağımlılıkta CVSS ≥ 4.0); yasaklı lisans (AGPL, SSPL, GPL — runtime) | Snyk dashboard, SARIF |
| **Secret scan** | Gitleaks (pre-commit + CI, tam geçmiş) + GitHub push protection | Her commit/PR | Herhangi bir bulgu (allowlist yalnızca SEC onayıyla) | PR block, SEC alarmı |
| **IaC scan** | Checkov (Helm, K8s manifest, Terraform, Dockerfile) + Kyverno CLI politika testi | IaC değişikliği olan PR | High bulgu; politika ihlali (privileged, root, hostPath, latest tag) | SARIF |
| **Container scan** | Trivy (OS + dil paketleri + misconfig + secret) | main build, gece yeniden tarama (registry) | Critical (fix mevcut) → fail; High → 7 gün istisna penceresi | Quay + DefectDojo |
| **SBOM** | CycloneDX (Maven plugin, `@cyclonedx/cyclonedx-npm`, Syft imaj SBOM) | main build | SBOM üretilemezse fail | Registry'de OCI attestation, Dependency-Track |
| **İmzalama** | Cosign (Sigstore) — keyless (GitHub OIDC → Fulcio) veya Vault/KMS anahtarı (air-gapped prod), SLSA provenance (in-toto) | Registry push | İmzasız imaj → admission reddi | Rekor transparency log |
| **DAST** | OWASP ZAP (baseline her deploy'da test ortamına; full + API scan OpenAPI ile gece) | test/uat deploy | High bulgu → release block | DefectDojo |
| **API fuzzing** | Schemathesis (OpenAPI tabanlı) | Gece | 5xx / şema ihlali | QA board |
| **Mobil** | MobSF (statik + dinamik), bağımlılık SCA | Mobil build | High → block | DefectDojo |

Tüm bulgular merkezi olarak **DefectDojo**'da toplanır (dedup, SLA takibi, risk kabulü iş akışı).

```yaml
# Snippet — PR güvenlik kapıları (özet; tam pipeline: devops-pipeline.md)
jobs:
  security:
    runs-on: ubuntu-latest
    permissions: { contents: read, security-events: write }
    steps:
      - uses: actions/checkout@<sha>        # tüm action'lar commit SHA ile pinlenir
        with: { fetch-depth: 0 }
      - name: Gitleaks
        uses: gitleaks/gitleaks-action@<sha>
      - name: Semgrep
        run: semgrep ci --config p/owasp-top-ten --config p/java --config .semgrep/aep-rules.yml --sarif -o semgrep.sarif
      - name: Dependency-Check
        run: ./mvnw -B org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=7
      - name: Checkov
        run: checkov -d deploy/ --framework helm,kubernetes,dockerfile --soft-fail false
      - uses: github/codeql-action/upload-sarif@<sha>
        with: { sarif_file: semgrep.sarif }
```

### 2.1 AEP-CLW'ye Özel Semgrep Kuralları (örnek katalog)

| Kural ID | Amaç |
|---|---|
| `aep.tenant.missing-context` | Repository çağrısı `TenantContext` doğrulaması olmadan |
| `aep.ledger.no-update-delete` | Ledger entity'lerinde `UPDATE`/`DELETE` sorgusu |
| `aep.money.no-double` | Parasal değerlerde `double`/`float` kullanımı (`BigDecimal`/`Money` zorunlu) |
| `aep.log.pii` | Logger çağrısında `phone`, `tckn`, `email`, `token`, `otp` alanları |
| `aep.idempotency.required` | Para hareketi endpoint'inde `Idempotency-Key` eksikliği |
| `aep.crypto.weak` | MD5/SHA1/ECB/`Random` kullanımı |
| `aep.authz.missing` | Controller metodunda `@PreAuthorize` eksik |

---

## 3. Tedarik Zinciri Güvenliği (SLSA)

- **Hedef: SLSA Build Level 3** — izole, ephemeral runner; imzalı provenance; kaynak ve build tanımı versiyonlu.
- Bağımlılıklar: private mirror (Nexus/Artifactory) üzerinden; Maven `dependencyLock`/checksum doğrulaması, npm `package-lock` + `npm ci --ignore-scripts` (izinli istisnalar hariç).
- GitHub Actions: third-party action'lar **commit SHA** ile pinli, `permissions:` varsayılan `read-all` → minimum, `pull_request_target` yasak, OpenSSF Scorecard ≥ 7.
- Base image: Red Hat UBI 9 minimal / distroless Java 21; haftalık yeniden build.
- Admission: prod ve preprod namespace'lerinde yalnızca `quay.io/aep-clw/*` + geçerli Cosign imzası + SBOM attestation'ı olan imajlar.

---

## 4. Manuel Güvenlik Faaliyetleri

### 4.1 Güvenlik Kod İncelemesi

Aşağıdaki yollar `CODEOWNERS` ile SEC şampiyonu/SEC onayı gerektirir: `**/security/**`, `**/ledger/**`, `**/crypto/**`,
Keycloak realm export'ları, Helm `networkpolicy`/`authorizationpolicy` şablonları, OPA politikaları, GitHub workflow dosyaları.

### 4.2 Pentest Planı

| Test | Kapsam | Zamanlama | Yapan | Standart |
|---|---|---|---|---|
| Web/API pentest | Gateway, BFF'ler, Public API, admin portal | MVP öncesi (S8 / M4) + yılda 1 + major release | Bağımsız CREST/OSCP sertifikalı firma | OWASP WSTG, ASVS L2 |
| Mobil pentest | White-label app (iOS/Android) | MVP öncesi + yılda 1 | Bağımsız firma | MASTG, MASVS L2+R |
| Multi-tenant izolasyon testi | Cross-tenant senaryoları | MVP öncesi + tenant tier değişikliği | Bağımsız firma + iç ekip | Özel senaryo seti |
| İş mantığı / finansal test | Çifte harcama, replay, yarış koşulu, kampanya istismarı | MVP öncesi + yılda 1 | Ödeme sistemleri uzmanı firma | Özel |
| Altyapı / OpenShift | Cluster, mesh, CI/CD | Yılda 1 | Bağımsız firma | CIS Benchmark, K8s pentest |
| Red team (hedefli) | Sosyal mühendislik, insider senaryosu | 2. yıl itibarıyla yılda 1 | Bağımsız | TIBER-benzeri |
| **BDDK/regülatif** | Lisans durumuna göre (bkz. regulatory-framework) | Regülasyon gereği | Yetkili firma | İlgili yönetmelik |

Bulgular DefectDojo'ya aktarılır, zafiyet SLA'larına tabidir; kritik/yüksek bulgular kapanmadan prod release yapılmaz.
Retest raporu kanıt olarak kontrol matrisine eklenir (CTL-044).

### 4.3 Bug Bounty

- **Faz 1 (MVP + 3 ay)**: Özel program (davetli araştırmacılar), platform: HackerOne/Intigriti veya yerel (ör. Bugbounter).
- **Faz 2 (GA + 6 ay)**: Public program.
- Kapsam: public API, mobil app, portallar; kapsam dışı: DoS, sosyal mühendislik, üçüncü taraf PSP.
- Ödül bandı (öneri): Kritik 3.000–10.000 USD, Yüksek 1.000–3.000, Orta 250–1.000, Düşük 100.
- `security.txt` (RFC 9116) ve Responsible Disclosure politikası yayınlanır.

---

## 5. Güvenlik Şampiyonları Programı

- Her takımda (backend squad'ları, frontend, mobil, DevOps) **1 şampiyon**; zamanının ~%10'u.
- Sorumluluklar: threat modeling oturumlarına katılım, güvenlik-hassas PR review, Semgrep kural önerileri, takım içi farkındalık.
- Eğitim: OWASP Top 10 / API Top 10, güvenli Java/Spring, React güvenliği, mobil güvenlik; yılda 1 CTF / secure code warrior benzeri.
- Aylık şampiyon toplantısı (SEC liderliğinde); metrikler: MTTR, tekrar eden bulgu tipleri.
- Tüm geliştiriciler için yıllık zorunlu güvenlik eğitimi + KVKK farkındalık (CTL-045).

---

## 6. Zafiyet Yönetimi ve SLA'lar

| Severity | CVSS v3.1/v4 | Örnek | Düzeltme SLA (prod) | İstisna Onayı |
|---|---|---|---|---|
| **Critical** | 9.0–10.0 veya aktif istismar (CISA KEV) | RCE, auth bypass, cross-tenant veri erişimi, bakiye manipülasyonu | **72 saat** (geçici önlem 24 saat) | CISO + Program Direktörü |
| **High** | 7.0–8.9 | Stored XSS admin portal, IDOR (tek tenant içi) | **7 gün** | CISO |
| **Medium** | 4.0–6.9 | CSRF düşük etkili, bilgi ifşası | **30 gün** | SEC şampiyonu + Tech Lead |
| **Low** | 0.1–3.9 | Eksik güvenlik başlığı | **90 gün** | Tech Lead |

- SLA, bulgu **doğrulandığı** anda başlar. İş etkisine göre (finansal akış, PII) severity bir üst seviyeye çıkarılabilir.
- SLA ihlali → otomatik eskalasyon (DefectDojo → Slack/Teams → CISO); sprint review'da "açık zafiyet" metriği raporlanır.
- Risk kabulü süreli (maks 90 gün), telafi edici kontrol zorunlu, kontrol matrisine kayıt.

### 6.1 Metrikler (KPI)

| Metrik | Hedef |
|---|---|
| Critical/High MTTR | < 3 gün / < 7 gün |
| SLA uyum oranı | ≥ %95 |
| PR'larda güvenlik kapısı yeşil oranı (ilk seferde) | ≥ %85 |
| Açık Critical zafiyet (prod) | 0 |
| İmzalı ve SBOM'lu prod imaj oranı | %100 |
| Threat model güncelliği (yeni servis için) | %100 |
