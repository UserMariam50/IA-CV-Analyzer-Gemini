import streamlit as st
from utils.pdf_reader import extract_text
from utils.cv_parser import (
    detect_skills, 
    calculate_score, 
    extract_skills_auto, 
    get_skills_for_job,
    SKILLS_BY_DOMAIN
)
import json
from datetime import datetime

st.set_page_config(page_title="AI CV Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI CV Analyzer")

# Sidebar : Configuration de l'analyse
with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Mode d'analyse
    analysis_mode = st.radio(
        "🎯 Mode d'analyse :",
        [
            "🤖 Automatique (IA détecte le domaine)",
            "📂 Choisir un domaine prédéfini",
            "✏️ Saisir mon propre domaine",
            "📝 Mode personnalisé (tout manuel)"
        ]
    )
    
    domain = None
    custom_skills = None
    user_domain = None
    
    # Mode 1: Automatique
    if analysis_mode == "🤖 Automatique (IA détecte le domaine)":
        st.info("🔍 L'IA analysera le CV pour détecter le domaine automatiquement.")
        domain = None
        user_domain = None
    
    # Mode 2: Domaine prédéfini
    elif analysis_mode == "📂 Choisir un domaine prédéfini":
        domain = st.selectbox(
            "Domaine :",
            list(SKILLS_BY_DOMAIN.keys())
        )
        st.info(f"💡 Compétences pour {domain}:")
        st.write(", ".join(SKILLS_BY_DOMAIN[domain][:10]))
        user_domain = None
    
    # Mode 3: Saisir son propre domaine
    elif analysis_mode == "✏️ Saisir mon propre domaine":
        user_domain = st.text_input(
            "✏️ Entrez votre domaine :",
            placeholder="Ex: cybersécurité, génie civil, médecine, éducation..."
        )
        if user_domain:
            st.success(f"📌 Domaine saisi : {user_domain}")
            st.info("💡 Le domaine sera utilisé pour personnaliser l'analyse.")
        
        st.caption("Ajoutez des compétences spécifiques (optionnel) :")
        custom_skills_input = st.text_area(
            "Compétences (une par ligne) :",
            placeholder="Python\nSQL\nMachine Learning\n...",
            height=100
        )
        if custom_skills_input:
            custom_skills = [s.strip() for s in custom_skills_input.split("\n") if s.strip()]
            st.success(f"✅ {len(custom_skills)} compétences ajoutées")
    
    # Mode 4: Mode personnalisé
    elif analysis_mode == "📝 Mode personnalisé (tout manuel)":
        st.info("✏️ Vous gérez entièrement l'analyse.")
        
        user_domain = st.text_input(
            "✏️ Domaine :",
            placeholder="Ex: data_science, finance, marketing...",
            help="Entrez le domaine que vous voulez analyser"
        )
        
        st.caption("🔧 Compétences à rechercher :")
        custom_skills_input = st.text_area(
            "Liste des compétences (une par ligne) :",
            placeholder="Python\nSQL\nMachine Learning\nTensorFlow\n...",
            height=150
        )
        if custom_skills_input:
            custom_skills = [s.strip() for s in custom_skills_input.split("\n") if s.strip()]
            st.success(f"✅ {len(custom_skills)} compétences configurées")
        
        if user_domain and custom_skills:
            st.success("✅ Configuration terminée !")
            with st.expander("📋 Résumé de la configuration"):
                st.write(f"**Domaine :** {user_domain}")
                st.write(f"**Compétences :** {', '.join(custom_skills[:10])}")
    
    # Option : Poste recherché
    st.divider()
    job_role = st.text_input("🎯 Poste recherché (optionnel) :", placeholder="Data Scientist")
    if job_role:
        job_skills = get_skills_for_job(job_role)
        if job_skills:
            st.success(f"✅ Compétences recommandées pour {job_role} :")
            st.write(", ".join(job_skills[:10]))

# Upload
file = st.file_uploader("📤 Téléchargez votre CV (PDF)", type=["pdf"])

