"""Demo script để thử nghiệm hệ thống chấm trắc nghiệm."""

from src.storage.file_storage import FileStorageManager
from src.business.exam_manager import ExamManager

def main():
    print("=== HỆ THỐNG CHẤM TRẮC NGHIỆM - DEMO ===\n")
    
    # Khởi tạo storage và manager
    storage = FileStorageManager(base_path="data")
    exam_manager = ExamManager(storage)
    
    # 1. Tạo đề thi
    print("1. Tạo đề thi mới...")
    success, msg, exam_id = exam_manager.create_exam(
        title="Đề thi Toán học",
        teacher_id="GV001"
    )
    print(f"   {msg}")
    if success:
        print(f"   Mã đề thi: {exam_id}\n")
    
    # 2. Thêm câu hỏi
    print("2. Thêm câu hỏi vào đề thi...")
    
    # Câu hỏi 1
    choices1 = {
        'A': '1',
        'B': '2',
        'C': '3',
        'D': '4'
    }
    success, msg, q_id = exam_manager.add_question(
        exam_id=exam_id,
        content="1 + 1 = ?",
        choices=choices1,
        correct_answer='B'
    )
    print(f"   Câu 1: {msg}")
    
    # Câu hỏi 2
    choices2 = {
        'A': '2',
        'B': '3',
        'C': '4',
        'D': '5'
    }
    success, msg, q_id = exam_manager.add_question(
        exam_id=exam_id,
        content="2 + 2 = ?",
        choices=choices2,
        correct_answer='C'
    )
    print(f"   Câu 2: {msg}")
    
    # Câu hỏi 3
    choices3 = {
        'A': '4',
        'B': '5',
        'C': '6',
        'D': '7'
    }
    success, msg, q_id = exam_manager.add_question(
        exam_id=exam_id,
        content="3 + 3 = ?",
        choices=choices3,
        correct_answer='C'
    )
    print(f"   Câu 3: {msg}\n")
    
    # 3. Xem thông tin đề thi
    print("3. Xem thông tin đề thi...")
    success, msg, exam_dict = exam_manager.get_exam(exam_id)
    if success:
        print(f"   Tên đề: {exam_dict['title']}")
        print(f"   Mã đề: {exam_dict['exam_id']}")
        print(f"   Số câu hỏi: {len(exam_dict['questions'])}")
        print(f"   Giáo viên: {exam_dict['created_by']}\n")
        
        # Hiển thị các câu hỏi
        print("   Danh sách câu hỏi:")
        for i, q in enumerate(exam_dict['questions'], 1):
            print(f"   Câu {i}: {q['content']}")
            for choice, text in q['choices'].items():
                marker = "✓" if choice == q['correct_answer'] else " "
                print(f"      [{marker}] {choice}. {text}")
            print()
    
    # 4. Liệt kê tất cả đề thi
    print("4. Danh sách tất cả đề thi trong hệ thống:")
    success, msg, exams = exam_manager.list_all_exams()
    print(f"   {msg}")
    for exam in exams:
        print(f"   - {exam['exam_id']}: {exam['title']} ({len(exam['questions'])} câu)")
    
    print("\n=== DEMO HOÀN TẤT ===")
    print("Dữ liệu đã được lưu vào thư mục 'data/'")
    print("Bạn có thể kiểm tra các file JSON trong thư mục đó.")

if __name__ == "__main__":
    main()
