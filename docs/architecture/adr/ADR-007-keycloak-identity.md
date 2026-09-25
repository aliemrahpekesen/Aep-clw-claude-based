# ADR-007: Kimlik ve Erişim Yönetimi için Keycloak (OIDC/OAuth2)

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, `SEC`, Backend Tech Lead
- **İlgili:** [multitenancy.md §2](../multitenancy.md), [service-catalog.md §2](../service-catalog.md)

## Context and Problem Statement

Dört farklı kimlik popülasyonu var: son kullanıcılar (telefon OTP, cihaz bağlama), kasiyerler/terminaller, tenant adminleri
(MFA), platform operatörleri. Multitenant, white-label (tenant markalı login), self-hosted (veri yerelliği), standart protokoller
(OIDC, OAuth2 client credentials, token exchange), MFA ve denetim gerekiyor.

## Decision Drivers

- Veri yerelliği (TR) → self-hosted
- Multitenancy: tenant başına tema, IdP ayarı, rol seti
- Telefon OTP + cihaz bağlama gibi özel akışlar için genişletilebilirlik
- OpenShift üzerinde operator ve Red Hat desteği (Red Hat build of Keycloak)
- Maliyet (kullanıcı başına lisans olmamalı — milyonlarca son kullanıcı)

## Considered Options

1. **Keycloak** (Red Hat build of Keycloak), realm-per-platform + **Organizations** = tenant
2. Keycloak realm-per-tenant
3. Auth0 / Okta CIAM (SaaS)
4. Kendi geliştirdiğimiz auth servisi (Spring Authorization Server)

## Decision Outcome

**Seçilen: Seçenek 1.**

| Realm | Kullanıcılar | Not |
|---|---|---|
| `clw-customers` | Son kullanıcılar (tüm tenant'lar); **Organization = tenant** | Custom authenticator SPI: telefon OTP (identity-service'e delege), cihaz bağlama; DPoP-bound token; login teması tenant'a göre (organization/`kc_org` hint) |
| `clw-business` | Tenant adminleri, kasiyerler, merchant kullanıcıları; Organization = tenant | MFA (WebAuthn/TOTP) zorunlu admin rollerinde; tenant SSO (kurumsal IdP federasyonu — Azure AD/Google) opsiyonel |
| `clw-platform` | Platform operatörleri, denetçiler | MFA zorunlu, IP kısıtı, kısa oturum |
| (client'lar) | POS terminalleri, servisler | `client_credentials`; terminal client'ları merchant-service tarafından Admin API ile oluşturulur |

- Token içeriği: `sub`, `tenant_id`, `org`, `actor_type` (CUSTOMER/CASHIER/ADMIN/PLATFORM/SERVICE/TERMINAL), `scope`, `merchant_id`/`store_id`/`terminal_id` (kapsam), `acr` (step-up), `cnf` (DPoP).
- Access token ömrü: müşteri 5 dk, admin 10 dk, terminal 15 dk; refresh token rotation + reuse detection.
- Servisler JWT'yi yerel doğrular (JWKS cache); Keycloak ödeme sıcak yolunda değil.
- Keycloak HA: 3+ replica, Infinispan cluster, PostgreSQL arka uç (ayrı cluster), ayrı SLO; kullanıcı sayısı büyüdükçe realm-per-stamp.
- Organizations özelliği (Keycloak 25+ GA) kullanılamazsa fallback: kullanıcı attribute `tenant_id` + grup hiyerarşisi.

### Consequences

- **Olumlu:** Standart protokoller, self-hosted, lisans maliyeti yok, genişletilebilir SPI, Red Hat desteği, tenant teması.
- **Olumsuz:** Keycloak operasyonu (upgrade, cache, DB) ekip sorumluluğunda; custom SPI bakımı (upgrade uyumluluğu); milyon+ kullanıcıda performans ayarı (user storage, session limitleri) — yük testi Sprint 3.
- **Kural:** Keycloak'a özel kod yalnız `identity-service` (Admin API adaptörü) ve SPI modülünde; diğer servisler yalnız standart JWT görür (ACL).

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **Keycloak + Organizations** | Tek realm yönetimi, tenant ölçeklenebilir | Organizations görece yeni özellik |
| Realm-per-tenant | Güçlü izolasyon | Binlerce realm → Keycloak performans/yönetim sorunları |
| Auth0/Okta | Yönetilen, zengin | Veri yerelliği, kullanıcı başı maliyet (milyonlarca MAU), vendor lock-in |
| Kendi auth servisi | Tam kontrol | Güvenlik riski, MFA/federasyon/admin UI yeniden yazımı |
