from typing import List, Dict, Any
from ..models.schemas import RecommendRequest, RecommendResponse, HerbSuggestion, DiagnosisRequest, DiagnosisResponse
from .graph import GraphService
from .llm import generate_recommendations, generate_diagnosis

class RecommenderService:
    def __init__(self, graph: GraphService):
        self.graph = graph

    def recommend(self, req: RecommendRequest) -> RecommendResponse:
        # Always handle empty lists safely
        symptoms = req.symptoms or []
        lifestyle = req.lifestyle or []

        facts = self.graph.herbs_for_symptoms(symptoms)
        herbs = list({str(f.get("herb", "")) for f in facts if f.get("herb")})
        avoid_map = self.graph.contraindications(herbs) if herbs else {}

        llm_text = ""
        try:
            llm_text = generate_recommendations(
                age=req.age,
                gender=req.gender,
                symptoms=symptoms,
                lifestyle=lifestyle,
                facts=facts or [],
                avoid_map=avoid_map or {}
            )
        except Exception as e:
            # Last-resort fallback text if LLM path throws
            llm_text = f"LLM path failed; using simple fallback. Error: {e}"

        # Build suggestions from graph facts (no LLM dependence)
        top = {}
        for f in facts or []:
            h = str(f.get("herb", "")).strip()
            if not h:
                continue
            top.setdefault(h, {"why": [], "how": "tea/decoction 1–2x daily"})
            why_piece = str(f.get("evidence") or f.get("condition") or "Traditional support")
            if why_piece and why_piece not in top[h]["why"]:
                top[h]["why"].append(why_piece)

        suggestions: List[HerbSuggestion] = []
        for i, (h, v) in enumerate(top.items()):
            if i >= 5:
                break
            suggestions.append(
                HerbSuggestion(
                    name=h,
                    why="; ".join(v["why"]) or "Traditional support",
                    how_to_use=v["how"],
                    avoid_with=[str(x) for x in (avoid_map.get(h, []) or [])]
                )
            )

        tips = [
            "Prioritize 7–8 hours of consistent sleep.",
            "Hydrate regularly; warm water or herbal tea can support digestion.",
            "Gentle daily movement (e.g., yoga, walking) supports overall balance."
        ]

        return RecommendResponse(
            suggestions=suggestions,
            tips=tips,
            disclaimer="This is an educational demo and not medical advice. Consult a qualified professional.",
            debug={"llm": (llm_text or "")[:1200]}
        )

    def diagnose(self, req: DiagnosisRequest) -> DiagnosisResponse:
        conditions = self.graph.conditions_from_symptoms(req.symptoms or [])
        out = generate_diagnosis(req.symptoms or [], req.lifestyle or [], conditions or [])
        return DiagnosisResponse(
            probable_conditions=(conditions or [])[:3],
            confidence=out["confidence"],
            rationale=out["text"],
            disclaimer="This is an educational demo and not medical advice. Consult a qualified professional."
        )
