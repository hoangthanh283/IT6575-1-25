package src;

import src.resource_exploiter.ResourcesExploiterWithLock;
import src.workers.ThreadedWorkerWithLock;

/**
 * Chương trình Main để trả lời Câu hỏi 3: Với ReentrantLock
 * So sánh với câu hỏi 1 để thấy sự khác biệt
 */
public class MainQ3 {
    public static void main(String[] args) {
        for (int test = 1; test <= 5; test++) {
            testWithLock(test);
        }
    }

    private static void testWithLock(int testNumber) {
        // Sử dụng ResourcesExploiterWithLock thay vì ResourcesExploiter
        ResourcesExploiterWithLock resource = new ResourcesExploiterWithLock(0);

        // Sử dụng ThreadedWorkerWithLock
        ThreadedWorkerWithLock worker1 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker2 = new ThreadedWorkerWithLock(resource);
        ThreadedWorkerWithLock worker3 = new ThreadedWorkerWithLock(resource);

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
        int diff = 3000 - finalValue;
        System.out.printf("Test %2d: rsc = %4d (Mong đợi: 3000) | Diff: %4d%n",
                         testNumber, finalValue, diff);
    }
}
