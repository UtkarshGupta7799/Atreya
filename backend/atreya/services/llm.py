from typing import List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

from ..utils.config import settings

PROMPT_TEMPLATE = """
You are an Ayurvedic wellness assistant. You must be cautious and include a disclaimer that you are not a doctor.
Given:
- user demographics: age={age}, gender={gender}
- symptoms: {symptoms}
- lifestyle: {lifestyle}
- graph facts (herbs that may help and why): {facts}
- interactions/avoid lists: {avoid_map}

Compose:
1) 3–5 gentle herb suggestions with short 'why' and simple 'how to use' (tea, decoction, dosage ranges).
2) 3 general lifestyle tips aligned with Ayurveda (sleep, hydration, movement, stress).
3) One-paragraph caution & disclaimer.

Return concise bullet points. Do NOT invent interactions that are not in facts/avoid lists.
""".strip()


def make_llm():
    if OPENAI_AVAILABLE and settings.openai_api_key:
        return ChatOpenAI(model=settings.openai_model, temperature=0.2)
    return None  # no-key fallback


def _simple_from_facts(age: int, gender: str,
                       symptoms: List[str],
                       lifestyle: List[str],
                       facts: List[Dict[str, Any]],
                       avoid_map: Dict[str, List[str]]) -> str:
    tally: Dict[str, Dict[str, Any]] = {}
    for f in facts or []:
        h = str(f.get("herb", "Unknown"))
        why = str(f.get("evidence") or f.get("condition") or "Traditional support")
        if h not in tally:
            tally[h] = {"why": set(), "how": "tea/decoction 1–2x daily"}
        tally[h]["why"].add(why)

    herbs_out = []
    for i, (h, v) in enumerate(tally.items()):
        if i >= 5:
            break
        why_list = "; ".join(sorted(v["why"])) if v["why"] else "Traditional support"
        avoid = ", ".join(map(str, avoid_map.get(h, []))) if avoid_map.get(h) else "—"
        herbs_out.append(f"- **{h}** — Why: {why_list}. How: {v['how']}. Avoid with: {avoid}")

    if not herbs_out:
        herbs_out = ["- No direct herb matches found in the graph. Consider general digestive and sleep support."]

    tips = [
        "- Prioritize 7–8 hours consistent sleep.",
        "- Hydrate through the day (warm water/herbal tea).",
        "- Gentle daily movement (walking/yoga) and simple, fresh meals."
    ]

    disclaimer = (
        "This is an educational demo and not medical advice. "
        "Always consult a qualified healthcare professional, especially if pregnant, nursing, or on medication."
    )

    parts = [
        "### Suggested Herbs",
        *herbs_out,
        "",
        "### General Tips",
        *tips,
        "",
        f"**Disclaimer:** {disclaimer}"
    ]
    return "\n".join(parts)


def generate_recommendations(age: int, gender: str,
                             symptoms: List[str], lifestyle: List[str],
                             facts: List[Dict[str, Any]],
                             avoid_map: Dict[str, List[str]]) -> str:
    llm = make_llm()
    if llm is None:
        return _simple_from_facts(age, gender, symptoms, lifestyle, facts, avoid_map)

    tmpl = PromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = tmpl | llm | StrOutputParser()
    return chain.invoke({
        "age": age,
        "gender": gender,
        "symptoms": ", ".join(symptoms) or "none",
        "lifestyle": ", ".join(lifestyle) or "none",
        "facts": facts,
        "avoid_map": avoid_map
    })


def generate_diagnosis(symptoms: List[str], lifestyle: List[str], conditions: List[str]) -> Dict[str, Any]:
    llm = make_llm()
    if llm is None:
        text = (
            "Likely conditions (from graph): "
            + (", ".join(conditions) if conditions else "none found")
            + ". This is a simple heuristic summary without an LLM.\n"
            "Caution: this is not medical advice."
        )
<<<<<<< HEAD
=======
        
>>>>>>> 3a0ec182ea7286fc3bd96cf0b01aee66f91770b6
        conf = min(1.0, max(0.3, len(conditions) / 5.0))
        return {"text": text, "confidence": conf}

    out = llm.invoke(
        f"You are an Ayurvedic triage helper. Symptoms: {symptoms}. Lifestyle: {lifestyle}. "
        f"Likely conditions (from graph): {conditions}. Pick 1–3 most probable and explain briefly. "
        f"Add a caution: this is not medical advice."
    )
    text = getattr(out, "content", str(out))
    conf = min(1.0, max(0.3, len(conditions) / 5.0))
    return {"text": text, "confidence": conf}
