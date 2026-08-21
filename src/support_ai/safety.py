from typing import Dict, Any

class SafetyRouter:
    def __init__(self):
        self.risky_words = ["суд", "прокурат", "роскомнадзор", "угроз", "персональн"]

    def check_ticket(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
       
        if any(w in text_lower for w in self.risky_words):
            return {"is_safe": False, "route": "operator", "reason": "high_risk", "confidence": 0.99}
           
        if len(text.split()) < 5:
            return {"is_safe": False, "route": "operator", "reason": "low_confidence", "confidence": 0.40}
           
        return {"is_safe": True, "route": "rag_pipeline", "confidence": 0.90}