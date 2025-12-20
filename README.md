<div align="center">
  <img src="https://raw.githubusercontent.com/UtkarshGupta7799/Atreya/main/atreya-banner.png"
       alt="Atreya — Personalized Wellness"
       width="100%" />
</div>

# 🌿 Atreya — Personalized Health Recommender

> **Educational / demo project** inspired by **Smart India Hackathon 2023** and **Social Summer of Code (SSoC) Season 3**.  
> Uses knowledge graphs and LLMs to generate **gentle, non-medical wellness suggestions**.  
> ⚠️ **Not medical advice** — always consult a qualified healthcare professional.

---

## ✨ Overview

**Atreya** is an AI-driven wellness recommender that combines **knowledge graphs** with **LLM reasoning** to explore Ayurveda-inspired wellness concepts in a structured, explainable way.

The system focuses on **education and demonstration**, not diagnosis or treatment.

---

## 🧠 How It Works

1. User inputs symptoms or lifestyle context  
2. Backend queries the **Neo4j knowledge graph**  
3. Relevant herbs, properties, and relations are retrieved  
4. **LangChain** structures the prompt  
5. LLM generates safe, non-medical wellness suggestions  

---

## 🛠️ Tech Stack

- **LangChain** — LLM prompt orchestration  
- **Neo4j** — Knowledge graph database  
- **FastAPI** — Backend API  
- **Streamlit** — Interactive frontend  
- **Python** — Core logic 

### 1) Make a new Python space
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) Install packages
```bash
pip install -r requirements.txt
```

### 3) Load the graph
```bash
python graph/load_data.py
```
### 4) Start the backend
```bash
uvicorn --app-dir backend main:app --reload --env-file .env
```
- It will print something like: `http://127.0.0.1:8000`
- Open `http://127.0.0.1:8000/docs` to see the API.

### 5) Start the front-end
In a **new** terminal (keep backend running):
```bash
streamlit run streamlit_app/app.py
```
- Streamlit page opens in your browser.
- Type symptoms/lifestyle → press **Get Recommendations**.

---

## Safety Disclaimer

- Outputs are informational only  
- No diagnosis, treatment, or prescription is provided  
- Intended for educational and research purposes  
- Always consult a certified medical professional for health decisions  

---

## Use Cases

- AI + Knowledge Graph demonstrations  
- LLM reasoning over structured data  
- Hackathons and academic projects  
- Educational exploration of wellness systems  

- All outputs are **suggestions** for discussion with a doctor.
---
