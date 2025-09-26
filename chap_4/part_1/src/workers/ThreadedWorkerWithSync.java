package src.workers;

import src.resource_exploiter.ResourcesExploiter;

public class ThreadedWorkerWithSync extends Thread {
    private ResourcesExploiter rExp;

    // Constructor
    public ThreadedWorkerWithSync(ResourcesExploiter resource) {
        this.rExp = resource;
    }
    
    // Override phương thức run() với synchronized block
    @Override
    public void run() {
        synchronized(rExp) {
            for (int i = 0; i < 1000; i++) {
                rExp.exploit();
            }
        }
    }
}