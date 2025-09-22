# Câu Hỏi Phần 1: Interface trong Các Hệ Thống Phân Tán

## Mini Key-Value Store Service (KVSS)

## Câu hỏi 1: Interface trong hệthống phân tán là gì? Tại sao cần phải có Interface khi triển khai các dịch vụ?

### Định nghĩa

Interface (giao diện) trong hệ thống phân tán là tập hợp các quy ước chuẩn (protocol, định dạng thông điệp, cú pháp lệnh, mã trạng thái, phiên bản...) mà cả phía cung cấp dịch vụ (server) và phía sử dụng dịch vụ (client) đều phải tuân thủ để có thể tương tác thống nhất với nhau.

### Vì sao cần Interface

- Tính thống nhất: các hệ thống khác nhau giao tiếp theo cùng một chuẩn, tránh "mạnh ai nấy làm".
- Khả năng tương thích: dễ dàng tích hợp giữa các dịch vụ/nhóm phát triển khác nhau.
- Dễ mở rộng: thêm client/server mới chỉ cần bám theo giao diện đã công bố.
- Bảo trì, gỡ lỗi: lỗi được chuẩn hóa, thông điệp dễ đọc, dễ kiểm thử.
- Tính tách biệt: client không cần biết server viết bằng gì, chỉ cần tuân chuẩn Interface.

## Câu hỏi 2: Hãy giải thích ý nghĩa của mã trạng thái201 CREATED,204 NO_CONTENTvà404 NOT_FOUNDtrong giao thức KVSS

### 201 CREATED

- Ý nghĩa: Tạo mới thành công một khóa (key) trong kho lưu trữ.
- Khi nào trả về: Khi client gửi lệnh `PUT` với một key chưa tồn tại trước đó.
- Ví dụ:

```
C: KV/1.0 PUT user42 Alice
S: 201 CREATED   (key 'user42' được tạo lần đầu)

C: KV/1.0 PUT user42 Bob
S: 200 OK        (key đã tồn tại, đây là cập nhật giá trị)
```

### 204 NO_CONTENT

- Ý nghĩa: Xóa thành công, không có dữ liệu trả về.
- Khi nào trả về: Khi client gửi lệnh `DEL` với key đang tồn tại.
- Ví dụ:

```
C: KV/1.0 DEL user42
S: 204 NO_CONTENT
```

### 404 NOT_FOUND

- Ý nghĩa: Không tìm thấy key trong kho lưu trữ.
- Khi nào trả về: Khi `GET` hoặc `DEL` một key không tồn tại (đảm bảo idempotent).
- Ví dụ:

```
C: KV/1.0 GET nonexistent
S: 404 NOT_FOUND

C: KV/1.0 DEL nonexistent
S: 404 NOT_FOUND   (xóa nhiều lần vẫn 404)
```

## Câu hỏi 3: Trong bài lab KVSS, nếu client không tuân thủ quy ước Interface (ví dụ: thiếu version KV/1.0), server sẽphản hồi thế nào? Tại sao phải quy định rõ ràng tình huống này?

### Phản hồi của server

- Thiếu hẳn tiền tố phiên bản (sai định dạng tổng thể):

```
C: PUT user42 Alice
S: 400 BAD_REQUEST
```

- Sai phiên bản (đúng định dạng nhưng khác version):

```
C: KV/2.0 GET user42
S: 426 UPGRADE_REQUIRED
```

### Lý do cần quy định rõ ràng

- Kiểm soát phiên bản: đảm bảo client/server nói cùng “ngôn ngữ”.
- Tương thích về sau: hỗ trợ tiến hóa giao thức (nâng cấp/loại bỏ phiên bản cũ) có trật tự.
- Giao tiếp lỗi rõ ràng: client biết sai gì để sửa (sai định dạng hay sai phiên bản).
- An toàn và ổn định: từ chối thông điệp không chuẩn tránh lỗi/khai thác.

## Câu hỏi 4: Quan sát một phiên làm việc qua Wireshark: hãy mô tả cách mà gói tin TCP được chia để truyền thông điệp theo "line-based protocol"

### Ví dụ:

```
nc 127.0.0.1 5050
KV/1.0 PUT user42 Alice
KV/1.0 GET user42

```

### Mô tả quá trình truyền:

#### 1. TCP Connection Setup (3-way handshake):

- **SYN**: Client → Server (thiết lập kết nối)
- **SYN-ACK**: Server → Client (xác nhận + thiết lập ngược)
- **ACK**: Client → Server (hoàn thành handshake)

#### 2. Data Transmission (Line-based Protocol):

**Request từ Client:**

```
TCP Payload: "KV/1.0 PUT user42 Alice\n"
```

**Response từ Server:**

```
TCP Payload: "201 CREATED\n"
```

#### 3. Đặc điểm Line-based Protocol:

- **Delimiter**: Sử dụng `\n` làm ký tự phân tách giữa các message
- **Stateless**: Mỗi dòng là một đơn vị độc lập
- **Simple Parsing**: Server chỉ cần đọc đến khi gặp `\n`

#### 4. TCP Segmentation:

- Nếu message nhỏ (< MSS): 1 message = 1 TCP segment
- Nếu message lớn: TCP sẽ chia thành nhiều segments
- Receiver sẽ reassemble các segments theo sequence number

#### 5. Connection Termination:

- **FIN**: Một bên gửi FIN để đóng kết nối
- **ACK**: Bên kia xác nhận
- **FIN**: Bên kia cũng gửi FIN
- **ACK**: Hoàn thành đóng kết nối

## Câu hỏi 5: Client gửi sai giao thức (`KV/1.0 POTT user42 Alice`) – server xử lý thế nào? Thể hiện đặc điểm gì của Interface?

Khi nhận được lệnh sai `KV/1.0 POTT user42 Alice`, server sẽ xử lý như sau:

* **Parse request**: Tách thành `["KV/1.0", "POTT", "user42", "Alice"]`
* **Kiểm tra version**: KV/1.0 --> Hợp lệ
* **Kiểm tra command**: POTT --> Không hợp lệ, không có trong danh sách PUT/GET/DEL/STATS/QUIT. Trả về 400 BAD_REQUEST.

```
C: KV/1.0 POTT user42 Alice
S: 400 BAD_REQUEST
```

### Đặc điểm Interface thể hiện

- Kiểm tra đầu vào nghiêm ngặt (validation) và tuân thủ hợp đồng (contract).
- Xử lý lỗi “êm” (graceful): không sập hệ thống, mã lỗi rõ ràng, hành vi nhất quán.
- Ranh giới giao thức rõ ràng giúp dễ bảo trì, dễ gỡ lỗi, tăng độ tin cậy và an toàn.
