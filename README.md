# 2026 CEO Projeleri - Proje Yönetim Sistemi

English Home 2026 yılı CEO öncelikli 4 stratejik projenin takip ve yönetim sistemi.

## 🎯 Projeler

1. **OMS Tek Stok Projesi** - %100 Omnichannel yapıya geçiş
2. **Alokasyon Optimizasyonu** - EHM'ye özel terzi işi alokasyon
3. **SGS 100 Gün Projesi** - Non-Product ürün grubunda SGS optimizasyonu
4. **İthal Süreçler** - Nakit akışı ve operasyonel optimizasyon

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/[kullanici-adi]/ceo_projeleri_2026.git
cd ceo_projeleri_2026
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın:**

**Ana Dashboard:**
```bash
streamlit run 0_dashboard.py
```

**Tek Proje:**
```bash
streamlit run 1_oms_tek_stok.py
streamlit run 2_alokasyon.py
streamlit run 3_sgs_100gun.py
streamlit run 4_ithal_surecler.py
```

## 👥 Kullanıcılar ve Roller

### Giriş Bilgileri

| Kullanıcı | Şifre | Rol | Açıklama |
|-----------|-------|-----|----------|
| ceo | `ceo2026` | CEO | Tüm projelere tam erişim |
| hakan | `proje2026` | Proje Yöneticisi | Proje koordinasyonu |
| ertugrul | `lojistik2026` | Sponsor | Lojistik GMY |
| gokhan | `ecom2026` | Sponsor | ECOM GMY |
| volkan | `magaza2026` | Manager | Mağazacılık GMY |
| ferhat | `stok2026` | Manager | Stok Yönetimi Direktörü |
| ozcan | `it2026` | Admin | IT GMY |
| demo | `demo2026` | Viewer | Demo kullanıcı |

### Rol Yetkileri

- **CEO**: Tüm projeleri görüntüleme ve düzenleme
- **Proje Yöneticisi**: Tüm projeleri düzenleme ve raporlama
- **Sponsor**: Sorumlu olduğu projeleri tam yönetim
- **Manager**: Görev düzenleme ve güncelleme
- **Admin**: Sistem ayarları ve kullanıcı yönetimi
- **Viewer**: Sadece görüntüleme

## 📊 Özellikler

### Genel
- ✅ Token tabanlı kullanıcı yönetimi
- ✅ Çoklu proje takibi
- ✅ Gantt chart görünümü
- ✅ Gerçek zamanlı ilerleme takibi
- ✅ JSON/CSV export/import
- ✅ Responsive tasarım

### Proje Yönetimi
- ✅ Faz ve görev bazlı planlama
- ✅ Sorumlu atama ve takibi
- ✅ Öncelik ve durum yönetimi
- ✅ Haftalık zaman planlaması
- ✅ Bağımlılık yönetimi

### Raporlama
- ✅ Durum bazlı analiz
- ✅ Sorumlu bazlı görev dağılımı
- ✅ İlerleme metrikleri
- ✅ Kritik yol analizi

## 🗂️ Dosya Yapısı

```
ceo_projeleri_2026/
├── 0_dashboard.py              # Ana dashboard (4 proje özeti)
├── 1_oms_tek_stok.py          # OMS Tek Stok Projesi
├── 2_alokasyon.py             # Alokasyon Optimizasyonu
├── 3_sgs_100gun.py            # SGS 100 Gün Projesi
├── 4_ithal_surecler.py        # İthal Süreçler Projesi
├── requirements.txt           # Python bağımlılıkları
├── README.md                  # Bu dosya
├── .gitignore                # Git ignore kuralları
└── data/
    ├── oms_proje_data.json   # OMS proje verisi
    ├── alokasyon_data.json   # Alokasyon proje verisi
    ├── sgs_data.json         # SGS proje verisi
    └── ithal_data.json       # İthal proje verisi
```

## 📈 Proje 1: OMS Tek Stok

**Hedef:** %100 Omnichannel yapıya geçiş
**Bitiş:** 1 Haziran 2026
**Toplam:** 11 Faz, 72 Görev, 74 Hafta

### Ana Fazlar:
- FAZ 0: Analiz ve Planlama
- FAZ 1: Sistem Altyapısı
- FAZ 2: Pilot Uygulama
- FAZ 3: OMS Mağaza Optimizasyonu
- FAZ 4: E-ticaret Koleksiyon Genişletme
- FAZ 5: Akyazı Depo Optimizasyonu
- FAZ 6: Tip1 Hariç GLM Stoğun Açılması
- FAZ 7: OMS Yaygınlaştırma
- FAZ 8: Akyazı Stoğun Açılması
- FAZ 9: Omnichannel Entegrasyon
- FAZ 10: Test ve Stabilizasyon
- FAZ 11: Yayınlama ve İzleme

## 🔧 Geliştirme

### Token Sistemi
Her kullanıcı için token bazlı giriş sistemi:
- Her giriş 1 token harcar
- 6 saat içinde yeniden giriş token harcamaz
- Token dolduğunda admin'den talep edilir

### Veri Yönetimi
- Projeler session state'te tutulur
- JSON export/import ile backup
- Versiyon kontrolü için data/ klasöründe saklanır

## 📝 Notlar

- Proje başlangıç tarihi: 6 Ocak 2026 (Pazartesi)
- Hedef bitiş tarihi: 1 Haziran 2026
- Tüm projeler paralel yürütülecek
- Haftalık checkpoint toplantıları yapılacak
- Aylık CEO raporlaması yapılacak

## 🤝 Katkıda Bulunma

Bu proje English Home için özel olarak geliştirilmiştir.

## 📧 İletişim

Proje Yöneticisi: Hakan Uğur
Şirket: Thorius Ltd.

---

**Thorius AR4U** | 2026 CEO Projeleri | English Home
