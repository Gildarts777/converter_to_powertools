import streamlit as st
import pandas as pd
import io
import streamlit_analytics2 as streamlit_analytics  # <--- NOTA IL '2' QUI

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Converter x Dany", page_icon="❤️")

# --- ZONA LOGICA ---
def elabora_dati(df_ini):
    final_columns = ['cardmarketId', 'quantity', 'name', 'set', 'setCode', 'cn', "condition",
            'language', 'isFirstEd', 'isReverseHolo', 'isSigned', 'oldPrice',
            'price', 'comment', 'location', 'nameDE', 'nameES', 'nameFR', 'nameIT',
            'rarity', 'listedAt']

    df_fin = pd.DataFrame(data={}, columns=final_columns)
    
    column_from = ["Quantity", 'Card Name', 'Set Name', 'Set Code', 'Card Number','Condition', "Language"]
    
    # Controllo colonne
    missing = [c for c in column_from if c not in df_ini.columns]
    if missing:
        st.error(f"Mancano queste colonne nel CSV: {missing}")
        return None

    column_to = ["quantity", 'name', "set", 'setCode', 'cn', "condition", "language"]

    df_fin[column_to] = df_ini[column_from]
    df_fin["cn"] = df_fin["cn"].astype(str).str.zfill(3)

    diz_condizioni = {
        "Mint": "MT", "NearMint": "NM", "Excellent": "EX",
        "Good": "GD", "LightPlayed": "LP", "Played": "PL", "Poor": "PO"}

    df_fin["condition"] = df_fin["condition"].map(lambda x: diz_condizioni.get(x, x))
    
    if "Printing" in df_ini.columns:
        df_fin["isReverseHolo"] = df_ini["Printing"].values == 'Reverse Holo'
    else:
        df_fin["isReverseHolo"] = False
        
    return df_fin

# --- ZONA INTERFACCIA CON TRACCIAMENTO ---
# Qui inizia il tracciamento
with streamlit_analytics.track():
    st.title("Convertitore CSV 🚀")
    st.write("Carica il file di PokèCard, ricevi quello per PowerTools.")

    # Widget per caricare il file
    uploaded_file = st.file_uploader("Scegli il file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Legge il file caricato
            df_input = pd.read_csv(uploaded_file, skiprows=1)
            
            # Elabora
            df_output = elabora_dati(df_input)
            
            if df_output is not None:
                st.success("Conversione riuscita! ✅")
                
                # Anteprima (opzionale)
                with st.expander("Vedi anteprima dati"):
                    st.dataframe(df_output.head())
                
                # Prepara il file per il download
                csv_buffer = df_output.to_csv(index=False).encode('utf-8')
                
                # Nome file originale
                original_name = uploaded_file.name.replace(".csv", "")
                new_name = f"{original_name}_to_powertools.csv"
                
                # Bottone Download
                st.download_button(
                    label="📥 SCARICA FILE CONVERTITO",
                    data=csv_buffer,
                    file_name=new_name,
                    mime="text/csv",
                    type="primary" 
                )
                
        except Exception as e:
            st.error(f"Errore nella lettura del file: {e}")

    # Info box
    with st.sidebar:
        st.info("**Istruzioni**\n\n1. Carica il file.\n2. Aspetta la spunta verde.\n3. Premi scarica.")
