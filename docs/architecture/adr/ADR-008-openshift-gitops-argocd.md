# ADR-008: OpenShift 4.x + Helm + GitOps (ArgoCD)

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `OPS`, `SEC`
- **İlgili:** [architecture-overview.md §7–8](../architecture-overview.md)

## Context and Problem Statement

19 servis + veri altyapısı (PostgreSQL, Kafka, Redis, ClickHouse, Keycloak, Vault) çok ortamlı (dev, test, staging, prod, DR)
ve çok bölgeli çalışacak. Hedef müşteri profili (bankalar, büyük perakende) ve regülasyon on-prem / yerli bulut seçeneğini gerekli kılıyor.
Konteyner platformu ve dağıtım modeli seçilmelidir.

## Decision Drivers

- On-prem / TR yerli bulut / hyperscaler taşınabilirliği
- Kurumsal destek, güvenlik sertleştirmesi (SCC, non-root), sertifikalı operatörler (Strimzi/AMQ Streams, CNPG/Crunchy, Keycloak)
- Denetlenebilir, geri alınabilir dağıtım (değişiklik yönetimi — denetim gereği)
- Service mesh (mTLS), gözlemlenebilirlik entegrasyonu

## Considered Options

1. **OpenShift 4.x + Helm + ArgoCD (OpenShift GitOps)**
2. Vanilla Kubernetes (RKE2 / EKS / AKS) + Helm + ArgoCD
3. OpenShift + Tekton ile push-based CD
4. VM tabanlı dağıtım (Ansible)

## Decision Outcome

**Seçilen: Seçenek 1.**

- **Helm**: servis başına chart yerine **ortak library chart** (`charts/clw-service`) + servis `values` dosyaları (Deployment, Service, HPA/KEDA ScaledObject, PDB, NetworkPolicy, ServiceMonitor, Vault annotations, PeerAuthentication).
- **GitOps repo** (`deploy/` monorepo içinde veya ayrı `aep-clw-gitops` repo — ADR-011'e bağlı): ortam overlay'leri `envs/{dev,test,staging,prod-tr1,dr-tr2}`; ArgoCD **ApplicationSet** (servis × ortam matrisi); prod senkronizasyonu **manuel onaylı** (sync window + PR approval = değişiklik kaydı).
- CI (GitHub Actions) yalnız imaj üretir, imzalar (cosign), SBOM ekler ve GitOps repo'ya **image tag PR**'ı açar; cluster'a doğrudan erişimi yoktur (pull-based).
- Progressive delivery: **Argo Rollouts** canary (%5 → %25 → %100) + Prometheus analiz (hata oranı, p99) — Tier-0 servislerde zorunlu.
- **OpenShift Service Mesh** (Istio tabanlı) mTLS STRICT; egress gateway harici sistemler için.
- Güvenlik: `restricted-v2` SCC, imza doğrulama (policy controller), NetworkPolicy default-deny, Vault Agent/CSI.
- Veri altyapısı operatörleri de GitOps ile yönetilir (CNPG `Cluster`, Strimzi `Kafka`/`KafkaTopic`/`KafkaUser`, ClickHouse operator CR'ları).

### Consequences

- **Olumlu:** Tüm değişiklikler Git'te (denetim izi, maker-checker = PR onayı), kolay rollback (git revert), ortam drift tespiti, DR cluster'ı aynı manifest'lerle; sertifikalı operatör ekosistemi.
- **Olumsuz:** OpenShift lisans maliyeti; platform ekibi yetkinlik gereksinimi; Service Mesh gecikme eklentisi (~1–3 ms/hop) — gecikme bütçesinde hesaplandı.
- **Kural:** Prod'a `oc apply`/`kubectl edit` yasak (break-glass hariç, audit'li); drift ArgoCD tarafından self-heal.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **OpenShift + ArgoCD** | Kurumsal destek, güvenlik varsayılanları, operatörler, taşınabilir | Lisans |
| Vanilla K8s | Maliyet, esneklik | Güvenlik sertleştirme ve entegrasyon ekip yükü; müşteri kurumsal tercihleri |
| Push-based CD (Tekton) | Tek pipeline | CI'ın cluster kimlik bilgisi (saldırı yüzeyi), drift tespiti yok |
| VM + Ansible | Tanıdık | Ölçekleme, self-healing, yoğunluk; 19 servis için sürdürülemez |
