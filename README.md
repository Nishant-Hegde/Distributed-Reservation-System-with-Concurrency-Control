# Distributed Reservation System with Concurrency Control

A distributed seat reservation system implemented in Python using TCP sockets.  
The system supports multiple concurrent clients, prevents double booking using concurrency control, persists reservation data, and secures communication using SSL/TLS.

---

## Features

- TCP-based client–server architecture
- Custom request–response reservation protocol
- Concurrency control using thread locking
- Prevention of double booking
- Persistent seat storage using JSON
- Logging of server activity
- Stress testing with multiple concurrent clients
- SSL/TLS encrypted communication between client and server

---

## System Architecture

The system consists of three main components:

- **Server**
  - Handles reservation requests
  - Maintains seat database
  - Ensures concurrency control
  - Stores seat data persistently

- **Client**
  - Allows users to reserve seats or check seat status

- **Stress Test Script**
  - Simulates multiple concurrent clients attempting reservations

Communication between client and server is secured using **SSL/TLS encryption**.

---

## Reservation Protocol

### Client → Server Commands

| Command | Description |
|------|------|
| `RESERVE <seat_number>` | Reserve a seat |
| `STATUS` | Get status of all seats |

### Server → Client Responses

| Response | Meaning |
|------|------|
| `SUCCESS` | Reservation successful |
| `FAILED_ALREADY_BOOKED` | Seat already reserved |
| `FAILED_INVALID_SEAT` | Seat number does not exist |
| `INVALID_COMMAND` | Command format incorrect |
| `INVALID_SEAT_NUMBER` | Seat number invalid |

---

## Concurrency Control

To prevent race conditions when multiple clients attempt to reserve seats simultaneously, the server uses a **thread lock**:

```python
lock = threading.Lock()