import time

def make_order_sinc(id_order):
    print(f"[Sync] Começando Pedido {id_order}")
    time.sleep(2)
    print(f"[Sync] Pedido {id_order} pronto!")

def execute_sinc():
    print("--- INICIANDO MODO SÍNCRONO---")
    start = time.time()

    make_order_sinc(1)
    make_order_sinc(2)
    make_order_sinc(3)

    end = time.time()
    print(f"--- TEMPO TOTAL SÍNCRONO: {end - start:.2f}---")

execute_sinc()

