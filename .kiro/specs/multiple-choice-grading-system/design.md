# Tài Liệu Thiết Kế - Hệ Thống Chấm Trắc Nghiệm

## Tổng Quan

Hệ thống chấm trắc nghiệm là một ứng dụng Python desktop và command-line cho phép quản lý đề thi, làm bài thi, chấm điểm tự động và thống kê kết quả. Hệ thống sử dụng kiến trúc MVC (Model-View-Controller) với lưu trữ dữ liệu dựa trên file JSON/CSV.

### Công Nghệ Sử Dụng

- **Ngôn ngữ**: Python 3.8+
- **GUI Framework**: Tkinter (có sẵn trong Python standard library)
- **CLI Framework**: argparse (có sẵn trong Python standard library)
- **Lưu trữ dữ liệu**: JSON (thư viện json), CSV (thư viện csv)
- **Testing**: pytest cho unit tests, Hypothesis cho property-based testing

## Kiến Trúc

Hệ thống được tổ chức theo mô hình MVC với các layer sau:

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  ┌──────────────┐    ┌──────────────┐  │
│  │  CLI View    │    │  GUI View    │  │
│  └──────────────┘    └──────────────┘  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Controller Layer                │
│  ┌──────────────────────────────────┐  │
│  │  Application Controller          │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Business Logic Layer            │
│  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │  Exam    │  │  Grading │  │ Stats │ │
│  │  Manager │  │  Engine  │  │ Engine│ │
│  └──────────┘  └──────────┘  └───────┘ │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Data Access Layer               │
│  ┌──────────────────────────────────┐  │
│  │  File Storage Manager            │  │
│  │  (JSON/CSV Handler)              │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         File System                     │
│  data/                                  │
│  ├── exams/                             │
│  ├── submissions/                       │
│  ├── results/                           │
│  └── users/                             │
└─────────────────────────────────────────┘
```

### Luồng Dữ Liệu

1. **Tạo Đề Thi**: GUI/CLI → Controller → ExamManager → FileStorage → JSON file
2. **Làm Bài**: GUI/CLI → Controller → ExamManager (load) → FileStorage (save submission)
3. **Chấm Bài**: Controller → GradingEngine → FileStorage (load exam + submission, save result)
4. **Thống Kê**: GUI/CLI → Controller → StatsEngine → FileStorage (load results) → Tính toán

## Các Thành Phần và Giao Diện

### 1. Data Models

#### Exam (Đề Thi)
```python
{
    "exam_id": "string",           # Mã đề thi (unique)
    "title": "string",             # Tên đề thi
    "created_by": "string",        # Mã giáo viên
    "created_at": "ISO8601",       # Thời gian tạo
    "questions": [                 # Danh sách câu hỏi
        {
            "question_id": "string",
            "content": "string",
            "choices": {
                "A": "string",
                "B": "string",
                "C": "string",
                "D": "string"
            },
            "correct_answer": "A|B|C|D"
        }
    ]
}
```

#### Submission (Bài Làm)
```python
{
    "submission_id": "string",     # Mã bài làm (unique)
    "exam_id": "string",           # Mã đề thi
    "student_id": "string",        # Mã học sinh
    "submitted_at": "ISO8601",     # Thời gian nộp
    "answers": {                   # Câu trả lời
        "question_id": "A|B|C|D"
    }
}
```

#### Result (Kết Quả)
```python
{
    "result_id": "string",         # Mã kết quả (unique)
    "submission_id": "string",     # Mã bài làm
    "exam_id": "string",           # Mã đề thi
    "student_id": "string",        # Mã học sinh
    "graded_at": "ISO8601",        # Thời gian chấm
    "score": "float",              # Điểm (0-10)
    "total_questions": "int",      # Tổng số câu
    "correct_answers": "int",      # Số câu đúng
    "wrong_answers": "int",        # Số câu sai
    "details": [                   # Chi tiết từng câu
        {
            "question_id": "string",
            "student_answer": "A|B|C|D",
            "correct_answer": "A|B|C|D",
            "is_correct": "boolean"
        }
    ]
}
```

#### User (Người Dùng)
```python
{
    "user_id": "string",           # Mã người dùng (unique)
    "name": "string",              # Tên
    "role": "teacher|student",     # Vai trò
    "created_at": "ISO8601"        # Thời gian tạo
}
```

### 2. Core Components

#### FileStorageManager
Quản lý việc đọc/ghi file JSON và CSV.

**Interface:**
```python
class FileStorageManager:
    def save_exam(exam: dict) -> bool
    def load_exam(exam_id: str) -> dict
    def list_exams() -> list[dict]
    def delete_exam(exam_id: str) -> bool
    
    def save_submission(submission: dict) -> bool
    def load_submission(submission_id: str) -> dict
    def list_submissions(exam_id: str = None, student_id: str = None) -> list[dict]
    
    def save_result(result: dict) -> bool
    def load_result(result_id: str) -> dict
    def list_results(exam_id: str = None, student_id: str = None) -> list[dict]
    
    def save_user(user: dict) -> bool
    def load_user(user_id: str) -> dict
    def list_users(role: str = None) -> list[dict]
    def delete_user(user_id: str) -> bool
    
    def import_from_json(file_path: str, data_type: str) -> bool
    def export_to_json(data: dict, file_path: str) -> bool
    def import_from_csv(file_path: str) -> dict
    def export_to_csv(data: list[dict], file_path: str) -> bool