if file:
    with st.spinner("📖 Lecture du PDF..."):
        text = extract_text(file)
    
    if "❌" in text or "⚠️" in text:
        st.error(text)
    else:
        # ============ 🔥 SAUVEGARDE DES PARAMÈTRES UTILISATEUR ============
        # Ajoutez ce bloc ici
        if analysis_mode in ["✏️ Saisir mon propre domaine", "📝 Mode personnalisé (tout manuel)"]:
            user_config = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "mode": analysis_mode,
                "domain": user_domain if user_domain else "Non spécifié",
                "skills": custom_skills if custom_skills else [],
                "file_name": file.name if file else "Inconnu"
            }
            
            with open("user_skills.json", "w", encoding="utf-8") as f:
                json.dump(user_config, f, ensure_ascii=False, indent=2)
            print("✅ Configuration utilisateur sauvegardée dans user_skills.json")
        # ============ FIN SAUVEGARDE ============
        
        # Analyse des compétences
        with st.spinner("🔍 Analyse des compétences..."):
            if analysis_mode == "✏️ Saisir mon propre domaine" or analysis_mode == "📝 Mode personnalisé (tout manuel)":
                skills_result = detect_skills(
                    text, 
                    custom_skills=custom_skills, 
                    domain=domain,
                    user_domain=user_domain
                )
            elif analysis_mode == "📂 Choisir un domaine prédéfini":
                skills_result = detect_skills(text, domain=domain)
            else:
                skills_result = detect_skills(text)
            
            auto_skills = extract_skills_auto(text)
            required = get_skills_for_job(job_role) if job_role else None
            score = calculate_score(skills_result, required)
        
        # Affichage des résultats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🎯 Score", f"{score}/100")
        with col2:
            st.metric("💪 Compétences", len(skills_result["found"]))
        with col3:
            domain_display = skills_result["domain"].replace("_", " ").title()
            if skills_result.get("domain_type") == "manual":
                domain_display = f"✏️ {domain_display}"
            st.metric("📂 Domaine", domain_display)
        with col4:
            total_skills = len(skills_result.get("skills_list", []))
            st.metric("🔍 Compétences recherchées", total_skills)
        
        # Afficher la configuration utilisée
        if skills_result.get("user_provided_skills"):
            with st.expander("📝 Compétences personnalisées de l'utilisateur"):
                st.write(", ".join(skills_result["user_provided_skills"]))
        
        # Compétences trouvées
        st.subheader("🛠️ Compétences détectées dans le CV")
        if skills_result["found"]:
            cols = st.columns(4)
            for i, skill in enumerate(skills_result["found"][:20]):
                cols[i % 4].success(f"✅ {skill}")
            
            if len(skills_result["found"]) > 20:
                with st.expander(f"📋 Voir les {len(skills_result['found'])} compétences"):
                    cols = st.columns(4)
                    for i, skill in enumerate(skills_result["found"]):
                        cols[i % 4].success(f"✅ {skill}")
        else:
            st.warning("Aucune compétence détectée")
        
        # Compétences automatiques
        if auto_skills:
            with st.expander("🔍 Compétences supplémentaires détectées"):
                st.write(", ".join(auto_skills[:30]))
        
        # Compétences du domaine
        domain_skills = SKILLS_BY_DOMAIN.get(skills_result["domain"], [])
        if domain_skills:
            with st.expander(f"📊 Comparaison - Domaine {skills_result['domain'].replace('_', ' ').title()}"):
                found_domain = [s for s in domain_skills if s in skills_result["found"]]
                missing_domain = [s for s in domain_skills if s not in skills_result["found"]]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ Trouvées ({len(found_domain)}) :")
                    if found_domain:
                        st.write(", ".join(found_domain[:10]))
                    else:
                        st.write("Aucune")
                with col2:
                    st.warning(f"❌ Manquantes ({len(missing_domain)}) :")
                    if missing_domain:
                        st.write(", ".join(missing_domain[:10]))
                    else:
                        st.write("Toutes trouvées !")
        
        # Télécharger le rapport
        st.download_button(
            label="📥 Télécharger le rapport",
            data=f"=== RAPPORT CV ANALYZER ===\n\n"
                 f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"Score: {score}/100\n"
                 f"Domaine: {skills_result['domain']}\n"
                 f"Compétences trouvées: {', '.join(skills_result['found'])}\n"
                 f"Compétences personnalisées: {', '.join(skills_result.get('user_provided_skills', []))}\n"
                 f"Compétences manquantes: {', '.join(missing_domain[:10]) if domain_skills and missing_domain else 'Aucune'}\n",
            file_name="cv_analysis.txt",
            mime="text/plain"
        )

else:
    st.info("👆 Téléchargez un PDF pour commencer l'analyse")


# import streamlit as st
# from utils.pdf_reader import extract_text
# from utils.cv_parser import (
#     detect_skills, 
#     calculate_score, 
#     extract_skills_auto, 
#     get_skills_for_job,
#     SKILLS_BY_DOMAIN
# )

