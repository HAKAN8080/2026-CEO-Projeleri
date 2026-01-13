
import streamlit as st

st.set_page_config(page_title="SGS 100 Gün Projesi", layout="wide", page_icon="⏱️")

st.title("⏱️ Proje 3: SGS 100 Gün Projesi")
st.header("Non-Product Ürün Grubunda SGS Optimizasyonu")

st.info("🚧 Bu proje yakında eklenecek...")

st.markdown("""
### 🎯 Proje Hedefleri:

- Non-Product ürün grubunun SGS'ni 100 günün altına düşürme
- Satın alma sistematiğinin optimizasyonu
- Alokasyon yazılımına entegre sevkiyat
- Stok devir hızının iyileştirilmesi

### 📋 Planlanan Fazlar:

1. **SGS Analizi** - Mevcut SGS değerlerinin detaylı analizi
2. **Satın Alma Optimizasyonu** - Sipariş süreçlerinin iyileştirilmesi
3. **Alokasyon Entegrasyonu** - Sevkiyat süreçlerinin entegrasyonu
4. **Pilot Uygulama** - Seçili ürün gruplarında test
5. **Yaygınlaştırma** - Tüm Non-Product grubuna rollout

### 👥 Proje Ekibi:

- **Sorumlu:** Satın Alma Ekibi
- **Destek:** Ertuğrul (Lojistik), Ferhat (Stok Yönetimi)

### 📊 Hedef Metrikler:

- **Mevcut SGS:** >100 gün
- **Hedef SGS:** <100 gün
- **Beklenen İyileştirme:** %30-40
- **Stok Devir Hızı:** 2x artış

---

Proje detayları hazırlandığında bu sayfada görüntülenecektir.
""")

if st.button("🔙 Dashboard'a Dön"):
    st.info("👉 Lütfen terminalde: `streamlit run 0_dashboard.py`")
