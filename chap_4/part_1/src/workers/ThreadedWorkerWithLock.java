package src.workers;

import src.resource_exploiter.ResourcesExploiterWithLock;

/**
 * Lớp ThreadedWorkerWithLock - worker sử dụng ReentrantLock
 * Kế thừa từ lớp Thread, tương tự ThreadedWorkerWithoutSync 
 * nhưng sử dụng ResourcesExploiterWithLock
 */
public class ThreadedWorkerWithLock extends Thread {
    private ResourcesExploiterWithLock rExp;
    
    // Constructor
    public ThreadedWorkerWithLock(ResourcesExploiterWithLock resource) {
        this.rExp = resource;
    }
    
    // Override phương thức run()
    @Override
    public void run() {
        // Giống ThreadedWorkerWithoutSync, nhưng lock được xử lý trong exploit()
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}
