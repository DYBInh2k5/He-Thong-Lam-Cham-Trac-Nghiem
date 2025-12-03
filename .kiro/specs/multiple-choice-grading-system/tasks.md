# Kế Hoạch Triển Khai - Hệ Thống Chấm Trắc Nghiệm

- [x] 1. Thiết lập cấu trúc dự án và data models



  - Tạo cấu trúc thư mục cho project (src/, data/, tests/)
  - Tạo các data model classes: Exam, Question, Submission, Result, User
  - Implement validation methods cho từng model
  - _Requirements: 1.1, 1.2, 3.3, 4.3, 5.1_

- [x] 1.1 Viết property test cho exam persistence


  - **Property 1: Exam persistence round-trip**
  - **Validates: Requirements 1.1**

- [x] 1.2 Viết property test cho submission persistence


  - **Property 9: Submission round-trip**
  - **Validates: Requirements 3.3**


- [x] 1.3 Viết property test cho user persistence

  - **Property 14: User persistence round-trip**
  - **Validates: Requirements 5.1**

- [x] 2. Implement FileStorageManager



  - Tạo FileStorageManager class với methods save/load cho từng entity type
  - Implement JSON serialization/deserialization với UTF-8 encoding
  - Implement auto-create directories và files nếu không tồn tại
  - Implement error handling cho file operations
  - _Requirements: 1.5, 3.5, 4.4, 5.4, 10.1, 10.3, 10.4, 10.5_

- [x] 2.1 Viết property test cho UTF-8 encoding


  - **Property 25: UTF-8 encoding preservation**
  - **Validates: Requirements 10.4**


- [x] 2.2 Viết property test cho auto-initialization

  - **Property 26: Auto-initialization**
  - **Validates: Requirements 10.5**


- [x] 2.3 Viết property test cho immediate persistence

  - **Property 24: Immediate persistence**
  - **Validates: Requirements 10.1**

- [x] 2.4 Viết unit tests cho FileStorageManager


  - Test save/load operations
  - Test directory creation
  - Test error handling

- [x] 3. Implement ExamManager



  - Tạo ExamManager class với methods create, update, delete, get, list exams
  - Implement add_question method
  - Implement validate_exam method với validation rules
  - Integrate với FileStorageManager
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 9.1, 9.2_

- [x] 3.1 Viết property test cho adding questions


  - **Property 2: Adding questions increases count**
  - **Validates: Requirements 1.2**


- [x] 3.2 Viết property test cho exam ID invariant

  - **Property 3: Exam ID invariant on update**
  - **Validates: Requirements 1.3**


- [x] 3.3 Viết property test cho deletion preserves results

  - **Property 4: Deletion preserves related results**
  - **Validates: Requirements 1.4**

- [x] 3.4 Viết unit tests cho ExamManager


  - Test exam creation và validation
  - Test empty exam rejection
  - Test question without correct answer rejection

- [ ] 4. Implement Import/Export functionality
  - Implement import_from_json và export_to_json methods
  - Implement import_from_csv và export_to_csv methods
  - Implement CSV parsing với proper format
  - Implement validation cho imported data
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 4.1 Viết property test cho JSON round-trip
  - **Property 5: JSON import/export round-trip**
  - **Validates: Requirements 2.1, 2.3**

- [ ] 4.2 Viết property test cho CSV round-trip
  - **Property 6: CSV import/export round-trip**
  - **Validates: Requirements 2.2, 2.4**

- [ ] 4.3 Viết property test cho invalid import
  - **Property 7: Invalid import preserves state**
  - **Validates: Requirements 2.5**

- [ ] 4.4 Viết unit tests cho import/export
  - Test JSON import/export
  - Test CSV import/export
  - Test invalid file handling

- [ ] 5. Implement SubmissionManager
  - Tạo SubmissionManager class với methods create, save_answer, submit, get, list
  - Implement answer validation (A, B, C, D only)
  - Integrate với FileStorageManager
  - _Requirements: 3.2, 3.3_

- [ ] 5.1 Viết property test cho answer persistence
  - **Property 8: Answer persistence**
  - **Validates: Requirements 3.2**

- [ ] 5.2 Viết unit tests cho SubmissionManager
  - Test submission creation
  - Test answer saving
  - Test answer validation

- [ ] 6. Implement GradingEngine
  - Tạo GradingEngine class với methods grade_submission, calculate_score, compare_answers
  - Implement grading logic: so sánh từng câu trả lời với đáp án đúng
  - Implement score calculation: (correct / total) * 10
  - Implement result generation với đầy đủ thông tin
  - Implement batch grading cho nhiều submissions
  - _Requirements: 4.1, 4.2, 4.3, 4.5_

- [ ] 6.1 Viết property test cho grading correctness
  - **Property 10: Grading correctness**
  - **Validates: Requirements 4.1**

- [ ] 6.2 Viết property test cho score calculation
  - **Property 11: Score calculation formula**
  - **Validates: Requirements 4.2**