```

#### ExamManager
Quản lý logic nghiệp vụ liên quan đến đề thi.

**Interface:**
```python
class ExamManager:
    def __init__(storage: FileStorageManager)
    
    def create_exam(title: str, teacher_id: str) -> str  # Returns exam_id
    def add_question(exam_id: str, content: str, choices: dict, correct: str) -> str
    def update_exam(exam_id: str, updates: dict) -> bool
    def delete_exam(exam_id: str) -> bool
    def get_exam(exam_id: str) -> dict
    def list_all_exams() -> list[dict]
    def validate_exam(exam: dict) -> tuple[bool, str]  # Returns (is_valid, error_message)
```

#### SubmissionManager
Quản lý bài làm của học sinh.

**Interface:**
```python
class SubmissionManager:
    def __init__(storage: FileStorageManager)
    
    def create_submission(exam_id: str, student_id: str) -> str  # Returns submission_id
    def save_answer(submission_id: str, question_id: str, answer: str) -> bool
    def submit(submission_id: str) -> bool
    def get_submission(submission_id: str) -> dict
    def list_submissions(exam_id: str = None, student_id: str = None) -> list[dict]
```

#### GradingEngine
Chấm điểm tự động.

**Interface:**
```python
class GradingEngine:
    def __init__(storage: FileStorageManager)
    
    def grade_submission(submission_id: str) -> str  # Returns result_id
    def calculate_score(correct: int, total: int) -> float
    def compare_answers(student_answer: str, correct_answer: str) -> bool
    def get_result(result_id: str) -> dict
```

#### StatsEngine
Tính toán thống kê.

**Interface:**
```python
class StatsEngine:
    def __init__(storage: FileStorageManager)
    
    def get_exam_statistics(exam_id: str) -> dict
    # Returns: {avg_score, max_score, min_score, total_submissions, pass_rate}
    
    def get_student_statistics(student_id: str) -> dict
    # Returns: {total_exams, avg_score, exams_list}
    
    def get_question_analysis(exam_id: str) -> list[dict]
    # Returns: [{question_id, correct_rate, total_answers}]
    
    def export_statistics(data: dict, format: str) -> str  # Returns file_path
```

#### UserManager
Quản lý người dùng.

**Interface:**
```python
class UserManager:
    def __init__(storage: FileStorageManager)
    
    def create_user(name: str, role: str) -> str  # Returns user_id
    def update_user(user_id: str, updates: dict) -> bool
    def delete_user(user_id: str) -> bool
    def get_user(user_id: str) -> dict
    def list_users(role: str = None) -> list[dict]
    def validate_user_id(user_id: str) -> bool
