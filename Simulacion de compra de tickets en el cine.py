import simpy
import random

def cliente(env, nombre, cine, salas):
    llegada = env.now
    print(f"{nombre} llegó al cine a las {llegada:.2f} horas.")
    with cine.request() as turno:
        yield turno
        print(f"{nombre} compra ticket a las {env.now:.2f} horas.")
        yield env.timeout(random.expovariate(1/5))  # Tiempo promedio de compra: 5 minutos
        print(f"{nombre} asignado a una sala a las {env.now:.2f} horas.")
        for sala in salas:
            if salas[sala] > 0:
                salas[sala] -= 1
                break

def llegada_clientes(env, cine, salas):
    cliente_id = 0
    while True:
        # Calcular el próximo tiempo de llegada
        proximo_tiempo = random.expovariate(1/10)
        if env.now + proximo_tiempo >= 12:  # Detener la llegada si excede las 12 horas
            break
        yield env.timeout(proximo_tiempo)  # Llegada cada 10 minutos en promedio
        cliente_id += 1
        env.process(cliente(env, f"Cliente {cliente_id}", cine, salas))

# Configuración del sistema
env = simpy.Environment()
cine = simpy.Resource(env, capacity=3)  # 3 taquillas disponibles
salas = {f"Sala {i}": 100 for i in range(1, 5)}  # 4 salas con 100 asientos cada una

env.process(llegada_clientes(env, cine, salas))
env.run(until=12)  # Ejecutar la simulación hasta las 12 horas
print("Capacidad final de las salas:", salas)