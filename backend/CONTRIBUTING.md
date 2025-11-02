# Contributing Guide

## Git Workflow

### Cấu trúc nhánh:
```
main
├── Frontend
│   ├── phufrontend
│   └── datfrontend
└── Backend
    ├── datbackend
    └── thaobackend
```

### Quy trình làm việc:

1. **Làm việc trên nhánh con:**
   ```bash
   git checkout phufrontend  # hoặc datfrontend, datbackend, thaobackend
   git pull origin phufrontend
   # Làm việc và commit
   git add .
   git commit -m "feat: your feature"
   git push origin phufrontend
   ```

2. **Merge nhánh con vào nhánh cha:**
   - Tạo Pull Request trên GitHub từ `phufrontend` → `Frontend` (hoặc tương tự cho backend)
   - Sau khi merge xong, update local:
   ```bash
   git checkout Frontend
   git pull origin Frontend
   ```

3. **Merge nhánh cha vào main:**
   - Tạo Pull Request trên GitHub từ `Frontend` → `main` (hoặc `Backend` → `main`)
   - Cần approval từ team leader trước khi merge
   - Sau khi merge, update main:
   ```bash
   git checkout main
   git pull origin main
   ```

### Commit Message Convention:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting, no code change
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### Example:
```bash
git commit -m "feat: add file upload component"
git commit -m "fix: resolve conflict detection bug"
git commit -m "docs: update API documentation"
```