```

### 3. Controller Layer

#### ApplicationController
Điều phối giữa View và Business Logic.

**Interface:**
```python
class ApplicationController:
    def __init__(storage: FileStorageManager)
    
    # Exam operations
    def handle_create_exam(title: str, teacher_id: str, questions: list) -> tuple[bool, str]
    def handle_import_exam(file_path: str, format: str) -> tuple[bool, str]
    def handle_export_exam(exam_id: str, file_path: str, format: str) -> tuple[bool, str]
    
    # Submission operations
    def handle_take_exam(exam_id: str, student_id: str) -> tuple[bool, dict]
    def handle_submit_exam(submission_id: str, answers: dict) -> tuple[bool, str]
    
    # Grading operations
    def handle_grade_submission(submission_id: str) -> tuple[bool, dict]
    def handle_batch_grade(exam_id: str) -> tuple[bool, list]
    
    # Statistics operations
    def handle_get_statistics(stat_type: str, id: str) -> tuple[bool, dict]
    def handle_export_statistics(data: dict, file_path: str) -> tuple[bool, str]
    
    # User operations
    def handle_create_user(name: str, role: str) -> tuple[bool, str]
    def handle_manage_users(action: str, user_id: str, data: dict) -> tuple[bool, str]
```

### 4. View Layer

#### CLI View
Command-line interface sử dụng argparse.

**Commands:**
```bash
# Exam management
python main.py exam create --title "Đề thi Toán" --teacher-id "GV001"
python main.py exam add-question --exam-id "E001" --content "..." --choices "..." --answer "A"
python main.py exam list
python main.py exam import --file "exam.json"
python main.py exam export --exam-id "E001" --output "exam.json"

# Taking exam
python main.py submit create --exam-id "E001" --student-id "HS001"
python main.py submit answer --submission-id "S001" --question-id "Q001" --answer "A"
python main.py submit finish --submission-id "S001"

# Grading
python main.py grade --submission-id "S001"
python main.py grade --exam-id "E001"  # Grade all submissions

# Statistics
python main.py stats exam --exam-id "E001"
python main.py stats student --student-id "HS001"
python main.py stats export --exam-id "E001" --output "stats.csv"

# User management
python main.py user create --name "Nguyễn Văn A" --role "student"
python main.py user list --role "teacher"
```

#### GUI View
Desktop application sử dụng Tkinter.

**Main Windows:**

1. **Main Menu Window**
   - Buttons: Quản lý đề thi, Làm bài thi, Chấm bài, Thống kê, Quản lý người dùng

2. **Exam Management Window**
   - List view: Danh sách đề thi
   - Buttons: Tạo mới, Sửa, Xóa, Import, Export
   - Form: Nhập thông tin đề thi và câu hỏi

3. **Take Exam Window**
   - Dropdown: Chọn đề thi
   - Input: Nhập mã học sinh
   - Question display: Hiển thị câu hỏi và radio buttons cho lựa chọn
   - Navigation: Câu trước, Câu sau, Nộp bài

4. **Grading Window**
   - List view: Danh sách bài làm chưa chấm
   - Buttons: Chấm bài, Chấm tất cả
   - Result display: Hiển thị kết quả chi tiết

5. **Statistics Window**
   - Tabs: Theo đề thi, Theo học sinh, Phân tích câu hỏi
   - Charts: Biểu đồ điểm số (sử dụng matplotlib nếu cần)
   - Export button: Xuất thống kê ra CSV

6. **User Management Window**
   - List view: Danh sách người dùng
   - Buttons: Thêm, Sửa, Xóa
   - Form: Nhập thông tin người dùng

## Mô Hình Dữ Liệu

### Cấu Trúc Thư Mục
```
project_root/
├── main.py                 # Entry point
├── src/
│   ├── models/            # Data models
│   │   ├── exam.py
│   │   ├── submission.py
│   │   ├── result.py
│   │   └── user.py
│   ├── storage/           # Data access layer
│   │   └── file_storage.py
│   ├── business/          # Business logic
│   │   ├── exam_manager.py
│   │   ├── submission_manager.py
│   │   ├── grading_engine.py
│   │   ├── stats_engine.py
│   │   └── user_manager.py
│   ├── controller/        # Controller layer
│   │   └── app_controller.py
│   └── views/             # Presentation layer
│       ├── cli_view.py
│       └── gui_view.py
├── data/                  # Data storage
│   ├── exams/
│   ├── submissions/
│   ├── results/
│   └── users/
└── tests/                 # Test files
    ├── unit/
    └── property/
