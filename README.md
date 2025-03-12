# **Computer Networks Assignment-2 (SEM-2, 2025)**
This repository contains all the code and scripts for **Assignment 2** of the Computer Networks course. The assignment covers **TCP congestion control analysis, SYN flood attack simulation, and evaluating the effect of Nagle’s algorithm on TCP/IP performance**.

---
## **Team Details**
- Team Number 10
- Member 1 - Shubham Agrawal 22110249
- Member 2 - Vraj Shah 22110292
---

## **Assignment Overview**
### **Task 1: TCP Congestion Control Analysis**
- Comparison of **Reno, BIC, and HighSpeed** congestion control algorithms.
- **Mininet-based network topology** simulation.
- Traffic generation and analysis using **iperf3**.

### **Task 2: SYN Flood Attack & Mitigation**
- Simulating a **SYN flood attack** using **hping3**.
- Capturing attack impact with **Wireshark/tcpdump**.
- Implementing **mitigation techniques** .

### **Task 3: Nagle’s Algorithm & Delayed ACK Analysis**
- Custom **TCP server and client** to analyze Nagle’s Algorithm effects.
- Measuring **throughput, packet overhead, and latency** under different configurations.
- Capturing and analyzing traffic using **tcpdump/Wireshark**.

---

## **Prerequisites**
Ensure the following tools are installed before running the scripts:
- **Mininet** (for network topology simulation)
- **iperf3** (for generating TCP traffic)
- **hping3** (for SYN flood attacks)
- **Wireshark/tshark** (for packet capture and analysis)
- **Python 3** (for running TCP client-server scripts)
- **Bash** (for executing attack and logging scripts)

Some scripts require **root privileges**, so use `sudo` where needed.

---

## **File Descriptions & Instructions**
### **Task-1**
- For every part, make sure to capture the network traffic using wireshark on the 's4-eth2' interface for Graphs and Analysis.

#### **Part-a:**
```bash
sudo python3 Part-a.py --cc <congetion_mechanism>
```

#### **Part-b:**
```bash
sudo python3 Part-b.py --cc <congetion_mechanism>
```

#### **Part-c:**
```bash
sudo python3 Part-c.py --cc <congetion_mechanism> --scenario <subpart(1,2a,2b,2c)>
```

#### **Part-d:**
```bash
sudo python3 Part-d.py --cc <congetion_mechanism> --scenario <subpart(1,2a,2b,2c)> --loss <loss in percentage(1%, 5%)>
```


### **Task-2**

#### **Part-A:**
- Set the correct ServerIP and ServerPort in both client_Q2.sh and server_Q2.sh
- Make sure to capture the network traffic using wireshark on the 'wifi' or 'ethernet' interface on the Server Machine(Victim) for Graphs and Analysis.
- Run in the Server Machine(Victim):
```bash
sudo sysctl net.ipv4.tcp_max_syn_backlog=4096
sudo sysctl net.ipv4.tcp_syncookies=0
sudo sysctl net.ipv4.tcp_synack_retries=1
chmod +x server_Q2.sh
sudo ./server_Q2.sh
```
- Run in the Client Machine(Attacker):
```bash
chmod +x client_Q2.sh
sudo ./client_Q2.sh
```
- Finally, process the captured .pcap file in the Server Machine(Victim) using the 'connections_plot.py' to obtain the plot of Connection Duration vs. Connection Start Time

#### **Part-B:**
- Set the correct ServerIP and ServerPort in both client_Q2.sh and server_Q2.sh
- Make sure to capture the network traffic using wireshark on the 'wifi' or 'ethernet' interface on the Server Machine(Victim) for Graphs and Analysis.
- Run in the Server Machine(Victim):
```bash
sudo sysctl net.ipv4.tcp_max_syn_backlog=64
sudo sysctl net.ipv4.tcp_syncookies=1
sudo sysctl net.ipv4.tcp_synack_retries=5
chmod +x server_Q2.sh
sudo ./server_Q2.sh
```
- Run in the Client Machine(Attacker):
```bash
chmod +x client_Q2.sh
sudo ./client_Q2.sh
```
- Finally, process the captured .pcap file in the Server Machine(Victim) using the 'connections_plot.py' to obtain the plot of Connection Duration vs. Connection Start Time

### **Task-3**
- Set the correct ServerIP and ServerPort in both client_Q3.py and server_Q3.py
- Make sure to capture the network traffic using wireshark on the 'wifi' or 'ethernet' interface on the Server Machine(Victim) for Graphs and Analysis.
- Run in the Server Machine (any one of four cases):
```bash
sudo python3 server_Q3.py
```
OR
```bash
sudo python3 server_Q3.py --disable-nagle
```
OR
```bash
sudo python3 server_Q3.py --disable-delayed-ack
```
OR
```bash
sudo python3 server_Q3.py --diable-nagle --disable-delayed-ack
```
- Run in the Client Machine (any one of four cases, corresponding to the Server):
```bash
sudo python3 client_Q3.py
```
OR
```bash
sudo python3 client_Q3.py --disable-nagle
```
OR
```bash
sudo python3 client_Q3.py --disable-delayed-ack
```
OR
```bash
sudo python3 client_Q3.py --diable-nagle --disable-delayed-ack
```
