#  IA-CV-Analyzer-Gemini
Analyseur de CV avec IA Gemini

**Analyseur de CV intelligent** utilisant l'IA Gemini pour extraire, analyser et évaluer les compétences des candidats.

## 🎯 Description

**AI CV Analyzer** est une application web interactive qui permet d'analyser automatiquement les CV au format PDF. Elle utilise l'API Gemini de Google pour :

- 📄 **Extraire** le texte des CV (même scannés)
- 🔍 **Détecter** les compétences techniques et soft skills
- 🎯 **Calculer** un score de compatibilité
- 📊 **Comparer** avec les compétences du domaine
- ✏️ **Personnaliser** l'analyse selon vos besoins

L'application est idéale pour :
- **Les recruteurs** : évaluer rapidement les candidats
- **Les candidats** : vérifier la pertinence de leur CV
- **Les formateurs** : analyser les profils des apprenants
- **Les Data Scientists** : explorer le traitement de texte avec l'IA

---

## ✨ Fonctionnalités

### 🤖 Mode Automatique
- Détection intelligente du domaine du CV
- Extraction automatique des compétences
- Scoring basé sur les compétences du domaine

### 📂 Domaines prédéfinis
- **Data Science** : Python, Machine Learning, TensorFlow, etc.
- **Software Engineering** : Java, React, Docker, Cloud, etc.
- **Finance** : Analyse financière, Risk Management, M&A, etc.
- **Marketing** : SEO, Social Media, Google Analytics, etc.
- **RH** : Recrutement, Employee Relations, HRIS, etc.
- **Design** : UX/UI, Figma, Adobe XD, etc.

### ✏️ Mode Personnalisé
- Saisie libre du domaine
- Saisie personnalisée des compétences (une par ligne)
- Scoring basé UNIQUEMENT sur vos compétences

### 📊 Analyse Avancée
- Score personnalisé (0-100)
- Compétences trouvées vs manquantes
- Extraction automatique des compétences non listées
- Export du rapport en format texte

### 🔒 Sécurité
- Clé API stockée dans `.env` (ignoré par Git)
- Aucune donnée sensible sauvegardée
- Traitement local des CV

---

## 🛠️ Architecture Technique
AI-CV-Analyzer/
│
├── app.py # Interface Streamlit
├── requirements.txt # Dépendances Python
├── .env # Configuration (clé API)
├── README.md # Documentation
│
├── utils/ # Code personnalisé
│ ├── init.py
│ ├── pdf_reader.py # Extraction PDF (pypdf + OCR)
│ ├── cv_parser.py # Détection des compétences
│ └── gemini_vision.py # OCR avec Gemini Vision
│
├── data/ # Données (CVs, etc.)
├── assets/ # Images, logos
└── venv/ # Environnement virtuel (ignoré)

----------------------------

# # Prérequis
- Python 3.11 ou supérieur
- Git (optionnel)
- Un compte Google AI Studio pour la clé API
  
----------------------------

 ##  Créer l'environnement virtuel
 Créer l'environnement virtuel
  # Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux

python3 -m venv venv
source venv/bin/activate

----------------------------

# 🎯 Guide d'utilisation

1. Configurer l'analyse
Dans la barre latérale, choisissez votre mode :

Mode	Description
🤖 Automatique	L'IA détecte le domaine et les compétences
📂 Domaine prédéfini	Choisissez parmi 6 domaines
✏️ Saisir mon domaine	Entrez votre domaine + compétences
📝 Mode personnalisé	Contrôle total sur l'analyse
2. Télécharger le CV
Format : PDF uniquement

Taille : jusqu'à 5 Mo

Support : PDF textuels et scannés

3. Analyser
Cliquez sur "Analyser"

Attendez quelques secondes

Découvrez les résultats

4. Interpréter les résultats
🎯 Score : compatibilité du CV

💪 Compétences : liste des compétences trouvées

📂 Domaine : domaine détecté ou saisi

🔍 Compétences recherchées : nombre total de compétences analysées

📊 Comparaison : compétences trouvées vs manquantes

5. Exporter
Téléchargez le rapport en format .txt

----------------------------

# 🔧 Dépendances Principales
Package	Version	Utilisation
streamlit	1.28+	Interface web
google-genai	2.0+	API Gemini
pypdf	3.0+	Extraction PDF
pdfplumber	0.10+	Extraction PDF avancée
pandas	2.0+	Analyse de données
python-dotenv	1.0+	Gestion du fichier .env
pillow	10.0+	Traitement d'images
pdf2image	1.16+	Conversion PDF → Images

----------------------------

# 🙏 Remerciements
Google Gemini : pour l'API IA

Streamlit : pour le framework web

Communauté Open Source : pour les outils utilisés

# 📚 Documentation complémentaire
Documentation Gemini

Documentation Streamlit

Guide Python
