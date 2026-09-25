# DevOps / SRE — Doküman İndeksi

Sahip: `OPS` (DevOps/SRE Lead) · Bağlam: [Proje Tüzüğü](../00-project-charter.md)

| Doküman | İçerik |
|---|---|
| [devops-pipeline.md](devops-pipeline.md) | GitHub Actions PR/main pipeline'ları (build, test, SAST/SCA/secret, Jib, Trivy, SBOM, Cosign, Quay), ArgoCD app-of-apps + PR tabanlı promotion (dev→test→uat→preprod→prod), Argo Rollouts canary + analiz, feature flag, Flyway expand-contract, rollback, SemVer/Conventional Commits; mermaid diyagram ve YAML snippet'leri |
| [openshift-platform.md](openshift-platform.md) | Cluster topolojisi, namespace-per-environment, Helm library chart, kaynak limitleri, HPA/KEDA (Kafka lag), PDB, default-deny NetworkPolicy, SCC/Kyverno/ACS, Service Mesh, Routes, Strimzi Kafka, CloudNativePG/Crunchy, Redis, Vault injector, ölçek ve maliyet |
| [observability.md](observability.md) | OpenTelemetry, RED/USE + iş metrikleri (TPS, top-up başarı oranı, ledger dengesizliği = 0 alarmı), Loki (JSON, PII maskeleme), Tempo, 15 dashboard, SLO/SLI + error budget, alarm politikası, on-call |
| [environments-and-dr.md](environments-and-dr.md) | Ortamlar, local docker-compose (postgres, kafka, keycloak, redis, mailhog, wiremock), DR (multi-AZ, cross-region, RPO ≤ 1 dk / RTO ≤ 15 dk), yedekleme, tatbikatlar, 26 runbook |

İlgili: [Güvenlik](../security/README.md) · [Uyum](../compliance/README.md) · [Kalite](../quality/README.md)
