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
    page_icon="assets/pizza_slice.png",  # ICONA APP / HOME SCREEN
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CSS PER SIDEBAR E TITOLI
# ==============================
st.markdown(
    """
    <style>
    [data-testid="stSidebar"]{
        width: 180px;
    }

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

    if "pagina" not in st.session_state:
        st.session_state.pagina = "home"

init_session()

# ==============================
# FUNZIONE RESET
# ==============================
def reset_app():
    st.session_state.ricetta = {
        "Farina (g)": 1000,
        "Acqua (g)": 800,
        "Sale (g)": 25,
        "Lievito fresco (g)": 8,
        "Olio evo (g)": 30,
        "Zucchero (g)": 10
    }
    st.session_state.extra = []
    st.session_state.pagina = "home"

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

    st.markdown(
        """
        ### 🍕 Calcolatore Teglie di Pizza
        ## 👋 Benvenuta Terry!

        **Usa questo strumento per personalizzare gli ingredienti del tuo impasto perfetto e calcolare il numero di teglie risultanti.**

        Scegli:
        **"Si, voglio modificare"** per gestire gli ingredienti  
        **"No, continua"** per vedere la lista finale.
        """
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
        if st.button("Si, voglio modificare"):
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
