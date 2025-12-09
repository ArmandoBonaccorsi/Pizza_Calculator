# =========================================
# pages/1_extra.py – Aggiunta / rimozione
# =========================================
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Ingredienti Extra")

# init stato extra
if "extra" not in st.session_state:
    st.session_state.extra = []

# CSS MOBILE
st.markdown("""
<style>
h1 { font-size: 1.6rem !important; }
.stButton>button {
    width: 100%;
    padding: 0.9rem;
    border-radius: 10px;
    font-size: 1.15rem;
}
</style>
""", unsafe_allow_html=True)

# ===========
# Title
# ===========
st.title("➕ Ingredienti Extra")

# ==============
# Aggiunta extra
# ==============
st.subheader("Aggiungi ingrediente")
col1, col2 = st.columns([2,1])

with col1:
    nome = st.text_input("Nome ingrediente")

with col2:
    grammi = st.number_input("Grammi", min_value=1, value=10)

if st.button("Aggiungi"):
    if nome.strip() != "":
        st.session_state.extra.append({"nome": nome, "grammi": grammi})
        st.rerun()
    else:
        st.warning("Inserisci un nome valido.")

# ============
# Rimozione
# ============
st.subheader("Rimuovi ingrediente")

lista_totale = list(st.session_state.ricetta.keys()) + [e["nome"] for e in st.session_state.extra]

if lista_totale:
    ingr_da_rimuovere = st.selectbox("Ingredienti disponibili", lista_totale)

    if st.button("Rimuovi selezionato"):
        # rimuove da base
        if ingr_da_rimuovere in st.session_state.ricetta:
            del st.session_state.ricetta[ingr_da_rimuovere]

        # rimuove da extra
        st.session_state.extra = [e for e in st.session_state.extra if e["nome"] != ingr_da_rimuovere]

        st.rerun()

# ==================
# PULSANTE CONTINUA
# ==================
if st.button("Conferma e continua"):
    # applica extra alla ricetta
    for e in st.session_state.extra:
        st.session_state.ricetta[f"{e['nome']} (g)"] = e["grammi"]

    st.session_state.lista_finale = True
    st.switch_page("pages/2_finale.py")
