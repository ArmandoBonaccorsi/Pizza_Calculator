# APP.PY — Versione A (Mobile Ottimizzato)
import streamlit as st
import pandas as pd

# ==============================
# STREAMLIT CONFIG
# ==============================
st.set_page_config(
    page_title="🍕 Pizza Calculator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# SESSION STATE INITIALIZATION
# ==============================
if "ricetta" not in st.session_state:
    st.session_state.ricetta = {
        "Farina (g)": 1000,
        "Acqua (g)": 800,
        "Sale (g)": 25,
        "Lievito fresco (g)": 8,
        "Olio evo (g)": 30,
        "Sugna (g)": 50,
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

# ==============================
# CSS MOBILE COMPATTO (VERSIONE A)
# ==============================
st.markdown(
    """
    <style>

    /* Riduzione padding globale */
    .block-container {
        padding-top: 1.1rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }

    /* Titolo leggibile e maiuscole non smozzicate */
    h1 {
        font-size: 1.55rem !important;
        line-height: 1.25 !important;
        overflow: visible !important;
        margin-bottom: 0.3rem !important;
        font-weight: 700 !important;
    }

    h2, h3 {
        font-size: 1.15rem !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Bottoni grandi per smartphone */
    .stButton>button {
        width: 100% !important;
        padding: 0.9rem 1rem !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
        margin-top: 0.3rem !important;
        margin-bottom: 0.3rem !important;
    }

    /* Data editor più compatto */
    .stDataFrame, .stDataEditor {
        font-size: 0.9rem !important;
    }

    /* Media query per smartphone */
    @media (max-width: 600px) {

        h1 {
            font-size: 1.45rem !important;
        }

        .stButton>button {
            padding: 1rem !important;
            font-size: 1.15rem !important;
        }

        .stDataFrame, .stDataEditor {
            font-size: 0.85rem !important;
        }

        .stTextInput>div>div>input {
            font-size: 1.1rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================
# FUNZIONI
# ==============================
def mostra_ingredienti(ricetta):
    df = pd.DataFrame(list(ricetta.items()), columns=["Ingrediente", "Grammi"])
    st.data_editor(df, disabled=True)
    st.subheader(f"Peso totale impasto: {sum(ricetta.values())} g")

def aggiorna_ricetta_da_tabella(df):
    for _, row in df.iterrows():
        st.session_state.ricetta[row["Ingrediente"]] = row["Grammi"]

def aggiungi_ingrediente_extra(nome, grammi):
    if nome.strip() != "":
        st.session_state.extra.append({"nome": nome, "grammi": grammi})
        st.session_state.aggiunta_extra = None
        st.rerun()
    else:
        st.warning("Inserisci un nome valido.")

def aggiorna_ricetta_finale():
    for ingr in st.session_state.extra:
        st.session_state.ricetta[f"{ingr['nome']} (g)"] = ingr["grammi"]
    st.session_state.lista_aggiornata = True
    st.rerun()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("Configurazione teglia")

forma = st.sidebar.radio("Forma teglia", ["Rotonda", "Rettangolare"])

if forma == "Rotonda":
    diametro = st.sidebar.number_input("Diametro (cm)", 10.0, value=30.0)
    larghezza = lunghezza = None
else:
    larghezza = st.sidebar.number_input("Larghezza (cm)", 10.0, value=30.0)
    lunghezza = st.sidebar.number_input("Lunghezza (cm)", 10.0, value=40.0)
    diametro = None

metodo = st.sidebar.radio(
    "Calcolo basato su:",
    ["Spessore impasto", "Densità impasto"]
)

if metodo == "Spessore impasto":
    spessore = st.sidebar.number_input("Spessore (mm)", min_value=5, value=8)
    densita = 0.55
else:
    densita = st.sidebar.number_input("Densità (g/cm³)", 0.1, value=0.55)
    spessore = None

st.sidebar.markdown("---")

if st.sidebar.button("Calcola numero teglie"):
    st.session_state.calcola_teglie = True

st.sidebar.markdown("---")

if st.sidebar.button("Ricomincia"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# ==============================
# MAIN
# ==============================
st.title("🍕 Calcolatore Ingredienti Pizza")

if not st.session_state.lista_aggiornata:

    st.header("Ingredienti di base (modificabili)")

    base_df = pd.DataFrame(list(st.session_state.ricetta.items()), columns=["Ingrediente", "Grammi"])
    edited_df = st.data_editor(base_df, num_rows="dynamic")
    aggiorna_ricetta_da_tabella(edited_df)

    st.subheader("Vuoi aggiungere o rimuovere ingredienti?")

    if st.button("Sì, voglio modificare"):
        st.session_state.aggiunta_extra = True

    if st.button("No, continua"):
        st.session_state.aggiunta_extra = False
        aggiorna_ricetta_finale()

    if st.session_state.aggiunta_extra:
        st.subheader("Aggiungi ingrediente extra")
        nome = st.text_input("Nome ingrediente", key="nome_extra")
        grammi = st.number_input("Grammi", min_value=1, value=10, key="grammi_extra")
        st.button("Aggiungi ingrediente", type="primary", on_click=lambda: aggiungi_ingrediente_extra(nome, grammi))

        st.subheader("Rimuovi ingrediente")
        ingrediente_rimuovi = st.selectbox(
            "Seleziona ingrediente da rimuovere",
            list(st.session_state.ricetta.keys()),
            key="select_remove"
        )
        if st.button("Rimuovi ingrediente", type="primary"):
            if ingrediente_rimuovi in st.session_state.ricetta:
                del st.session_state.ricetta[ingrediente_rimuovi]
                st.rerun()

# ==============================
# LISTA INGREDIENTI FINALE
# ==============================
if st.session_state.lista_aggiornata:
    st.header("🍕 Lista Ingredienti Finale 🍕")
    mostra_ingredienti(st.session_state.ricetta)

# ==============================
# CALCOLO TEGLIE
# ==============================
if st.session_state.calcola_teglie and st.session_state.lista_aggiornata:

    st.header("📐 Risultato calcolo teglie")

    peso_totale = sum(st.session_state.ricetta.values())

    if forma == "Rotonda":
        r = diametro / 2
        area = 3.14159 * r * r
    else:
        area = larghezza * lunghezza

    if metodo == "Spessore impasto":
        volume = area * (spessore / 10)
        peso_teglia = volume * densita
    else:
        peso_teglia = area * densita

    numero = peso_totale / peso_teglia

    st.write(f"**Numero teglie:** {numero:.2f}")
    st.write(f"**Peso impasto per teglia:** {peso_teglia:.0f} g")
