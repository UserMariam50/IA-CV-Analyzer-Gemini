import os
import google as genai
from PIL import Image
import io
from pdf2image import convert_from_bytes
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv("GEMINI_KEY")

if not GOOGLE_API_KEY:
    print("⚠️ Attention: GEMINI_KEY non trouvée dans .env")

genai.configure(api_key=GOOGLE_API_KEY)

def extract_text_with_gemini(file_bytes):
    """
    Extrait le texte d'un PDF scanné avec Gemini Vision
    (Version de secours)
    """
    try:
        print("🔄 Conversion du PDF en images...")
        images = convert_from_bytes(file_bytes, dpi=150)
        print(f"📄 {len(images)} pages détectées")
        
        # Limiter à 5 pages
        if len(images) > 5:
            print(f"⚠️ Limité aux 5 premières pages sur {len(images)}")
            images = images[:5]
        
        #  Modèle valide
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        all_text = ""
        
        for i, img in enumerate(images):
            print(f"📖 Analyse page {i+1}/{len(images)} avec Gemini...")
            
            # Redimensionner
            img.thumbnail((1024, 1024))
            
            # Prompt
            prompt = f"""
            Extrais TOUT le texte de cette page de CV scanné (page {i+1}).
            
            Structure le résultat comme suit :
            - Informations personnelles (nom, prénom, email, téléphone, adresse)
            - Résumé / Objectif professionnel
            - Expériences professionnelles (avec dates et entreprises)
            - Formation / Diplômes (avec dates et établissements)
            - Compétences techniques
            - Langues
            - Centres d'intérêt
            
            Sois précis, ne manque aucune information.
            """
            
            # Appel API
            response = model.generate_content([
                prompt,
                img
            ])
            
            all_text += f"\n=== PAGE {i+1} ===\n"
            all_text += response.text
            all_text += "\n"
        
        return all_text
    
    except Exception as e:
        return f"❌ Erreur Gemini Vision: {str(e)}"