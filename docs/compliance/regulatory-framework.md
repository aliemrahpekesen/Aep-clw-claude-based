# AEP-CLW — Regülasyon Çerçevesi (Regulatory Framework)

| Alan | Değer |
|---|---|
| Doküman sahibi | `CMP` (Compliance & Risk Officer) |
| Katkı | `SEC`, `AUD`, `SA`, `PO`, Hukuk |
| Sürüm | v1.0 — Sprint 0 |
| Gözden geçirme | 6 ayda bir + her mevzuat değişikliğinde + yeni ülke/tenant segmenti öncesi |

> **UYARI — Hukuki Görüş Değildir.** Bu doküman, ürün ve mimari kararlara girdi sağlamak amacıyla hazırlanmış bir **uyum
> ön değerlendirmesidir**; hukuki görüş, mütalaa veya regülatör teyidi yerine geçmez. Mevzuat atıfları, eşik ve süreler
> değişebilir; özellikle **6493 sayılı Kanun kapsamında sınırlı ağ (kapalı devre) istisnasının uygulanabilirliği**,
> lisans gereksinimi ve MASAK yükümlülük statüsü, canlıya geçiş öncesinde **ödeme hukuku alanında uzman bir hukuk bürosu**
> tarafından yazılı olarak teyit edilmeli, gerekli görülürse **TCMB'den görüş** alınmalıdır.

---

## 1. Özet Değerlendirme

| Soru | Kısa Yanıt |
|---|---|
| AEP-CLW (platform) bir ödeme/e-para kuruluşu mu? | **Tasarım hedefi: Hayır.** Platform, tenant'lara teknoloji hizmeti (SaaS) veren **teknik hizmet sağlayıcı** olarak konumlanır; fonları **tutmaz**, fon akışı tenant'ın (ve/veya lisanslı iş ortağının) hesaplarında gerçekleşir. Bu konumlandırma sözleşme ve fon akış mimarisiyle desteklenmelidir. |
| Tenant'ın ön ödemeli cüzdanı e-para mı? | Değer yalnızca **tenant'ın kendi işyerlerinde veya tenant ile ticari anlaşması olan sınırlı bir ağda**, sınırlı mal/hizmet için kullanılıyorsa **kapalı devre istisnası** değerlendirilebilir. Aksi halde e-para ihracı → **TCMB lisansı** veya lisanslı e-para kuruluşu ile iş birliği gerekir. |
| MASAK yükümlüsü kim? | İstisna kapsamındaki kapalı devre yapıda tenant/platform genellikle 5549 kapsamında "yükümlü" sayılmayabilir; ancak **risk temelli yaklaşım** gereği AML/KYC kontrolleri ürün içinde **varsayılan açık** tasarlanır. Lisanslı model (TCMB) seçilirse tam yükümlülük doğar. |
| PCI-DSS kapsamı | Kart verisi sisteme girmez (PSP hosted/iframe/SDK) → hedef **SAQ A** (tenant web kanalı). Platformun servis sağlayıcı rolü ve mobil SDK akışı QSA ile teyit edilecek. |
| KVKK/GDPR rolü | Müşteri verileri için genellikle **tenant = veri sorumlusu**, **AEP-CLW = veri işleyen**; platform kendi workforce/tenant irtibat verileri için veri sorumlusu. |

---

## 2. Türkiye — 6493 Sayılı Kanun ve Kapalı Devre (Sınırlı Ağ) İstisnası

### 2.1 Mevzuat

- **6493 sayılı** Ödeme ve Menkul Kıymet Mutabakat Sistemleri, Ödeme Hizmetleri ve Elektronik Para Kuruluşları Hakkında Kanun (yetkili otorite: 7192 sayılı Kanun ile 2020 itibarıyla **TCMB**).
- **Ödeme Hizmetleri ve Elektronik Para İhracı ile Ödeme Hizmeti Sağlayıcıları Hakkında Yönetmelik** (TCMB, 2021).
- **Ödeme Hizmeti Sağlayıcılarının Bilgi Sistemleri ile Ödeme Hizmetleri Alanındaki Veri Paylaşım Servislerine İlişkin Yönetmelik** (TCMB, 2021).
- Kanun'un kapsam dışı işlemler hükmü: yalnızca ihraççının işyerlerinde veya ihraççı ile ticari anlaşması olan **sınırlı bir hizmet sağlayıcı ağı** içinde ya da **sınırlı çeşitte mal/hizmet** alımında kullanılabilen ödeme araçlarına dayanan hizmetler.

