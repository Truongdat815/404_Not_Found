# SQL Server Setup Guide

## Database Configuration

### Connection String Options

Hệ thống tự động thử kết nối với 2 options:
1. `localhost\SQLEXPRESS` (thường dùng)
2. `localhost` (default instance)

### Environment Variables

Thêm vào file `.env` trong thư mục `backend/`:

```env
DB_USER=sa
DB_PASSWORD=12345
DB_NAME=Hackathon
```

### SQL Server Setup

#### 1. Đảm bảo SQL Server đang chạy:
- Mở SQL Server Configuration Manager
- Kiểm tra SQL Server service đang Running

#### 2. Tạo database:
```sql
CREATE DATABASE Hackathon;
```

#### 3. Enable SQL Server Authentication:
- SQL Server Management Studio → Security → Login → sa
- Right-click → Properties → Set password: 12345
- Status → Enable login

#### 4. Enable SQL Server Authentication mode:
- SQL Server Configuration Manager → SQL Server Properties → Security
- Select "SQL Server and Windows Authentication mode"

### ODBC Driver

Cần cài đặt ODBC Driver:
- **ODBC Driver 17 for SQL Server** (khuyến nghị)
- Hoặc **SQL Server Native Client**

Download từ: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Kiểm tra kết nối

Khi khởi động server, nếu kết nối thành công sẽ thấy:
```
✅ Database connected successfully!
✅ Database tables created/verified
```

Nếu thất bại, kiểm tra:
1. SQL Server đang chạy
2. Database "Hackathon" đã được tạo
3. User "sa" có quyền truy cập
4. ODBC Driver đã được cài đặt

## Database Schema

### Table: analysis_history

```sql
CREATE TABLE analysis_history (
    id INT PRIMARY KEY IDENTITY(1,1),
    text_input NVARCHAR(MAX),
    file_name NVARCHAR(255),
    created_at DATETIME2 DEFAULT GETDATE(),
    conflicts_json NVARCHAR(MAX),  -- JSON format
    ambiguities_json NVARCHAR(MAX),  -- JSON format
    suggestions_json NVARCHAR(MAX),  -- JSON format
    model_used NVARCHAR(50),
    processing_time_seconds INT
);
```

Tables sẽ được tự động tạo khi server khởi động (nếu chưa có).

## API Endpoints

### History Endpoints:
- `GET /api/history` - Lấy lịch sử phân tích
- `GET /api/history/{id}` - Lấy kết quả theo ID
- `DELETE /api/history/{id}` - Xóa kết quả
- `GET /api/history/search?q=...` - Tìm kiếm

### Export Endpoints:
- `GET /api/export/json/{id}` - Export JSON
- `GET /api/export/docx/{id}` - Export DOCX

## Troubleshooting

### Lỗi: "Cannot connect to SQL Server"
- Kiểm tra SQL Server service đang chạy
- Kiểm tra SQL Server Browser service
- Kiểm tra firewall không block port 1433

### Lỗi: "Login failed for user 'sa'"
- Enable SQL Server Authentication
- Reset password cho user sa
- Kiểm tra user có quyền truy cập database

### Lỗi: "ODBC Driver not found"
- Cài đặt ODBC Driver 17 for SQL Server
- Hoặc thử với SQL Server Native Client

---

**Lưu ý:** Mỗi developer có SQL Server riêng trên máy local, không chia sẻ database.

