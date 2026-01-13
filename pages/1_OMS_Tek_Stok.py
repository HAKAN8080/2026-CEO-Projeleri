import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib

st.set_page_config(page_title="OMS Tek Stok Projesi", layout="wide", page_icon="🏪")

# ==============================================
# KULLANICI YETKİLENDİRME SİSTEMİ
# ==============================================

MODULE_TOKEN_COST = 1

USERS = {
    "ceo": {
        "password": hashlib.sha256("ceo2026".encode()).hexdigest(),
        "role": "ceo",
        "name": "CEO",
        "title": "Genel Müdür",
        "initial_tokens": 1000
    },
    "hakan": {
        "password": hashlib.sha256("proje2026".encode()).hexdigest(),
        "role": "project_manager",
        "name": "Hakan Uğur",
        "title": "Proje Yöneticisi",
        "initial_tokens": 1000
    },
    "ertugrul": {
        "password": hashlib.sha256("lojistik2026".encode()).hexdigest(),
        "role": "sponsor",
        "name": "Ertuğrul Bey",
        "title": "Lojistik GMY",
        "initial_tokens": 100
    },
    "gokhan": {
        "password": hashlib.sha256("ecom2026".encode()).hexdigest(),
        "role": "sponsor",
        "name": "Gökhan Bey",
        "title": "ECOM GMY",
        "initial_tokens": 100
    },
    "volkan": {
        "password": hashlib.sha256("magaza2026".encode()).hexdigest(),
        "role": "manager",
        "name": "Volkan Bey",
        "title": "Mağazacılık GMY",
        "initial_tokens": 100
    },
    "ozcan": {
        "password": hashlib.sha256("it2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Özcan Bey",
        "title": "IT GMY",
        "initial_tokens": 100
    },
    "demo": {
        "password": hashlib.sha256("demo2026".encode()).hexdigest(),
        "role": "viewer",
        "name": "Demo Kullanıcı",
        "title": "Misafir",
        "initial_tokens": 100
    }
}

# ==============================================
# TOKEN YÖNETİM FONKSİYONLARI
# ==============================================

def init_token_system():
    if "token_data" not in st.session_state:
        st.session_state.token_data = {}
    
    username = st.session_state.get("username")
    if username and username not in st.session_state.token_data:
        st.session_state.token_data[username] = {
            "remaining_tokens": USERS[username]["initial_tokens"],
            "total_tokens": USERS[username]["initial_tokens"],
            "last_login": None,
            "last_login_date": None,
            "login_count_today": 0,
            "tokens_used_today": 0
        }

def check_token_charge():
    username = st.session_state.username
    now = datetime.now()
    
    token_info = st.session_state.token_data[username]
    last_login = token_info["last_login"]
    last_date = token_info["last_login_date"]
    
    if last_login is None:
        return True
    
    today = now.date()
    
    if last_date != today:
        token_info["login_count_today"] = 0
        token_info["tokens_used_today"] = 0
        return True
    
    hours_since_login = (now - last_login).total_seconds() / 3600
    
    if hours_since_login >= 6:
        return True
    
    return False

def charge_token():
    username = st.session_state.username
    now = datetime.now()
    
    token_info = st.session_state.token_data[username]
    
    if token_info["remaining_tokens"] > 0:
        token_info["remaining_tokens"] -= MODULE_TOKEN_COST
        token_info["tokens_used_today"] += MODULE_TOKEN_COST
        token_info["login_count_today"] += 1
        token_info["last_login"] = now
        token_info["last_login_date"] = now.date()
        return True
    else:
        return False

def get_token_balance():
    username = st.session_state.username
    return st.session_state.token_data[username]["remaining_tokens"]

def get_token_usage_percent():
    username = st.session_state.username
    token_info = st.session_state.token_data[username]
    used = token_info["total_tokens"] - token_info["remaining_tokens"]
    return int((used / token_info["total_tokens"]) * 100)

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
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .login-subtitle {
        color: #666;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-header">
        <div style="font-size: 4rem; margin-bottom: 20px;">🏪</div>
        <div class="login-title">OMS Tek Stok Projesi</div>
        <div class="login-subtitle">2026 CEO Projeleri - Proje Yönetim Sistemi</div>
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
                    init_token_system()
                    st.rerun()
                else:
                    st.error("❌ Kullanıcı adı veya şifre hatalı!")
    
    return False

# ==============================================
# PROJE VERİLERİ
# ==============================================

def get_default_project_data():
    """OMS Tek Stok projesi için varsayılan veri yapısı"""
    return {
        "FAZ 0: ANALİZ VE PLANLAMA": {
            "baslangic": 0,
            "sure": 3,
            "renk": "🔴",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "0.10",
                    "gorev": "EVE Ürün Portföyü Analizi",
                    "aciklama": "EVE ürün portföyünün detaylı analizi ve değerlendirmesi",
                    "sure": 1,
                    "baslangic_hafta": 1,
                    "sorumlu": "Ertuğrul + Gökhan + Tayfun",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.20",
                    "gorev": "Paket Tipi Belirleme",
                    "aciklama": "Ürünler için paket tiplendirme ve standardizasyon",
                    "sure": 1,
                    "baslangic_hafta": 2,
                    "sorumlu": "Ertuğrul + Gökhan + Ali Akçay",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.30",
                    "gorev": "Ürün Sınıflandırma",
                    "aciklama": "Ürün kategorilendirme ve sınıflandırma sistemi",
                    "sure": 1,
                    "baslangic_hafta": 2,
                    "sorumlu": "Ertuğrul + Gökhan + Ferhat",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.40",
                    "gorev": "Maliyet Analizi",
                    "aciklama": "Proje ve operasyonel maliyet analizi",
                    "sure": 1,
                    "baslangic_hafta": 3,
                    "sorumlu": "Finans + Ertuğrul + Gökhan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.50",
                    "gorev": "ROI Analizi",
                    "aciklama": "Yatırım getirisi ve fayda analizi",
                    "sure": 1,
                    "baslangic_hafta": 3,
                    "sorumlu": "Finans + Ertuğrul + Gökhan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.60",
                    "gorev": "Veri Toplama",
                    "aciklama": "Sistem ve operasyonel verilerinin toplanması",
                    "sure": 2,
                    "baslangic_hafta": 1,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "0.70",
                    "gorev": "Kapasite Analizi",
                    "aciklama": "Depo ve sistem kapasite analizi",
                    "sure": 1,
                    "baslangic_hafta": 3,
                    "sorumlu": "Ertuğrul + Ferhat",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 1: SİSTEM ALTYAPISI": {
            "baslangic": 3,
            "sure": 6,
            "renk": "🟢",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "1.10",
                    "gorev": "Simülasyon Modülü",
                    "aciklama": "Stok ve sevkiyat simülasyon modülü geliştirme",
                    "sure": 2,
                    "baslangic_hafta": 4,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.20",
                    "gorev": "Koli Bozma Algoritması",
                    "aciklama": "Otomatik koli bozma ve açık adet yönetimi algoritması",
                    "sure": 2,
                    "baslangic_hafta": 4,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.30",
                    "gorev": "Transfer Sistemi",
                    "aciklama": "Depolar arası transfer yönetim sistemi",
                    "sure": 2,
                    "baslangic_hafta": 5,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.40",
                    "gorev": "Açık Adet Dashboard",
                    "aciklama": "Açık adet takip ve yönetim dashboard'u",
                    "sure": 2,
                    "baslangic_hafta": 5,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.50",
                    "gorev": "Önceliklendirme",
                    "aciklama": "Ürün ve sipariş önceliklendirme sistemi",
                    "sure": 2,
                    "baslangic_hafta": 7,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.60",
                    "gorev": "Sevk Kural Motoru",
                    "aciklama": "Sevkiyat kural motoru geliştirme",
                    "sure": 3,
                    "baslangic_hafta": 5,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.70",
                    "gorev": "Sevk Algoritması",
                    "aciklama": "Optimum sevkiyat algoritması",
                    "sure": 2,
                    "baslangic_hafta": 7,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.80",
                    "gorev": "Sevk Dashboard",
                    "aciklama": "Sevkiyat takip ve yönetim dashboard'u",
                    "sure": 2,
                    "baslangic_hafta": 7,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "1.90",
                    "gorev": "Entegrasyon Test",
                    "aciklama": "Tüm modüllerin entegrasyon testleri",
                    "sure": 1,
                    "baslangic_hafta": 8,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 2: PİLOT UYGULAMA": {
            "baslangic": 9,
            "sure": 15,
            "renk": "🔵",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "2.10",
                    "gorev": "Pilot Seçimi",
                    "aciklama": "Pilot mağaza ve depo seçimi",
                    "sure": 1,
                    "baslangic_hafta": 10,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.20",
                    "gorev": "EVE Paketleme",
                    "aciklama": "EVE ürünlerinin yeni paket sistemine göre hazırlanması",
                    "sure": 2,
                    "baslangic_hafta": 11,
                    "sorumlu": "Tayfun + Ali Akçay",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.30",
                    "gorev": "Stok Transferi",
                    "aciklama": "Pilot için stok transferi",
                    "sure": 1,
                    "baslangic_hafta": 13,
                    "sorumlu": "Ertuğrul + Ferhat",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.40",
                    "gorev": "Pilot 1. Ay",
                    "aciklama": "İlk ay pilot uygulama ve izleme",
                    "sure": 4,
                    "baslangic_hafta": 14,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.50",
                    "gorev": "Optimizasyon",
                    "aciklama": "Pilot sonuçlarına göre sistem optimizasyonu",
                    "sure": 1,
                    "baslangic_hafta": 18,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.60",
                    "gorev": "Faz 2A Geçiş",
                    "aciklama": "Genişletilmiş pilot geçişi",
                    "sure": 3,
                    "baslangic_hafta": 19,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.70",
                    "gorev": "EVE %50",
                    "aciklama": "EVE ürünlerinin %50'sinin sisteme dahil edilmesi",
                    "sure": 6,
                    "baslangic_hafta": 19,
                    "sorumlu": "Tayfun + Ali Akçay",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.80",
                    "gorev": "Tam Geçiş",
                    "aciklama": "Pilot lokasyonlarda tam geçiş",
                    "sure": 2,
                    "baslangic_hafta": 22,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.90",
                    "gorev": "Depo Kararı",
                    "aciklama": "Depo konsolidasyon nihai kararı",
                    "sure": 1,
                    "baslangic_hafta": 24,
                    "sorumlu": "Yönetim",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "2.91",
                    "gorev": "Depo Düzenleme",
                    "aciklama": "Depoda fiziksel düzenleme ve hazırlık",
                    "sure": 1,
                    "baslangic_hafta": 24,
                    "sorumlu": "Ertuğrul",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 3: OMS MAĞAZA OPTİMİZASYONU": {
            "baslangic": 24,
            "sure": 12,
            "renk": "🟡",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "3.10",
                    "gorev": "Mevcut Mağaza Ağı Analizi",
                    "aciklama": "300 mağazanın detaylı analizi ve segmentasyonu",
                    "sure": 2,
                    "baslangic_hafta": 25,
                    "sorumlu": "Ertuğrul + Gökhan + Volkan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.20",
                    "gorev": "Personel ve Kargo Maliyet Modelleme",
                    "aciklama": "Mağaza bazlı maliyet modelleri",
                    "sure": 2,
                    "baslangic_hafta": 25,
                    "sorumlu": "Ertuğrul + Gökhan + Finans",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.30",
                    "gorev": "Matematiksel Optimizasyon Modeli",
                    "aciklama": "Mağaza stok optimizasyon modeli",
                    "sure": 3,
                    "baslangic_hafta": 27,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.40",
                    "gorev": "Bölge Bazlı Talep Analizi",
                    "aciklama": "Bölgesel talep tahmin modelleri",
                    "sure": 2,
                    "baslangic_hafta": 27,
                    "sorumlu": "Ertuğrul + Gökhan + Pazarlama",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.50",
                    "gorev": "İstisna Mağaza Belirleme",
                    "aciklama": "Özel durum mağazaların tespiti",
                    "sure": 1,
                    "baslangic_hafta": 29,
                    "sorumlu": "Volkan + Ertuğrul + Gökhan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.60",
                    "gorev": "Yeni Mağaza Açılış Senaryoları",
                    "aciklama": "Yeni mağaza açılışları için sistem hazırlığı",
                    "sure": 2,
                    "baslangic_hafta": 30,
                    "sorumlu": "Ertuğrul + Gökhan + Finans",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.70",
                    "gorev": "ISO In-Store Ordering Ürün Segmentasyonu",
                    "aciklama": "ISO için ürün segmentasyonu",
                    "sure": 2,
                    "baslangic_hafta": 30,
                    "sorumlu": "Ertuğrul + Gökhan + Volkan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.80",
                    "gorev": "ISO Teşvik Mekanizması Tasarımı",
                    "aciklama": "Mağaza personeli teşvik sistemi",
                    "sure": 2,
                    "baslangic_hafta": 32,
                    "sorumlu": "Volkan + Pazarlama + Finans",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.90",
                    "gorev": "OMS Kural Motoru ISO Entegrasyonu",
                    "aciklama": "ISO sistemi ile OMS entegrasyonu",
                    "sure": 2,
                    "baslangic_hafta": 32,
                    "sorumlu": "Ertuğrul + Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.100",
                    "gorev": "Mağazacılık ile El Sıkışma Toplantıları",
                    "aciklama": "Mağaza operasyonları ile koordinasyon",
                    "sure": 2,
                    "baslangic_hafta": 34,
                    "sorumlu": "Yönetim + Ertuğrul + Gökhan + Volkan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.110",
                    "gorev": "Mağaza Açılış Pilot Projesi",
                    "aciklama": "Yeni mağaza pilot uygulaması",
                    "sure": 3,
                    "baslangic_hafta": 34,
                    "sorumlu": "Volkan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.120",
                    "gorev": "ISO Teşvik Pilotu",
                    "aciklama": "Teşvik sisteminin pilot uygulaması",
                    "sure": 2,
                    "baslangic_hafta": 35,
                    "sorumlu": "Volkan + Pazarlama",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "3.130",
                    "gorev": "Sonuç Değerlendirme ve Strateji Finalizasyonu",
                    "aciklama": "Pilot sonuçlarının değerlendirilmesi",
                    "sure": 1,
                    "baslangic_hafta": 36,
                    "sorumlu": "Yönetim + Tüm Ekip",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 4: E-TİCARET KOLEKSİYON GENİŞLETME": {
            "baslangic": 36,
            "sure": 4,
            "renk": "🟣",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "4.10",
                    "gorev": "Koleksiyon Genişletilmesi Çalışması",
                    "aciklama": "Yeni marka, ürün grupları ve mevcut koleksiyonun genişletilmesi",
                    "sure": 2,
                    "baslangic_hafta": 37,
                    "sorumlu": "Fatih",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "4.20",
                    "gorev": "Koli Standartlarını Gözden Geçirme",
                    "aciklama": "E-ticaret için koli standartlarının revize edilmesi",
                    "sure": 1,
                    "baslangic_hafta": 37,
                    "sorumlu": "Fatih",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "4.30",
                    "gorev": "Ürünlerin Tip 1 Leştirilmesi",
                    "aciklama": "Prepack optimizasyonu ve Tip 1 dönüşümü",
                    "sure": 2,
                    "baslangic_hafta": 38,
                    "sorumlu": "Fatih",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "4.40",
                    "gorev": "Bundle Satış Odaklı Kolileme",
                    "aciklama": "Bundle satış için özel paketleme",
                    "sure": 2,
                    "baslangic_hafta": 39,
                    "sorumlu": "Fatih",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 5: AKYAZI DEPO OPTİMİZASYONU": {
            "baslangic": 40,
            "sure": 4,
            "renk": "🟠",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "5.10",
                    "gorev": "Atıl Stok Temizleme",
                    "aciklama": "Akyazı deposundaki atıl stokların temizlenmesi",
                    "sure": 2,
                    "baslangic_hafta": 41,
                    "sorumlu": "Gökhan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "5.20",
                    "gorev": "Akyazı Mağazasına Ürün Çıkışı",
                    "aciklama": "Akyazı outlet mağazasına ürün transferi",
                    "sure": 1,
                    "baslangic_hafta": 41,
                    "sorumlu": "Gökhan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "5.30",
                    "gorev": "Akyazı Stok Yönetim RPT Modeli",
                    "aciklama": "Güvenlik stoğu ve reorder point modeli",
                    "sure": 2,
                    "baslangic_hafta": 42,
                    "sorumlu": "Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 6: TİP1 HARİÇ GLM STOĞUN AÇILMASI": {
            "baslangic": 44,
            "sure": 4,
            "renk": "🟢",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "6.10",
                    "gorev": "Palet - Koli - AA Yönetim Sisteminin Kurulması",
                    "aciklama": "Palet, koli ve açık adet yönetim sistemi",
                    "sure": 2,
                    "baslangic_hafta": 45,
                    "sorumlu": "Ertuğrul",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "6.20",
                    "gorev": "Stok Yönetim Modülü",
                    "aciklama": "Paletten satış, koliden satış yönetimi",
                    "sure": 2,
                    "baslangic_hafta": 45,
                    "sorumlu": "Ferhat",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "6.30",
                    "gorev": "Açık Adet Kalanın Yönetimi",
                    "aciklama": "Bozulmuş koli ve açık adet stoklarının yönetimi",
                    "sure": 1,
                    "baslangic_hafta": 46,
                    "sorumlu": "Ertuğrul + Ferhat",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "6.40",
                    "gorev": "Karma Koli Metodu Analizi",
                    "aciklama": "Karma koli oluşturma ve yönetim metodolojisi",
                    "sure": 1,
                    "baslangic_hafta": 47,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 7: OMS YAYGИНLAŞTIRMA VE OPTİMİZASYON": {
            "baslangic": 48,
            "sure": 8,
            "renk": "🔵",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "7.10",
                    "gorev": "Mevcut 50 Mağaza OMS Performans İyileştirme",
                    "aciklama": "Mevcut OMS kullanımının optimize edilmesi",
                    "sure": 2,
                    "baslangic_hafta": 49,
                    "sorumlu": "Özcan + Volkan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "7.20",
                    "gorev": "Bölge 1 - OMS Rollout (80 Mağaza)",
                    "aciklama": "İlk bölge mağazalarına OMS kurulumu",
                    "sure": 2,
                    "baslangic_hafta": 50,
                    "sorumlu": "Volkan + IT",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "7.30",
                    "gorev": "Bölge 2 - OMS Rollout (80 Mağaza)",
                    "aciklama": "İkinci bölge mağazalarına OMS kurulumu",
                    "sure": 2,
                    "baslangic_hafta": 51,
                    "sorumlu": "Volkan + IT",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "7.40",
                    "gorev": "Bölge 3 - OMS Rollout (90 Mağaza)",
                    "aciklama": "Üçüncü bölge mağazalarına OMS kurulumu",
                    "sure": 2,
                    "baslangic_hafta": 52,
                    "sorumlu": "Volkan + IT",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "7.50",
                    "gorev": "OMS Teşvik Programı Başlatma",
                    "aciklama": "Mağaza personeli için OMS teşvik programı",
                    "sure": 3,
                    "baslangic_hafta": 53,
                    "sorumlu": "Volkan + Pazarlama",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "7.60",
                    "gorev": "Tüm Mağazalarda Doğrulama",
                    "aciklama": "300 mağazada OMS çalışırlığının doğrulanması",
                    "sure": 2,
                    "baslangic_hafta": 54,
                    "sorumlu": "Hakan + Volkan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 8: AKYAZI STOĞUN TÜM KANALLARA AÇILMASI": {
            "baslangic": 56,
            "sure": 4,
            "renk": "🟣",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "8.10",
                    "gorev": "Hızlı Toplama ve Sevk Algoritması",
                    "aciklama": "Akyazı stoklarının hızlı picking algoritması",
                    "sure": 2,
                    "baslangic_hafta": 57,
                    "sorumlu": "Ertuğrul + Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "8.20",
                    "gorev": "Koli - Açık Adet Satış Entegrasyonu",
                    "aciklama": "Tüm kanallarda koli ve açık adet satış",
                    "sure": 2,
                    "baslangic_hafta": 57,
                    "sorumlu": "Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "8.30",
                    "gorev": "E-ticaret Akyazı Entegrasyonu",
                    "aciklama": "Akyazı stoklarının e-ticaret platformuna açılması",
                    "sure": 2,
                    "baslangic_hafta": 59,
                    "sorumlu": "Gökhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 9: OMNICHANNEL ENTEGRASYON": {
            "baslangic": 60,
            "sure": 6,
            "renk": "🟡",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "9.10",
                    "gorev": "Cross-Channel Stok Görünürlüğü",
                    "aciklama": "Tüm kanallar tek stok havuzundan görüntüleme",
                    "sure": 2,
                    "baslangic_hafta": 61,
                    "sorumlu": "Gökhan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "9.20",
                    "gorev": "Sipariş Yönlendirme Algoritması",
                    "aciklama": "En optimal noktadan sipariş karşılama",
                    "sure": 2,
                    "baslangic_hafta": 61,
                    "sorumlu": "Hakan + Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "9.30",
                    "gorev": "Click & Collect Aktifleştirme",
                    "aciklama": "Online sipariş, mağazadan teslim",
                    "sure": 2,
                    "baslangic_hafta": 63,
                    "sorumlu": "Gökhan + Volkan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "9.40",
                    "gorev": "Ship from Store",
                    "aciklama": "Mağazalardan e-ticaret siparişlerini gönderme",
                    "sure": 2,
                    "baslangic_hafta": 63,
                    "sorumlu": "Gökhan + Ertuğrul",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "9.50",
                    "gorev": "İade Yönetimi - Omnichannel",
                    "aciklama": "Her kanaldan alınan ürünün her kanaldan iadesi",
                    "sure": 2,
                    "baslangic_hafta": 65,
                    "sorumlu": "Gökhan + Volkan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 10: TEST VE STABİLİZASYON": {
            "baslangic": 66,
            "sure": 4,
            "renk": "🟠",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "10.10",
                    "gorev": "End-to-End Test Senaryoları",
                    "aciklama": "Tüm kanallar için gerçek zamanlı testler",
                    "sure": 2,
                    "baslangic_hafta": 67,
                    "sorumlu": "Hakan + Tüm Ekip",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "10.20",
                    "gorev": "Performans ve Yük Testi",
                    "aciklama": "Yoğun dönemlerde sistem performans testi",
                    "sure": 1,
                    "baslangic_hafta": 67,
                    "sorumlu": "Özcan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "10.30",
                    "gorev": "Kullanıcı Kabul Testleri",
                    "aciklama": "Mağaza ve e-ticaret kullanıcılarının testleri",
                    "sure": 1,
                    "baslangic_hafta": 68,
                    "sorumlu": "Volkan + Gökhan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "10.40",
                    "gorev": "Stabilizasyon ve Bug Fixing",
                    "aciklama": "Tespit edilen sorunların çözümü",
                    "sure": 2,
                    "baslangic_hafta": 69,
                    "sorumlu": "Özcan + IT",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        },
        "FAZ 11: YAYINLAMA VE İZLEME": {
            "baslangic": 70,
            "sure": 4,
            "renk": "🟢",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "11.10",
                    "gorev": "Go-Live: Tek Stok Sistemi",
                    "aciklama": "100% omnichannel sistemin canlıya alınması",
                    "sure": 1,
                    "baslangic_hafta": 71,
                    "sorumlu": "CEO + Tüm Ekip",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "11.20",
                    "gorev": "7 Gün Yoğun İzleme",
                    "aciklama": "Canlıya geçişten sonra 7/24 monitoring",
                    "sure": 1,
                    "baslangic_hafta": 71,
                    "sorumlu": "Özcan + Hakan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "11.30",
                    "gorev": "İlk Ay Performans Analizi",
                    "aciklama": "Stok kullanım oranları, satış artışı analizi",
                    "sure": 2,
                    "baslangic_hafta": 72,
                    "sorumlu": "Hakan",
                    "oncelik": "Yüksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "11.40",
                    "gorev": "CEO Sunumu ve Proje Kapanışı",
                    "aciklama": "Proje sonuçlarının CEO'ya sunumu",
                    "sure": 1,
                    "baslangic_hafta": 73,
                    "sorumlu": "Hakan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
            ]
        }
    }

# ==============================================
# ANA UYGULAMA
# ==============================================

if not check_password():
    st.stop()

# Token kontrolü
init_token_system()
if check_token_charge():
    if not charge_token():
        st.error("⚠️ Token limitiniz doldu!")
        st.stop()

# Proje verilerini yükle
if "proje_verileri" not in st.session_state:
    st.session_state.proje_verileri = get_default_project_data()

fazlar = st.session_state.proje_verileri

# ==============================================
# HEADER
# ==============================================

col1, col2 = st.columns([3, 1])

with col1:
    st.title("🏪 OMS Tek Stok Projesi")
    st.caption("2026 CEO Projeleri - Proje #1")

with col2:
    user_info = st.session_state.user_info
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; color: white;'>
        <div style='font-size: 0.9rem; font-weight: 600;'>{user_info['name']}</div>
        <div style='font-size: 0.8rem; opacity: 0.9;'>{user_info['title']}</div>
        <div style='font-size: 0.75rem; opacity: 0.8;'>Token: {get_token_balance()} / {st.session_state.token_data[st.session_state.username]['total_tokens']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.button("🚪 Çıkış", key="logout"):
    st.session_state.authenticated = False
    st.rerun()

st.markdown("---")

# ==============================================
# PROJE BİLGİLERİ
# ==============================================

proje_baslangic = datetime(2026, 1, 1)  # 1 Ocak 2026
proje_bitis = datetime(2026, 6, 1)
toplam_sure = sum([faz['sure'] for faz in fazlar.values()])
bugun = datetime.now()
gecen_gun = (bugun - proje_baslangic).days
gecen_hafta = max(1, gecen_gun // 7)

# Özet metrikler
st.markdown("### 📊 Proje Özeti")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Başlangıç", proje_baslangic.strftime("%d.%m.%Y"))

with col2:
    st.metric("Bitiş", proje_bitis.strftime("%d.%m.%Y"))

with col3:
    kalan_gun = (proje_bitis - bugun).days
    st.metric("Kalan Gün", f"{kalan_gun}")

with col4:
    st.metric("Toplam Hafta", f"{toplam_sure}")

with col5:
    progress = min(100, int((gecen_hafta / toplam_sure) * 100))
    st.metric("İlerleme", f"%{progress}")

st.markdown("---")

# ==============================================
# TABLAR
# ==============================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Genel Bakış", 
    "📅 Gantt Chart", 
    "✏️ Düzenle",
    "➕ Ekle",
    "📥 Veri İşlemleri",
    "📈 Raporlar"
])

# TAB 1: GENEL BAKIŞ
with tab1:
    st.header("📋 Proje Fazları ve Görevler")
    
    for faz_adi, faz in fazlar.items():
        with st.expander(f"{faz['renk']} {faz_adi} - {faz['durum']}", expanded=True):
            st.caption(f"**Başlangıç:** Hafta {faz['baslangic']} | **Süre:** {faz['sure']} hafta")
            
            if faz['gorevler']:
                df_gorevler = pd.DataFrame(faz['gorevler'])
                df_gorevler = df_gorevler[['id', 'gorev', 'sorumlu', 'oncelik', 'durum', 'baslangic_hafta', 'sure']]
                
                # Durum renklendirme
                def highlight_durum(row):
                    if row['durum'] == 'Tamamlandı':
                        return ['background-color: #d4edda'] * len(row)
                    elif row['durum'] == 'Devam Ediyor':
                        return ['background-color: #fff3cd'] * len(row)
                    elif row['durum'] == 'Beklemede':
                        return ['background-color: #f8d7da'] * len(row)
                    else:
                        return [''] * len(row)
                
                st.dataframe(
                    df_gorevler.style.apply(highlight_durum, axis=1),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("Bu fazda henüz görev yok.")

# TAB 2: GANTT CHART
with tab2:
    st.header("📅 Gantt Chart")
    
    gantt_data = []
    for faz_adi, faz in fazlar.items():
        for gorev in faz['gorevler']:
            baslangic_tarih = proje_baslangic + timedelta(weeks=gorev['baslangic_hafta']-1)
            bitis_tarih = baslangic_tarih + timedelta(weeks=gorev['sure'])
            
            gantt_data.append({
                'Görev': f"{gorev['id']} - {gorev['gorev'][:40]}",
                'Başlangıç': baslangic_tarih.strftime('%Y-%m-%d'),
                'Bitiş': bitis_tarih.strftime('%Y-%m-%d'),
                'Faz': faz_adi,
                'Durum': gorev['durum'],
                'Sorumlu': gorev['sorumlu']
            })
    
    if gantt_data:
        df_gantt = pd.DataFrame(gantt_data)
        st.dataframe(df_gantt, use_container_width=True, hide_index=True)
        
        # CSV export
        csv = df_gantt.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Gantt Chart'ı CSV olarak İndir",
            csv,
            "oms_gantt_chart.csv",
            "text/csv",
            use_container_width=True
        )

# TAB 3: DÜZENLE
with tab3:
    st.header("✏️ Görev Düzenle")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        faz_sec = st.selectbox("Faz Seçin", list(fazlar.keys()), key="edit_faz_select")
    
    with col2:
        if fazlar[faz_sec]['gorevler']:
            gorev_listesi = [f"{g['id']} - {g['gorev']}" for g in fazlar[faz_sec]['gorevler']]
            gorev_sec = st.selectbox("Görev Seçin", gorev_listesi, key="edit_gorev_select")
            gorev_sec_id = gorev_sec.split(" - ")[0]
            
            gorev = next((g for g in fazlar[faz_sec]['gorevler'] if g['id'] == gorev_sec_id), None)
            
            if gorev:
                st.markdown("---")
                with st.form(f"edit_form_{gorev['id'].replace('.', '_')}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        yeni_gorev = st.text_input("Görev Adı", value=gorev['gorev'])
                        yeni_aciklama = st.text_area("Açıklama", value=gorev['aciklama'])
                        yeni_sure = st.number_input("Süre (hafta)", min_value=1, value=gorev['sure'])
                        yeni_bas_h = st.number_input("Başlangıç Haftası", min_value=1, value=gorev['baslangic_hafta'])
                    
                    with col2:
                        yeni_sorumlu = st.text_input("Sorumlu", value=gorev['sorumlu'])
                        yeni_oncelik = st.selectbox(
                            "Öncelik",
                            ["Kritik", "Yüksek", "Orta", "Düşük"],
                            index=["Kritik", "Yüksek", "Orta", "Düşük"].index(gorev['oncelik'])
                        )
                        yeni_durum = st.selectbox(
                            "Durum",
                            ["Planlandı", "Devam Ediyor", "Tamamlandı", "Beklemede"],
                            index=["Planlandı", "Devam Ediyor", "Tamamlandı", "Beklemede"].index(gorev['durum'])
                        )
                        yeni_id = st.text_input("ID", value=gorev['id'])
                    
                    col1, col2 = st.columns(2)
                    kaydet = col1.form_submit_button("💾 Kaydet", use_container_width=True)
                    sil = col2.form_submit_button("🗑️ Sil", use_container_width=True)
                    
                    if kaydet:
                        idx = next((i for i, g in enumerate(fazlar[faz_sec]['gorevler']) if g['id'] == gorev_sec_id), None)
                        if idx is not None:
                            st.session_state.proje_verileri[faz_sec]['gorevler'][idx] = {
                                'id': yeni_id,
                                'gorev': yeni_gorev,
                                'aciklama': yeni_aciklama,
                                'sure': yeni_sure,
                                'baslangic_hafta': yeni_bas_h,
                                'sorumlu': yeni_sorumlu,
                                'oncelik': yeni_oncelik,
                                'durum': yeni_durum
                            }
                            st.success("✅ Görev kaydedildi!")
                            st.rerun()
                    
                    if sil:
                        st.session_state.proje_verileri[faz_sec]['gorevler'] = [
                            g for g in fazlar[faz_sec]['gorevler'] if g['id'] != gorev_sec_id
                        ]
                        st.success(f"✅ Görev silindi!")
                        st.rerun()

# TAB 4: EKLE
with tab4:
    st.header("➕ Yeni Görev Ekle")
    
    with st.form("yeni_gorev"):
        hedef = st.selectbox("Hangi Faza Eklenecek?", list(fazlar.keys()))
        
        col1, col2 = st.columns(2)
        with col1:
            yeni_id = st.text_input("Görev ID", placeholder="Örn: 1.10")
            yeni_gorev = st.text_input("Görev Adı")
            yeni_aciklama = st.text_area("Açıklama")
            yeni_sure = st.number_input("Süre (hafta)", min_value=1, value=1)
        
        with col2:
            yeni_bas_h = st.number_input("Başlangıç Haftası", min_value=1, value=1)
            yeni_sorumlu = st.text_input("Sorumlu")
            yeni_oncelik = st.selectbox("Öncelik", ["Kritik", "Yüksek", "Orta", "Düşük"])
            yeni_durum = st.selectbox("Durum", ["Planlandı", "Devam Ediyor", "Tamamlandı", "Beklemede"])
        
        if st.form_submit_button("➕ Görevi Ekle", use_container_width=True):
            if yeni_id and yeni_gorev:
                mevcut_idler = [g['id'] for g in fazlar[hedef]['gorevler']]
                if yeni_id in mevcut_idler:
                    st.error(f"⚠️ {yeni_id} ID'si zaten kullanılıyor!")
                else:
                    st.session_state.proje_verileri[hedef]['gorevler'].append({
                        'id': yeni_id,
                        'gorev': yeni_gorev,
                        'aciklama': yeni_aciklama,
                        'sure': yeni_sure,
                        'baslangic_hafta': yeni_bas_h,
                        'sorumlu': yeni_sorumlu,
                        'oncelik': yeni_oncelik,
                        'durum': yeni_durum
                    })
                    st.success(f"✅ Yeni görev eklendi!")
                    st.rerun()

# TAB 5: VERİ İŞLEMLERİ
with tab5:
    st.header("📥 Veri İşlemleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Dışa Aktar")
        
        json_data = json.dumps(st.session_state.proje_verileri, ensure_ascii=False, indent=2)
        st.download_button(
            "📥 JSON olarak İndir",
            json_data,
            "oms_proje_verileri.json",
            "application/json",
            use_container_width=True
        )
        
        tum_gorevler = []
        for faz_adi, faz in fazlar.items():
            for g in faz['gorevler']:
                tum_gorevler.append({'Faz': faz_adi, **g})
        
        df_export = pd.DataFrame(tum_gorevler)
        st.download_button(
            "📥 CSV olarak İndir",
            df_export.to_csv(index=False).encode('utf-8'),
            "oms_gorevler.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        st.subheader("📥 İçe Aktar")
        
        uploaded = st.file_uploader("JSON Dosyası Yükle", type=['json'])
        if uploaded:
            try:
                data = json.loads(uploaded.read())
                st.success("✅ Dosya okundu!")
                
                if st.button("✅ Veriyi Yükle", use_container_width=True):
                    st.session_state.proje_verileri = data
                    st.success("✅ Veriler güncellendi!")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Hata: {str(e)}")

# TAB 6: RAPORLAR
with tab6:
    st.header("📈 Proje Raporları")
    
    # Durum bazlı analiz
    durum_sayilari = {}
    for faz in fazlar.values():
        for gorev in faz['gorevler']:
            durum = gorev['durum']
            durum_sayilari[durum] = durum_sayilari.get(durum, 0) + 1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Görev Durumları")
        for durum, sayi in durum_sayilari.items():
            st.metric(durum, sayi)
    
    with col2:
        st.subheader("Faz Bazlı Görev Sayıları")
        for faz_adi, faz in fazlar.items():
            st.metric(faz_adi, len(faz['gorevler']))
    
    # Sorumlu bazlı görev dağılımı
    st.markdown("---")
    st.subheader("Sorumlu Bazlı Görev Dağılımı")
    
    sorumlu_gorevler = {}
    for faz in fazlar.values():
        for gorev in faz['gorevler']:
            sorumlu = gorev['sorumlu']
            if sorumlu not in sorumlu_gorevler:
                sorumlu_gorevler[sorumlu] = []
            sorumlu_gorevler[sorumlu].append(gorev['gorev'])
    
    for sorumlu, gorevler in sorumlu_gorevler.items():
        with st.expander(f"{sorumlu} - {len(gorevler)} görev"):
            for gorev in gorevler:
                st.write(f"• {gorev}")

st.markdown("---")
st.caption(f"🏪 OMS Tek Stok Projesi | CEO Projeleri 2026 | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
