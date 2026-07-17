# Remote Procedure Call (RPC)

The RPC pattern uses messaging to run a function on a remote server and wait
for the result. The client publishes a request with two properties:
`reply_to`, an exclusive callback queue where it expects the answer, and
`correlation_id`, a unique id used to match the response to the request. The
server processes the request and publishes the result back to the `reply_to`
queue with the same `correlation_id`.

```mermaid
sequenceDiagram
    participant C as Client
    participant RQ as rpc queue
    participant S as Server
    participant CQ as callback queue
    C->>RQ: fib(30) [reply_to, correlation_id]
    RQ->>S: fib(30)
    S->>CQ: 832040 [correlation_id]
    CQ->>C: 832040
```

## Usage

Start the server, which computes Fibonacci numbers:

```bash
python server.py
```

Then request a computation from a client:

```bash
python client.py 30
```
