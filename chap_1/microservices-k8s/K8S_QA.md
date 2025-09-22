# Câu hỏi và Đáp án Kubernetes Microservices Lab

## Câu hỏi 6: Sau khi chạy `kubectl apply -f users-deploy.yaml`, dùng lệnh nào để kiểm tra Pod của service users đã chạy thành công? Hãy chụp màn hình kết quả.

### Đáp án:

**Lệnh kiểm tra Pod của service users:**

```bash
kubectl get pods -n micro-lab
```

**Hoặc để xem chi tiết hơn:**

```bash
kubectl get pods -n micro-lab -l app=users
```

**Hoặc để xem trạng thái chi tiết:**

```bash
kubectl describe pods -n micro-lab -l app=users
```

### Kết quả màn hình:

**Kiểm tra trạng thái tất cả pods:**
![Kubectl get pods](images/Screenshot%202025-09-22%20at%2017.37.19.png)

**Kiểm tra services:**
![Kubectl get services](images/Screenshot%202025-09-22%20at%2017.39.19.png)

**Kiểm tra chi tiết deployment:**
![Kubectl deployment details](images/Screenshot%202025-09-22%20at%2017.39.28.png)

## Câu hỏi 7: Trong file `users-deploy.yaml`, hãy chỉ ra:

- Deployment quản lý bao nhiêu replica ban đầu?
- Service thuộc loại nào (ClusterIP, NodePort, LoadBalancer)?

Dựa trên nội dung file `users-deploy.yaml` quản lý 1 replica ban đầu và Service thuộc loại ClusterIP

```yaml
apiVersion: v1
kind: Service
metadata:
  name: users-svc
spec:
  selector:
    app: users
  ports:
  - port: 80
    targetPort: 80
```

```
NAME          TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
catalog-svc   ClusterIP   10.109.149.108   <none>        80/TCP    17m
orders-svc    ClusterIP   10.106.7.77      <none>        80/TCP    16m
users-svc     ClusterIP   10.109.7.158     <none>        80/TCP    17m
```

---

## Câu hỏi 8: Sau khi cài Ingress, em cần thêm dòng nào vào file `/etc/hosts` để truy cập bằng tên miền `micro.local`?

**Dòng cần thêm vào `/etc/hosts`:**

```
172.17.0.2 micro.local
```
