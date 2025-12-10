import streamlit as st
import pandas as pd

def show_finale():
    st.header("Lista Finale Ingredienti 🍕")

    df = pd.DataFrame(list(st.session_state.ricetta.items()), columns=["Ingrediente", "Grammi"])
    st.data_editor(df, disabled=True)
    st.subheader(f"Peso totale impasto: {sum(st.session_state.ricetta.values())} g")

    st.sidebar.header("Configurazione teglia")
    forma = st.sidebar.radio("Forma teglia", ["Rotonda", "Rettangolare"])

    if forma == "Rotonda":
        diametro = st.sidebar.number_input("Diametro (cm)", 10.0, value=30.0)
        larghezza = lunghezza = None
    else:
        larghezza = st.sidebar.number_input("Larghezza (cm)", 10.0, value=30.0)
        lunghezza = st.sidebar.number_input("Lunghezza (cm)", 10.0, value=40.0)
        diametro = None

    metodo = st.sidebar.radio("Calcolo basato su:", ["Spessore impasto", "Densità impasto"])

    if metodo == "Spessore impasto":
        spessore = st.sidebar.number_input("Spessore (mm)", min_value=5, value=8)
        densita = 0.55
    else:
        densita = st.sidebar.number_input("Densità (g/cm³)", 0.1, value=0.55)
        spessore = None

    st.sidebar.markdown("---")
    if st.sidebar.button("Calcola numero teglie"):
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

        st.subheader("📐 Risultato calcolo teglie")
        st.write(f"**Numero teglie:** {numero:.2f}")
        st.write(f"**Peso impasto per teglia:** {peso_teglia:.0f} g")
