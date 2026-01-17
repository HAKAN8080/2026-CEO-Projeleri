import streamlit as st
import hashlib
from datetime import datetime

st.set_page_config(
    page_title="CEO Projeleri 2026 - Dashboard", 
    layout="wide", 
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ==============================================
# KULLANICI SİSTEMİ
# ==============================================

USERS = {
    "ceo": {
        "password": hashlib.sha256("ceo2026".encode()).hexdigest(),
        "role": "ceo",
        "name": "CEO",
        "title": "Genel Müdür"
    },
    "hakan": {
        "password": hashlib.sha256("proje2026".encode()).hexdigest(),
        "role": "project_manager",
        "name": "Hakan Uğur",
        "title": "Proje Yöneticisi"
    },
    "demo": {
        "password": hashlib.sha256("demo2026".encode()).hexdigest(),
        "role": "viewer",
        "name": "Demo Kullanıcı",
        "title": "Misafir"
    }
}

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_info = None
    
    if st.session_state.authenticated:
        return True
    
    st.markdown("""
    <style>
    .login-header {
        text-align: center;
        padding: 40px 0 30px;
    }
    .login-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .login-subtitle {
        color: #666;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-header">
        <div style="font-size: 5rem; margin-bottom: 20px;">📊</div>
        <div class="login-title">2026 CEO Projeleri</div>
        <div class="login-subtitle">English Home - Stratejik Proje Yönetim Sistemi</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanıcı Adı", key="login_username")
            password = st.text_input("Şifre", type="password", key="login_password")
            login = st.form_submit_button("🔐 Giriş Yap", use_container_width=True)
            
            if login:
                hashed = hashlib.sha256(password.encode()).hexdigest()
                
                if username in USERS and USERS[username]["password"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = USERS[username]
                    st.rerun()
                else:
                    st.error("❌ Kullanıcı adı veya şifre hatalı!")
    
    return False

if not check_password():
    st.stop()

# ==============================================
# ANA DASHBOARD
# ==============================================

# Header
col1, col2 = st.columns([4, 1])

with col1:
    st.title("📊 2026 CEO Projeleri Dashboard")
    st.caption("English Home - Stratejik Proje Takip Sistemi")

with col2:
    user_info = st.session_state.user_info
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; color: white;'>
        <div style='font-size: 0.9rem; font-weight: 600;'>{user_info['name']}</div>
        <div style='font-size: 0.8rem; opacity: 0.9;'>{user_info['title']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.button("🚪 Çıkış", key="logout"):
    st.session_state.authenticated = False
    st.rerun()

st.markdown("---")

# Proje özet bilgileri
proje_baslangic = datetime(2026, 1, 1)
proje_bitis = datetime(2026, 6, 1)
bugun = datetime.now()
kalan_gun = (proje_bitis - bugun).days

# Üst metrikler
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Toplam Proje", "4", delta="Aktif")

with col2:
    st.metric("Başlangıç", proje_baslangic.strftime("%d.%m.%Y"))

with col3:
    st.metric("Hedef Bitiş", proje_bitis.strftime("%d.%m.%Y"))

with col4:
    st.metric("Kalan Gün", f"{kalan_gun}", delta=f"{kalan_gun//30} ay")

with col5:
    gecen_gun = (bugun - proje_baslangic).days
    toplam_gun = (proje_bitis - proje_baslangic).days
    progress = min(100, int((gecen_gun / toplam_gun) * 100))
    st.metric("Genel İlerleme", f"%{progress}")

st.markdown("---")

# Proje Kartları
st.header("🎯 Stratejik Projeler")

# Proje 1: OMS
col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px; color: white; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 1.8rem;'>📦 Proje 1: OMS Proje Plani</h2>
            <p style='margin: 10px 0 0 0; opacity: 0.9;'>Stok Optimizasyonu ve OMS Yayginlastirma</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**📋 Kapsam:**")
        st.write("• Daha fazla TIP 1 urun donusumu")
        st.write("• Akyazi maksimum stok optimizasyonu")
        st.write("• GLM stogunun satisa acilmasi")
        st.write("• OMS verimlilik ve yayginlastirma")

        st.markdown("**📊 Durum:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Faz", "5")
        with col_b:
            st.metric("Gorev", "23")
        with col_c:
            st.metric("Hafta", "20")

        st.markdown("**👥 Sorumlu:**")
        st.write("Fatih, Gokhan, Ertugrul, Ozcan, Ferhat, Volkan")

        if st.button("📂 Projeyi Ac", key="oms", use_container_width=True, type="primary"):
            st.switch_page("pages/1_OMS_Proje_Plani.py")

with col2:
    with st.container():
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
        border-radius: 15px; color: white; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 1.8rem;'>📦 Proje 2: Alokasyon Optimizasyonu</h2>
            <p style='margin: 10px 0 0 0; opacity: 0.9;'>EHM Özel Terzi İşi Alokasyon</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📋 Kapsam:**")
        st.write("• EHM'ye özel alokasyon algoritması")
        st.write("• Mağaza bazlı talep tahmini")
        st.write("• Stok optimizasyonu")
        st.write("• Sevkiyat entegrasyonu")
        
        st.markdown("**📊 Durum:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Faz", "Yakında")
        with col_b:
            st.metric("Görev", "Yakında")
        with col_c:
            st.metric("Hafta", "Yakında")
        
        st.markdown("**👥 Sorumlu:**")
        st.write("Ertuğrul, Ferhat, IT Ekibi")
        
        if st.button("📂 Projeyi Aç", key="alokasyon", use_container_width=True):
            st.switch_page("pages/2_Alokasyon.py")

# Proje 3 ve 4
col3, col4 = st.columns(2)

with col3:
    with st.container():
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
        border-radius: 15px; color: white; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 1.8rem;'>⏱️ Proje 3: SGS 100 Gün</h2>
            <p style='margin: 10px 0 0 0; opacity: 0.9;'>Non-Product SGS Optimizasyonu</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📋 Kapsam:**")
        st.write("• Non-Product ürün grubunda SGS <100 gün")
        st.write("• Satın alma sistematiği optimizasyonu")
        st.write("• Alokasyon entegre sevkiyat")
        st.write("• Stok devir hızı iyileştirme")
        
        st.markdown("**📊 Durum:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Faz", "Yakında")
        with col_b:
            st.metric("Görev", "Yakında")
        with col_c:
            st.metric("Hafta", "Yakında")
        
        st.markdown("**👥 Sorumlu:**")
        st.write("Satınalma, Ertuğrul, Ferhat")
        
        if st.button("📂 Projeyi Aç", key="sgs", use_container_width=True):
            st.switch_page("pages/3_SGS_100_Gun.py")

with col4:
    with st.container():
        st.markdown("""
        <div style='padding: 20px; background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
        border-radius: 15px; color: white; margin-bottom: 20px;'>
            <h2 style='margin: 0; font-size: 1.8rem;'>🌍 Proje 4: İthal Süreçler</h2>
            <p style='margin: 10px 0 0 0; opacity: 0.9;'>Nakit ve Operasyonel Optimizasyon</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**📋 Kapsam:**")
        st.write("• Nakit akışı optimizasyonu")
        st.write("• Ödeme zamanlaması iyileştirme")
        st.write("• Demoraj performansı artırma")
        st.write("• Gümrük süreç optimizasyonu")
        
        st.markdown("**📊 Durum:**")
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Faz", "Yakında")
        with col_b:
            st.metric("Görev", "Yakında")
        with col_c:
            st.metric("Hafta", "Yakında")
        
        st.markdown("**👥 Sorumlu:**")
        st.write("Finans, Lojistik, Kategori")
        
        if st.button("📂 Projeyi Aç", key="ithal", use_container_width=True):
            st.switch_page("pages/4_Ithal_Surecler.py")

st.markdown("---")

# Hızlı Erişim
st.header("⚡ Hızlı Erişim")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='padding: 15px; background: #f0f2f6; border-radius: 10px; text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 10px;'>📊</div>
        <div style='font-weight: 600;'>Haftalık Rapor</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Hazırlanıyor</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='padding: 15px; background: #f0f2f6; border-radius: 10px; text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 10px;'>📅</div>
        <div style='font-weight: 600;'>Toplantı Takvimi</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Hazırlanıyor</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='padding: 15px; background: #f0f2f6; border-radius: 10px; text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 10px;'>⚠️</div>
        <div style='font-weight: 600;'>Kritik Görevler</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Hazırlanıyor</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='padding: 15px; background: #f0f2f6; border-radius: 10px; text-align: center;'>
        <div style='font-size: 2rem; margin-bottom: 10px;'>👥</div>
        <div style='font-weight: 600;'>Ekip Yükü</div>
        <div style='font-size: 0.9rem; color: #666; margin-top: 5px;'>Hazırlanıyor</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.caption(f"""
📊 2026 CEO Projeleri Dashboard | Thorius AR4U | English Home  
Son Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M')}
""")
