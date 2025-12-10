# app.py
import streamlit as st
import pandas as pd
import extra
import finale

# ==============================
# CONFIG STREAMLIT
# ==============================
st.set_page_config(
    page_title="🍕 Pizza Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# BLOCCO PWA (aggiunto)
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
# CARICA ICONA SVG
# ==============================
def load_svg(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None

svg_icon = load_svg("pizza_slice.svg")

if svg_icon:
    st.sidebar.markdown(svg_icon, unsafe_allow_html=True)
else:
    st.sidebar.write("🍕")   # fallback


# ==============================
# CSS PER SIDEBAR E TITOLI
# ==============================
st.markdown(
    """
    <style>
    /* Sidebar più stretta */
    [data-testid="stSidebar"]{
        width: 180px;
    }

    /* Titolo principale compatto */
    h1 {
        font-size: 1.5rem !important;
        line-height: 1.1 !important;
        font-weight: 700 !important;
    }

    h2 {
        font-size: 1.15rem !important;
        margin-top: 0.15rem !important;
        margin-bottom: 0.15rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    if "aggiunta_extra" not in st.session_state:
        st.session_state.aggiunta_extra = None

    if "lista_aggiornata" not in st.session_state:
        st.session_state.lista_aggiornata = False

    if "calcola_teglie" not in st.session_state:
        st.session_state.calcola_teglie = False

    if "pagina" not in st.session_state:
        st.session_state.pagina = "home"

init_session()

# ==============================
# FUNZIONE RESET (Ricomincia)
# ==============================
def reset_app():
    st.session_state["ricetta"] = {
        "Farina (g)": 1000,
        "Acqua (g)": 800,
        "Salt (g)": 25,
        "Lievito fresco (g)": 8,
        "Olio evo (g)": 30,
        "Zucchero (g)": 10
    }

    st.session_state["extra"] = []
    st.session_state["aggiunta_extra"] = None
    st.session_state["lista_aggiornata"] = False
    st.session_state["calcola_teglie"] = False
    st.session_state["pagina"] = "home"

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

st.sidebar.button("Ricomincia", on_click=reset_app)

# ==============================
# PAGINE
# ==============================
if st.session_state.pagina == "home":

    # 🔵 MESSAGGIO DI BENVENUTO (PRIMA DEL TITOLO)
    st.markdown(
        """
        ### 🍕 Calcolatore Teglie di Pizza
        ## 👋 Benvenuta Terry!

        **Usa questo strumento per personalizzare gli ingredienti del tuo impasto perfetto e calcolare il numero di teglie risultanti.**

        Per gestire gli ingredienti, scegli:
        **"Si, voglio modificare"**  oppure **"No, continua"** per vedere la lista finale.

        Quando i pulsanti non sono visibili, scrolla in verticale.
        Se la sidebar non è visibile, clicca sulle **freccine ">>"** in alto a sinistra per visualizzare i pulsanti di navigazione.
        """
    )

    st.header("Ingredienti base (modificabili)")

    df_base = pd.DataFrame(list(st.session_state.ricetta.items()), columns=["Ingrediente", "Grammi"])
    edited_df = st.data_editor(df_base, num_rows="dynamic")

    # Aggiorna ricetta se modificata
    for _, row in edited_df.iterrows():
        st.session_state.ricetta[row["Ingrediente"]] = row["Grammi"]

    st.subheader("Vuoi modificare la lista degli ingredienti?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Si, voglio modificare", key="modifica_si"):
            st.session_state.pagina = "extra"
            st.rerun()

    with col2:
        if st.button("No, continua", key="modifica_no"):
            st.session_state.pagina = "finale"
            st.rerun()

elif st.session_state.pagina == "extra":
    extra.show_extra()

elif st.session_state.pagina == "finale":
    finale.show_finale()
