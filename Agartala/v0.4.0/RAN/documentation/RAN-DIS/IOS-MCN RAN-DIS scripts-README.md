# Scripts required for setting up environment for split 7.2 RAN

## setup linuxptp
This script is to setup the linuxptp application in the RAN. PTP is a time synchronization protocol.
```
./setup_linuxptp.sh
```

## setup dhcp_server
DHCP server can be setup in the DU to assign IPs to the RUs connected to them, the server setup requires the interface it is set on to have IP 192.168.4.1 and assigns the clients the IP from 192.168.4.20 to 192.168.4.50.
```
./setup_dhcp_server.sh
```

## setup tuned
Installs the tuned-adm application and starts the tuned.service with realtime profile, configure the .env under scripts folder with the isolated CPUs provided in the GRUB configuration. 
```
./setup_tuned.sh
```

## vf_setup_du
The vf_setup_du.sh script is used to create 2 VFs and bind them with igb_uio driver, this scripts is supported only for Intel E810 XXVDA4T NIC, uses the interface provided in .env environment file.
```
./vf_setup_du.sh
```
To remove the VFs created, the script can be run as following. 
```
./vf_setup_du.sh --remove <interface>
```

>**Note:** Please note that all the above mentioned scripts require root access to be run, can either run them in root mode or using sudo. 