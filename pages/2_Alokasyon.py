import streamlit as st

st.set_page_config(page_title="Alokasyon Optimizasyonu", layout="wide", page_icon="📦")

st.title("📦 Proje 2: Alokasyon Optimizasyonu")
st.header("EHM'ye Özel Terzi İşi Alokasyon")

st.info("🚧 Bu proje yakında eklenecek...")

st.markdown("""
### 🎯 Proje Hedefleri:

- EHM'ye özel alokasyon algoritması geliştirme
- Mağaza bazlı talep tahmini modeli
- Stok optimizasyonu ve verimlilik artışı
- Sevkiyat süreçleriyle entegrasyon

### 📋 Planlanan Fazlar:

1. **Mevcut Durum Analizi** - Alokasyon sisteminin değerlendirilmesi
2. **Algoritma Geliştirme** - EHM'ye özel algoritma tasarımı
3. **Pilot Uygulama** - Seçili mağazalarda test
4. **Yaygınlaştırma** - Tüm mağaza ağına rollout
5. **Optimizasyon** - Sürekli iyileştirme

### 👥 Proje Ekibi:

- **Sorumlu:** Ertuğrul (Lojistik GMY)
- **Destek:** Ferhat (Stok Yönetimi), IT Ekibi

---

Proje detayları hazırlandığında bu sayfada görüntülenecektir.
""")

if st.button("🔙 Dashboard'a Dön"):
    st.info("👉 Lütfen terminalde: `streamlit run 0_dashboard.py`")
