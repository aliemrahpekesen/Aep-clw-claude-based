# Güvenlik (Security) — Doküman İndeksi

Sahip: `SEC` (CISO / Security Architect) · Bağlam: [Proje Tüzüğü](../00-project-charter.md)

| Doküman | İçerik |
|---|---|
| [security-architecture.md](security-architecture.md) | Zero trust, defense-in-depth, Keycloak/OIDC PKCE/MFA/step-up, mTLS + JWT audience, RBAC/ABAC rol modeli, maker-checker, Vault, şifreleme & crypto-shredding, QR/token güvenliği, MASVS L2, OWASP API Top 10, PII maskeleme, tenant izolasyonu |
| [threat-model.md](threat-model.md) | STRIDE tehdit modeli: varlıklar, aktörler, güven sınırları (DFD), 42 tehdit (çifte harcama, replay, yarış koşulu, tenant sızıntısı, insider fraud, webhook sahteciliği, ATO), saldırı ağaçları |
| [secure-sdlc.md](secure-sdlc.md) | Güvenlik kapıları (Semgrep, SonarQube, Dependency-Check/Snyk, Gitleaks, Checkov, Trivy, ZAP, CycloneDX, Cosign), SLSA, pentest planı, bug bounty, güvenlik şampiyonları, zafiyet SLA'ları |
| [incident-response.md](incident-response.md) | Olay müdahale planı, severity/kategori, KVKK 72 saat bildirimi, 10 playbook, tatbikatlar |

İlgili: [Uyum](../compliance/README.md) · [Kontrol Matrisi](../compliance/control-matrix.md) · [DevOps](../devops/README.md) · [Kalite](../quality/README.md)