```

### Định Dạng File

#### Exam JSON
```json
{
  "exam_id": "E001",
  "title": "Đề thi Toán học",
  "created_by": "GV001",
  "created_at": "2024-12-02T10:00:00Z",
  "questions": [
    {
      "question_id": "Q001",
      "content": "1 + 1 = ?",
      "choices": {
        "A": "1",
        "B": "2",
        "C": "3",
        "D": "4"
      },
      "correct_answer": "B"
    }
  ]
}
```

#### CSV Import Format (Exam)
```csv
question_id,content,choice_A,choice_B,choice_C,choice_D,correct_answer
Q001,"1 + 1 = ?","1","2","3","4",B
Q002,"2 + 2 = ?","2","3","4","5",C
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Exam persistence round-trip
*For any* exam with valid data, saving then loading the exam should produce an equivalent exam with all information preserved (exam_id, title, questions, choices, correct answers).
**Validates: Requirements 1.1**

### Property 2: Adding questions increases count
*For any* exam and valid question, adding the question to the exam should increase the question count by exactly one.
**Validates: Requirements 1.2**

### Property 3: Exam ID invariant on update
*For any* exam, updating the exam's information should preserve the original exam_id unchanged.
**Validates: Requirements 1.3**

### Property 4: Deletion preserves related results
*For any* exam with associated results, deleting the exam should remove the exam but keep all related result records intact.
**Validates: Requirements 1.4**

### Property 5: JSON import/export round-trip
*For any* valid exam, exporting to JSON then importing should produce an equivalent exam with identical data.
**Validates: Requirements 2.1, 2.3**

### Property 6: CSV import/export round-trip
*For any* valid exam, exporting to CSV then importing should produce an exam with equivalent question data.
**Validates: Requirements 2.2, 2.4**

### Property 7: Invalid import preserves state
*For any* invalid import file and current system state, attempting to import should reject the operation and leave the system state unchanged.
**Validates: Requirements 2.5**

### Property 8: Answer persistence
*For any* submission and answer, saving an answer then loading the submission should retrieve the same answer.
**Validates: Requirements 3.2**

### Property 9: Submission round-trip
*For any* valid submission with student_id, exam_id, and answers, saving then loading should produce an equivalent submission with all data preserved.
**Validates: Requirements 3.3**

### Property 10: Grading correctness
*For any* exam and submission, the grading result should correctly identify each answer as correct or incorrect by comparing with the exam's correct answers.
**Validates: Requirements 4.1**

### Property 11: Score calculation formula
*For any* grading result, the score should equal (correct_answers / total_questions) * 10, rounded to appropriate precision.
**Validates: Requirements 4.2**

### Property 12: Result completeness
*For any* graded submission, the result should contain score, total_questions, correct_answers, wrong_answers, and detailed comparison for each question.
**Validates: Requirements 4.3**

### Property 13: Batch grading completeness
*For any* set of submissions for an exam, batch grading should produce exactly one result for each submission.
**Validates: Requirements 4.5**

### Property 14: User persistence round-trip
*For any* valid user with name, user_id, and role, saving then loading should produce an equivalent user with all information preserved.
**Validates: Requirements 5.1**

### Property 15: User ID invariant on update
*For any* user, updating the user's information should preserve the original user_id unchanged.
**Validates: Requirements 5.2**

### Property 16: User deletion preserves submissions
*For any* user with associated submissions and results, deleting the user should remove the user but keep all related submissions and results intact.
**Validates: Requirements 5.3**

