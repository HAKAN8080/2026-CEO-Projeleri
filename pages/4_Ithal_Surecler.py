import streamlit as st

st.set_page_config(page_title="İthal Süreçler Projesi", layout="wide", page_icon="🌍")

st.title("🌍 Proje 4: İthal Süreçler Optimizasyonu")
st.header("Nakit Akışı ve Operasyonel Süreç İyileştirme")

st.info("🚧 Bu proje yakında eklenecek...")

st.markdown("""
### 🎯 Proje Hedefleri:

Bu proje 2 ana odak noktasına sahiptir:

#### 1️⃣ Nakit Akışı Optimizasyonu
- Sipariş süreçlerinin gözden geçirilmesi
- Ödeme zamanlamasının optimize edilmesi
- Nakit akışına olumsuz etkilerin minimize edilmesi

#### 2️⃣ Operasyonel Süreç İyileştirme
- Demoraj performansının artırılması
- Ardiye maliyetlerinin optimize edilmesi
- Gümrük süreçlerinin hızlandırılması
- Zaman ve para kayıplarının önlenmesi

### 📋 Planlanan Fazlar:

1. **Mevcut Durum Analizi** - İthal süreçlerin detaylı incelemesi
2. **Kayıp Noktaları Tespiti** - Zaman ve para kayıplarının belirlenmesi
3. **Optimizasyon Planı** - İyileştirme stratejilerinin geliştirilmesi
4. **Pilot Uygulama** - Seçili tedarikçilerle test
5. **Yaygınlaştırma** - Tüm ithal süreçlere rollout

### 👥 Proje Ekibi:

- **Kategori:** Sipariş ve tedarikçi yönetimi
- **Finans:** Ödeme zamanlaması ve nakit akışı
- **Lojistik:** Demoraj, ardiye, gümrük süreçleri

### 🎯 Beklenen Kazanımlar:

- **Nakit Akışı:** %15-20 iyileştirme
- **Demoraj Maliyeti:** %30-40 azalma
- **Gümrük Süresi:** %25-30 kısalma
- **Operasyonel Verimlilik:** Genel süreç iyileştirmesi

---

⚠️ **Not:** Bu proje birçok departmanın koordinasyonunu gerektiren kapsamlı bir çalışmadır.

Proje detayları hazırlandığında bu sayfada görüntülenecektir.
""")

if st.button("🔙 Dashboard'a Dön"):
    st.info("👉 Lütfen terminalde: `streamlit run 0_dashboard.py`")
