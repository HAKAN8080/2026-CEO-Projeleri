import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import hashlib

st.set_page_config(page_title="Alokasyon Optimizasyonu", layout="wide", page_icon="📦")

# ==============================================
# KULLANICI YETKİLENDİRME
# ==============================================

USERS = {
    "ceo": {"password": hashlib.sha256("ceo2026".encode()).hexdigest(), "role": "ceo", "name": "CEO", "title": "Genel Mudur"},
    "hakan": {"password": hashlib.sha256("proje2026".encode()).hexdigest(), "role": "project_manager", "name": "Hakan Ugur", "title": "Proje Yoneticisi"},
    "demo": {"password": hashlib.sha256("demo2026".encode()).hexdigest(), "role": "viewer", "name": "Demo Kullanici", "title": "Misafir"}
}

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.user_info = None
    if st.session_state.authenticated:
        return True
    st.markdown("""
    <div style="text-align:center;padding:40px;">
        <div style="font-size:4rem;">📦</div>
        <h1 style="background:linear-gradient(135deg,#f093fb,#f5576c);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Alokasyon Optimizasyonu</h1>
    </div>
    """, unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login"):
            username = st.text_input("Kullanici Adi")
            password = st.text_input("Sifre", type="password")
            if st.form_submit_button("Giris Yap", use_container_width=True):
                hashed = hashlib.sha256(password.encode()).hexdigest()
                if username in USERS and USERS[username]["password"] == hashed:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.user_info = USERS[username]
                    st.rerun()
                else:
                    st.error("Hatali giris!")
    return False

# ==============================================
# PROJE VERİLERİ - BOS SABLON
# ==============================================

def get_default_project_data():
    return {
        "FAZ 1: ORNEK FAZ": {
            "baslangic": 1,
            "sure": 4,
            "renk": "#f093fb",
            "emoji": "🔴",
            "durum": "Planlandı",
            "gorevler": [
                {"id": "A1.1", "gorev": "Ornek gorev 1", "aciklama": "Aciklama", "sure": 2, "baslangic_hafta": 1, "sorumlu": "Sorumlu", "oncelik": "Kritik", "durum": "Planlandı"},
                {"id": "A1.2", "gorev": "Ornek gorev 2", "aciklama": "Aciklama", "sure": 2, "baslangic_hafta": 3, "sorumlu": "Sorumlu", "oncelik": "Yuksek", "durum": "Planlandı"}
            ]
        }
    }

# ==============================================
# GANTT CHART - EXCEL TARZI
# ==============================================

def render_gantt(fazlar):
    min_h, max_h = 999, 0
    for f in fazlar.values():
        for g in f['gorevler']:
            min_h = min(min_h, g['baslangic_hafta'])
            max_h = max(max_h, g['baslangic_hafta'] + g['sure'])
    haftalar = list(range(min_h, max_h + 1))

    def h2t(h): return datetime(2026, 1, 19) + timedelta(weeks=h-1)
    bugun = datetime.now()
    ref = datetime(2026, 1, 19)
    bh = max(1, ((bugun - ref).days // 7) + 1)

    st.markdown("""<style>
    .gt{border-collapse:collapse;font-size:11px;width:100%}
    .gt th,.gt td{border:1px solid #ddd;padding:6px 3px;text-align:center}
    .gt th{background:#f5f5f5;font-weight:600}
    .gt .tk{text-align:left;min-width:200px;max-width:280px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .gt .fh{background:#e3f2fd;font-weight:700}
    .gb{border-radius:2px;height:18px}
    .tc{background:#fff9c4!important}
    </style>""", unsafe_allow_html=True)

    html = '<div style="overflow-x:auto"><table class="gt"><tr><th class="tk">Gorev</th><th>ID</th><th>Sorumlu</th><th>H</th>'
    for h in haftalar:
        t = h2t(h)
        tc = ' tc' if h == bh else ''
        html += f'<th class="{tc}"><div style="font-size:10px">{h}</div><div style="font-size:8px;color:#888">{t.strftime("%d.%m")}</div></th>'
    html += '</tr>'

    for fn, f in fazlar.items():
        html += f'<tr class="fh"><td colspan="4">{f["emoji"]} {fn}</td>'
        for h in haftalar:
            tc = ' tc' if h == bh else ''
            html += f'<td class="{tc}"></td>'
        html += '</tr>'
        for g in f['gorevler']:
            html += f'<tr><td class="tk" title="{g["gorev"]}">{g["gorev"][:40]}</td><td>{g["id"]}</td><td style="font-size:10px">{g["sorumlu"][:15]}</td><td>{g["sure"]}</td>'
            for h in haftalar:
                tc = ' tc' if h == bh else ''
                if g['baslangic_hafta'] <= h < g['baslangic_hafta'] + g['sure']:
                    html += f'<td class="{tc}"><div class="gb" style="background:{f["renk"]}"></div></td>'
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

if "alokasyon_verileri" not in st.session_state:
    st.session_state.alokasyon_verileri = get_default_project_data()

fazlar = st.session_state.alokasyon_verileri

col1, col2 = st.columns([3, 1])
with col1:
    st.title("📦 Alokasyon Optimizasyonu")
    st.caption("2026 CEO Projeleri - Proje #2")
with col2:
    ui = st.session_state.user_info
    st.markdown(f'<div style="text-align:right;padding:10px;background:linear-gradient(135deg,#f093fb,#f5576c);border-radius:10px;color:white"><b>{ui["name"]}</b><br><small>{ui["title"]}</small></div>', unsafe_allow_html=True)

if st.button("Cikis"):
    st.session_state.authenticated = False
    st.rerun()

st.markdown("---")

# Ozet
tg = sum([len(f['gorevler']) for f in fazlar.values()])
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faz", len(fazlar))
col2.metric("Gorev", tg)
col3.metric("Baslangic", "19.01.2026")
col4.metric("Bitis", "01.06.2026")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📅 Gantt Chart", "📋 Gorevler", "✏️ Duzenle", "📥 Veri"])

with tab1:
    st.header("📅 Gantt Chart")
    render_gantt(fazlar)

with tab2:
    st.header("📋 Gorev Listesi")
    for fn, f in fazlar.items():
        with st.expander(f'{f["emoji"]} {fn}', expanded=True):
            if f['gorevler']:
                df = pd.DataFrame(f['gorevler'])[['id','gorev','sorumlu','oncelik','durum','baslangic_hafta','sure']]
                st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.header("✏️ Gorev Duzenle")

    # Yeni Faz Ekle
    st.subheader("Yeni Faz Ekle")
    with st.form("yeni_faz"):
        yf_ad = st.text_input("Faz Adi", placeholder="FAZ X: Faz Adi")
        yf_renk = st.color_picker("Renk", "#f093fb")
        yf_emoji = st.selectbox("Emoji", ["🔴","🟠","🟡","🟢","🔵","🟣"])
        if st.form_submit_button("Faz Ekle"):
            if yf_ad and yf_ad not in fazlar:
                st.session_state.alokasyon_verileri[yf_ad] = {"baslangic":1,"sure":4,"renk":yf_renk,"emoji":yf_emoji,"durum":"Planlandı","gorevler":[]}
                st.success("Faz eklendi!")
                st.rerun()

    st.markdown("---")

    # Gorev Ekle/Duzenle
    st.subheader("Gorev Ekle")
    faz_sec = st.selectbox("Faz Sec", list(fazlar.keys()))
    with st.form("yeni_gorev"):
        c1, c2 = st.columns(2)
        with c1:
            g_id = st.text_input("ID", placeholder="A1.1")
            g_gorev = st.text_input("Gorev Adi")
            g_sure = st.number_input("Sure (hafta)", min_value=1, value=2)
            g_bas = st.number_input("Baslangic Haftasi", min_value=1, value=1)
        with c2:
            g_sorumlu = st.text_input("Sorumlu")
            g_oncelik = st.selectbox("Oncelik", ["Kritik","Yuksek","Orta","Dusuk"])
            g_durum = st.selectbox("Durum", ["Planlandı","Devam Ediyor","Tamamlandi"])
            g_aciklama = st.text_input("Aciklama")
        if st.form_submit_button("Gorev Ekle"):
            if g_id and g_gorev:
                st.session_state.alokasyon_verileri[faz_sec]['gorevler'].append({
                    "id":g_id,"gorev":g_gorev,"aciklama":g_aciklama,"sure":g_sure,
                    "baslangic_hafta":g_bas,"sorumlu":g_sorumlu,"oncelik":g_oncelik,"durum":g_durum
                })
                st.success("Gorev eklendi!")
                st.rerun()

with tab4:
    st.header("📥 Veri Islemleri")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("JSON Indir", json.dumps(st.session_state.alokasyon_verileri, ensure_ascii=False, indent=2), "alokasyon.json", "application/json", use_container_width=True)
    with c2:
        up = st.file_uploader("JSON Yukle", type=['json'])
        if up:
            data = json.loads(up.read())
            if st.button("Yukle"):
                st.session_state.alokasyon_verileri = data
                st.rerun()

st.markdown("---")
st.caption(f"📦 Alokasyon | 2026 CEO Projeleri | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
