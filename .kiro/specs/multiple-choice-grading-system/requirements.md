# Tài Liệu Yêu Cầu - Hệ Thống Chấm Trắc Nghiệm

## Giới Thiệu

Hệ thống chấm trắc nghiệm là một ứng dụng desktop và command-line cho phép giáo viên tạo đề thi, học sinh làm bài thi, và tự động chấm điểm với khả năng quản lý và thống kê kết quả. Hệ thống lưu trữ dữ liệu dưới dạng file (JSON/CSV) và hỗ trợ nhiều người dùng.

## Thuật Ngữ

- **Hệ Thống**: Hệ thống chấm trắc nghiệm
- **Giáo Viên**: Người dùng có quyền tạo và quản lý đề thi
- **Học Sinh**: Người dùng làm bài thi
- **Đề Thi**: Tập hợp các câu hỏi trắc nghiệm với đáp án đúng
- **Câu Hỏi**: Một câu hỏi trắc nghiệm với nhiều lựa chọn (A, B, C, D)
- **Bài Làm**: Tập hợp các câu trả lời của học sinh cho một đề thi
- **Kết Quả**: Điểm số và thông tin chi tiết về bài làm đã được chấm

## Yêu Cầu

### Yêu Cầu 1: Quản Lý Đề Thi

**User Story:** Là một giáo viên, tôi muốn tạo và quản lý đề thi trắc nghiệm, để có thể kiểm tra kiến thức của học sinh.

#### Tiêu Chí Chấp Nhận

1. WHEN giáo viên tạo đề thi mới, THE Hệ Thống SHALL lưu đề thi với thông tin bao gồm tên đề, mã đề, và danh sách câu hỏi
2. WHEN giáo viên thêm câu hỏi vào đề thi, THE Hệ Thống SHALL lưu câu hỏi với nội dung, các lựa chọn (A, B, C, D), và đáp án đúng
3. WHEN giáo viên chỉnh sửa đề thi, THE Hệ Thống SHALL cập nhật thông tin đề thi và giữ nguyên mã đề
4. WHEN giáo viên xóa đề thi, THE Hệ Thống SHALL xóa đề thi khỏi hệ thống và giữ lại các kết quả đã chấm liên quan
5. THE Hệ Thống SHALL lưu trữ đề thi dưới định dạng JSON

### Yêu Cầu 2: Import và Export Đề Thi

**User Story:** Là một giáo viên, tôi muốn import và export đề thi, để có thể chia sẻ và sao lưu đề thi dễ dàng.

#### Tiêu Chí Chấp Nhận

1. WHEN giáo viên import file JSON chứa đề thi, THE Hệ Thống SHALL đọc và lưu đề thi vào hệ thống
2. WHEN giáo viên import file CSV chứa câu hỏi, THE Hệ Thống SHALL phân tích và tạo đề thi từ dữ liệu CSV
3. WHEN giáo viên export đề thi, THE Hệ Thống SHALL tạo file JSON chứa toàn bộ thông tin đề thi
4. WHEN giáo viên export đề thi sang CSV, THE Hệ Thống SHALL tạo file CSV với định dạng chuẩn
5. IF file import có định dạng không hợp lệ, THEN THE Hệ Thống SHALL báo lỗi chi tiết và không thay đổi dữ liệu hiện tại

### Yêu Cầu 3: Làm Bài Thi

**User Story:** Là một học sinh, tôi muốn làm bài thi trắc nghiệm, để kiểm tra kiến thức của mình.

#### Tiêu Chí Chấp Nhận

1. WHEN học sinh chọn đề thi để làm, THE Hệ Thống SHALL hiển thị danh sách câu hỏi với các lựa chọn
2. WHEN học sinh chọn đáp án cho câu hỏi, THE Hệ Thống SHALL lưu lựa chọn của học sinh
3. WHEN học sinh nộp bài, THE Hệ Thống SHALL lưu bài làm với thông tin học sinh, mã đề, và các câu trả lời
4. THE Hệ Thống SHALL cho phép học sinh xem lại và thay đổi câu trả lời trước khi nộp bài
5. THE Hệ Thống SHALL lưu trữ bài làm dưới định dạng JSON

### Yêu Cầu 4: Chấm Điểm Tự Động

**User Story:** Là một giáo viên, tôi muốn hệ thống tự động chấm điểm bài thi, để tiết kiệm thời gian và đảm bảo tính chính xác.

#### Tiêu Chí Chấp Nhận

1. WHEN hệ thống chấm bài làm, THE Hệ Thống SHALL so sánh từng câu trả lời với đáp án đúng
2. WHEN hệ thống tính điểm, THE Hệ Thống SHALL tính tổng số câu đúng và tính điểm theo thang điểm 10
3. WHEN hệ thống hoàn thành chấm bài, THE Hệ Thống SHALL lưu kết quả với điểm số, số câu đúng, số câu sai, và chi tiết từng câu
4. THE Hệ Thống SHALL lưu trữ kết quả chấm bài dưới định dạng JSON
5. WHEN chấm nhiều bài làm cùng lúc, THE Hệ Thống SHALL xử lý tuần tự và lưu kết quả cho từng bài

### Yêu Cầu 5: Quản Lý Người Dùng

**User Story:** Là một quản trị viên, tôi muốn quản lý thông tin giáo viên và học sinh, để theo dõi và phân quyền người dùng.

#### Tiêu Chí Chấp Nhận

