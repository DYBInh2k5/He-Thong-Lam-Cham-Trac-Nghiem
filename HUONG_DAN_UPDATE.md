# 🔄 HƯỚNG DẪN UPDATE HỆ THỐNG

## ✨ Tin tốt: Update CỰC KỲ ĐƠN GIẢN!

Render.com có tính năng **Auto Deploy** - tự động deploy lại khi bạn push code mới lên GitHub.

---

## 🚀 CÁCH 1: Dùng Script Tự Động (KHUYẾN NGHỊ)

### Chỉ cần chạy 1 lệnh:

```bash
update.bat
```

Script sẽ tự động:
1. ✅ Add files đã thay đổi
2. ✅ Commit với message
3. ✅ Push lên GitHub
4. ✅ Render tự động deploy

**Đợi 1-2 phút** → Website đã được update!

---

## 🛠️ CÁCH 2: Thủ Công (3 Lệnh)

### Bước 1: Add và Commit
```bash
git add .
git commit -m "Update: Mo ta thay doi cua ban"
```

### Bước 2: Push lên GitHub
```bash
git push origin main
```

### Bước 3: Đợi Render Deploy
- Render tự động phát hiện thay đổi
- Tự động build và deploy
- Đợi 1-2 phút

---

## 📋 VÍ DỤ CÁC TRƯỜNG HỢP UPDATE

### 1. Thêm tính năng mới
```bash
# Sửa code...
git add .
git commit -m "Them tinh nang xuat PDF"
git push origin main
```

### 2. Sửa bug
```bash
# Sửa bug...
git add .
git commit -m "Fix loi cham diem"
git push origin main
```

### 3. Cập nhật giao diện
```bash
# Sửa HTML/CSS...
git add .
git commit -m "Cap nhat giao dien dep hon"
git push origin main
```

### 4. Thay đổi nhiều file
```bash
# Sửa nhiều file...
update.bat
# Nhập mô tả: "Cap nhat toan bo he thong"
```

---

## 🔍 KIỂM TRA TIẾN TRÌNH DEPLOY

### Cách 1: Qua Dashboard
1. Mở: https://dashboard.render.com
2. Click vào service của bạn
3. Xem tab **"Events"** hoặc **"Logs"**
4. Đợi status chuyển sang **"Live"**

### Cách 2: Qua Email
- Render sẽ gửi email thông báo:
  - ✅ Deploy thành công
  - ❌ Deploy thất bại (nếu có lỗi)

---

## ⚠️ LƯU Ý QUAN TRỌNG

### 1. Dữ liệu sẽ bị mất khi deploy
- **Free plan**: Mỗi lần deploy = reset dữ liệu
- **Giải pháp**: 
  - Xuất CSV trước khi update
  - Hoặc upgrade lên Paid plan

### 2. Downtime khi deploy
- Website sẽ **offline 30-60 giây** khi deploy
- Thông báo cho người dùng trước khi update

### 3. Test trước khi push
```bash
# Chạy test local
python test_web.py

# Nếu OK mới push
git push origin main
```

---

## 🎯 QUY TRÌNH UPDATE CHUẨN

### 1. Sửa code local
- Thêm tính năng mới
- Sửa bug
- Cải thiện giao diện

### 2. Test local
```bash
# Chạy web local
python web_app.py

# Test trong browser
http://127.0.0.1:5000

# Chạy tests
python test_web.py
```

### 3. Commit và Push
```bash
update.bat
# Hoặc
git add .
git commit -m "Mo ta thay doi"
git push origin main
```

### 4. Đợi Deploy
- Vào Dashboard Render
- Xem logs
- Đợi status "Live"

### 5. Test Production
- Truy cập URL production
- Test các tính năng mới
- Kiểm tra không có lỗi

---

## 🆘 XỬ LÝ LỖI

### Lỗi: Deploy failed
**Nguyên nhân**: Code có lỗi syntax hoặc thiếu dependencies

**Giải pháp**:
1. Xem logs trên Render Dashboard
2. Sửa lỗi trong code
3. Push lại:
```bash
git add .
git commit -m "Fix loi deploy"
git push origin main
```

### Lỗi: Git push rejected
**Nguyên nhân**: Có conflict với code trên GitHub

**Giải pháp**:
```bash
git pull origin main
# Giải quyết conflict nếu có
git push origin main
```

### Lỗi: Website không update
**Nguyên nhân**: Render chưa deploy

**Giải pháp**:
1. Vào Render Dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 💡 TIPS & TRICKS

### 1. Commit thường xuyên
```bash
# Mỗi khi hoàn thành 1 tính năng nhỏ
git add .
git commit -m "Hoan thanh tinh nang X"
```

### 2. Viết commit message rõ ràng
```bash
# TỐT
git commit -m "Them chuc nang xuat Excel cho ket qua"

# KHÔNG TỐT
git commit -m "update"
```

### 3. Backup trước khi update lớn
```bash
# Tạo branch backup
git branch backup-$(date +%Y%m%d)

# Update
git add .
git commit -m "Update lon"
git push origin main
```

### 4. Rollback nếu cần
```bash
# Xem lịch sử commit
git log

# Quay lại commit trước
git revert HEAD
git push origin main
```

---

## 📊 THEO DÕI PHIÊN BẢN

### Tạo file CHANGELOG.md
```markdown
# Lịch Sử Thay Đổi

## [1.1.0] - 2024-12-03
- Thêm tính năng xuất Excel
- Sửa lỗi chấm điểm
- Cải thiện giao diện

## [1.0.0] - 2024-12-02
- Phiên bản đầu tiên
- Tạo đề thi
- Chấm điểm tự động
```

---

## ✅ CHECKLIST UPDATE

- [ ] Sửa code xong
- [ ] Test local OK
- [ ] Chạy `python test_web.py` - PASS
- [ ] Commit với message rõ ràng
- [ ] Push lên GitHub
- [ ] Kiểm tra Render Dashboard
- [ ] Đợi deploy xong (1-2 phút)
- [ ] Test trên production
- [ ] Thông báo người dùng (nếu cần)

---

## 🎉 KẾT LUẬN

Update hệ thống CỰC KỲ ĐƠN GIẢN:
1. Sửa code
2. Chạy `update.bat`
3. Đợi 1-2 phút
4. Xong!

**Render tự động lo tất cả!**
