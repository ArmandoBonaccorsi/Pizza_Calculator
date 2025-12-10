# extra.py
import streamlit as st
import pandas as pd

def add_and_return():
    nome = st.session_state.get("nome_nuovo_ing", "").strip()
    valore = st.session_state.get("valore_nuovo_ing", 0)
    if nome:
        key_name = f"{nome} (g)"
        st.session_state.ricetta[key_name] = valore
        st.session_state.extra.append({"nome": nome, "grammi": valore})
    st.session_state.pagina = "home"

def remove_and_return():
    torem = st.session_state.get("sel_rimuovi", "")
    if torem and torem in st.session_state.ricetta:
        del st.session_state.ricetta[torem]
    st.session_state.pagina = "home"

def show_extra():
    st.title("Gestione Ingredienti Extra")
    st.markdown("---")

    st.markdown(
        """
        <div id="add_box" style="
            width:48%;
            min-width:220px;
            border: 1.5px solid #1E8F39;
            border-radius: 10px;
            padding: 10px;
            background-color: #F6FFF7;
            margin-bottom: 12px;
            font-size:0.9rem;
        ">
            <h4 style="color:#1E8F39; margin:0 0 8px 0; font-weight:700;">➕ Aggiungi ingrediente</h4>
        """,
        unsafe_allow_html=True,
    )

    st.text_input("Nome nuovo ingrediente", key="nome_nuovo_ing")
    st.number_input("Grammi", min_value=1, value=10, key="valore_nuovo_ing")

    st.button("Conferma aggiungi", key="btn_add", on_click=add_and_return)

    st.markdown(
        """
        <style>
        #add_box button {
            color: #1E8F39 !important;
            background-color: #E8FFE9 !important;
            border: 1.5px solid #1E8F39 !important;
            border-radius: 6px !important;
            padding: .45rem .7rem !important;
            font-weight:700 !important;
        }
        #add_box h4 { font-size:0.95rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    st.markdown(
        """
        <div id="rem_box" style="
            width:48%;
            min-width:220px;
            border: 1.5px solid #C11A1A;
            border-radius: 10px;
            padding: 10px;
            background-color: #FFF6F6;
            margin-top: 10px;
            font-size:0.9rem;
        ">
            <h4 style="color:#C11A1A; margin:0 0 8px 0; font-weight:700;">➖ Rimuovi ingrediente</h4>
        """,
        unsafe_allow_html=True,
    )

    elenco = list(st.session_state.ricetta.keys())
    if elenco:
        st.selectbox("Seleziona ingrediente da eliminare", elenco, key="sel_rimuovi")
    else:
        st.write("Nessun ingrediente disponibile.")

    st.button("Conferma rimuovi", key="btn_remove", on_click=remove_and_return)

    st.markdown(
        """
        <style>
        #rem_box button {
            color: #C11A1A !important;
            background-color: #FFECEC !important;
            border: 1.5px solid #C11A1A !important;
            border-radius: 6px !important;
            padding: .45rem .7rem !important;
            font-weight:700 !important;
        }
        #rem_box h4 { font-size:0.95rem !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.info("Dopo conferma verrai riportato alla Home con la lista aggiornata.")
