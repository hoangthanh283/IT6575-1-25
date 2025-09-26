package src;

import src.resource_exploiter.ResourcesExploiter;
import src.workers.ThreadedWorkerWithoutSync;

/**
 * Chương trình Main để trả lời Câu hỏi 1: Không có đồng bộ hóa
 * Mô phỏng race condition khi nhiều luồng cùng truy cập tài nguyên chia sẻ
 */
public class MainQ1 {
    public static void main(String[] args) {
        for (int test = 1; test <= 5; test++) {
            testRaceCondition(test);
        }
    }

    private static void testRaceCondition(int testNumber) {
        ResourcesExploiter resource = new ResourcesExploiter(0);

        ThreadedWorkerWithoutSync worker1 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker2 = new ThreadedWorkerWithoutSync(resource);
        ThreadedWorkerWithoutSync worker3 = new ThreadedWorkerWithoutSync(resource);

        worker1.start();
        worker2.start();
        worker3.start();
        try {
            worker1.join();
            worker2.join();
            worker3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        int finalValue = resource.getRsc();
        int lostUpdates = 3000 - finalValue;
        System.out.printf("Test %2d: rsc = %4d (Mong đợi: 3000) | Diff: %4d%n",
                         testNumber, finalValue, lostUpdates);
    }
}