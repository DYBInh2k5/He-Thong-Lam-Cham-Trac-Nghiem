"""Tool đơn giản để tạo đề thi và chấm điểm."""

from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager
from src.business.grading_engine import GradingEngine
from src.models.submission import Submission
from datetime import datetime
import uuid


def tao_de_thi():
    """Tạo đề thi mới."""
    print("\n=== TẠO ĐỀ THI ===")
    
    storage = FileStorageManager(base_path="data")
    manager = ExamManager(storage)
    
    # Nhập thông tin đề thi
    ten_de = input("Nhập tên đề thi: ")
    ma_gv = input("Nhập mã giáo viên (ví dụ: GV001): ")
    
    # Tạo đề thi
    success, msg, exam_id = manager.create_exam(ten_de, ma_gv)
    if not success:
        print(f"Lỗi: {msg}")
        return None
    
    print(f"\n✓ Đã tạo đề thi: {exam_id}")
    print("\nNhập 4 câu hỏi:")
    
    # Nhập 4 câu hỏi
    for i in range(1, 5):
        print(f"\n--- Câu {i} ---")
        noi_dung = input(f"Nội dung câu {i}: ")
        
        choices = {}
        for choice in ['A', 'B', 'C', 'D']:
            choices[choice] = input(f"  Đáp án {choice}: ")
        
        dap_an_dung = input("Đáp án đúng (A/B/C/D): ").upper()
        
        success, msg, q_id = manager.add_question(exam_id, noi_dung, choices, dap_an_dung)
        if success:
            print(f"  ✓ Đã thêm câu {i}")
        else:
            print(f"  ✗ Lỗi: {msg}")
    
    # Hiển thị đề thi
    print("\n=== ĐỀ THI ĐÃ TẠO ===")
    success, msg, exam_dict = manager.get_exam(exam_id)
    if success:
        print(f"Mã đề: {exam_id}")
        print(f"Tên đề: {exam_dict['title']}\n")
        
        for i, q in enumerate(exam_dict['questions'], 1):
            print(f"Câu {i}: {q['content']}")
            for choice, text in q['choices'].items():
                marker = "✓" if choice == q['correct_answer'] else " "
                print(f"  [{marker}] {choice}. {text}")
            print()
    
    print(f"\n✓ Lưu mã đề này để chấm bài: {exam_id}")
    return exam_id


def cham_bai():
    """Chấm bài thi."""
    print("\n=== CHẤM BÀI THI ===")
    
    storage = FileStorageManager(base_path="data")
    grading = GradingEngine(storage)
    
    # Nhập thông tin
    exam_id = input("Nhập mã đề thi: ")
    ma_hs = input("Nhập mã học sinh (ví dụ: HS001): ")
    
    # Kiểm tra đề thi có tồn tại không
    exam_dict = storage.load_exam(exam_id)
    if not exam_dict:
        print(f"✗ Đề thi không tồn tại: {exam_id}")
        return
    
    print(f"\nĐề thi: {exam_dict['title']}")
    print(f"Số câu: {len(exam_dict['questions'])}\n")
    
    # Nhập đáp án của học sinh
    print("Nhập đáp án của học sinh (A/B/C/D):")
    answers = {}
    
    for i, q in enumerate(exam_dict['questions'], 1):
        print(f"\nCâu {i}: {q['content']}")
        for choice, text in q['choices'].items():
            print(f"  {choice}. {text}")
        
        dap_an = input(f"Đáp án học sinh chọn: ").upper()
        answers[q['question_id']] = dap_an
    
    # Tạo submission
    submission_id = f"S{uuid.uuid4().hex[:8].upper()}"
    submission = Submission(
        submission_id=submission_id,
        exam_id=exam_id,
        student_id=ma_hs,
        answers=answers
    )
    
    # Lưu submission
    storage.save_submission(submission.to_dict())
    
    # Chấm bài
    print("\n⏳ Đang chấm bài...")
    success, msg, result = grading.grade_submission(submission_id)
    
    if not success:
        print(f"✗ Lỗi: {msg}")
        return
    
    # Hiển thị kết quả
    print("\n" + "="*50)
    print("KẾT QUẢ CHẤM BÀI")
    print("="*50)
    print(f"Học sinh: {ma_hs}")
    print(f"Đề thi: {exam_dict['title']}")
    print(f"Mã đề: {exam_id}")
    print(f"\nĐiểm: {result['score']}/10")
    print(f"Số câu đúng: {result['correct_answers']}/{result['total_questions']}")
    print(f"Số câu sai: {result['wrong_answers']}/{result['total_questions']}")
    
    # Chi tiết từng câu
    print("\n--- CHI TIẾT TỪNG CÂU ---")
    for i, detail in enumerate(result['details'], 1):
        status = "✓ ĐÚNG" if detail['is_correct'] else "✗ SAI"
        print(f"Câu {i}: {status}")
        print(f"  Học sinh chọn: {detail['student_answer']}")
        print(f"  Đáp án đúng: {detail['correct_answer']}")
    
    print("\n" + "="*50)
    print(f"✓ Kết quả đã được lưu với mã: {result['result_id']}")


def menu():
    """Menu chính."""
    while True:
        print("\n" + "="*50)
        print("HỆ THỐNG CHẤM TRẮC NGHIỆM")
        print("="*50)
        print("1. Tạo đề thi mới (4 câu)")
        print("2. Chấm bài thi")
        print("3. Thoát")
        print("="*50)
        
        chon = input("\nChọn chức năng (1/2/3): ")
        
        if chon == '1':
            tao_de_thi()
        elif chon == '2':
            cham_bai()
        elif chon == '3':
            print("\nTạm biệt!")
            break
        else:
            print("\n✗ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    menu()