### Property 17: User ID uniqueness
*For any* two users in the system, attempting to create a new user with an existing user_id should be rejected with an error.
**Validates: Requirements 5.5**

### Property 18: Statistics calculation accuracy
*For any* set of results for an exam, the calculated average, maximum, and minimum scores should match the actual values computed from the result set.
**Validates: Requirements 6.1**

### Property 19: Student results completeness
*For any* student_id, querying student statistics should return all results associated with that student.
**Validates: Requirements 6.2**

### Property 20: Question analysis accuracy
*For any* exam with results, the correct answer rate for each question should equal (correct_count / total_answers) for that question.
**Validates: Requirements 6.3**

### Property 21: Statistics export format
*For any* statistics data, exporting to CSV should produce a valid CSV file that can be parsed and contains all the statistics information.
**Validates: Requirements 6.4**

### Property 22: Corrupted file handling
*For any* corrupted or malformed data file, attempting to load should return an error without modifying existing system state.
**Validates: Requirements 9.3**

### Property 23: ID uniqueness enforcement
*For any* entity type (exam, user, submission), attempting to create an entity with a duplicate ID should be rejected with an error.
**Validates: Requirements 9.4**

### Property 24: Immediate persistence
*For any* data modification operation, the changes should be immediately written to the corresponding file.
**Validates: Requirements 10.1**

### Property 25: UTF-8 encoding preservation
*For any* data containing Vietnamese characters, saving then loading should preserve all characters correctly without encoding errors.
**Validates: Requirements 10.4**

### Property 26: Auto-initialization
*For any* missing data file, the first access should automatically create the file with valid default structure.
**Validates: Requirements 10.5**

## Error Handling

### Validation Errors

1. **Empty Exam**: Reject exams with zero questions
2. **Missing Correct Answer**: Reject questions without a correct_answer field
3. **Invalid Answer Choice**: Reject answers not in {A, B, C, D}
4. **Duplicate IDs**: Reject creation of entities with existing IDs
5. **Missing Required Fields**: Reject entities missing required fields

### File System Errors

1. **File Not Found**: Auto-create with default structure
2. **Permission Denied**: Return clear error message
3. **Corrupted JSON**: Return parse error without modifying data
4. **Invalid CSV Format**: Return format error with line number
5. **Disk Full**: Return storage error message

### Business Logic Errors

1. **Exam Not Found**: Return error when grading submission for non-existent exam
2. **Submission Not Found**: Return error when accessing non-existent submission
3. **User Not Found**: Return error when accessing non-existent user
4. **Invalid Role**: Reject user creation with role other than "teacher" or "student"

### Error Response Format

All errors should return a tuple: `(success: bool, message: str, data: Optional[dict])`

Example:
```python
(False, "Đề thi không tồn tại: E001", None)
(True, "Tạo đề thi thành công", {"exam_id": "E001"})
```

## Testing Strategy

### Unit Testing

Unit tests will verify specific functionality of individual components:

1. **FileStorageManager Tests**
   - Test saving and loading each entity type
   - Test file creation and directory structure
   - Test UTF-8 encoding with Vietnamese text
   - Test error handling for corrupted files

2. **ExamManager Tests**
   - Test exam creation with valid data
   - Test adding questions to exams
   - Test exam validation rules
   - Test exam update and delete operations

3. **GradingEngine Tests**
   - Test score calculation with known inputs
   - Test answer comparison logic
   - Test result structure completeness

4. **StatsEngine Tests**
   - Test statistics calculations with known datasets
   - Test aggregation functions (avg, min, max)
   - Test filtering by exam_id and student_id

5. **UserManager Tests**
   - Test user creation and validation
   - Test uniqueness constraints
   - Test user update preserving ID

### Property-Based Testing

Property-based tests will verify universal properties across randomly generated inputs using **Hypothesis** library:

**Configuration**: Each property test should run a minimum of 100 iterations.

**Test Tagging**: Each property-based test must include a comment with this format:
```python
# Feature: multiple-choice-grading-system, Property X: [property description]
```

**Property Test Coverage**:

