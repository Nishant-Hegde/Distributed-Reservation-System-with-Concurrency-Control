# Secure Distributed Seat Reservation System

A distributed seat reservation system implemented in Python using **TCP socket programming**. The system supports **multiple concurrent clients**, prevents **double booking using concurrency control**, stores reservation data persistently, and secures communication using **SSL/TLS encryption**.

---

## Features

- TCP-based client–server architecture  
- Custom reservation request–response protocol  
- Multi-client support using threading  
- Concurrency control using thread locking  
- Prevention of double booking  
- Persistent seat storage using JSON  
- Server request logging  
- Stress testing using concurrent client threads  
- SSL/TLS encrypted communication  

---

## System Architecture

The system follows a **multi-client client–server architecture**.

```
           Client 1
              |
           Client 2
              |
           Client 3
              |
       -------------------
       |     SERVER      |
       | Seat Manager    |
       | Thread Handler  |
       -------------------
               |
            seats.json
```

### Components

**Server**
- Accepts multiple client connections
- Handles reservation requests
- Maintains seat database
- Ensures concurrency control
- Logs activity

**Client**
- Allows users to reserve seats
- Allows users to check seat availability

**Stress Test Script**
- Simulates multiple concurrent clients attempting seat reservations

**Seat Storage**
- Reservation data is stored in a JSON file (`seats.json`) so that bookings persist across server restarts.

---

## Reservation Protocol

### Client → Server Commands

| Command | Description |
|--------|-------------|
| `RESERVE <seat_number>` | Reserve a seat |
| `STATUS` | Get status of all seats |

Example:

```
RESERVE 3
```

---

### Server → Client Responses

| Response | Meaning |
|----------|---------|
| `SUCCESS` | Reservation successful |
| `FAILED_ALREADY_BOOKED` | Seat already reserved |
| `FAILED_INVALID_SEAT` | Seat number does not exist |
| `INVALID_COMMAND` | Command format incorrect |
| `INVALID_SEAT_NUMBER` | Seat number invalid |

Example response:

```
SUCCESS
```

---

## Concurrency Control

To prevent **race conditions** when multiple clients try to reserve the same seat simultaneously, the server uses a **thread lock**.

```python
lock = threading.Lock()
```

Critical section for seat reservation:

```python
with lock:
    if seat_id not in seats:
        response = "FAILED_INVALID_SEAT"
    elif seats[seat_id]:
        response = "FAILED_ALREADY_BOOKED"
    else:
        seats[seat_id] = True
        save_seats(seats)
        response = "SUCCESS"
```

This ensures that **only one thread modifies the seat data at a time**, preventing double booking.

---

## Persistent Storage

Seat reservation data is stored in:

```
seats.json
```

Example file content:

```
{
 "1": false,
 "2": true,
 "3": false,
 "4": false,
 "5": true
}
```

Where:
- `true` = seat booked  
- `false` = seat available  

---

## Logging

Server activity is logged in:

```
server.log
```

Example log entry:

```
2026-03-12 21:10:23 - ('127.0.0.1', 54321) -> RESERVE 3
2026-03-12 21:10:23 - ('127.0.0.1', 54321) <- SUCCESS
```

This helps track requests and debug system behavior.

---

## SSL/TLS Security

The system secures communication between the client and server using **SSL/TLS encryption**.

Server configuration:

```python
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
```

Client configuration:

```python
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
```

The socket connection is wrapped using:

```python
secure_socket = context.wrap_socket(socket)
```

This ensures all communication between the client and server is **encrypted**.

---

## Project Structure

```
Distributed-Reservation-System/
│
├── server.py
├── client.py
├── stress_test.py
├── seats.json
├── server.log
├── cert.pem
├── key.pem
└── README.md
```

---

## Running the Project

### 1. Generate SSL Certificates

Run the following command to generate a self-signed certificate:

```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

### 2. Start the Server

```
python server.py
```

Output:

```
Secure reservation server running on port 12000
```

---

### 3. Run the Client

```
python client.py
```

Example interaction:

```
------ Reservation Client ------
1. Reserve Seat
2. Check Seat Status
Enter choice: 1
Enter seat number (1-5): 3

Server response: SUCCESS
```

---

### 4. Run Stress Test (Optional)

```
python stress_test.py
```

Example output:

```
Seat 3 -> SUCCESS
Seat 2 -> SUCCESS
Seat 3 -> FAILED_ALREADY_BOOKED
Seat 1 -> SUCCESS
```

This demonstrates **multiple concurrent clients interacting with the server simultaneously**.

---

## Key Concepts Demonstrated

- Socket Programming  
- Client–Server Architecture  
- Multithreading  
- Concurrency Control  
- Persistent Data Storage  
- SSL/TLS Secure Communication  

---

## Conclusion

This project demonstrates how to build a **secure distributed reservation system** using low-level socket programming in Python. It supports **multiple concurrent clients**, prevents **double booking using concurrency control**, and ensures **secure communication through SSL/TLS encryption**.