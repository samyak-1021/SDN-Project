# SDN-Based Firewall using Mininet and POX

## Problem Statement

In this project, we implement a basic firewall using Software Defined Networking (SDN) concepts. The idea is to control network traffic using a controller instead of traditional hardware-based rules. We use Mininet to simulate the network and POX as the SDN controller.

---

## Objective

- To understand how SDN works in a practical setup  
- To create simple firewall rules using a controller  
- To allow and block traffic between hosts based on IP  
- To test the behavior of the network using basic tools  

---

## Topology

We are using a very simple setup:

- 1 Switch → s1  
- 3 Hosts → h1, h2, h3  

All hosts are connected to a single switch.

---

## Setup & Execution

### Step 1: Start the Controller

```bash
cd pox
./pox.py log.level --DEBUG firewall
```

This runs the firewall logic and also shows logs for better understanding.

---

### Step 2: Start Mininet

```bash
sudo mn --controller=remote --switch=ovsk --topo single,3
```

This creates the network and connects it to the controller.

---

## Firewall Logic

The logic is kept simple:

- Traffic from **h1 → h2** is allowed  
- Traffic from **h1 → h3** is blocked  

This is implemented using OpenFlow rules from the controller.

---

## Testing & Results

### Ping Test

- h1 → h2 works normally (packets are received)  
- h1 → h3 fails (packets are dropped)  

This confirms that the firewall rule is working.

---

### iperf Test

- h1 → h2 shows proper bandwidth (connection successful)  
- h1 → h3 fails to connect (blocked by firewall)  

---

### Flow Table Check

Using:

```bash
dpctl dump-flows
```

We can see the drop rule:

```
ip,nw_src=10.0.0.1,nw_dst=10.0.0.3 actions=drop
```

This confirms that the controller installed the rule correctly.

---

## Observations

- The controller receives packets and decides what to do  
- It installs rules dynamically in the switch  
- Blocking is done by simply not assigning any action (drop)  
- The behavior changes instantly based on rules  

---

## Key Concepts Used

- SDN (Software Defined Networking)  
- OpenFlow protocol  
- Controller-based decision making  
- Flow rules (match + action)  
- Packet handling in controller  

---

## Proof of Execution

Screenshots of all steps (ping, iperf, logs, flow table) are included.

---

## Conclusion

This project shows how SDN can be used to implement a simple firewall. Instead of configuring each device manually, we control everything from a central controller. Even with a small setup, it clearly demonstrates how traffic can be allowed or blocked dynamically.

---