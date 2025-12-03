# Hệ Thống Chấm Trắc Nghiệm

Hệ thống chấm trắc nghiệm tự động với giao diện desktop và command-line.

## Cài Đặt

```bash
pip install -r requirements.txt
```

## Cấu Trúc Dự Án

```
project_root/
├── main.py                 # Entry point
├── src/
│   ├── models/            # Data models
│   ├── storage/           # Data access layer
│   ├── business/          # Business logic
│   ├── controller/        # Controller layer
│   └── views/             # Presentation layer
├── data/                  # Data storage
├── tests/                 # Test files
└── requirements.txt       # Dependencies
```

## Sử Dụng

### CLI Mode
```bash
python main.py cli
```

### GUI Mode
```bash
python main.py gui
```

## Testing

```bash
# Run all tests
pytest

# Run unit tests only
pytest tests/unit/

# Run property tests only
pytest tests/property/
```

## Tính Năng

- ✅ Quản lý đề thi và câu hỏi
- ✅ Làm bài thi trắc nghiệm
- ✅ Chấm điểm tự động
- ✅ Thống kê kết quả
- ✅ Import/Export JSON và CSV
- ✅ Quản lý người dùng (giáo viên, học sinh)
- ✅ Giao diện CLI và GUI

## Yêu Cầu

- Python 3.8+
- pytest (cho testing)
- hypothesis (cho property-based testing)
