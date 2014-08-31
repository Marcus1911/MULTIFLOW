::::::::: Marcus Sandri ::::::::::
Universidade Federal de Sao Carlos
         UFSCar - Brazil

This Project is used for demonstrate how Openflow can detect and disjoint a Multipath-TCP's subflow.
- Multiflow is a POX component developed by Marcus Sandri


Basically we look at dissect the MPTCP packet and look at:

Multiflow Algorithm:

TCP arrives on POX Controller
We dissect (MP_CAPABLE and MP_JOIN) 

If CAPABLE:
  We forward all mp_capables (whatever the application source) into the same route.

If JOIN:
  We Look at other avaliable paths. If there's a path, we forwarded the packet and record it receiver-token on the controller.
  For all SYN with same token arriving on controller:
    We Forwarding to avaliable paths;
    If has none avaliable path:
      SYN will be droped


----------------------------------------------------------------------------------

If you have some issue or many of them, please send me an email: marcus.sandri@ufscar.br

 
Run it:

./checkout
./rundemo


