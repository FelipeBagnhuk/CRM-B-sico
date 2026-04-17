import asyncio
import time

async def make_order_async(id_order):
    print(f"[Async] Começando pedido {id_order}...")
    await asyncio.sleep(2)
    print(f"[Async] Pedido {id_order} pronto!")

async def execute_async():
    print("--- INICIANDO MODO ASSINCRONO ---")
    start = time.time()

    await asyncio.gather(
        make_order_async(1),
        make_order_async(2),
        make_order_async(3)
    )

    end = time.time()
    print(f"--- TEMPO TOTAL ASYNC: {end - start:.2f} segundos ---")

asyncio.run(execute_async())