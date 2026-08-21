import time
from typing import List, Dict

class LLMGenerator:
    """
    Отвечает за генерацию итогового ответа (черновика) пользователю.
    Это самая медленная и дорогая часть системы, поэтому она вынесена 
    в асинхронный "холодный" контур и не блокирует роутинг.
    """
    
    def __init__(self, prompt_template: str = None):
        # Базовый системный промпт. В продакшене он будет сложнее
        # и может зависеть от определенного интента.
        self.default_prompt = (
            "Ты — полезный ассистент поддержки. "
            "Используй следующий контекст для ответа на вопрос пользователя: '{context}'"
        )
        self.prompt_template = prompt_template or self.default_prompt

    def generate_draft(self, query: str, context_texts: List[str]) -> str:
        """
        Имитация генерации ответа через вызов LLM API (например, YandexGPT или OpenAI).
        """
        # Имитируем асинхронную задержку сети/инференса LLM
        time.sleep(0.4) 
        
        if not context_texts:
            return "К сожалению, я не нашел точного ответа. Перевожу на оператора."
            
        # Для PoC берем самый релевантный (первый) текст из контекста
        primary_context = context_texts[0]
        
        # В реальной системе здесь будет формироваться payload и отправляться POST-запрос к API
        draft = f"[Черновик LLM]: Здравствуйте! Согласно базе знаний: '{primary_context}'"
        
        return draft