1. **Round-trip Properties** (Properties 1, 5, 6, 9, 14)
   - Generate random exams, submissions, users
   - Test save/load cycles preserve data
   - Test JSON and CSV serialization

2. **Invariant Properties** (Properties 3, 15)
   - Generate random entities and updates
   - Verify IDs remain unchanged after updates

3. **Calculation Properties** (Properties 11, 18, 20)
   - Generate random result sets
   - Verify mathematical correctness of scores and statistics

4. **Constraint Properties** (Properties 17, 23)
   - Generate entities with duplicate IDs
   - Verify system rejects duplicates

5. **State Preservation Properties** (Properties 4, 7, 16, 22)
   - Generate operations that should not affect certain data
   - Verify related data remains intact

6. **Encoding Properties** (Property 25)
   - Generate strings with Vietnamese characters
   - Verify encoding/decoding preserves characters

**Hypothesis Strategies**:

```python
from hypothesis import strategies as st

# Strategy for generating exams
exam_strategy = st.builds(
    dict,
    exam_id=st.text(min_size=1, max_size=10),
    title=st.text(min_size=1, max_size=100),
    questions=st.lists(question_strategy, min_size=1, max_size=50)
)

# Strategy for generating questions
question_strategy = st.builds(
    dict,
    question_id=st.text(min_size=1, max_size=10),
    content=st.text(min_size=1, max_size=500),
    choices=st.fixed_dictionaries({
        'A': st.text(min_size=1),
        'B': st.text(min_size=1),
        'C': st.text(min_size=1),
        'D': st.text(min_size=1)
    }),
    correct_answer=st.sampled_from(['A', 'B', 'C', 'D'])
)

# Strategy for Vietnamese text
vietnamese_text = st.text(
    alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll'),
        whitelist_characters='àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ'
    ),
    min_size=1,
    max_size=100
)
```

### Integration Testing

Integration tests will verify end-to-end workflows:

1. **Complete Exam Workflow**
   - Create exam → Add questions → Save → Load → Verify

2. **Complete Grading Workflow**
   - Create exam → Create submission → Submit answers → Grade → Verify result

3. **Import/Export Workflow**
   - Create exam → Export JSON → Import → Verify equivalence
   - Create exam → Export CSV → Import → Verify equivalence

4. **Statistics Workflow**
   - Create multiple results → Calculate statistics → Verify accuracy

### Test Data

Test data should include:
- Vietnamese characters in all text fields
- Edge cases: empty strings, maximum lengths, special characters
- Boundary values: 0 questions, 100 questions, 0% score, 100% score
- Invalid data: missing fields, wrong types, duplicate IDs

## Performance Considerations

### File I/O Optimization

1. **Lazy Loading**: Load data only when needed
2. **Caching**: Cache frequently accessed exams and users in memory
3. **Batch Operations**: Group multiple writes into single file operation
4. **Indexing**: Maintain in-memory index of IDs for fast lookups

### Scalability Limits

Given file-based storage:
- **Exams**: Up to 1000 exams per system
- **Questions per Exam**: Up to 200 questions
- **Submissions**: Up to 10,000 submissions
- **Users**: Up to 1000 users

For larger scale, consider migrating to database storage.

## Security Considerations

1. **Input Validation**: Validate all user inputs before processing
2. **File Path Sanitization**: Prevent directory traversal attacks in file operations
3. **Data Integrity**: Use checksums or validation to detect corrupted files
4. **Access Control**: Implement role-based permissions (teacher vs student)
5. **Backup**: Recommend regular backups of data directory

## Future Enhancements

1. **Database Migration**: Support SQLite or PostgreSQL for better scalability
2. **Web Interface**: Add web-based interface alongside desktop/CLI
3. **Real-time Collaboration**: Multiple users editing simultaneously
4. **Advanced Analytics**: Machine learning for question difficulty analysis
5. **Question Bank**: Shared repository of questions across exams
6. **Timed Exams**: Add time limits and automatic submission
7. **Question Types**: Support multiple correct answers, true/false, fill-in-blank
8. **Multimedia**: Support images in questions and answers
