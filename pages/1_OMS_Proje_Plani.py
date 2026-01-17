import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib

st.set_page_config(page_title="OMS Proje Plani", layout="wide", page_icon="📦")

# ==============================================
# KULLANICI YETKİLENDİRME
# ==============================================

USERS = {
    "ceo": {
        "password": hashlib.sha256("ceo2026".encode()).hexdigest(),
        "role": "ceo",
        "name": "CEO",
        "title": "Genel Mudur"
    },
    "hakan": {
        "password": hashlib.sha256("proje2026".encode()).hexdigest(),
        "role": "project_manager",
        "name": "Hakan Ugur",
        "title": "Proje Yoneticisi"
    },
    "demo": {
        "password": hashlib.sha256("demo2026".encode()).hexdigest(),
        "role": "viewer",
        "name": "Demo Kullanici",
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
    .login-header { text-align: center; padding: 40px 0 30px; }
    .login-title {
        font-size: 2.5rem; font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-header">
        <div style="font-size: 4rem; margin-bottom: 20px;">📦</div>
        <div class="login-title">OMS Proje Plani</div>
        <div style="color: #666;">2026 CEO Projeleri</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Kullanici Adi")
            password = st.text_input("Sifre", type="password")
            login = st.form_submit_button("Giris Yap", use_container_width=True)
            if login:
                hashed = hashlib.sha256(password.encode()).hexdigest()
                if username in USERS and USERS[username]["password"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = USERS[username]
                    st.rerun()
                else:
                    st.error("Kullanici adi veya sifre hatali!")
    return False

# ==============================================
# PROJE VERİLERİ - Excel'den (5 FAZ)
# ==============================================

def get_default_project_data():
    """OMS Proje Plani - Excel'den alinan 5 Faz"""
    return {
        "FAZ 1: DAHA FAZLA TIP 1": {
            "baslangic": 1,
            "sure": 14,
            "renk": "#e74c3c",
            "emoji": "🔴",
            "durum": "Devam Ediyor",
            "gorevler": [
                {
                    "id": "F1.1",
                    "gorev": "Koli standartlarini gozden gecirerek TIP 1'e gecebilecek urunler incelenecek, tip1 tanimlama std gozden gecirilecek",
                    "aciklama": "Mevcut koli standartlarinin analizi ve TIP 1 donusum potansiyeli",
                    "sure": 8,
                    "baslangic_hafta": 1,
                    "sorumlu": "Fatih",
                    "oncelik": "Kritik",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F1.2",
                    "gorev": "Tip1 tanimlama standardinin gozden gecirilmesi",
                    "aciklama": "Tip 1 urun tanimlama kriterlerinin guncellenmesi",
                    "sure": 3,
                    "baslangic_hafta": 3,
                    "sorumlu": "Fatih",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "F1.3",
                    "gorev": "Ureticiden gonderim, konsinye siparis (MP ya da konsinye) ya da Market Place yonetimi konusunda proje gelistirilmesi",
                    "aciklama": "Alternatif tedarik ve satis kanallari projesi",
                    "sure": 14,
                    "baslangic_hafta": 2,
                    "sorumlu": "Gokhan / Emre / Fatih",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                }
            ]
        },
        "FAZ 2: AKYAZI MAKSIMUM STOK OPTIMIZASYONU": {
            "baslangic": 1,
            "sure": 4,
            "renk": "#e67e22",
            "emoji": "🟠",
            "durum": "Devam Ediyor",
            "gorevler": [
                {
                    "id": "F2.1",
                    "gorev": "Akyazi stok yonetim, RPT modeli (Guvenlik stogu, kalan stok nasil alinmali / sevkedilmeli)",
                    "aciklama": "Reorder Point modeli ve guvenlik stogu belirleme",
                    "sure": 4,
                    "baslangic_hafta": 1,
                    "sorumlu": "Gokhan / Ertugrul",
                    "oncelik": "Kritik",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F2.2",
                    "gorev": "Atik stok temizleme",
                    "aciklama": "Akyazi deposundaki atil stoklarin tasfiyesi",
                    "sure": 2,
                    "baslangic_hafta": 1,
                    "sorumlu": "Gokhan / Ertugrul",
                    "oncelik": "Yuksek",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F2.3",
                    "gorev": "Akyazi magazasina urun cikisi",
                    "aciklama": "Outlet magazaya stok transferi",
                    "sure": 2,
                    "baslangic_hafta": 1,
                    "sorumlu": "Gokhan / Ertugrul",
                    "oncelik": "Orta",
                    "durum": "Devam Ediyor"
                }
            ]
        },
        "FAZ 3: TIP1 HARIC GLM STOGUN SATISA ACILMASI": {
            "baslangic": 1,
            "sure": 16,
            "renk": "#9b59b6",
            "emoji": "🟣",
            "durum": "Devam Ediyor",
            "gorevler": [
                {
                    "id": "F3.1",
                    "gorev": "GLM depodan cikis mi yapilacak Akyaziya mi cekilecek karar verilmesi (Gecis yonetimi)",
                    "aciklama": "Depo stratejisi ve gecis plani karari",
                    "sure": 2,
                    "baslangic_hafta": 1,
                    "sorumlu": "Ertugrul / Gokhan",
                    "oncelik": "Kritik",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F3.2",
                    "gorev": "Tip 1 Akyaziya girmemesi",
                    "aciklama": "Tip 1 urunlerin Akyazi deposuna girisi engelleme",
                    "sure": 2,
                    "baslangic_hafta": 2,
                    "sorumlu": "Ertugrul / Gokhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "F3.3",
                    "gorev": "WMS algoritmasi calisilacak",
                    "aciklama": "Depo yonetim sistemi algoritma gelistirme",
                    "sure": 8,
                    "baslangic_hafta": 1,
                    "sorumlu": "Ertugrul / Ozcan",
                    "oncelik": "Kritik",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F3.4",
                    "gorev": "Siparisin cikis yerine gore musteriye terminlendirilmesi - musteri deneyimi",
                    "aciklama": "Musteri teslimat suresi optimizasyonu",
                    "sure": 12,
                    "baslangic_hafta": 1,
                    "sorumlu": "Gokhan / Ozcan",
                    "oncelik": "Yuksek",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F3.5",
                    "gorev": "STO'larin ayrismasi ve ayri tipte gelmesi, bunun onceliklendirilmesi",
                    "aciklama": "Stock Transfer Order yonetimi ve onceliklendirme",
                    "sure": 10,
                    "baslangic_hafta": 6,
                    "sorumlu": "Ertugrul / Ozcan",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "F3.6",
                    "gorev": "Acik adet kalan stogun yonetimi",
                    "aciklama": "Bozulmus koli ve acik adet stok yonetimi",
                    "sure": 4,
                    "baslangic_hafta": 12,
                    "sorumlu": "Ertugrul / Ferhat",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "F3.7",
                    "gorev": "Karma koli metodu analiz edilmeli",
                    "aciklama": "Farkli urunlerden koli olusturma metodolojisi",
                    "sure": 4,
                    "baslangic_hafta": 12,
                    "sorumlu": "Ertugrul",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                }
            ]
        },
        "FAZ 4: DAHA FAZLA / VERIMLI / OPTIMUM OMS": {
            "baslangic": 1,
            "sure": 14,
            "renk": "#f1c40f",
            "emoji": "🟡",
            "durum": "Devam Ediyor",
            "gorevler": [
                {
                    "id": "F4.1",
                    "gorev": "Mevcut Magaza Agi Analizi",
                    "aciklama": "Tum magazalarin OMS performans analizi",
                    "sure": 4,
                    "baslangic_hafta": 1,
                    "sorumlu": "Ertugrul + Gokhan + Volkan",
                    "oncelik": "Kritik",
                    "durum": "Devam Ediyor"
                },
                {
                    "id": "F4.2",
                    "gorev": "Personel ve Kargo Maliyet Modelleme",
                    "aciklama": "Magaza bazli maliyet modelleri olusturma",
                    "sure": 4,
                    "baslangic_hafta": 2,
                    "sorumlu": "Ertugrul + Gokhan + Finans",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.3",
                    "gorev": "Matematiksel Optimizasyon Modeli",
                    "aciklama": "OMS icin matematiksel optimizasyon",
                    "sure": 4,
                    "baslangic_hafta": 4,
                    "sorumlu": "Ertugrul + Gokhan",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.4",
                    "gorev": "Bolge Bazli Talep Analizi",
                    "aciklama": "Bolgesel talep tahmin modelleri",
                    "sure": 4,
                    "baslangic_hafta": 5,
                    "sorumlu": "Ertugrul + Gokhan + Pazarlama",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.5",
                    "gorev": "Istisna Magaza Belirleme",
                    "aciklama": "Ozel durum magazalarin tespiti",
                    "sure": 2,
                    "baslangic_hafta": 5,
                    "sorumlu": "Volkan + Ertugrul + Gokhan",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.6",
                    "gorev": "Yeni Magaza Acilis Senaryolari",
                    "aciklama": "Yeni magaza acilislari icin OMS plani",
                    "sure": 4,
                    "baslangic_hafta": 6,
                    "sorumlu": "Ertugrul + Gokhan + Finans",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.7",
                    "gorev": "ISO In-Store Ordering Urun Segmentasyonu",
                    "aciklama": "Magazadan siparis icin urun segmentasyonu",
                    "sure": 4,
                    "baslangic_hafta": 8,
                    "sorumlu": "Ertugrul + Gokhan + Volkan",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.8",
                    "gorev": "ISO/OMS Tesvik Mekanizmasi Tasarimi",
                    "aciklama": "Magaza personeli tesvik sistemi",
                    "sure": 4,
                    "baslangic_hafta": 8,
                    "sorumlu": "Volkan + Pazarlama + Finans",
                    "oncelik": "Orta",
                    "durum": "Planlandı"
                },
                {
                    "id": "F4.9",
                    "gorev": "Magazacilik ile El Sikisma Toplantilari",
                    "aciklama": "Magaza operasyonlari ile koordinasyon",
                    "sure": 2,
                    "baslangic_hafta": 12,
                    "sorumlu": "Ertugrul + Gokhan + Volkan",
                    "oncelik": "Yuksek",
                    "durum": "Planlandı"
                }
            ]
        },
        "FAZ 5: AKYAZI DEPO STOGUNUN TUM KANALLARA ACILMASI": {
            "baslangic": 12,
            "sure": 8,
            "renk": "#27ae60",
            "emoji": "🟢",
            "durum": "Planlandı",
            "gorevler": [
                {
                    "id": "F5.1",
                    "gorev": "Mumkunse gerek kalmayacak sekilde kalan stogun pratik yonetiminin adinin koyulmasi",
                    "aciklama": "Kalan stok icin pratik yonetim stratejisi belirleme",
                    "sure": 8,
                    "baslangic_hafta": 12,
                    "sorumlu": "Ertugrul / Gokhan / Ferhat",
                    "oncelik": "Kritik",
                    "durum": "Planlandı"
                }
            ]
        }
    }

# ==============================================
# GANTT CHART - EXCEL TARZI
# ==============================================

def render_excel_style_gantt(fazlar, proje_baslangic):
    """Excel tarzinda haftalik kutucuklu Gantt chart"""

    # Hafta araligini bul
    min_hafta = 999
    max_hafta = 0
    for faz in fazlar.values():
        for gorev in faz['gorevler']:
            min_hafta = min(min_hafta, gorev['baslangic_hafta'])
            max_hafta = max(max_hafta, gorev['baslangic_hafta'] + gorev['sure'])

    haftalar = list(range(min_hafta, max_hafta + 1))

    def hafta_to_tarih(hafta):
        # Hafta 1 = 19 Ocak 2026 (Excel'deki ilk tarih)
        return datetime(2026, 1, 19) + timedelta(weeks=hafta-1)

    # Bugunun haftasi
    bugun = datetime.now()
    ref_date = datetime(2026, 1, 19)
    bugun_hafta = max(1, ((bugun - ref_date).days // 7) + 1)

    # CSS
    st.markdown("""
    <style>
    .gantt-wrapper { overflow-x: auto; margin: 20px 0; }
    .gantt-tbl { border-collapse: collapse; font-size: 11px; width: 100%; }
    .gantt-tbl th, .gantt-tbl td { border: 1px solid #ddd; padding: 6px 3px; text-align: center; }
    .gantt-tbl th { background: #f5f5f5; font-weight: 600; position: sticky; top: 0; z-index: 10; }
    .gantt-tbl .g-task { text-align: left; min-width: 220px; max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .gantt-tbl .g-resp { min-width: 100px; font-size: 10px; color: #555; }
    .gantt-tbl .g-dur { min-width: 40px; font-weight: 600; }
    .gantt-tbl .g-wk { min-width: 32px; }
    .gantt-tbl .faz-hdr { background: #e3f2fd; font-weight: 700; font-size: 12px; }
    .g-bar { border-radius: 2px; height: 18px; }
    .wk-hdr { font-size: 10px; }
    .dt-hdr { font-size: 8px; color: #888; }
    .today-col { background: #fff9c4 !important; }
    </style>
    """, unsafe_allow_html=True)

    # HTML
    html = '<div class="gantt-wrapper"><table class="gantt-tbl">'

    # Header
    html += '<tr><th class="g-task">Gorev</th><th>ID</th><th class="g-resp">Sorumlu</th><th class="g-dur">H</th>'
    for h in haftalar:
        tarih = hafta_to_tarih(h)
        tc = ' today-col' if h == bugun_hafta else ''
        html += f'<th class="g-wk{tc}"><div class="wk-hdr">{h}</div><div class="dt-hdr">{tarih.strftime("%d.%m")}</div></th>'
    html += '</tr>'

    # Fazlar ve gorevler
    for faz_adi, faz in fazlar.items():
        # Faz header
        kisa_ad = faz_adi.split(":")[1].strip() if ":" in faz_adi else faz_adi
        html += f'<tr class="faz-hdr"><td colspan="4">{faz["emoji"]} FAZ {faz_adi.split(":")[0].replace("FAZ ", "")}: {kisa_ad[:40]}</td>'
        for h in haftalar:
            tc = ' today-col' if h == bugun_hafta else ''
            html += f'<td class="{tc}"></td>'
        html += '</tr>'

        # Gorevler
        for g in faz['gorevler']:
            html += '<tr>'
            html += f'<td class="g-task" title="{g["gorev"]}">{g["gorev"][:40]}...</td>'
            html += f'<td>{g["id"]}</td>'
            html += f'<td class="g-resp">{g["sorumlu"][:20]}</td>'
            html += f'<td class="g-dur">{g["sure"]}</td>'

            for h in haftalar:
                tc = ' today-col' if h == bugun_hafta else ''
                if g['baslangic_hafta'] <= h < g['baslangic_hafta'] + g['sure']:
                    html += f'<td class="{tc}"><div class="g-bar" style="background:{faz["renk"]}"></div></td>'
                else:
                    html += f'<td class="{tc}"></td>'
            html += '</tr>'

    html += '</table></div>'
    st.markdown(html, unsafe_allow_html=True)

# ==============================================
# ANA UYGULAMA
# ==============================================

if not check_password():
    st.stop()

if "oms_proje_verileri" not in st.session_state:
    st.session_state.oms_proje_verileri = get_default_project_data()

fazlar = st.session_state.oms_proje_verileri

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📦 OMS Proje Plani")
    st.caption("2026 CEO Projeleri - Proje #1")
with col2:
    user_info = st.session_state.user_info
    st.markdown(f"""
    <div style='text-align: right; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
        <div style='font-size: 0.9rem; font-weight: 600;'>{user_info['name']}</div>
        <div style='font-size: 0.8rem; opacity: 0.9;'>{user_info['title']}</div>
    </div>
    """, unsafe_allow_html=True)

if st.button("Cikis", key="logout"):
    st.session_state.authenticated = False
    st.rerun()

st.markdown("---")

# Proje ozeti
proje_baslangic = datetime(2026, 1, 19)
proje_bitis = datetime(2026, 6, 1)
bugun = datetime.now()

toplam_gorev = sum([len(faz['gorevler']) for faz in fazlar.values()])
devam_eden = sum([len([g for g in faz['gorevler'] if g['durum'] == 'Devam Ediyor']) for faz in fazlar.values()])

st.markdown("### Proje Ozeti")
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("Baslangic", "19.01.2026")
with col2:
    st.metric("Bitis", "01.06.2026")
with col3:
    kalan = (proje_bitis - bugun).days
    st.metric("Kalan Gun", f"{max(0, kalan)}")
with col4:
    st.metric("Faz", f"{len(fazlar)}")
with col5:
    st.metric("Gorev", f"{toplam_gorev}")
with col6:
    st.metric("Devam Eden", f"{devam_eden}")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Gantt Chart", "📋 Gorev Listesi", "✏️ Duzenle", "📥 Veri Islemleri", "📈 Raporlar"])

# TAB 1: GANTT
with tab1:
    st.header("📅 Gantt Chart - Excel Tarzi")

    # Legend
    st.markdown("**Faz Renkleri:**")
    cols = st.columns(len(fazlar))
    for i, (faz_adi, faz) in enumerate(fazlar.items()):
        with cols[i]:
            kisa = faz_adi.split(":")[0]
            st.markdown(f'<div style="display:flex;align-items:center;gap:5px;"><div style="width:16px;height:16px;background:{faz["renk"]};border-radius:2px;"></div><span style="font-size:11px;">{faz["emoji"]} {kisa}</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    render_excel_style_gantt(fazlar, proje_baslangic)

    ref_date = datetime(2026, 1, 19)
    bugun_hafta = max(1, ((bugun - ref_date).days // 7) + 1)
    st.info(f"📍 Bugun: {bugun.strftime('%d.%m.%Y')} - Hafta {bugun_hafta}")

# TAB 2: GOREV LISTESI
with tab2:
    st.header("📋 Proje Fazlari ve Gorevler")
    for faz_adi, faz in fazlar.items():
        with st.expander(f"{faz['emoji']} {faz_adi} ({len(faz['gorevler'])} gorev)", expanded=True):
            if faz['gorevler']:
                df = pd.DataFrame(faz['gorevler'])
                df = df[['id', 'gorev', 'sorumlu', 'oncelik', 'durum', 'baslangic_hafta', 'sure']]
                df.columns = ['ID', 'Gorev', 'Sorumlu', 'Oncelik', 'Durum', 'Baslangic', 'Sure']

                def style_row(row):
                    if row['Durum'] == 'Tamamlandi':
                        return ['background-color: #d4edda'] * len(row)
                    elif row['Durum'] == 'Devam Ediyor':
                        return ['background-color: #fff3cd'] * len(row)
                    return [''] * len(row)

                st.dataframe(df.style.apply(style_row, axis=1), use_container_width=True, hide_index=True)

# TAB 3: DUZENLE
with tab3:
    st.header("✏️ Gorev Duzenle")
    col1, col2 = st.columns([1, 2])
    with col1:
        faz_sec = st.selectbox("Faz Secin", list(fazlar.keys()), key="edit_faz")
    with col2:
        if fazlar[faz_sec]['gorevler']:
            gorev_list = [f"{g['id']} - {g['gorev'][:40]}" for g in fazlar[faz_sec]['gorevler']]
            gorev_sec = st.selectbox("Gorev Secin", gorev_list, key="edit_gorev")
            gorev_id = gorev_sec.split(" - ")[0]
            gorev = next((g for g in fazlar[faz_sec]['gorevler'] if g['id'] == gorev_id), None)

            if gorev:
                st.markdown("---")
                with st.form("edit_form"):
                    c1, c2 = st.columns(2)
                    with c1:
                        yeni_gorev = st.text_input("Gorev", value=gorev['gorev'])
                        yeni_aciklama = st.text_area("Aciklama", value=gorev['aciklama'])
                        yeni_sure = st.number_input("Sure (hafta)", min_value=1, value=gorev['sure'])
                        yeni_bas = st.number_input("Baslangic Haftasi", min_value=1, value=gorev['baslangic_hafta'])
                    with c2:
                        yeni_sorumlu = st.text_input("Sorumlu", value=gorev['sorumlu'])
                        oncelikler = ["Kritik", "Yuksek", "Orta", "Dusuk"]
                        yeni_oncelik = st.selectbox("Oncelik", oncelikler, index=oncelikler.index(gorev['oncelik']) if gorev['oncelik'] in oncelikler else 0)
                        durumlar = ["Planlandı", "Devam Ediyor", "Tamamlandi", "Beklemede"]
                        yeni_durum = st.selectbox("Durum", durumlar, index=durumlar.index(gorev['durum']) if gorev['durum'] in durumlar else 0)
                        yeni_id = st.text_input("ID", value=gorev['id'])

                    c1, c2 = st.columns(2)
                    if c1.form_submit_button("Kaydet", use_container_width=True):
                        idx = next((i for i, g in enumerate(fazlar[faz_sec]['gorevler']) if g['id'] == gorev_id), None)
                        if idx is not None:
                            st.session_state.oms_proje_verileri[faz_sec]['gorevler'][idx] = {
                                'id': yeni_id, 'gorev': yeni_gorev, 'aciklama': yeni_aciklama,
                                'sure': yeni_sure, 'baslangic_hafta': yeni_bas, 'sorumlu': yeni_sorumlu,
                                'oncelik': yeni_oncelik, 'durum': yeni_durum
                            }
                            st.success("Kaydedildi!")
                            st.rerun()
                    if c2.form_submit_button("Sil", use_container_width=True):
                        st.session_state.oms_proje_verileri[faz_sec]['gorevler'] = [g for g in fazlar[faz_sec]['gorevler'] if g['id'] != gorev_id]
                        st.success("Silindi!")
                        st.rerun()

# TAB 4: VERI ISLEMLERI
with tab4:
    st.header("📥 Veri Islemleri")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Disa Aktar")
        json_data = json.dumps(st.session_state.oms_proje_verileri, ensure_ascii=False, indent=2)
        st.download_button("JSON Indir", json_data, "oms_proje.json", "application/json", use_container_width=True)

        all_tasks = []
        for faz_adi, faz in fazlar.items():
            for g in faz['gorevler']:
                all_tasks.append({'Faz': faz_adi, **g})
        df_exp = pd.DataFrame(all_tasks)
        st.download_button("CSV Indir", df_exp.to_csv(index=False).encode('utf-8'), "oms_proje.csv", "text/csv", use_container_width=True)

    with col2:
        st.subheader("Ice Aktar")
        uploaded = st.file_uploader("JSON Yukle", type=['json'])
        if uploaded:
            try:
                data = json.loads(uploaded.read())
                st.success("Dosya okundu!")
                if st.button("Yukle", use_container_width=True):
                    st.session_state.oms_proje_verileri = data
                    st.success("Yuklendi!")
                    st.rerun()
            except Exception as e:
                st.error(f"Hata: {e}")

# TAB 5: RAPORLAR
with tab5:
    st.header("📈 Raporlar")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Durum Dagilimi")
        durum_say = {}
        for faz in fazlar.values():
            for g in faz['gorevler']:
                d = g['durum']
                durum_say[d] = durum_say.get(d, 0) + 1
        for d, s in durum_say.items():
            st.metric(d, s)

    with col2:
        st.subheader("Faz Bazli Gorevler")
        for faz_adi, faz in fazlar.items():
            kisa = faz_adi.split(":")[0]
            st.metric(kisa, len(faz['gorevler']))

    st.markdown("---")
    st.subheader("Sorumlu Dagilimi")
    sorumlu_gorev = {}
    for faz in fazlar.values():
        for g in faz['gorevler']:
            s = g['sorumlu']
            if s not in sorumlu_gorev:
                sorumlu_gorev[s] = []
            sorumlu_gorev[s].append(g['gorev'])

    cols = st.columns(2)
    for i, (s, gs) in enumerate(sorumlu_gorev.items()):
        with cols[i % 2]:
            with st.expander(f"{s} ({len(gs)} gorev)"):
                for gorev in gs:
                    st.write(f"• {gorev[:50]}...")

st.markdown("---")
st.caption(f"📦 OMS Proje Plani | 2026 CEO Projeleri | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
