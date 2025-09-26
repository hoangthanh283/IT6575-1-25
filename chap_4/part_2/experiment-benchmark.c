#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <pthread.h>
#include <sys/time.h>

#define INIT_BALANCE 50

int balance = INIT_BALANCE;
int credits = 0;
int debits = 0;

// Global variables for experiment parameters
int num_threads;
int num_trans;

// Coarse locking - 1 mutex cho tất cả
pthread_mutex_t coarse_mutex;

// Fine locking - 3 mutex riêng biệt
pthread_mutex_t b_lock, c_lock, d_lock;

// Coarse locking transaction
void * coarse_transactions(void * args) {
    int thread_id = *(int*)args;
    int i, v;
    
    for(i = 0; i < num_trans; i++) {
        srand(time(NULL) + thread_id + i);
        v = rand() % 100;
        
        pthread_mutex_lock(&coarse_mutex);
        if(rand() % 2) {
            balance = balance + v;
            credits = credits + v;
        } else {
            balance = balance - v;
            debits = debits + v;
        }
        pthread_mutex_unlock(&coarse_mutex);
    }
    return NULL;
}

// Fine locking transaction
void * fine_transactions(void * args) {
    int thread_id = *(int*)args;
    int i, v;
    
    for(i = 0; i < num_trans; i++) {
        srand(time(NULL) + thread_id + i);
        v = rand() % 100;
        
        if(rand() % 2) {
            // Credit
            pthread_mutex_lock(&b_lock);
            balance = balance + v;
            pthread_mutex_unlock(&b_lock);
            
            pthread_mutex_lock(&c_lock);
            credits = credits + v;
            pthread_mutex_unlock(&c_lock);
        } else {
            // Debit
            pthread_mutex_lock(&b_lock);
            balance = balance - v;
            pthread_mutex_unlock(&b_lock);
            
            pthread_mutex_lock(&d_lock);
            debits = debits + v;
            pthread_mutex_unlock(&d_lock);
        }
    }
    return NULL;
}

double get_time_diff(struct timeval start, struct timeval end) {
    return (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_usec - start.tv_usec) / 1000.0;
}

double run_coarse_test(int threads, int transactions) {
    pthread_t *thread_list;
    int *thread_ids;
    struct timeval start, end;
    
    num_threads = threads;
    num_trans = transactions;
    
    // Reset variables
    balance = INIT_BALANCE;
    credits = 0;
    debits = 0;
    
    // Allocate memory
    thread_list = malloc(threads * sizeof(pthread_t));
    thread_ids = malloc(threads * sizeof(int));
    
    // Initialize thread IDs
    for(int i = 0; i < threads; i++) {
        thread_ids[i] = i;
    }
    
    // Initialize mutex
    pthread_mutex_init(&coarse_mutex, NULL);
    
    // Run test
    gettimeofday(&start, NULL);
    
    for(int i = 0; i < threads; i++) {
        pthread_create(&thread_list[i], NULL, coarse_transactions, &thread_ids[i]);
    }
    
    for(int i = 0; i < threads; i++) {
        pthread_join(thread_list[i], NULL);
    }
    
    gettimeofday(&end, NULL);
    
    // Cleanup
    pthread_mutex_destroy(&coarse_mutex);
    free(thread_list);
    free(thread_ids);
    
    return get_time_diff(start, end);
}

double run_fine_test(int threads, int transactions) {
    pthread_t *thread_list;
    int *thread_ids;
    struct timeval start, end;
    
    num_threads = threads;
    num_trans = transactions;
    
    // Reset variables
    balance = INIT_BALANCE;
    credits = 0;
    debits = 0;
    
    // Allocate memory
    thread_list = malloc(threads * sizeof(pthread_t));
    thread_ids = malloc(threads * sizeof(int));
    
    // Initialize thread IDs
    for(int i = 0; i < threads; i++) {
        thread_ids[i] = i;
    }
    
    // Initialize mutexes
    pthread_mutex_init(&b_lock, NULL);
    pthread_mutex_init(&c_lock, NULL);
    pthread_mutex_init(&d_lock, NULL);
    
    // Run test
    gettimeofday(&start, NULL);
    
    for(int i = 0; i < threads; i++) {
        pthread_create(&thread_list[i], NULL, fine_transactions, &thread_ids[i]);
    }
    
    for(int i = 0; i < threads; i++) {
        pthread_join(thread_list[i], NULL);
    }
    
    gettimeofday(&end, NULL);
    
    // Cleanup
    pthread_mutex_destroy(&b_lock);
    pthread_mutex_destroy(&c_lock);
    pthread_mutex_destroy(&d_lock);
    free(thread_list);
    free(thread_ids);
    
    return get_time_diff(start, end);
}

int main() {
    // Experiment parameters
    int thread_counts[] = {2, 4, 8, 16, 2, 4, 8, 16};
    int transaction_counts[] = {1000, 1000, 1000, 1000, 10000, 10000, 10000, 10000};
    int num_experiments = 8;
    
    printf("=== THÍ NGHIỆM SO SÁNH COARSE vs FINE LOCKING ===\n\n");
    printf("%-8s %-12s %-15s %-15s %-10s\n", 
           "Threads", "Transactions", "Coarse (ms)", "Fine (ms)", "Speedup");
    printf("%-8s %-12s %-15s %-15s %-10s\n", 
           "-------", "------------", "-----------", "---------", "-------");
    
    for(int i = 0; i < num_experiments; i++) {
        int threads = thread_counts[i];
        int transactions = transaction_counts[i];
        
        printf("%-8d %-12d ", threads, transactions);
        fflush(stdout);
        
        // Run coarse locking test
        double coarse_time = run_coarse_test(threads, transactions);
        printf("%-15.2f ", coarse_time);
        fflush(stdout);
        
        // Run fine locking test  
        double fine_time = run_fine_test(threads, transactions);
        printf("%-15.2f ", fine_time);
        
        // Calculate metrics
        double speedup = coarse_time / fine_time;
        printf("%-10.2f ", speedup);
        printf("\n");
    }    
    return 0;
}
