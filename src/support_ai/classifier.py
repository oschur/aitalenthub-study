class IntentClassifier:
    """
    Классификатор интентов. 
    Определяет тему обращения для последующей типизации и сужения контекста в RAG.
    В рамках PoC реализован на базовых правилах. В production-версии здесь 
    будет загружаться легковесная ML-модель (например, Logistic Regression или BERT).
    """
    
    def __init__(self):
        # В будущем здесь будет загрузка весов модели из папки models/
        # Например: self.model = load_model("models/intent_classifier.pkl")
        pass
        
    def predict_intent(self, text: str) -> str:
        """
        Предсказывает категорию (интент) тикета на основе текста.
        """
        text_lower = text.lower()
        
        # Простейшая эвристика для мок-реализации
        # Ищем корни слов, связанные с финансами
        if any(keyword in text_lower for keyword in ["деньг", "оплат", "списа", "подписк"]):
            return "billing"
        
        # Фолбек на техническую поддержку для всего остального
        return "tech"