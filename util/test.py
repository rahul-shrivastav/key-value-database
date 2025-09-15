# test script to benchmark a server using asyncio for metrics.
import asyncio, time
from config import Config

async def worker(id, ops, host=Config.host, port=Config.port):
    reader, writer = await asyncio.open_connection(host, port)
    start = time.perf_counter()
    for i in range(ops):
        writer.write(("$SET"+f"#key"+"#v" +'~' ).encode())
        await writer.drain()
        await reader.readuntil(b"~")
    writer.close()
    await writer.wait_closed()
    return time.perf_counter() - start

async def main():
    num_clients = 1000        
    ops_per_client = 2000
    t0 = time.perf_counter()

    durations = await asyncio.gather(
        *[worker(i, ops_per_client) for i in range(num_clients)]
    )

    total_time = time.perf_counter() - t0
    total_ops  = num_clients * ops_per_client

    print(f"Total Clients: {num_clients}")
    print(f"Total Ops per client: {ops_per_client}")
    print(f"Total ops: {total_ops}")
    print(f"Total time: {total_time:.3f} s")
    print(f"Throughput: {total_ops/total_time:.3f} ops/sec")
    print(f"Avg latency: {sum(durations)/(num_clients*ops_per_client)*1000:.3f} ms/req")

if __name__ == "__main__":
    asyncio.run(main())