# st.set_page_config(page_title="AI CV Analyzer", page_icon="📄", layout="wide")

# st.title("📄 AI CV Analyzer")

# # Sidebar : Configuration de l'analyse
# with st.sidebar:
#     st.header("⚙️ Paramètres")
    
#     # NOUVELLE OPTION : Mode d'analyse
#     analysis_mode = st.radio(
#         "🎯 Mode d'analyse :",
#         [
#             "🤖 Automatique (IA détecte le domaine)",
#             "📂 Choisir un domaine prédéfini",
#             "✏️ Saisir mon propre domaine",
#             "📝 Mode personnalisé (tout manuel)"
#         ]
#     )
    
#     domain = None
#     custom_skills = None
#     user_domain = None
    
#     # Mode 1: Automatique
#     if analysis_mode == "🤖 Automatique (IA détecte le domaine)":
#         st.info("🔍 L'IA analysera le CV pour détecter le domaine automatiquement.")
#         domain = None
#         user_domain = None
    
#     # Mode 2: Domaine prédéfini
#     elif analysis_mode == "📂 Choisir un domaine prédéfini":
#         domain = st.selectbox(
#             "Domaine :",
#             list(SKILLS_BY_DOMAIN.keys())
#         )
#         # Afficher les compétences du domaine
#         st.info(f"💡 Compétences pour {domain}:")
#         st.write(", ".join(SKILLS_BY_DOMAIN[domain][:10]))
#         user_domain = None
    
#     # 🆕 Mode 3: Saisir son propre domaine
#     elif analysis_mode == "✏️ Saisir mon propre domaine":
#         user_domain = st.text_input(
#             "✏️ Entrez votre domaine :",
#             placeholder="Ex: cybersécurité, génie civil, médecine, éducation..."
#         )
#         if user_domain:
#             st.success(f"📌 Domaine saisi : {user_domain}")
#             st.info("💡 Le domaine sera utilisé pour personnaliser l'analyse.")
        
#         # Optionnel: ajouter des compétences pour ce domaine
#         st.caption("Ajoutez des compétences spécifiques (optionnel) :")
#         custom_skills_input = st.text_area(
#             "Compétences (une par ligne) :",
#             placeholder="Python\nSQL\nMachine Learning\n...",
#             height=100
#         )
#         if custom_skills_input:
#             custom_skills = [s.strip() for s in custom_skills_input.split("\n") if s.strip()]
#             st.success(f"✅ {len(custom_skills)} compétences ajoutées")
    
#     # Mode 4: Mode personnalisé
#     elif analysis_mode == "📝 Mode personnalisé (tout manuel)":
#         st.info("✏️ Vous gérez entièrement l'analyse.")
        
#         # Saisie du domaine
#         user_domain = st.text_input(
#             "✏️ Domaine :",
#             placeholder="Ex: data_science, finance, marketing...",
#             help="Entrez le domaine que vous voulez analyser"
#         )
        
#         # Saisie des compétences
#         st.caption("🔧 Compétences à rechercher :")
#         custom_skills_input = st.text_area(
#             "Liste des compétences (une par ligne) :",
#             placeholder="Python\nSQL\nMachine Learning\nTensorFlow\n...",
#             height=150
#         )
#         if custom_skills_input:
#             custom_skills = [s.strip() for s in custom_skills_input.split("\n") if s.strip()]
#             st.success(f"✅ {len(custom_skills)} compétences configurées")
        
#         # Afficher un résumé
#         if user_domain and custom_skills:
#             st.success("✅ Configuration terminée !")
#             with st.expander("📋 Résumé de la configuration"):
#                 st.write(f"**Domaine :** {user_domain}")
#                 st.write(f"**Compétences :** {', '.join(custom_skills[:10])}")
    
#     # Option : Poste recherché (pour les recommandations)
#     st.divider()
#     job_role = st.text_input("🎯 Poste recherché (optionnel) :", placeholder="Data Scientist")
#     if job_role:
#         job_skills = get_skills_for_job(job_role)
#         if job_skills:
#             st.success(f"✅ Compétences recommandées pour {job_role} :")
#             st.write(", ".join(job_skills[:10]))

# # Upload
# file = st.file_uploader("📤 Téléchargez votre CV (PDF)", type=["pdf"])

# if file:
#     with st.spinner("📖 Lecture du PDF..."):
#         text = extract_text(file)
    
