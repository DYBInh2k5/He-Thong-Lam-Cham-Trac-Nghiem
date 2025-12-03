"""Test web app trước khi deploy."""

import sys

def test_imports():
    """Test import các module cần thiết."""
    print("Testing imports...")
    try:
        from flask import Flask
        print("✓ Flask OK")
        
        from src.storage.file_storage import FileStorageManager
        print("✓ FileStorageManager OK")
        
        from src.business.exam_manager import ExamManager
        print("✓ ExamManager OK")
        
        from src.business.grading_engine import GradingEngine
        print("✓ GradingEngine OK")
        
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False


def test_web_app():
    """Test web app có chạy được không."""
    print("\nTesting web app...")
    try:
        from web_app import app
        
        with app.test_client() as client:
            # Test trang chủ
            response = client.get('/')
            assert response.status_code == 200
            print("✓ Trang chủ OK")
            
            # Test API list exams
            response = client.get('/api/list-exams')
            assert response.status_code == 200
            print("✓ API list exams OK")
            
            # Test trang teacher
            response = client.get('/teacher')
            assert response.status_code == 200
            print("✓ Trang teacher OK")
            
            # Test trang student
            response = client.get('/student')
            assert response.status_code == 200
            print("✓ Trang student OK")
            
            # Test trang statistics
            response = client.get('/statistics')
            assert response.status_code == 200
            print("✓ Trang statistics OK")
        
        return True
    except Exception as e:
        print(f"✗ Web app error: {e}")
        return False


def main():
    """Chạy tất cả tests."""
    print("="*50)
    print("KIỂM TRA HỆ THỐNG TRƯỚC KHI DEPLOY")
    print("="*50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test web app
    if not test_web_app():
        success = False
    
    print("\n" + "="*50)
    if success:
        print("✅ TẤT CẢ TESTS PASS - SẴN SÀNG DEPLOY!")
        print("="*50)
        print("\nBước tiếp theo:")
        print("1. Đọc file: DEPLOY_NHANH.md")
        print("2. Hoặc chạy: deploy.bat")
        return 0
    else:
        print("❌ CÓ LỖI - VUI LÒNG SỬA TRƯỚC KHI DEPLOY")
        print("="*50)
        return 1


if __name__ == "__main__":
    sys.exit(main())