1. WHEN thêm người dùng mới, THE Hệ Thống SHALL lưu thông tin bao gồm tên, mã số, vai trò (giáo viên hoặc học sinh)
2. WHEN cập nhật thông tin người dùng, THE Hệ Thống SHALL giữ nguyên mã số và cập nhật các thông tin khác
3. WHEN xóa người dùng, THE Hệ Thống SHALL xóa thông tin người dùng nhưng giữ lại các bài làm và kết quả liên quan
4. THE Hệ Thống SHALL lưu trữ thông tin người dùng dưới định dạng JSON
5. THE Hệ Thống SHALL đảm bảo mỗi mã số người dùng là duy nhất

### Yêu Cầu 6: Thống Kê Kết Quả

**User Story:** Là một giáo viên, tôi muốn xem thống kê kết quả thi, để đánh giá hiệu quả học tập và độ khó của đề thi.

#### Tiêu Chí Chấp Nhận

1. WHEN giáo viên xem thống kê theo đề thi, THE Hệ Thống SHALL hiển thị điểm trung bình, điểm cao nhất, điểm thấp nhất
2. WHEN giáo viên xem thống kê theo học sinh, THE Hệ Thống SHALL hiển thị danh sách các bài thi đã làm và điểm số
3. WHEN giáo viên xem phân tích câu hỏi, THE Hệ Thống SHALL hiển thị tỷ lệ trả lời đúng cho từng câu hỏi
4. WHEN giáo viên export thống kê, THE Hệ Thống SHALL tạo file CSV chứa dữ liệu thống kê
5. THE Hệ Thống SHALL tính toán thống kê dựa trên tất cả kết quả đã lưu

### Yêu Cầu 7: Giao Diện Command-Line

**User Story:** Là một người dùng, tôi muốn sử dụng hệ thống qua command-line, để thực hiện các thao tác nhanh chóng.

#### Tiêu Chí Chấp Nhận

1. WHEN người dùng chạy lệnh tạo đề thi, THE Hệ Thống SHALL yêu cầu nhập thông tin và tạo đề thi mới
2. WHEN người dùng chạy lệnh import, THE Hệ Thống SHALL đọc file và import dữ liệu vào hệ thống
3. WHEN người dùng chạy lệnh chấm bài, THE Hệ Thống SHALL chấm điểm và hiển thị kết quả
4. WHEN người dùng chạy lệnh thống kê, THE Hệ Thống SHALL hiển thị thống kê theo yêu cầu
5. IF lệnh có tham số không hợp lệ, THEN THE Hệ Thống SHALL hiển thị hướng dẫn sử dụng

### Yêu Cầu 8: Giao Diện Desktop

**User Story:** Là một người dùng, tôi muốn sử dụng giao diện đồ họa desktop, để thao tác dễ dàng và trực quan hơn.

#### Tiêu Chí Chấp Nhận

1. WHEN người dùng mở ứng dụng desktop, THE Hệ Thống SHALL hiển thị giao diện chính với menu điều hướng
2. WHEN giáo viên tạo đề thi qua giao diện, THE Hệ Thống SHALL cung cấp form nhập liệu với validation
3. WHEN học sinh làm bài qua giao diện, THE Hệ Thống SHALL hiển thị câu hỏi và cho phép chọn đáp án
4. WHEN người dùng xem kết quả qua giao diện, THE Hệ Thống SHALL hiển thị thông tin chi tiết và trực quan
5. THE Hệ Thống SHALL cập nhật giao diện ngay lập tức khi dữ liệu thay đổi

### Yêu Cầu 9: Xử Lý Lỗi và Validation

**User Story:** Là một người dùng, tôi muốn hệ thống báo lỗi rõ ràng khi có vấn đề, để biết cách khắc phục.

#### Tiêu Chí Chấp Nhận

1. IF đề thi không có câu hỏi nào, THEN THE Hệ Thống SHALL từ chối lưu và báo lỗi
2. IF câu hỏi thiếu đáp án đúng, THEN THE Hệ Thống SHALL từ chối lưu câu hỏi và báo lỗi
3. IF file dữ liệu bị hỏng hoặc không đọc được, THEN THE Hệ Thống SHALL báo lỗi và không làm mất dữ liệu hiện tại
4. IF mã đề thi hoặc mã người dùng bị trùng, THEN THE Hệ Thống SHALL từ chối thao tác và báo lỗi
5. WHEN có lỗi xảy ra, THE Hệ Thống SHALL hiển thị thông báo lỗi bằng tiếng Việt và rõ ràng

### Yêu Cầu 10: Lưu Trữ và Đồng Bộ Dữ Liệu

**User Story:** Là một người dùng, tôi muốn dữ liệu được lưu trữ an toàn, để không bị mất thông tin quan trọng.

#### Tiêu Chí Chấp Nhận

1. WHEN dữ liệu thay đổi, THE Hệ Thống SHALL lưu ngay lập tức vào file
2. WHEN đọc dữ liệu từ file, THE Hệ Thống SHALL kiểm tra tính hợp lệ trước khi sử dụng
3. THE Hệ Thống SHALL tổ chức file dữ liệu theo cấu trúc thư mục rõ ràng (exams, submissions, results, users)
4. THE Hệ Thống SHALL sử dụng encoding UTF-8 cho tất cả file để hỗ trợ tiếng Việt
5. IF file dữ liệu không tồn tại, THEN THE Hệ Thống SHALL tạo file mới với cấu trúc mặc định
