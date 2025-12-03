# 🚀 Hướng Dẫn Deploy Lên Render.com

## Bước 1: Chuẩn bị

✅ Code đã được kiểm tra - 39 tests PASS
✅ File cấu hình đã sẵn sàng

## Bước 2: Tạo tài khoản Render.com

1. Truy cập: https://render.com
2. Click **"Get Started"** hoặc **"Sign Up"**
3. Đăng ký bằng:
   - GitHub (khuyến nghị)
   - GitLab
   - Email

## Bước 3: Push code lên GitHub

### 3.1. Tạo repository trên GitHub
1. Truy cập: https://github.com/new
2. Đặt tên: `he-thong-cham-trac-nghiem`
3. Chọn **Public** hoặc **Private**
4. Click **"Create repository"**

### 3.2. Push code
```bash
# Khởi tạo git (nếu chưa có)
git init

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit - Hệ thống chấm trắc nghiệm"

# Add remote (thay YOUR_USERNAME bằng username GitHub của bạn)
git remote add origin https://github.com/YOUR_USERNAME/he-thong-cham-trac-nghiem.git

# Push
git branch -M main
git push -u origin main
```

## Bước 4: Deploy trên Render

1. Đăng nhập vào Render.com
2. Click **"New +"** → **"Web Service"**
3. Chọn **"Connect a repository"**
4. Chọn repository `he-thong-cham-trac-nghiem`
5. Cấu hình:
   - **Name**: `he-thong-cham-trac-nghiem`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web_app:app`
   - **Plan**: Chọn **Free**
6. Click **"Create Web Service"**

## Bước 5: Đợi Deploy

- Render sẽ tự động build và deploy (3-5 phút)
- Bạn sẽ nhận được URL: `https://he-thong-cham-trac-nghiem.onrender.com`

## Bước 6: Truy cập

Sau khi deploy xong, truy cập URL của bạn:
- `https://YOUR-APP-NAME.onrender.com`

## ⚠️ Lưu ý quan trọng

### 1. Free Plan của Render:
- **Miễn phí 100%**
- App sẽ **sleep sau 15 phút không hoạt động**
- Lần đầu truy cập sau khi sleep sẽ mất 30-60 giây để wake up
- Giới hạn 750 giờ/tháng (đủ dùng)

### 2. Dữ liệu:
- Dữ liệu lưu trong thư mục `data/`
- **Lưu ý**: Render free plan sẽ **xóa dữ liệu khi restart**
- Để lưu dữ liệu lâu dài, cần:
  - Upgrade lên Paid plan ($7/tháng)
  - Hoặc dùng database (PostgreSQL, MongoDB)

### 3. Bảo mật:
- Thêm authentication nếu cần
- Giới hạn số lượng request
- Backup dữ liệu thường xuyên

## 🎯 Các nền tảng deploy khác (miễn phí)

### 1. **PythonAnywhere** (Khuyến nghị cho dữ liệu lâu dài)
- URL: https://www.pythonanywhere.com
- Ưu điểm: Dữ liệu không bị xóa
- Nhược điểm: Cấu hình phức tạp hơn

### 2. **Railway.app**
- URL: https://railway.app
- Ưu điểm: Dễ dùng, $5 credit miễn phí/tháng
- Nhược điểm: Sau khi hết credit phải trả phí

### 3. **Fly.io**
- URL: https://fly.io
- Ưu điểm: Performance tốt
- Nhược điểm: Cần credit card

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. Logs trên Render Dashboard
2. File `requirements.txt` đúng format
3. Port được set đúng (Render tự động set)

## ✅ Checklist Deploy

- [ ] Code đã test (39 tests pass)
- [ ] Đã tạo GitHub repository
- [ ] Đã push code lên GitHub
- [ ] Đã tạo tài khoản Render.com
- [ ] Đã connect repository
- [ ] Đã deploy thành công
- [ ] Đã test trên URL production

## 🎉 Hoàn thành!

Sau khi deploy, chia sẻ link với mọi người:
`https://YOUR-APP-NAME.onrender.com`
