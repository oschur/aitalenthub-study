import csv
import os
from src.support_ai import TicketOrchestrator

def run_evaluation(dataset_path: str = "data/tickets_sample.csv"):
    app = TicketOrchestrator()
    
    print("=== Запуск обработки датасета ===")
    
    if not os.path.exists(dataset_path):
        print(f"Файл {dataset_path} не найден!")
        return

    total = 0
    passed = 0

    with open(dataset_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ticket_id = row['ticket_id']
            text = row['text']
            expected = row['expected_route']
            
            res = app.process_ticket(ticket_id, text)
            
            actual_route = "operator" if res['status'] == "routed_to_operator" else "rag_pipeline"
            is_match = actual_route == expected
            
            if is_match: passed += 1
            total += 1
            
            status_symbol = "✅" if is_match else "❌"
            print(f"[{ticket_id}] {status_symbol} Text: '{text[:20]}...' | Route: {actual_route} | Latency: {res['latency_ms']}ms")

    print(f"\nИтог: {passed}/{total} тестов пройдено успешно.")

if __name__ == "__main__":
    run_evaluation()