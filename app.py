# app.py
import streamlit as st
import pandas as pd
import extra
import finale

# ==============================
# CONFIG STREAMLIT
# ==============================
st.set_page_config(
    page_title="Pizza Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# BLOCCO PWA (best effort su Streamlit Cloud)
# ==============================
st.markdown("""
<link rel="manifest" href="/manifest.json">
<script>
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("/service-worker.js");
    });
  }
</script>
""", unsafe_allow_html=True)

# ==============================
# SIDEBAR ICONA
# ==============================
st.sidebar.image("assets/pizza_slice.png", width=120)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
[data-testid="stSidebar"] {
    width: 180px;
}
h1 {
    font-size: 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# INIZIALIZZAZIONE SESSION STATE
# ==============================
def init_session():
    if "ricetta" not in st.session_state:
        st.session_state.ricetta = {
            "Farina (g)": 1000,
            "Acqua (g)": 800,
            "Sale (g)": 25,
            "Lievito fresco (g)": 8,
            "Olio evo (g)": 30,
            "Zucchero (g)": 10
        }

    if "extra" not in st.session_state:
        st.session_state.extra = []

    if "pagina" not in st.session_state:
        st.session_state.pagina = "home"

init_session()

# ==============================
# TITOLO PRINCIPALE (UNICO)
# ==============================
col_icon, col_title = st.columns([1, 12], vertical_alignment="center")

with col_icon:
    st.image("assets/pizza_slice.png", width=42)

with col_title:
    st.markdown("## Calcolatore Teglie di Pizza")

# ==============================
# SIDEBAR NAVIGAZIONE
# ==============================
st.sidebar.title("Navigazione")

if st.sidebar.button("Home"):
    st.session_state.pagina = "home"
    st.rerun()

if st.sidebar.button("Ingredienti Extra"):
    st.session_state.pagina = "extra"
    st.rerun()

if st.sidebar.button("Lista finale ingredienti"):
    st.session_state.pagina = "finale"
    st.rerun()

st.sidebar.markdown("---")

# ==============================
# PAGINE
# ==============================
if st.session_state.pagina == "home":

    # 🔵 SOLO MESSAGGIO DI BENVENUTO (senza titolo duplicato)
    st.markdown("""
    ### 👋 Benvenuta Terry!

    **Usa questo strumento per personalizzare gli ingredienti del tuo impasto perfetto
    e calcolare il numero di teglie risultanti.**

    Per gestire gli ingredienti, scegli:
    **"Sì, voglio modificare"** oppure **"No, continua"** per vedere la lista finale.

    Quando i pulsanti non sono visibili, scorri in verticale.
    Se la sidebar non è visibile, clicca sulle freccine **">>"** in alto a sinistra.
    """)

    st.header("Ingredienti base (modificabili)")

    df_base = pd.DataFrame(
        list(st.session_state.ricetta.items()),
        columns=["Ingrediente", "Grammi"]
    )

    edited_df = st.data_editor(df_base, num_rows="dynamic")

    for _, row in edited_df.iterrows():
        st.session_state.ricetta[row["Ingrediente"]] = row["Grammi"]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Sì, voglio modificare"):
            st.session_state.pagina = "extra"
            st.rerun()

    with col2:
        if st.button("No, continua"):
            st.session_state.pagina = "finale"
            st.rerun()

elif st.session_state.pagina == "extra":
    extra.show_extra()

elif st.session_state.pagina == "finale":
    finale.show_finale()
