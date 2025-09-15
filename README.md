# In-Memory Key-Value Database

A lightweight Redis-like in-memory key-value database built in Python with a **custom text-based wire protocol** and **asynchronous I/O multiplexing** using `asyncio`. Supports multiple concurrent clients and core commands like `SET`, `GET`, `PING`, and `DEL`.

---

## Features

- **Custom TCP protocol** with `$`/`#`/`~` delimiters for command encoding.
- **Asynchronous server** using Python `asyncio` for efficient I/O multiplexing.
- **Data structures**: fast O(1) key-value storage with support for lists, sets, and hashes.
- **Optional TTL support** for automatic key expiration.
- **High performance**: tested with thousands of concurrent clients.

---

## Supported Commands

| Command | Description |
|---------|-------------|
| SET     | Set a key with an optional TTL |
| GET     | Get the value of a key |
| PING    | Test connectivity with the server |
| DEL     | Delete a key from the database |

---

## Usage

### Start the Server

```bash
python server.py
```
### Start the Client

```bash
python client.py
```

## Benchmarks

| Metric                 | Value                     |
|------------------------|---------------------------|
| Total Clients          | 1,000                     |
| Total Ops per Client   | 2,000                     |
| Total Ops              | 2,000,000                 |
| Total Time             | 85.815 s                  |
| Throughput             | 23,305.87 ops/sec         |
| Avg Latency            | 42.734 ms/req             |
