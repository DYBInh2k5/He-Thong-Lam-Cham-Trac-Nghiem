"""Tool chấm nhanh từ file CSV."""

from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager
from src.business.grading_engine import GradingEngine
from src.models.submission import Submission
import uuid
import csv


def tao_de_mau():
    """Tạo đề thi mẫu 4 câu."""
    storage = FileStorageManager(base_path="data")
    manager = ExamManager(storage)
    
    # Tạo đề thi
    success, msg, exam_id = manager.create_exam("Đề thi mẫu", "GV001")
    
    # 4 câu hỏi mẫu
    questions = [
        ("1 + 1 = ?", {'A': '1', 'B': '2', 'C': '3', 'D': '4'}, 'B'),
        ("2 + 2 = ?", {'A': '2', 'B': '3', 'C': '4', 'D': '5'}, 'C'),
        ("3 + 3 = ?", {'A': '4', 'B': '5', 'C': '6', 'D': '7'}, 'C'),
        ("4 + 4 = ?", {'A': '6', 'B': '7', 'C': '8', 'D': '9'}, 'C'),
    ]
    
    for content, choices, correct in questions:
        manager.add_question(exam_id, content, choices, correct)
    
    print(f"✓ Đã tạo đề thi mẫu: {exam_id}")
    return exam_id


def cham_tu_dap_an(exam_id, student_id, dap_an_list):
    """Chấm bài từ danh sách đáp án.
    
    Args:
        exam_id: Mã đề thi
        student_id: Mã học sinh
        dap_an_list: List đáp án ['A', 'B', 'C', 'D']
    """
    storage = FileStorageManager(base_path="data")
    grading = GradingEngine(storage)
    
    # Load đề thi
    exam_dict = storage.load_exam(exam_id)
    if not exam_dict:
        print(f"✗ Đề thi không tồn tại: {exam_id}")
        return
    
    # Tạo answers dict
    answers = {}
    for i, q in enumerate(exam_dict['questions']):
        if i < len(dap_an_list):
            answers[q['question_id']] = dap_an_list[i]
    
    # Tạo submission
    submission_id = f"S{uuid.uuid4().hex[:8].upper()}"
    submission = Submission(
        submission_id=submission_id,
        exam_id=exam_id,
        student_id=student_id,
        answers=answers
    )
    
    storage.save_submission(submission.to_dict())
    
    # Chấm bài
    success, msg, result = grading.grade_submission(submission_id)
    
    if success:
        print(f"\n{'='*50}")
        print(f"KẾT QUẢ - Học sinh: {student_id}")
        print(f"{'='*50}")
        print(f"Điểm: {result['score']}/10")
        print(f"Đúng: {result['correct_answers']}/{result['total_questions']} câu")
        print(f"Sai: {result['wrong_answers']}/{result['total_questions']} câu")
        
        print("\nChi tiết:")
        for i, detail in enumerate(result['details'], 1):
            status = "✓" if detail['is_correct'] else "✗"
            print(f"  Câu {i}: {status} (Chọn: {detail['student_answer']}, Đúng: {detail['correct_answer']})")
        print(f"{'='*50}\n")
    else:
        print(f"✗ Lỗi: {msg}")


def main():
    print("=== DEMO CHẤM NHANH ===\n")
    
    # Tạo đề thi mẫu
    exam_id = tao_de_mau()
    
    print("\nĐề thi có 4 câu:")
    print("  Câu 1: 1 + 1 = ? (Đáp án: B)")
    print("  Câu 2: 2 + 2 = ? (Đáp án: C)")
    print("  Câu 3: 3 + 3 = ? (Đáp án: C)")
    print("  Câu 4: 4 + 4 = ? (Đáp án: C)")
    
    # Chấm cho 3 học sinh với đáp án khác nhau
    print("\n--- Chấm bài cho 3 học sinh ---")
    
    # Học sinh 1: Làm đúng hết
    print("\n1. Học sinh HS001 (Làm đúng hết):")
    cham_tu_dap_an(exam_id, "HS001", ['B', 'C', 'C', 'C'])
    
    # Học sinh 2: Sai 1 câu
    print("2. Học sinh HS002 (Sai câu 1):")
    cham_tu_dap_an(exam_id, "HS002", ['A', 'C', 'C', 'C'])
    
    # Học sinh 3: Sai 2 câu
    print("3. Học sinh HS003 (Sai câu 1 và 2):")
    cham_tu_dap_an(exam_id, "HS003", ['A', 'A', 'C', 'C'])
    
    print(f"\n✓ Mã đề thi: {exam_id}")
    print("✓ Bạn có thể dùng mã này để chấm thêm học sinh khác")
    print("\nVí dụ code:")
    print(f"  cham_tu_dap_an('{exam_id}', 'HS004', ['B', 'C', 'C', 'C'])")


if __name__ == "__main__":
    main()
