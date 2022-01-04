#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#define MAXP 100 //max number of processes
#define MAXA 10   //max number of arguments
#define INT_MAX 10000 //max cpu time
int p[MAXP][MAXA]; //process[1][3] represents the arrival time of process 3

typedef struct p {
    int id;
    struct p *next;
}node;

typedef struct q {
    node *first;
    node *rear;
}queue;

queue *insert(queue *head, int x) {
    node *s = NULL;
    
    s = (node*)malloc(sizeof(node));
    s->id = x;
    s->next = NULL;
    
    if(head->rear == NULL) {
        head->first = s;
        head->rear = s;
    }
    else {
        head->rear->next = s;
        head->rear = s;
    }
    return head;
}

void del(queue *head) {
    node *p = NULL;
    p = head->first;
    
    if(head->first != NULL) {
        if(head->first == head->rear) {
            head->first = NULL;
            head->rear = NULL;
        }
        else {
            head->first = head->first->next;
            free(p);
            p = NULL;
        }
    }
}

void printque(queue *head){
    node *temp = head->first;
    while(temp != NULL)
    {
        printf("%d",temp->id);
        temp = temp->next;
    }
}
int isfinished(int n,int process[][10]) {
    for(int i=0;i<n;i++) {
        if(process[i][1] > 0)
            return 1;
    }
    return 0;
}
void FCFS(int n) { //first come first serve
    FILE *fp;
    fp = freopen("input-0.txt","w",stdout);
    int time = 0, worktime = 0;
    int process[n+1][10];
    for(int i=0;i<n;i++) {
        for(int j=0;j<=7;j++)
            process[i][j] = p[i][j];
    }
    queue *head = (queue*)malloc(sizeof(queue));
    head->first = NULL;
    head->rear = NULL;
    while(isfinished(n,process)) {
        printf("%d ",time);
        for(int i=0;i<n;i++) {
            if(process[i][3] == time) {
                insert(head, process[i][0]);
                process[i][4] = 1; //0 = not arrived, 1 = rdy, 2 = running, 3 = blocked 4 = finished
            }
        }
        if(head->first != NULL) {
            int now = head->first->id;
            if(process[now][4] == 1)
                process[now][4] = 2;
        }
        int flag = 0;
        for(int i=0;i<n;i++) {
            if(process[i][4] == 1) {
                printf("%d:ready ",process[i][0]);
            }
            else if(process[i][4] == 2) {
                printf("%d:running ",process[i][0]);
                   process[i][1]--;
                if(process[i][1] == process[i][5]/2)
                {
                    del(head);
                    process[i][4] = 3;
                }
                else if(process[i][1] == 0) {
                    del(head);
                    process[i][6] = time;
                    process[i][4] = 4;
                }
                flag = 1;
            }
            else if(process[i][4] == 3) {
                printf("%d:blocked ",process[i][0]);
                process[i][2]--;
                if(process[i][2] == 0) {
                    process[i][4] = 1;
                    insert(head,process[i][0]);
                }
            }
        }
        printf("\n");
        time++;
        if(flag == 1)
            worktime++;
    }
    
    printf("\n");
    printf("Finishing time: %d\n",time-1);
    printf("CPU utilization: %.2f\n", (float)worktime/(float)time);
    for(int i=0;i<n;i++)
        printf("Turnaround process %d:%d\n",process[i][0],process[i][6] - process[i][3] + 1);
    fclose(fp);
}
void RR(int n) {
    FILE *fp;
    fp = freopen("input-1.txt","w",stdout);
    int process[n+1][10];
    for(int i=0;i<n;i++) {
        for(int j=0;j<=7;j++)
            process[i][j] = p[i][j];
    }
    int time = 0, worktime = 0;
    queue *head = (queue*)malloc(sizeof(queue));
    head->first = NULL;
    head->rear = NULL;
    while(isfinished(n,process)) {
        printf("%d ",time);
        for(int i=0;i<n;i++) {
            if(process[i][3] == time) {
                insert(head, process[i][0]);
                process[i][4] = 1; //0 = not arrived, 1 = rdy, 2 = running, 3 = blocked 4 = finished
            }
        }
        if(head->first != NULL) {
            int now = head->first->id;
            if(process[now][4] == 1)
                process[now][4] = 2;
        }
        int flag = 0;
        for(int i=0;i<n;i++) {
            if(process[i][4] == 1) {
                printf("%d:ready ",process[i][0]);
            }
            else if(process[i][4] == 2) {
                printf("%d:running ",process[i][0]);
                process[i][1]--;
                process[i][7]++;
                if(process[i][1] == 0) {
                    del(head);
                    process[i][6] = time;
                    process[i][4] = 4;
                }
                else if(process[i][1] == process[i][5]/2)
                {
                    del(head);
                    process[i][4] = 3;
                }
                else if(process[i][7] == 2) {
                    del(head);
                    process[i][4] = 1;
                    process[i][7] = 0;
                    insert(head,process[i][0]);
                }
                flag = 1;
            }
            else if(process[i][4] == 3) {
                printf("%d:blocked ",process[i][0]);
                process[i][2]--;
                if(process[i][2] == 0) {
                    process[i][4] = 1;
                    insert(head,process[i][0]);
                }
            }
        }
        printf("\n");
        time++;
        if(flag == 1)
            worktime++;
    }
    
    printf("\n");
    printf("Finishing time: %d\n",time-1);
    printf("CPU utilization: %.2f\n", (float)worktime/(float)time);
    for(int i=0;i<n;i++)
        printf("Turnaround process %d:%d\n",process[i][0],process[i][6] - process[i][3] + 1);
    fclose(fp);
}
void SJF(int n) {
    FILE *fp;
    fp = freopen("input-2.txt","w",stdout);
    int process[n+1][10];
    for(int i=0;i<n;i++) {
        for(int j=0;j<=7;j++)
            process[i][j] = p[i][j];
    }
    int time = 0, worktime = 0;
    queue *head = (queue*)malloc(sizeof(queue));
    head->first = NULL;
    head->rear = NULL;
    while(isfinished(n,process)) {
        printf("%d ",time);
        int flag = 0;
        int min = INT_MAX;
        int now = MAXP+1;
        for(int i=0;i<n;i++) {
            if(process[i][3] <= time) {
                process[i][4] = 0;
                if(process[i][1] == process[i][5]/2 && process[i][2] > 0) {
                    process[i][4] = 3;
                    process[i][2]--;
                }
                else if(process[i][1] < min && process[i][1] > 0) {
                    min = process[i][1];
                    now = process[i][0];
                }
            }
        }
        //printf("min = %d and now = %d",min,now);
        
        min = INT_MAX;
        for(int i=0;i<n;i++) {
            if(process[i][3] <= time) {
                if(process[i][0] == now) {
                    process[i][4] = 2;
                    process[i][1]--;
                    if(process[i][1] == 0) {
                        process[i][6] = time;
                    }
                    flag = 1;
                    worktime++;
                }
                else if(process[i][1] == 0) {
                    process[i][4] = 4;
                }
                else if(process[i][4] == 0)
                    process[i][4] = 1;
            }
        }
        for(int i=0;i<n;i++) {
            if(process[i][4] == 1)
                printf("%d:ready ",process[i][0]);
            else if(process[i][4] == 2)
                printf("%d:running ",process[i][0]);
            else if(process[i][4] == 3)
                printf("%d:blocked ",process[i][0]);
        }
        time++;
        printf("\n");
    }
    printf("\n");
       printf("Finishing time: %d\n",time-1);
       printf("CPU utilization: %.2f\n", (float)worktime/(float)time);
       for(int i=0;i<n;i++)
           printf("Turnaround process %d:%d\n",process[i][0],process[i][6] - process[i][3] + 1);
    fclose(fp);
}
int main(int argc, const char * argv[]) {
    FILE *fp;
    fp = freopen("input.txt","r",stdin);
    int n;
    scanf("%d",&n);
    for(int i=0;i<n;i++) {
        scanf("%d%d%d%d",&p[i][0],&p[i][1],&p[i][2],&p[i][3]);
        p[i][5] = p[i][1];
        p[i][7] = 0;
    }
    fclose(fp);
    FCFS(n);
    RR(n);
    SJF(n);
    
    return 0;
}