#     if "❌" in text or "⚠️" in text:
#         st.error(text)
#     else:
#         # Analyse des compétences
#         with st.spinner("🔍 Analyse des compétences..."):
#             #  Paramètres pour detect_skills
#             if analysis_mode == "✏️ Saisir mon propre domaine" or analysis_mode == "📝 Mode personnalisé (tout manuel)":
#                 skills_result = detect_skills(
#                     text, 
#                     custom_skills=custom_skills, 
#                     domain=domain,
#                     user_domain=user_domain
#                 )
#             elif analysis_mode == "📂 Choisir un domaine prédéfini":
#                 skills_result = detect_skills(text, domain=domain)
#             else:
#                 skills_result = detect_skills(text)
            
#             # Extraction automatique
#             auto_skills = extract_skills_auto(text)
            
#             # Score
#             required = get_skills_for_job(job_role) if job_role else None
#             score = calculate_score(skills_result, required)
        
#         # Affichage des résultats
#         col1, col2, col3, col4 = st.columns(4)
#         with col1:
#             st.metric("🎯 Score", f"{score}/100")
#         with col2:
#             st.metric("💪 Compétences", len(skills_result["found"]))
#         with col3:
#             domain_display = skills_result["domain"].replace("_", " ").title()
#             if skills_result.get("domain_type") == "manual":
#                 domain_display = f"✏️ {domain_display}"
#             st.metric("📂 Domaine", domain_display)
#         with col4:
#             total_skills = len(skills_result.get("skills_list", []))
#             st.metric("🔍 Compétences recherchées", total_skills)
        
#         # 🆕 Afficher la configuration utilisée
#         if skills_result.get("user_provided_skills"):
#             with st.expander("📝 Compétences personnalisées de l'utilisateur"):
#                 st.write(", ".join(skills_result["user_provided_skills"]))
        
#         # Compétences trouvées
#         st.subheader("🛠️ Compétences détectées dans le CV")
#         if skills_result["found"]:
#             cols = st.columns(4)
#             for i, skill in enumerate(skills_result["found"][:20]):
#                 cols[i % 4].success(f"✅ {skill}")
            
#             if len(skills_result["found"]) > 20:
#                 with st.expander(f"📋 Voir les {len(skills_result['found'])} compétences"):
#                     cols = st.columns(4)
#                     for i, skill in enumerate(skills_result["found"]):
#                         cols[i % 4].success(f"✅ {skill}")
#         else:
#             st.warning("Aucune compétence détectée")
        
#         # Compétences automatiques
#         if auto_skills:
#             with st.expander("🔍 Compétences supplémentaires détectées"):
#                 st.write(", ".join(auto_skills[:30]))
        
#         # Compétences du domaine
#         domain_skills = SKILLS_BY_DOMAIN.get(skills_result["domain"], [])
#         if domain_skills:
#             with st.expander(f"📊 Comparaison - Domaine {skills_result['domain'].replace('_', ' ').title()}"):
#                 found_domain = [s for s in domain_skills if s in skills_result["found"]]
#                 missing_domain = [s for s in domain_skills if s not in skills_result["found"]]
                
#                 col1, col2 = st.columns(2)
#                 with col1:
#                     st.success(f"✅ Trouvées ({len(found_domain)}) :")
#                     if found_domain:
#                         st.write(", ".join(found_domain[:10]))
#                     else:
#                         st.write("Aucune")
#                 with col2:
#                     st.warning(f"❌ Manquantes ({len(missing_domain)}) :")
#                     if missing_domain:
#                         st.write(", ".join(missing_domain[:10]))
#                     else:
#                         st.write("Toutes trouvées !")
        
#         # Télécharger le rapport
#         st.download_button(
#             label="📥 Télécharger le rapport",
#             data=f"=== RAPPORT CV ANALYZER ===\n\n"
#                  f"Score: {score}/100\n"
#                  f"Domaine: {skills_result['domain']}\n"
#                  f"Compétences trouvées: {', '.join(skills_result['found'])}\n"
#                  f"Compétences personnalisées: {', '.join(skills_result.get('user_provided_skills', []))}\n"
#                  f"Compétences manquantes: {', '.join(missing_domain[:10]) if domain_skills and missing_domain else 'Aucune'}\n",
#             file_name="cv_analysis.txt",
#             mime="text/plain"
#         )

# else:
#     st.info("👆 Téléchargez un PDF pour commencer l'analyse")