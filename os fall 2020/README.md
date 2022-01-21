1. This repo contains the code of First Come First Serve, Shortest Job First and Round Robin job schedulers for CSCI-UA-202 Operating Systems

2. The input is fixed to be named “input.txt”, if one wants to change the name of the input file, one needs to change the code at line 281 from “input.txt” to “yourfilename.txt”

4. Each process is input as follow - Job Number, CPU time, I/O time, Entering time
```
for(int i=0;i<n;i++) {
        scanf("%d%d%d%d",&p[i][0],&p[i][1],&p[i][2],&p[i][3]);
}
```
3. The program assumes that all processes have a non-zero CPU time and a non-zero I/O time.
