# 🎓 Hệ Thống Chấm Trắc Nghiệm

Hệ thống chấm trắc nghiệm tự động, hiện đại với giao diện web đẹp mắt.

[![Tests](https://img.shields.io/badge/tests-39%20passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-lightgrey)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🌟 Demo

**Live Demo**: [https://he-thong-lam-cham-trac-nghiem.onrender.com](https://he-thong-lam-cham-trac-nghiem.onrender.com)

## ✨ Tính Năng

### 👨‍🏫 Dành cho Giáo Viên
- ✅ Tạo đề thi trắc nghiệm (1-50 câu)
- ✅ Quản lý đề thi (xem, sửa, xóa)
- ✅ Xem thống kê điểm số
- ✅ Xem kết quả từng học sinh
- ✅ Xuất báo cáo Excel/CSV
- ✅ Import/Export đề thi

### 👨‍🎓 Dành cho Học Sinh
- ✅ Làm bài thi online
- ✅ Xem kết quả ngay lập tức
- ✅ Chi tiết từng câu đúng/sai
- ✅ Giao diện thân thiện, dễ sử dụng

### 📊 Thống Kê & Báo Cáo
- ✅ Điểm trung bình, cao nhất, thấp nhất
- ✅ Số lượng học sinh làm bài
- ✅ Phân tích từng câu hỏi
- ✅ Xuất báo cáo chi tiết

## 🚀 Cài Đặt & Chạy Local

### 1. Clone repository
```bash
git clone https://github.com/DYBInh2k5/He-Thong-Lam-Cham-Trac-Nghiem.git
cd He-Thong-Lam-Cham-Trac-Nghiem
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy web app
```bash
python web_app.py
```

### 4. Truy cập
Mở trình duyệt: `http://127.0.0.1:5000`

## 📱 Sử Dụng

### Giáo Viên
1. Truy cập trang chủ
2. Chọn **"Giáo Viên"**
3. Nhập thông tin đề thi
4. Chọn số câu hỏi (1-50)
5. Nhập nội dung câu hỏi
6. Lưu và nhận **mã đề**

### Học Sinh
1. Truy cập trang chủ
2. Chọn **"Học Sinh"**
3. Nhập **mã đề** và **mã học sinh**
4. Làm bài thi
5. Nộp bài và xem kết quả

### Thống Kê
1. Truy cập **"Thống Kê & Quản Lý"**
2. Xem danh sách đề thi
3. Xem kết quả học sinh
4. Xuất báo cáo Excel

## 🧪 Testing

```bash
# Chạy tất cả tests
python -m pytest -v

# Test web app
python test_web.py

# Chỉ unit tests
python -m pytest tests/unit/ -v

# Chỉ property tests
python -m pytest tests/property/ -v
```

**Kết quả**: 39/39 tests PASS ✅

## 🔄 Cập Nhật Hệ Thống

### Cách 1: Tự động (Khuyến nghị)
```bash
update.bat
```

### Cách 2: Thủ công
```bash
git add .
git commit -m "Mo ta thay doi"
git push origin main
```

Render.com sẽ **tự động deploy** sau 1-2 phút!

📖 Chi tiết: [HUONG_DAN_UPDATE.md](HUONG_DAN_UPDATE.md)

## 🌐 Deploy lên Internet

### Render.com (Miễn phí)
1. Đọc: [DEPLOY_NHANH.md](DEPLOY_NHANH.md)
2. Hoặc: [README_DEPLOY.md](README_DEPLOY.md)

### Các nền tảng khác
- PythonAnywhere
- Railway.app
- Fly.io
- Heroku

## 📁 Cấu Trúc Dự Án

```
He-Thong-Lam-Cham-Trac-Nghiem/
├── web_app.py              # Flask web application
├── src/
│   ├── models/            # Data models (Exam, Question, User, etc.)
│   ├── storage/           # File storage manager
│   ├── business/          # Business logic (ExamManager, GradingEngine)
│   └── views/             # View layer
├── templates/             # HTML templates
│   ├── index.html        # Trang chủ
│   ├── teacher.html      # Trang giáo viên
│   ├── student.html      # Trang học sinh
│   └── statistics.html   # Trang thống kê
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── property/         # Property-based tests
├── data/                  # Data storage (JSON files)
├── requirements.txt       # Python dependencies
└── render.yaml           # Render.com config
```

## 🛠️ Công Nghệ

- **Backend**: Python 3.11 + Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Storage**: File-based (JSON)
- **Testing**: pytest + Hypothesis
- **Deploy**: Render.com
- **Version Control**: Git + GitHub

## 📊 Thống Kê Dự Án

- **Files**: 46
- **Lines of Code**: 6000+
- **Tests**: 39 (100% pass)
- **Web Pages**: 5
- **API Endpoints**: 10+
- **Models**: 5 (Exam, Question, Submission, Result, User)

## 📝 Tài Liệu

- [DEPLOY_NHANH.md](DEPLOY_NHANH.md) - Hướng dẫn deploy nhanh
- [README_DEPLOY.md](README_DEPLOY.md) - Hướng dẫn deploy chi tiết
- [HUONG_DAN_UPDATE.md](HUONG_DAN_UPDATE.md) - Hướng dẫn update hệ thống
- [CHANGELOG.md](CHANGELOG.md) - Lịch sử thay đổi

## 🤝 Đóng Góp

Mọi đóng góp đều được chào đón! Hãy:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📄 License

MIT License - Xem [LICENSE](LICENSE) để biết thêm chi tiết

## 👨‍💻 Tác Giả

**Võ Duy Bình**
- Email: binh.vd01500@sinhvien.hoasen.edu.vn
- GitHub: [@DYBInh2k5](https://github.com/DYBInh2k5)

## 🙏 Cảm Ơn

- Flask Framework
- Render.com
- GitHub
- Tất cả contributors

## 📞 Liên Hệ & Hỗ Trợ

- **Issues**: [GitHub Issues](https://github.com/DYBInh2k5/He-Thong-Lam-Cham-Trac-Nghiem/issues)
- **Email**: binh.vd01500@sinhvien.hoasen.edu.vn

---

⭐ Nếu thấy hữu ích, hãy cho project một star nhé!
