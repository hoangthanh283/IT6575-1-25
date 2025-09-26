package src;

import src.resource_exploiter.ResourcesExploiter;
import src.workers.ThreadedWorkerWithSync;

/**
 * Chương trình Main để trả lời Câu hỏi 1: Có đồng bộ hóa
 */
public class MainQ2 {
    public static void main(String[] args) {
        for (int test = 1; test <= 5; test++) {
            testWithSync(test);
        }
    }

    private static void testWithSync(int testNumber) {
        ResourcesExploiter resource = new ResourcesExploiter(0);
        ThreadedWorkerWithSync worker1 = new ThreadedWorkerWithSync(resource);
        ThreadedWorkerWithSync worker2 = new ThreadedWorkerWithSync(resource);
        ThreadedWorkerWithSync worker3 = new ThreadedWorkerWithSync(resource);

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