- [ ] 6.3 Viết property test cho result completeness
  - **Property 12: Result completeness**
  - **Validates: Requirements 4.3**

- [ ] 6.4 Viết property test cho batch grading
  - **Property 13: Batch grading completeness**
  - **Validates: Requirements 4.5**

- [ ] 6.5 Viết unit tests cho GradingEngine
  - Test grading với known inputs
  - Test score calculation accuracy
  - Test batch grading

- [ ] 7. Implement UserManager
  - Tạo UserManager class với methods create, update, delete, get, list users
  - Implement user ID uniqueness validation
  - Implement user ID preservation on update
  - Implement deletion với preservation của submissions/results
  - _Requirements: 5.1, 5.2, 5.3, 5.5, 9.4_

- [ ] 7.1 Viết property test cho user ID invariant
  - **Property 15: User ID invariant on update**
  - **Validates: Requirements 5.2**

- [ ] 7.2 Viết property test cho user deletion
  - **Property 16: User deletion preserves submissions**
  - **Validates: Requirements 5.3**

- [ ] 7.3 Viết property test cho user ID uniqueness
  - **Property 17: User ID uniqueness**
  - **Validates: Requirements 5.5**

- [ ] 7.4 Viết property test cho ID uniqueness enforcement
  - **Property 23: ID uniqueness enforcement**
  - **Validates: Requirements 9.4**

- [ ] 7.5 Viết unit tests cho UserManager
  - Test user creation và validation
  - Test uniqueness constraints
  - Test user deletion

- [ ] 8. Implement StatsEngine
  - Tạo StatsEngine class với methods get_exam_statistics, get_student_statistics, get_question_analysis
  - Implement tính toán avg, min, max scores
  - Implement filtering results theo exam_id và student_id
  - Implement tính toán correct answer rate cho từng câu hỏi
  - Implement export_statistics sang CSV
  - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 8.1 Viết property test cho statistics calculation
  - **Property 18: Statistics calculation accuracy**
  - **Validates: Requirements 6.1**

- [ ] 8.2 Viết property test cho student results
  - **Property 19: Student results completeness**
  - **Validates: Requirements 6.2**

- [ ] 8.3 Viết property test cho question analysis
  - **Property 20: Question analysis accuracy**
  - **Validates: Requirements 6.3**

- [ ] 8.4 Viết property test cho statistics export
  - **Property 21: Statistics export format**
  - **Validates: Requirements 6.4**

- [ ] 8.5 Viết unit tests cho StatsEngine
  - Test statistics calculations
  - Test filtering operations
  - Test CSV export

- [ ] 9. Implement ApplicationController
  - Tạo ApplicationController class để điều phối giữa business logic và views
  - Implement handlers cho tất cả operations: exam, submission, grading, stats, user
  - Implement error handling và return format (success, message, data)
  - Implement Vietnamese error messages
  - _Requirements: 9.5_

- [ ] 9.1 Viết property test cho corrupted file handling
  - **Property 22: Corrupted file handling**
  - **Validates: Requirements 9.3**

- [ ] 9.2 Viết unit tests cho ApplicationController
  - Test error handling
  - Test response format
  - Test Vietnamese messages

- [ ] 10. Checkpoint - Đảm bảo tất cả tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement CLI View
  - Tạo CLI interface sử dụng argparse
  - Implement commands: exam (create, add-question, list, import, export)
  - Implement commands: submit (create, answer, finish)
  - Implement commands: grade (single, batch)
  - Implement commands: stats (exam, student, export)
  - Implement commands: user (create, list)
  - Implement help messages và error handling
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 11.1 Viết unit tests cho CLI commands
  - Test command parsing
  - Test invalid parameter handling
  - Test help message display

- [ ] 12. Implement GUI View với Tkinter
  - Tạo main window với menu navigation
  - Implement Exam Management Window (list, create, edit, delete, import, export)
  - Implement Take Exam Window (select exam, display questions, submit)
  - Implement Grading Window (list submissions, grade, view results)
  - Implement Statistics Window (tabs cho exam/student/question stats, export)
  - Implement User Management Window (list, create, edit, delete)
  - Implement form validation và error dialogs
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 12.1 Viết unit tests cho GUI components
  - Test window creation
  - Test form validation
  - Test data binding

- [ ] 13. Implement main entry point
  - Tạo main.py với argument parsing để chọn CLI hoặc GUI mode
  - Implement initialization logic
  - Setup logging
  - _Requirements: All_

- [ ] 14. Tạo sample data và documentation
  - Tạo sample exams, users, submissions cho testing
  - Viết README.md với hướng dẫn cài đặt và sử dụng
  - Viết user guide cho CLI và GUI
  - Tạo example CSV files cho import

- [ ] 15. Final Checkpoint - Kiểm tra toàn bộ hệ thống
  - Ensure all tests pass, ask the user if questions arise.
