import os
import io
from dotenv import load_dotenv
import streamlit as st
from google import genai
from google.genai import types

# Charger la clé API
load_dotenv()

# Initialiser le client
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

def extract_text(file):
    """
    Extrait le texte d'un PDF.
    - PDF textuel → extraction simple
    - PDF scanné → Gemini Vision
    """
    try:
        # Lire le contenu
        file_bytes = file.read()
        
        # MÉTHODE 1 : PDF textuel (rapide)
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"
            
            if text.strip():
                st.success("✅ Texte extrait directement du PDF")
                return text.strip()
        except:
            pass
        
        # MÉTHODE 2 : PDF scanné → Gemini Vision
        st.info("🔄 PDF scanné - Lecture avec Gemini...")
        
        # Upload du fichier
        uploaded_file = client.files.upload(
            file=io.BytesIO(file_bytes),
            config=types.UploadFileConfig(
                display_name="CV",
                mime_type="application/pdf"
            )
        )
        
        # Prompt
        prompt = """
        Extrais TOUT le texte de ce CV scanné.
        Structure proprement avec les sections :
        - Informations personnelles
        - Expériences professionnelles
        - Formation
        - Compétences
        - Langues
        """
        
        # Envoyer la requête
        response = client.models.generate_content(
            model='gemini-2.5-flash',  #  Modèle valide
            contents=[
                prompt,
                uploaded_file
            ]
        )
        
        # Nettoyer
        client.files.delete(name=uploaded_file.name)
        
        st.success("✅ Texte extrait avec Gemini Vision")
        return response.text
        
    except Exception as e:
        return f"❌ Erreur: {str(e)}"