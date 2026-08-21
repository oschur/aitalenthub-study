import time
import logging
from typing import Dict, Any

from .safety import SafetyRouter
from .classifier import IntentClassifier
from .retriever import HybridRetriever
from .generator import LLMGenerator

# Настройка аудита решений согласно требованиям PoC
logging.basicConfig(
    filename='audit_log.txt', 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s'
)

class TicketOrchestrator:
    """
    Главный класс приложения, связывающий все компоненты в единый пайплайн.
    Реализует каскадную архитектуру: 
    мгновенный роутинг (горячий путь) + RAG генерацию (холодный путь).
    """
    def __init__(self):
        self.safety_router = SafetyRouter()
        self.intent_classifier = IntentClassifier()
        self.retriever = HybridRetriever()
        self.generator = LLMGenerator()

    def process_ticket(self, ticket_id: str, text: str) -> Dict[str, Any]:
        """
        Основной метод обработки входящего обращения (тикета).
        """
        start_time = time.time()
        result = {"ticket_id": ticket_id, "original_text": text}

        # 1. ГОРЯЧИЙ ПУТЬ: Проверка на риски и роутинг
        safety_decision = self.safety_router.check_ticket(text)
        
        # Эскалация рискованного или low-confidence тикета на оператора
        if not safety_decision["is_safe"]:
            result["status"] = "routed_to_operator"
            result["reason"] = safety_decision["reason"]
            logging.info(f"[{ticket_id}] ESCALATED -> Operator. Reason: {safety_decision['reason']}")
            
            result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
            return result

        # 2. ХОЛОДНЫЙ ПУТЬ: RAG-пайплайн для безопасных типовых тикетов
        
        # 2.1 Определение интента
        intent = self.intent_classifier.predict_intent(text)
        result["intent"] = intent
        
        # 2.2 Гибридный поиск и реранжирование (BM25 + Semantic)
        raw_docs = self.retriever.retrieve(text)
        best_docs = self.retriever.rerank(text, raw_docs, top_n=1)
        
        # Подготовка текстов для промпта
        context_texts = [self.retriever.get_document_text(doc["id"]) for doc in best_docs]
        
        # 2.3 LLM-генерация черновика
        draft = self.generator.generate_draft(text, context_texts)
        
        # Формирование успешного ответа
        result["status"] = "auto_draft_ready"
        result["draft"] = draft
        logging.info(f"[{ticket_id}] RAG DRAFT_CREATED. Intent: {intent}")

        result["latency_ms"] = round((time.time() - start_time) * 1000, 2)
        return result
