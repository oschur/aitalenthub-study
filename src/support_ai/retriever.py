import json
from typing import List, Dict

class HybridRetriever:
    def __init__(self, kb_path: str = "data/knowledge_base/sample_kb.json"):
        try:
            with open(kb_path, 'r', encoding='utf-8') as f:
                docs = json.load(f)
                self.kb_docs = {doc["id"]: doc for doc in docs}
        except FileNotFoundError:
            self.kb_docs = {
                "doc_1": {"text": "Для возврата средств перейдите в раздел Оплата", "type": "billing"},
                "doc_2": {"text": "Баг решается очисткой кэша", "type": "tech"}
            }

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        semantic_results = [{"id": "doc_1", "score": 0.8}]
        bm25_results = [{"id": "doc_2", "score": 1.5}]
        return semantic_results + bm25_results

    def rerank(self, query: str, docs: List[Dict], top_n: int = 1) -> List[Dict]:
        sorted_docs = sorted(docs, key=lambda x: x["score"], reverse=True)
        return sorted_docs[:top_n]
        
    def get_document_text(self, doc_id: str) -> str:
        return self.kb_docs.get(doc_id, {}).get("text", "")