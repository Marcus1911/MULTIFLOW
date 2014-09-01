

**Marcus Sandri** 
> Universidade Federal de Sao Carlos
    UFSCar - Brazil

* *This Project is used for demonstrate how Openflow can detect and disjoint a Multipath-TCP's subflow.*
* *Multiflow is a POX component developed by Marcus Sandri*
* *The main idea it's look inside the MPTCP packet and split it into avaliable paths.*

**Basic explanation about Multiflow algorithm:**

```
TCP arrives on POX Controller
We dissect(MP_CAPABLE and MP_JOIN) 

IF mp_capable:
  We forward all mp_capables (whatever the application source) into the same route.

IF mp_join:
  We search avaliable paths. 
  IF there's a path:
    We forwarding the packet and record it receiver-token on the controller;
    For all [SYN] with same receiver-token arriving on controller:
      We Forwarding to those avaliable paths;
      IF has no more avaliable path:     \\ Which means: "the sum of all forwarded subflows plus this subflow is bigger than paths avaliable"
        [SYN] will be droped
```

----------------------------------------------------------------------------------

- [x] If you have some issue, please send me an email:  **marcus.sandri@ufscar.br**

 
 
**Run before all:**

- **./checkout**
- **./rundemo**