### 2.2 İstisna Değerlendirme Kriterleri (ürün kontrol listesi)

| # | Kriter | Kapalı devre ile uyumlu | İstisnayı riske atan tasarım | Ürün Kontrolü |
|---|---|---|---|---|
| K1 | Kabul noktası | Yalnızca tenant'ın kendi mağazaları / franchise'ları / sözleşmeli sınırlı ağ | Açık ağ, herhangi bir işyerinde kabul, diğer tenant'larda harcama | **Tenant'lar arası harcama teknik olarak imkânsız** (ledger tenant izolasyonu); işyeri ağı tenant sözleşmesiyle sınırlı |
| K2 | Mal/hizmet çeşidi | Tenant'ın markası altında sınırlı ürün yelpazesi | Genel amaçlı alışveriş | Tenant onboarding'de faaliyet alanı beyanı |
| K3 | Nakde çevrilebilirlik | Bakiye nakit olarak çekilemez (yalnızca mevzuat gereği iade) | ATM/nakit çekim, serbest para iadesi | Cash-out özelliği **yok**; hesap kapatmada iade yalnızca kaynak ödeme aracına + maker-checker |
| K4 | P2P transfer | Yok veya aynı tenant içinde, düşük limitli hediye | Serbest P2P, kişiler arası para transferi | P2P **feature flag, varsayılan kapalı**; açılırsa hukuk onayı şartı + limit |
| K5 | Üçüncü taraf ödeme | Yok | Fatura ödeme, başka firmalara ödeme | Kapsam dışı |
| K6 | Hacim | Sınırlı ağ ölçeğiyle orantılı | Çok büyük hacim, ulusal açık ağ | Tenant bazlı hacim izleme raporu (AB PSD2 eşiği referansıyla, bkz. §5) |
| K7 | Fon koruması | Tenant'ın bilançosunda müşteri avansı/yükümlülük | — | Ledger'da müşteri yükümlülük hesapları + günlük fon mutabakatı (CTL-035) |

### 2.3 Ne Zaman E-Para Lisansı (TCMB) Gerekir?

Aşağıdakilerden **herhangi biri** gerçekleşirse hizmet büyük olasılıkla e-para ihracı / ödeme hizmeti sayılır ve **TCMB
lisansı** (e-para kuruluşu / ödeme kuruluşu) veya lisanslı bir kuruluşla **ihraççı-ajan/iş birliği modeli** gerekir:

