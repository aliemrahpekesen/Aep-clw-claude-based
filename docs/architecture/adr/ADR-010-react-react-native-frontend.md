# ADR-010: Web için React + TypeScript, Mobil için React Native (Expo) White-Label

- **Status:** Proposed
- **Tarih:** 2026-09-25
- **Karar vericiler:** `CA`, Frontend Tech Lead, Mobile Lead, `UX`
- **İlgili:** [architecture-overview.md §2.1](../architecture-overview.md), [multitenancy.md §7, §10](../multitenancy.md)

## Context and Problem Statement

Kanallar: white-label müşteri mobil uygulaması (her tenant kendi mağaza listelemesiyle), Tenant Admin Portalı, Platform Admin
Konsolu, Web POS. Tenant temalama (renk, logo, font, dil), hızlı özellik teslimi, küçük ekip (2 FE + 2 MOB), kod paylaşımı
ve güvenlik (cihaz bağlama, secure storage, attestation) gereksinimleri var.

## Decision Drivers

- Tek dil/ekosistem (TypeScript) ile web ve mobil arasında kod paylaşımı (API client, validation, i18n, design token)
- White-label build otomasyonu (tenant başına ayrı bundle id, ikon, tema)
- Native güvenlik yetenekleri (Keystore/Secure Enclave, biyometri, Play Integrity/App Attest, FLAG_SECURE)
- OTA güncelleme ihtiyacı (kritik UI düzeltmeleri) — mağaza kurallarına uygun
- Ekip büyüklüğü

## Considered Options

- **Web:** React 18 + TS + Vite · Angular · Next.js (SSR)
- **Mobil:** React Native (Expo) · Flutter · Native (Swift + Kotlin) · PWA

## Decision Outcome

**Seçilen: Web → React 18 + TypeScript + Vite (SPA); Mobil → React Native + Expo (EAS Build, config plugins).**

Web:
- TanStack Query (sunucu durumu), React Router, React Hook Form + Zod (OpenAPI'den türetilen şemalar), i18next, OpenAPI'den üretilen TS client.
- **Design System** (`packages/design-system`): design token'lar (tenant temalı CSS variables), erişilebilirlik WCAG 2.1 AA, Storybook.
- Admin portalda SSR gerekmez (kimlik doğrulamalı SPA); SEO ihtiyacı yok → Next.js karmaşıklığı gereksiz.
- Web POS: kamera ile QR okuma (`BarcodeDetector` / ZXing fallback), kiosk modu, düşük bant genişliği optimizasyonu.

Mobil:
- Expo SDK (managed + config plugins), **EAS Build** ile tenant başına build: `app.config.ts` tenant parametrelerini (bundle id, isim, ikon, splash, renkler, Keycloak org, API base URL) CI'dan alır.
- Güvenlik: `expo-secure-store` / native modül ile Keystore/Secure Enclave anahtarları (cihaz bağlama, QR TOTP seed), biyometri (`expo-local-authentication`), root/jailbreak tespiti, Play Integrity / App Attest (native modül), certificate pinning, screenshot engelleme.
- **OTA (EAS Update)**: yalnız JS/asset düzeltmeleri, mağaza politikalarına uygun; güvenlik-kritik kod (QR token, kripto) native modülde ve OTA ile değiştirilemez; OTA paketleri imzalı (code signing).
- Ortak paketler (`packages/api-client`, `packages/i18n`, `packages/design-tokens`, `packages/validation`) web ve mobil arasında paylaşılır.

### Consequences

- **Olumlu:** Tek dil, paylaşılan paketler, küçük ekiple 4 kanal; white-label otomasyonu; hızlı iterasyon.
- **Olumsuz:** RN'de ağır animasyon/performans kritik ekranlarda native'e göre sınırlar (cüzdan uygulaması için kabul edilebilir); native modül bakımı (attestation, HCE/NFC — v2) gerekir; tenant başına mağaza hesabı/listeleme operasyonu (tenant'ın kendi developer hesabı veya platform hesabı — sözleşme konusu).
- **NFC-HCE ödeme** (charter kapsamında) Android'de native modül ile v2'de; iOS'ta HCE kısıtları nedeniyle QR birincil.

## Pros and Cons of the Options

| Seçenek | Artı | Eksi |
|---|---|---|
| **React + Vite** | Ekosistem, ekip yetkinliği, RN ile paylaşım | Mimari disiplini ekip sağlamalı |
| Angular | Yapılandırılmış | RN ile paylaşım yok |
| Next.js | SSR/SEO | İhtiyaç yok, sunucu bileşeni karmaşıklığı |
| **React Native (Expo)** | Kod paylaşımı, EAS white-label, OTA | Native modül ihtiyacı |
| Flutter | Performans, tutarlı UI | Dart — web ekibiyle paylaşım yok |
| Native ×2 | En iyi performans/erişim | İki kod tabanı, ekip ×2 |
| PWA | Kurulum yok | iOS kısıtları (push, biyometri, secure storage), mağaza varlığı yok |
