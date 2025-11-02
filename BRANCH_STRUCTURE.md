# Git Branch Structure

## Cấu trúc nhánh đã được tạo:

```
main
├── Frontend
│   ├── phufrontend
│   └── datfrontend
└── Backend
    ├── datbackend
    └── thaobackend
```

## Danh sách nhánh:

### Nhánh chính:
- `main` - Nhánh production chính
- `Frontend` - Nhánh tích hợp frontend
- `Backend` - Nhánh tích hợp backend

### Nhánh con Frontend:
- `phufrontend` - Nhánh làm việc của Phú (Frontend Developer)
- `datfrontend` - Nhánh làm việc của Đạt (Team Leader - Frontend)

### Nhánh con Backend:
- `datbackend` - Nhánh làm việc của Đạt (Team Leader - Backend)
- `thaobackend` - Nhánh làm việc của Thảo (Backend Developer)

## Quy trình làm việc:

1. **Làm việc trên nhánh con:**
   - Mỗi thành viên làm việc trên nhánh riêng của mình
   - Commit và push thường xuyên

2. **Merge vào nhánh cha:**
   - Tạo Pull Request từ nhánh con → nhánh cha (Frontend hoặc Backend)
   - Review code và merge sau khi được approve

3. **Merge vào main:**
   - Tạo Pull Request từ nhánh cha → main
   - Cần approval từ Team Leader trước khi merge

## Lệnh nhanh để checkout:

```bash
# Frontend
git checkout Frontend
git checkout phufrontend
git checkout datfrontend

# Backend
git checkout Backend
git checkout datbackend
git checkout thaobackend

# Main
git checkout main
```

## Trạng thái hiện tại:

✅ Tất cả các nhánh đã được tạo và push lên remote repository
✅ Cấu trúc thư mục backend và frontend đã được setup
✅ File .gitignore đã được cấu hình
✅ README và CONTRIBUTING guide đã được tạo

## Bước tiếp theo:

1. Thiết lập Branch Protection Rules trên GitHub:
   - Settings → Branches → Add rule
   - Bảo vệ nhánh `main`: Require pull request reviews, require approvals
   - Bảo vệ nhánh `Frontend` và `Backend`: Require pull request reviews

2. Mỗi thành viên checkout nhánh của mình và bắt đầu làm việc

3. Tham khảo file `CONTRIBUTING.md` để biết chi tiết về workflow

