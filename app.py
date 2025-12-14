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
# BLOCCO PWA (informativo – Streamlit Cloud ignora manifest custom)
# ==============================
col_icon, col_title = st.columns([1, 10], vertical_alignment="center")

with col_icon:
    st.image("assets/pizza_slice.png", width=48)

with col_title:
    st.markdown("### Calcolatore Teglie di Pizza")

st.markdown("#### 👋 Benvenuta Terry!")

st.markdown(
    """
    **Usa questo strumento per personalizzare gli ingredienti del tuo impasto perfetto
    e calcolare il numero di teglie risultanti.**

    Per gestire gli ingredienti, scegli:
    **\"Sì, voglio modificare\"** oppure **\"No, continua\"** per vedere la lista finale.

    Quando i pulsanti non sono visibili, scorri in verticale.
    Se la sidebar non è visibile, clicca sulle **frecce “>>”** in alto a sinistra.
    """
)


# ==============================
# ICONA SIDEBAR
# ==============================
st.sidebar.image(
    "assets/pizza_slice.png",
    width=90
)

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
# FUNZIONE RESET
# ==============================
def reset_app():
    st.session_state["ricetta"] = {
        "Farina (g)": 1000,
        "Acqua (g)": 800,
        "Sale (g)": 25,
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

    # TITOLO CON ICONA
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px;">
            <img src="assets/pizza_slice.png" width="48">
            <h3 style="margin:0;">Calcolatore Teglie di Pizza</h3>
        </div>
        <h4>👋 Benvenuta Terry!</h4>

        <p>
        <strong>Usa questo strumento per personalizzare gli ingredienti del tuo impasto perfetto
        e calcolare il numero di teglie risultanti.</strong>
        </p>

        <p>
        Per gestire gli ingredienti, scegli:
        <strong>"Sì, voglio modificare"</strong> oppure
        <strong>"No, continua"</strong> per vedere la lista finale.
        </p>

        <p>
        Quando i pulsanti non sono visibili, scorri in verticale.
        Se la sidebar non è visibile, clicca sulle <strong>frecce “>>”</strong> in alto a sinistra.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.header("Ingredienti base (modificabili)")

    df_base = pd.DataFrame(
        list(st.session_state.ricetta.items()),
        columns=["Ingrediente", "Grammi"]
    )

    edited_df = st.data_editor(df_base, num_rows="dynamic")

    for _, row in edited_df.iterrows():
        st.session_state.ricetta[row["Ingrediente"]] = row["Grammi"]

    st.subheader("Vuoi modificare la lista degli ingredienti?")
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