1. Birden fazla bağımsız markada (tenant'lar arası veya geniş koalisyon) harcanabilen ortak cüzdan / ortak puan-para.
2. Bakiyenin nakde çevrilmesi, banka hesabına transfer, serbest P2P.
3. Tenant'ın sınırlı ağı dışındaki işyerlerinde kabul (ör. kampüs kartıyla şehirdeki herhangi bir kafede).
4. Platformun (AEP-CLW'nin) müşteri fonlarını kendi hesabında toplaması (pooled account) — **platform açısından** ödeme hizmeti riski.
5. Ön ödemeli kart şeması (Visa/Mastercard ön ödemeli kart) ile birleştirme.

**Mimari karşılık**: `tenant.regulatory_model ∈ {CLOSED_LOOP_EXEMPT, LICENSED_PARTNER, SELF_LICENSED}` konfigürasyonu;
model, özellik bayraklarını (P2P, cash-out, çoklu marka) ve limit tavanlarını belirler. Model değişikliği platform
admin + CMP maker-checker'ı gerektirir.

### 2.4 Lisanslı Model Seçilirse Ek Gereksinimler (özet)

Fon koruma (safeguarding — ayrı hesap / teminat), özkaynak, bağımsız denetim, bilgi sistemleri denetimi,
**birincil ve ikincil sistemlerin yurt içinde** bulundurulması, TCMB raporlamaları, şikâyet yönetimi, dış hizmet alımı
kuralları, MASAK tam yükümlülük. AEP-CLW mimarisi bu gereksinimleri **karşılayabilecek şekilde** tasarlanır (TR bölge
hosting, audit, raporlama altyapısı) — detay ayrı gap analizi ile.

---

## 3. MASAK — 5549 Sayılı Kanun

| Konu | Gereklilik | Sistem Karşılığı |
|---|---|---|
| Müşteri tanıma (KYC) | Kimlik tespiti, gerçek faydalanıcı, risk temelli yaklaşım; uzaktan kimlik tespitine ilişkin MASAK düzenlemeleri | KYC seviyeleri (Tier 0–3), NFC çipli kimlik okuma + canlılık testi — [aml-kyc-policy.md](aml-kyc-policy.md) |
| Şüpheli işlem bildirimi (STR) | Şüphenin oluştuğu tarihten itibaren **en geç 10 iş günü** (gecikmesinde sakınca olan hallerde derhal) | compliance-service vaka yönetimi, SLA sayacı, STR hazırlama iş akışı |
| Bildirim yapıldığının ifşa yasağı (tipping-off) | STR bilgisi taraflara verilemez | AML vakaları yalnızca `COMPLIANCE_OFFICER` görür; support ekranında görünmez |
| Kayıt saklama | Belge ve kayıtlar **8 yıl** | Ledger + KYC kayıtları retention policy; WORM arşiv |
| Yaptırım / malvarlığı dondurma | 6415 ve 7262 sayılı Kanunlar kapsamında listeler (BM, ulusal) | Onboarding + günlük yeniden tarama, eşleşmede otomatik dondurma + inceleme |
| Uyum programı | Eğitim, iç denetim, izleme-kontrol, uyum görevlisi | Yükümlülük statüsüne göre; ürün raporları hazır |

---

## 4. KVKK (6698) ve GDPR

| Konu | KVKK | GDPR | Sistem Karşılığı |
|---|---|---|---|
| Hukuki sebep & aydınlatma | md.4–5, md.10 | Art.6, 13–14 | Onay/aydınlatma metni versiyonlama, kanıt (timestamp, versiyon, kanal) — customer-service |
| Açık rıza (pazarlama) | md.5/1 | Art.7 | Granüler rıza, geri çekme; İYS (İleti Yönetim Sistemi) entegrasyonu (ticari elektronik ileti) |
| Özel nitelikli veri | md.6 (biyometrik) | Art.9 | Selfie/liveness biyometrik verisi: açık rıza, ayrı şifreleme anahtarı, KYC sağlayıcısında kısa saklama |
| İlgili kişi hakları | md.11 (30 gün) | Art.15–22 (1 ay) | Self-service veri indirme, silme talebi iş akışı, crypto-shredding |
| Veri güvenliği | md.12 | Art.32 | [security-architecture.md](../security/security-architecture.md) |
| İhlal bildirimi | 72 saat (Kurul kararı) | 72 saat (Art.33) | [incident-response.md](../security/incident-response.md) |
| Yurt dışı aktarım | md.9 (2024 değişikliği: yeterlilik, standart sözleşme + Kurum'a bildirim, BCR) | Chapter V (SCC, adequacy) | Varsayılan **TR veri yerelliği**; AB tenant'ları için AB bölgesi; alt işleyen listesi |
| VERBİS | Kayıt yükümlülüğü (eşiklere göre) | ROPA (Art.30) | İşleme envanteri dokümanı |
| DPIA | Önerilir | Art.35 (zorunlu durumlar) | Yüksek riskli işlemler (fraud profilleme, biyometrik) için DPIA |
| Otomatik karar | md.11/1-g (itiraz) | Art.22 | Fraud red kararlarına insan incelemesi itiraz kanalı |

---

## 5. AB — PSD2 / EMD2 (AB tenant'ları için)

- **PSD2 Art.3(k) — Limited Network Exclusion (LNE)**: Yalnızca ihraççının tesislerinde veya sınırlı bir hizmet sağlayıcı ağında / çok sınırlı mal-hizmet yelpazesinde kullanılan araçlar. EBA Kılavuzu (EBA/GL/2022/02) kriterleri: sınırlı ağ, ortak marka/marka sözleşmesi, coğrafi sınır, ürün sınırlılığı.
- **PSD2 Art.37(2)**: Son 12 ayda işlem toplamı **1 milyon EUR'yu aşan** LNE faaliyetleri için yetkili otoriteye **bildirim** yükümlülüğü → Sistem: tenant bazlı 12 aylık kayan toplam raporu + %80 eşik uyarısı.
- **EMD2 Art.1(4)**: LNE kapsamındaki araçlarda saklanan değer e-para sayılmaz.
- **PSD3 / PSR** (yasama sürecinde): LNE kriterlerinin daraltılması bekleniyor → yıllık yeniden değerlendirme.
- **SCA**: LNE kapsamında zorunlu değil; ancak kart ile yükleme işlemleri PSP/issuer tarafında 3DS2/SCA'ya tabidir.
- **AMLR / 6AMLD**, **DORA** (lisanslı modelde ICT risk yönetimi) — izleme listesinde.

---

## 6. PCI-DSS v4.0.x — Kapsam Daraltma

| Unsur | Tasarım | Etki |
|---|---|---|
| Kart verisi girişi (web) | PSP **hosted payment page / iframe** (tüm kart alanları PSP domain'inde) | **SAQ A** uygunluğu |
| Kart verisi girişi (mobil) | PSP native SDK doğrudan PSP'ye gönderir; uygulama kart verisini işlemez/loglamaz | SAQ A/A-EP sınırı → **QSA teyidi** gerekli |
| Kayıtlı kart | PSP token (network token tercihen), maskeli PAN | Kapsam dışı (token PCI kapsamı dışında, detokenizasyon yok) |
| Ödeme sayfası script bütünlüğü | CSP, SRI, ödeme sayfasının statik ve imzalı dağıtımı | SAQ A (2025 revizyonu) uygunluk kriteri: sayfanın script tabanlı saldırılara karşı korunduğunun teyidi |
| Platform servis sağlayıcı rolü | Tenant'ların kart akışını etkileyebilen bileşen (ödeme sayfası barındırma) | Servis sağlayıcı AOC gerekebilir → QSA ile scoping workshop (Sprint 2) |
| Segmentasyon | funding-service ve ödeme sayfası ayrı namespace + NetworkPolicy | Kapsam sınırlama kanıtı |

---

## 7. BDDK Bilgi Sistemleri İlkeleri (En İyi Uygulama Referansı)

"Bankaların Bilgi Sistemleri ve Elektronik Bankacılık Hizmetleri Hakkında Yönetmelik" doğrudan bankalara uygulanır; AEP-CLW
bu yönetmeliği ve TCMB'nin ödeme hizmeti sağlayıcıları için bilgi sistemleri yönetmeliğini **hedef olgunluk çerçevesi**
olarak alır (banka/lisanslı tenant'lara dış hizmet sağlarken beklenen seviye):

| İlke | Sistem Karşılığı |
|---|---|
| BS yönetişimi, BS stratejisi, risk yönetimi | Güvenlik politika seti, risk register, kontrol matrisi |
| Kimlik doğrulama, iki bileşenli doğrulama, işlem güvenliği | MFA, step-up, cihaz bağlama |
| İz kayıtları (audit trail), değiştirilemezlik, erişim | Hash-zincirli audit log, WORM |
| Birincil/ikincil sistemlerin yurt içinde bulunması | TR bölge hosting (lisanslı/banka tenant'ları için zorunlu kabul) |
| İş sürekliliği, felaket kurtarma, tatbikat | RPO ≤ 1 dk / RTO ≤ 15 dk, yıllık DR tatbikatı |
| Dış hizmet alımı (outsourcing) | Tedarikçi risk değerlendirmesi, sözleşme hükümleri, denetim hakkı |
| Sızma testleri, bağımsız denetim | Yıllık pentest, BS denetimi |
| Değişiklik yönetimi, görevler ayrılığı | GitOps, PR review, SoD matrisi |

---

## 8. Standartlar ve Güvence Raporları

| Çerçeve | Hedef | Zaman Çizelgesi |
|---|---|---|
| **ISO/IEC 27001:2022** | ISMS sertifikasyonu; Annex A 93 kontrol → kontrol matrisi eşlemesi; ISO 27017/27018 (bulut/PII) ek | GA + 9–12 ay |
| **ISO 22301** | İş sürekliliği (opsiyonel) | 2. yıl |
| **SOC 2 Type II** | Security, Availability, Confidentiality, Processing Integrity (TSC) — gözlem periyodu 6→12 ay | Type I: GA + 6 ay; Type II: GA + 12–15 ay |
| **ISAE 3402 / SOC 1** | Finansal raporlama kontrolleri (tenant denetçileri için) | Talebe göre |
| **PCI-DSS** | SAQ A (+ gerekirse servis sağlayıcı AOC) | MVP öncesi |

---

## 9. Vergi ve Muhasebe — e-Fatura / VUK

| Konu | Gereklilik | Sistem Karşılığı |
|---|---|---|
| e-Fatura / e-Arşiv | GİB mükellefiyet eşikleri; yetkili entegratör üzerinden | accounting-service entegratör adaptörü (tenant bazlı) |
| Ön ödeme (yükleme) vergisel niteliği | Yüklemenin avans mı satış mı olduğu (çok amaçlı vs tek amaçlı voucher mantığı), KDV doğma anı | Tenant bazlı konfig: fatura yükleme anında mı harcama anında mı; **vergi danışmanı teyidi** |
| Defter/belge saklama | VUK md.253: 5 yıl (izleyen yıldan itibaren); TTK md.82: 10 yıl | Retention politikası: finansal kayıtlar min. 10 yıl (en uzun süre) |
| Breakage & ertelenmiş gelir | TFRS 15 / IFRS 15 — kullanılmayan bakiye geliri (beklenen breakage oranı) | accounting-service breakage modülü, GL eşleme |
| e-Defter | Tenant yükümlülüğü | GL/yevmiye export (ERP) |

---

## 10. Tüketici Mevzuatı — Hediye Kartı ve Ön Ödemeli Bakiye

| Konu | Gereklilik (değerlendirme) | Sistem Karşılığı |
|---|---|---|
| Geçerlilik süresi | 6502 sayılı Tüketicinin Korunması Hakkında Kanun ve ilgili Ticaret Bakanlığı düzenlemeleri; hediye kartı/çek geçerlilik süresi ve bilgilendirme kuralları (güncel asgari süre **hukuk ile teyit**) | Tenant konfig: `voucher.min_validity` platform tavanı ile; son kullanma öncesi bildirim (30/7/1 gün) |
| Önceden bilgilendirme | Süre, koşullar, ücretler açıkça gösterilmeli | Satın alma ekranında zorunlu gösterim, şablon |
| Bakiye iadesi | Hesap kapatmada kalan bakiye iadesi (lisanslı modelde e-para geri ödeme hakkı) | İade iş akışı (kaynak araca), maker-checker |
| Haksız şart | Tek taraflı süre kısaltma, fahiş hareketsizlik ücreti | Ücret/koşul değişikliklerinde ileriye dönük uygulama + bildirim |
| Mesafeli sözleşmeler | Cayma hakkı istisnaları | Hukuki metin şablonları |
| AB | Üye devlet bazlı hediye kartı kuralları (ör. minimum süreler) | Ülke profili konfigürasyonu |

---

## 11. Gereklilik → Kontrol Eşleme Tablosu

| Req ID | Regülasyon / Standart | Gereklilik (özet) | Sistem Kontrolü | Bileşen | CTL |
|---|---|---|---|---|---|
| R-01 | 6493 / LNE | Tenant'lar arası harcama yok | Ledger tenant izolasyonu, cross-tenant engel | ledger, payment | CTL-011 |
| R-02 | 6493 / LNE | Nakde çevrim yok | Cash-out özelliği yok; iade yalnızca kaynak araca | wallet, funding | CTL-029 |
| R-03 | 6493 / LNE | P2P kısıtlı | Feature flag varsayılan kapalı, açma maker-checker + hukuk onayı | tenant-service | CTL-029 |
| R-04 | PSD2 Art.37(2) | 1M EUR / 12 ay bildirimi | Hacim izleme raporu, %80 alarm | reporting | CTL-048 |
| R-05 | 6493 / fon koruma | Müşteri fonlarının izlenebilirliği | Günlük yükümlülük ↔ banka bakiye mutabakatı | settlement, ledger | CTL-035 |
| R-06 | 5549 | KYC, risk temelli | KYC tier + limitler | customer, compliance | CTL-048 |
| R-07 | 5549 | STR 10 iş günü | Vaka SLA sayacı, eskalasyon | compliance | CTL-051 |
| R-08 | 5549 md.8 | 8 yıl saklama | Retention + WORM | audit, ledger | CTL-052 |
| R-09 | 6415 / 7262 | Yaptırım taraması, dondurma | Onboarding + günlük yeniden tarama | compliance | CTL-049 |
| R-10 | 5549 | İşlem izleme | Senaryo motoru | compliance, risk | CTL-050 |
| R-11 | KVKK md.12 / GDPR Art.32 | Veri güvenliği | Şifreleme, erişim kontrolü | tüm | CTL-012, CTL-013 |
| R-12 | KVKK md.7 / GDPR Art.17 | Silme / imha | Crypto-shredding, periyodik imha | customer | CTL-016 |
| R-13 | KVKK md.10 / GDPR Art.13 | Aydınlatma & rıza kaydı | Versiyonlu onay kaydı | customer | CTL-017 |
| R-14 | KVKK Kurul kararı / GDPR Art.33 | 72 saat ihlal bildirimi | IR planı, tatbikat | SEC/CMP | CTL-043 |
| R-15 | KVKK md.9 | Yurt dışı aktarım | TR veri yerelliği, alt işleyen kaydı | platform | CTL-059 |
| R-16 | PCI-DSS | Kart verisi saklanmaz | PSP tokenizasyonu, SAQ A | funding | CTL-018 |
| R-17 | PCI-DSS 6.4.3 / 11.6.1 (SAQ A kriteri) | Ödeme sayfası script bütünlüğü | CSP, SRI | web | CTL-018 |
| R-18 | BDDK/TCMB BS ilkeleri | İz kayıtları değiştirilemez | Hash zinciri + WORM | audit | CTL-041 |
| R-19 | BDDK/TCMB BS ilkeleri | Görevler ayrılığı | SoD matrisi, maker-checker | admin | CTL-007, CTL-008 |
| R-20 | BDDK/TCMB BS ilkeleri | İş sürekliliği / DR | DR planı, tatbikat | OPS | CTL-057 |
| R-21 | BDDK/TCMB BS ilkeleri | Yurt içi birincil/ikincil sistem | TR bölge (lisanslı tenant) | OPS | CTL-057 |
| R-22 | ISO 27001 A.5.15–5.18 / SOC2 CC6 | Erişim yönetimi | MFA, RBAC, erişim gözden geçirme | Keycloak | CTL-002, CTL-009 |
| R-23 | ISO 27001 A.8.32 / SOC2 CC8 | Değişiklik yönetimi | PR review, GitOps | CI/CD | CTL-023, CTL-026 |
| R-24 | ISO 27001 A.8.8 / SOC2 CC7 | Teknik zafiyet yönetimi | SLA, tarama | SEC | CTL-042 |
| R-25 | ISO 27001 A.8.15–8.16 / SOC2 CC7.2 | Loglama & izleme | SIEM, alarm | OPS | CTL-040 |
| R-26 | SOC2 PI1 | İşlem bütünlüğü | Ledger invariant, idempotency | ledger | CTL-030, CTL-031 |
| R-27 | SOC2 A1 | Kullanılabilirlik | SLO, HA, kapasite | OPS | CTL-046, CTL-058 |
| R-28 | VUK / e-Fatura | e-Belge düzenleme | Entegratör adaptörü, mutabakat | accounting | CTL-037 |
| R-29 | VUK md.253 / TTK md.82 | Kayıt saklama 5/10 yıl | Retention | audit, accounting | CTL-052 |
| R-30 | 6502 | Hediye kartı süre/bilgilendirme | Min. süre konfig, bildirim | voucher | CTL-029 |
| R-31 | TFRS 15 | Breakage muhasebesi | Breakage modülü | accounting | CTL-037 |
| R-32 | ISO 27001 A.5.19–5.22 | Tedarikçi güvenliği | Tedarikçi değerlendirme | CMP | CTL-059 |

---

## 12. Açık Aksiyonlar

| # | Aksiyon | Sahip | Hedef |
|---|---|---|---|
| 1 | 6493 kapalı devre istisnası için hukuk bürosu yazılı görüşü (pilot tenant iş modeliyle) | CMP | Sprint 2 |
| 2 | TCMB'ye görüş başvurusu gerekliliği değerlendirmesi | CMP + Hukuk | Sprint 3 |
| 3 | PCI QSA scoping workshop (web + mobil SDK + servis sağlayıcı rolü) | SEC | Sprint 2 |
| 4 | Hediye kartı asgari geçerlilik süresi ve bakiye iadesi — güncel tüketici mevzuatı teyidi | CMP | Sprint 3 |
| 5 | Yükleme işlemlerinin KDV/fatura niteliği — vergi danışmanı görüşü | CMP + Finance | Sprint 4 |
| 6 | DPIA: fraud profilleme ve biyometrik KYC | CMP + SEC | Sprint 3 |
