package src.workers;

import src.resource_exploiter.ResourcesExploiter;

public class ThreadedWorkerWithoutSync extends Thread {
    private ResourcesExploiter rExp;
    
    // Constructor
    public ThreadedWorkerWithoutSync(ResourcesExploiter resource) {
        this.rExp = resource;
    }
    
    // Override phương thức run() - được thực thi khi thread start()
    @Override
    public void run() {
        for (int i = 0; i < 1000; i++) {
            rExp.exploit();
        }
    }
}
