# 🗄️ Mini Key-Value Store Service (KVSS)
**Bài thực hành Interface trong Hệ thống Phân tán - IT6575**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://python.org)
[![Protocol](https://img.shields.io/badge/Protocol-TCP-green.svg)](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](#)

## 📖 Tổng quan

Dự án này thực hiện một **Key-Value Store Service** đơn giản tuân thủ nghiêm ngặt **Interface Specification KV/1.0**. Đây là bài thực hành nhằm hiểu rõ về:

- 🔌 **Interface Design** trong hệ thống phân tán
- 🌐 **Line-based Protocol** over TCP
- 🔄 **Client-Server Architecture**
- 🧪 **Protocol Testing & Validation**
- 📊 **Network Traffic Analysis**

### ✨ Tính năng chính

- **TCP Server đa luồng** - Hỗ trợ nhiều client đồng thời
- **In-memory Storage** - Lưu trữ key-value trong RAM
- **Comprehensive Logging** - Ghi log chi tiết với timestamp
- **Robust Error Handling** - Xử lý lỗi đầy đủ theo specification
- **Interactive & Batch Client** - Hỗ trợ chế độ tương tác và batch
- **Automated Testing Suite** - 10 test cases tự động (100% pass)
- **Manual Testing Tools** - Hướng dẫn test với nc/telnet/Wireshark

## 📁 Cấu trúc project

```
kvss/
├── server/
│   └── kvss_server.py              # KVSS Server (TCP multi-threaded)
├── client/
│   └── kvss_client.py              # KVSS Client (interactive & batch)
├── tests/
│   └── test_kvss.py                # Automated test suite (10 test cases)
├── LAB_QUESTIONS_ANSWERS.md        # Trả lời 5 câu hỏi Interface
├── run_demo.sh                     # Script demo tự động
├── cleanup_ports.sh                # Dọn dẹp tiến trình/port 5050
└── README.md                       # Tài liệu này
```

> Lưu ý: Các tài liệu PDF của môn học nằm ở thư mục gốc dự án `Chuong1/`.

### 📊 Thống kê dự án

| Thành phần | Số dòng code (LOC) | Tính năng |
|------------|---------------------|-----------|
| `server/kvss_server.py` | 213 | TCP Server, Protocol Parser, Storage, Logging |
| `client/kvss_client.py` | 207 | Interactive Client, Batch Mode, CLI |
| `tests/test_kvss.py` | 216 | Automated Testing, 10 Test Cases |
| **Tổng cộng** | **636** | **Complete KVSS Implementation** |

## 🔌 Interface Specification KV/1.0

### 🌐 Connection Parameters
| Tham số | Giá trị | Mô tả |
|---------|---------|-------|
| **Protocol** | TCP | Transmission Control Protocol |
| **Host** | `127.0.0.1` | Localhost (loopback interface) |
| **Port** | `5050` | Cổng dịch vụ KVSS mặc định |
| **Encoding** | `UTF-8` | Mã hóa ký tự |
| **Format** | Line-based | Mỗi thông điệp kết thúc bằng `\n` |

### 📝 Command Syntax (EBNF)
```ebnf
request     ::= version " " command [ " " args ] "\n"
version     ::= "KV/1.0"
command     ::= "PUT" | "GET" | "DEL" | "STATS" | "QUIT"
args        ::= key [ " " value ]
key         ::= word
value       ::= text
word        ::= [a-zA-Z0-9_]+
text        ::= .+
```

### 🎯 Commands Overview

| Command | Cú pháp | Mục đích | Phản hồi |
|---------|--------|---------|----------|
| `PUT` | `KV/1.0 PUT <key> <value>` | Lưu/Cập nhật key-value | `201 CREATED` / `200 OK` |
| `GET` | `KV/1.0 GET <key>` | Lấy giá trị theo key | `200 OK <value>` / `404 NOT_FOUND` |
| `DEL` | `KV/1.0 DEL <key>` | Xóa key-value | `204 NO_CONTENT` / `404 NOT_FOUND` |
| `STATS` | `KV/1.0 STATS` | Lấy thống kê server | `200 OK keys=N uptime=Ns served=N` |
| `QUIT` | `KV/1.0 QUIT` | Đóng kết nối | `200 OK bye` |

### 📊 HTTP-style Status Codes

| Code | Status | Ý nghĩa | Khi nào |
|------|--------|---------|---------|
| `200` | `OK [data]` | Thành công (có thể kèm dữ liệu) | GET, STATS, QUIT |
| `201` | `CREATED` | Tạo mới tài nguyên | PUT key mới |
| `204` | `NO_CONTENT` | Thành công, không có nội dung | DEL thành công |
| `400` | `BAD_REQUEST` | ❌ Cú pháp/command không hợp lệ | Request lỗi định dạng |
| `404` | `NOT_FOUND` | ❌ Không tồn tại key | GET/DEL key không tồn tại |
| `426` | `UPGRADE_REQUIRED` | ❌ Thiếu/sai phiên bản | Không có tiền tố `KV/1.0` |
| `500` | `SERVER_ERROR` | ❌ Lỗi nội bộ server | Lỗi bất ngờ |

## 🚀 Quick Start Guide

### 📋 Chuẩn bị
```bash
python3 --version          # Python 3.6+

# (Khuyến nghị) Tạo virtual environment
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
# venv\Scripts\activate   # Windows

# Công cụ test thủ công (tùy chọn)
nc -h       # netcat
which telnet || true
which wireshark || true
```

### 1️⃣ Khởi động KVSS Server
```bash
cd server
python3 kvss_server.py
# 2025-.. INFO - KVSS Server started on 127.0.0.1:5050
```

### 2️⃣ Dùng KVSS Client

#### 🎮 Chế độ tương tác
```bash
cd ../client
python3 kvss_client.py
# gõ lệnh:  PUT key value | GET key | DEL key | STATS | QUIT
```

#### 🤖 Chế độ batch (qua stdin)
```bash
echo -e "PUT user42 Alice\nGET user42\nSTATS\nQUIT" | python3 kvss_client.py
```

#### ⚙️ Host/Port tùy chỉnh
```bash
python3 kvss_client.py 127.0.0.1 5050
```

### 3️⃣ Manual Testing với netcat
```bash
# Terminal 1
cd server && python3 kvss_server.py

# Terminal 2
nc 127.0.0.1 5050
KV/1.0 PUT user42 Alice
KV/1.0 GET user42
KV/1.0 STATS
KV/1.0 DEL user42
KV/1.0 GET user42
KV/1.0 QUIT
```

### 4️⃣ Automated Testing Suite
```bash
cd tests
python3 test_kvss.py
# Kết quả mong đợi: 10/10 tests passed
```

## 💡 Protocol Examples
```bash
# Create
KV/1.0 PUT user42 Alice      # → 201 CREATED
# Read
KV/1.0 GET user42            # → 200 OK Alice
# Update
KV/1.0 PUT user42 Bob        # → 200 OK
# Stats
KV/1.0 STATS                 # → 200 OK keys=.. uptime=..s served=..
# Delete
KV/1.0 DEL user42            # → 204 NO_CONTENT
# Not found
KV/1.0 GET user42            # → 404 NOT_FOUND
# Close
KV/1.0 QUIT                  # → 200 OK bye
```

## 🔍 Phân tích mạng với Wireshark (tùy chọn)
- Bắt gói trên loopback `lo/lo0`, filter: `tcp.port == 5050`.
- Dễ quan sát vì là giao thức văn bản, phân cách bởi `\n`.
- Dùng Follow TCP Stream để xem toàn bộ phiên.

## 📚 Câu hỏi & Trả lời
Xem `LAB_QUESTIONS_ANSWERS.md` để đọc trả lời chi tiết cho 5 câu hỏi về Interface.

## ⚠️ Lưu ý & Troubleshooting
- Port 5050 bận? Chạy `./cleanup_ports.sh` hoặc kiểm tra `lsof -i :5050`.
- Log server nằm ở `kvss_server.log`.
- Server lưu dữ liệu trong RAM (không persistent).

## 👤 Tác giả
Bài thực hành Interface trong Hệ thống Phân tán - IT6575
