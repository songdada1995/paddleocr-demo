# PaddleOCR Demo

基于 FastAPI 的 PaddleOCR 服务示例

---

## 环境要求
- Python 3.10.11

## 安装依赖
```bash
pip install -r requirements.txt
pip install pymysql
pip install pytz
```

## 初始化数据库
```bash
python pre_start.py
```

## 启动服务
Windows 下：
```bash
set ENV=development
uvicorn main:app --reload
```
Linux/macOS 下：
```bash
export ENV=development
uvicorn main:app --reload
```

---

## 接口文档
- [Swagger UI (推荐)](http://127.0.0.1:8000/docs)
- [ReDoc](http://127.0.0.1:8000/redoc)

---

## 说明
- 启动后访问上述文档页面，可在线调试接口。
- 需先注册/获取 Token，使用 Authorize 按钮进行认证。
