# Distributed Reservation System with Concurrency Control

## Overview
This project implements a distributed reservation system using low-level TCP
socket programming in Python. Multiple clients can concurrently request
reservations for shared resources, and the server ensures consistency using
proper concurrency control mechanisms.

The primary goal of the system is to prevent race conditions such as double
booking when multiple clients attempt to reserve the same resource
simultaneously.

---

## Current Status
- TCP-based client–server communication
- Support for multiple concurrent clients (thread-per-client model)
- Shared in-memory reservation store
- Concurrency control using mutex locks
- SSL/TLS security: not implemented yet

---

## Architecture
- Centralized server managing reservation state
- Multiple clients connect over TCP sockets
- Each client handled by a separate thread
- Critical sections protected using locks

Client 1  \
Client 2   --->  Reservation Server  --->  Shared Seat Store  
Client N  /

---

## Reservation Model
- Fixed set of seats (1–5)
- Seat states: FREE or BOOKED
- Server atomically checks and updates seat status

---

## Communication Protocol

Client → Server  
RESERVE <seat_number>

Server → Client  
SUCCESS  
FAILED_ALREADY_BOOKED  
FAILED_INVALID_SEAT  
INVALID_COMMAND

---

## Concurrency Control
- Thread-per-client server model
- Shared dictionary for reservation state
- Mutex lock ensures mutual exclusion

---

## Technology Stack
- Python 3
- TCP sockets (`socket`)
- Multithreading (`threading`)
- Synchronization (`threading.Lock`)
- SSL/TLS (planned)

---

## How to Run

Server:
python server.py

Client:
python client.py

Run multiple clients in different terminals to test concurrency.

---

## Project Structure
Distributed-Reservation-System-with-Concurrency-Control/
- server.py
- client.py
- README.md
- .gitignore

---

## Planned Enhancements
- SSL/TLS secure communication
- STATUS and CANCEL commands
- Performance evaluation

---

## Collaboration Guidelines
- Commit only working code
- Do not force-push to main
- Discuss major changes before implementation

---

## Authors
Distributed Systems Project – Team Repository
