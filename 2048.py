import random
import sys

# Inicializar el tablero
def inicializar_tablero():
    tablero = [[0] * 4 for _ in range(4)]
    agregar_nuevo_numero(tablero)
    agregar_nuevo_numero(tablero)
    return tablero

# Mostrar el tablero
def mostrar_tablero(tablero):
    print("+------+------+------+------+") 
    for fila in tablero:
        print("| " + " | ".join(f"{num:4}" if num != 0 else "    " for num in fila) + " |")
        print("+------+------+------+------+")

# Agregar un nuevo número (2 o 4) en una casilla vacía
def agregar_nuevo_numero(tablero):
    filas_vacias = [(i, j) for i in range(4) for j in range(4) if tablero[i][j] == 0]
    if filas_vacias:
        i, j = random.choice(filas_vacias)
        tablero[i][j] = random.choice([2, 4])

# Funciones para mover y combinar números
def mover_izquierda(tablero, puntos):
    nuevo_tablero, movido = [], False
    for fila in tablero:
        nueva_fila, fila_movida, puntos_ganados = compactar_fila(fila)
        nuevo_tablero.append(nueva_fila + [0] * (4 - len(nueva_fila)))
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return nuevo_tablero, movido, puntos

def mover_derecha(tablero, puntos):
    nuevo_tablero, movido = [], False
    for fila in tablero:
        nueva_fila, fila_movida, puntos_ganados = compactar_fila(fila[::-1])
        nueva_fila.reverse()
        nuevo_tablero.append([0] * (4 - len(nueva_fila)) + nueva_fila)
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return nuevo_tablero, movido, puntos

def mover_arriba(tablero, puntos):
    return mover_vertical(tablero, True, puntos)

def mover_abajo(tablero, puntos):
    return mover_vertical(tablero, False, puntos)

def mover_vertical(tablero, hacia_arriba, puntos):
    nuevo_tablero, movido = list(map(list, zip(*tablero))), False
    for i in range(4):
        if hacia_arriba:
            nueva_fila, fila_movida, puntos_ganados = compactar_fila(nuevo_tablero[i])
            nuevo_tablero[i] = nueva_fila + [0] * (4 - len(nueva_fila))
        else:
            nueva_fila, fila_movida, puntos_ganados = compactar_fila(nuevo_tablero[i][::-1])
            nueva_fila.reverse()
            nuevo_tablero[i] = [0] * (4 - len(nueva_fila)) + nueva_fila
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return list(map(list, zip(*nuevo_tablero))), movido, puntos

def compactar_fila(fila):
    compactada = [num for num in fila if num != 0]
    combinada = []
    skip = False
    puntos_ganados = 0
    for i in range(len(compactada)):
        if skip:
            skip = False
            continue
        if i + 1 < len(compactada) and compactada[i] == compactada[i + 1]:
            combinada.append(compactada[i] * 2)
            puntos_ganados += 5
            skip = True
        else:
            combinada.append(compactada[i])
    return combinada, len(combinada) < len(fila), puntos_ganados

# Contar casillas vacías
def contar_casillas_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Obtener el número más grande en el tablero
def obtener_numero_mas_grande(tablero):
    return max(max(fila) for fila in tablero)

# Menú de selección de modalidad
def menu_seleccion():
    while True:
        print("Seleccione la modalidad de juego:")
        print("1. 1 Jugador")
        print("2. Jugador vs Jugador")
        print("3. Jugador vs Máquina")
        print("4. Como jugar")
        seleccion = input("Ingrese el número de la modalidad (1/2/3/4): ")
        if seleccion in ['1', '2', '3', '4']:
            return int(seleccion)
        else:
            print("Selección no válida. Inténtelo de nuevo.")

# Preguntar si el jugador quiere seguir jugando o salir
def preguntar_continuar():
    while True:
        respuesta = input("¿Deseas jugar otra partida? (si/no/replay): ").lower()
        if respuesta in ['si', 'no', 'replay']:
            return respuesta
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Función para deshacer el último movimiento
def undo_move(historial_movimientos, tablero, movimientos):
    if len(historial_movimientos) > 0:
        tablero = historial_movimientos.pop()
        movimientos -= 1
    return tablero, movimientos

# Función para preguntar si el jugador quiere jugar el nivel bonus
def preguntar_bonus():
    while True:
        respuesta = input("¡Has llegado a 2048! ¿Deseas jugar el nivel bonus y tratar de llegar a 4096? (si/no): ").lower()
        if respuesta == 'si':
            return True
        elif respuesta == 'no':
            return False
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Función para manejar el nivel bonus
def jugar_nivel_bonus(tablero, puntos, historial_movimientos):
    print("Nivel Bonus: ¡Intenta llegar a 4096!")
    movimientos = 0
    while True:
        mostrar_tablero(tablero)
        casillas_vacias = contar_casillas_vacias(tablero)
        numero_mas_grande = obtener_numero_mas_grande(tablero)
        print(f"Movimientos: {movimientos}")
        print(f"Casillas vacías: {casillas_vacias}")
        print(f"Número más grande: {numero_mas_grande}")
        print(f"Puntos: {puntos}")
        movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
        if movimiento == "exit":
            print("Gracias por jugar 2048!")
            sys.exit()
        if movimiento == "menu":
            return
        if movimiento == "undo":
            tablero, movimientos = undo_move(historial_movimientos, tablero, movimientos)
            continue
        if movimiento in ['w', 'a', 's', 'd']:
            historial_movimientos.append([fila[:] for fila in tablero])
            if movimiento == 'w':
                nuevo_tablero, movido, puntos = mover_arriba(tablero, puntos)
            elif movimiento == 'a':
                nuevo_tablero, movido, puntos = mover_izquierda(tablero, puntos)
            elif movimiento == 's':
                nuevo_tablero, movido, puntos = mover_abajo(tablero, puntos)
            elif movimiento == 'd':
                nuevo_tablero, movido, puntos = mover_derecha(tablero, puntos)
            
            if movido:
                agregar_nuevo_numero(nuevo_tablero)
                tablero = nuevo_tablero
                movimientos += 1
            else:
                historial_movimientos.pop()
                print("Movimiento inválido, no se puede mover en esa dirección.")
            
            if any(4096 in fila for fila in tablero):
                print("¡Ganaste! Llegaste a 4096.")
                mostrar_tablero(tablero)
                if preguntar_continuar() == 'menu':
                    return
            
            if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                print("¡Juego Terminado! No hay más movimientos posibles.")
                mostrar_tablero(tablero)
                if preguntar_continuar() == 'menu':
                    return
        else:
            print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de 1 Jugador
def jugar_1_jugador():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = 0
        puntos = 0
        while True:
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos: {movimientos}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos: {puntos}")
            movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
            if movimiento == "exit":
                print("Gracias por jugar 2048!")
                sys.exit()
            if movimiento == "menu":
                return
            if movimiento == "undo":
                tablero, movimientos = undo_move(historial_movimientos, tablero, movimientos)
                continue
            if movimiento in ['w', 'a', 's', 'd']:
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento, [fila[:] for fila in tablero]))
                if movimiento == 'w':
                    nuevo_tablero, movido, puntos = mover_arriba(tablero, puntos)
                elif movimiento == 'a':
                    nuevo_tablero, movido, puntos = mover_izquierda(tablero, puntos)
                elif movimiento == 's':
                    nuevo_tablero, movido, puntos = mover_abajo(tablero, puntos)
                elif movimiento == 'd':
                    nuevo_tablero, movido, puntos = mover_derecha(tablero, puntos)
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos += 1
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
                
                if any(2048 in fila for fila in tablero):
                    print("¡Ganaste! Llegaste a 2048.")
                    mostrar_tablero(tablero)
                    if preguntar_bonus():
                        jugar_nivel_bonus(tablero, puntos, historial_movimientos)
                    else:
                        respuesta = preguntar_continuar()
                        if respuesta == 'menu':
                            return
                        elif respuesta == 'replay':
                            reproducir_jugadas(historial_jugadas)
                            return
                
                if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                    print("¡Juego Terminado! No hay más movimientos posibles.")
                    mostrar_tablero(tablero)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
            else:
                print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de Jugador vs Jugador
def jugar_jugador_vs_jugador():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = [0, 0]
        puntos = [0, 0]
        jugadores = ["Jugador 1", "Jugador 2"]
        turno = 0
        while True:
            jugador_actual = jugadores[turno]
            print(f"Turno de {jugador_actual}")
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos de {jugador_actual}: {movimientos[turno]}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos de {jugador_actual}: {puntos[turno]}")
            movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
            if movimiento == "exit":
                print("Gracias por jugar 2048!")
                sys.exit()
            if movimiento == "menu":
                return
            if movimiento == "undo":
                tablero, movimientos[turno] = undo_move(historial_movimientos, tablero, movimientos[turno])
                continue
            if movimiento in ['w', 'a', 's', 'd']:
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento, [fila[:] for fila in tablero], jugador_actual))
                if movimiento == 'w':
                    nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                elif movimiento == 'a':
                    nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                elif movimiento == 's':
                    nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                elif movimiento == 'd':
                    nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos[turno] += 1
                    turno = 1 - turno  # Cambiar turno
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
                
                if any(2048 in fila for fila in tablero):
                    print(f"¡{jugador_actual} gana! Llegó a 2048.")
                    mostrar_tablero(tablero)
                    ganador = determinar_ganador(puntos)
                    print(ganador)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
                
                if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                    print("¡Juego Terminado! No hay más movimientos posibles.")
                    mostrar_tablero(tablero)
                    ganador = determinar_ganador(puntos)
                    print(ganador)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
            else:
                print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de Jugador vs Máquina
def jugar_jugador_vs_maquina():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = [0, 0]
        puntos = [0, 0]
        jugadores = ["Jugador", "Máquina"]
        turno = 0
        while True:
            jugador_actual = jugadores[turno]
            print(f"Turno de {jugador_actual}")
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos de {jugador_actual}: {movimientos[turno]}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos de {jugador_actual}: {puntos[turno]}")
            
            if turno == 0:  # Turno del jugador
                movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
                if movimiento == "exit":
                    print("Gracias por jugar 2048!")
                    sys.exit()
                if movimiento == "menu":
                    return
                if movimiento == "undo":
                    tablero, movimientos[turno] = undo_move(historial_movimientos, tablero, movimientos[turno])
                    continue
                if movimiento in ['w', 'a', 's', 'd']:
                    historial_movimientos.append([fila[:] for fila in tablero])
                    historial_jugadas.append((movimiento, [fila[:] for fila in tablero], jugador_actual))
                    if movimiento == 'w':
                        nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                    elif movimiento == 'a':
                        nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                    elif movimiento == 's':
                        nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                    elif movimiento == 'd':
                        nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                    
                    if movido:
                        agregar_nuevo_numero(nuevo_tablero)
                        tablero = nuevo_tablero
                        movimientos[turno] += 1
                        turno = 1 - turno  # Cambiar turno
                    else:
                        historial_movimientos.pop()
                        historial_jugadas.pop()
                        print("Movimiento inválido, no se puede mover en esa dirección.")
                else:
                    print("Movimiento no válido. Usa WASD para moverte.")
            else:  # Turno de la máquina
                input("Presiona ENTER para que la máquina realice su movimiento...")
                print("Turno de la máquina.")
                movimiento_maquina = elegir_movimiento_maquina(tablero)
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento_maquina, [fila[:] for fila in tablero], jugador_actual))
                if movimiento_maquina == 'w':
                    nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                elif movimiento_maquina == 'a':
                    nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                elif movimiento_maquina == 's':
                    nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                elif movimiento_maquina == 'd':
                    nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos[turno] += 1
                    turno = 1 - turno  # Cambiar turno
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
            
            if any(2048 in fila for fila in tablero):
                print(f"¡{jugador_actual} gana! Llegó a 2048.")
                mostrar_tablero(tablero)
                ganador = determinar_ganador(puntos)
                print(ganador)
                respuesta = preguntar_continuar()
                if respuesta == 'menu':
                    return
                elif respuesta == 'replay':
                    reproducir_jugadas(historial_jugadas)
                    return
            
            if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                print("¡Juego Terminado! No hay más movimientos posibles.")
                mostrar_tablero(tablero)
                ganador = determinar_ganador(puntos)
                print(ganador)
                respuesta = preguntar_continuar()
                if respuesta == 'menu':
                    return
                elif respuesta == 'replay':
                    reproducir_jugadas(historial_jugadas)
                    return

# Función para determinar el ganador basado en puntos
def determinar_ganador(puntos):
    if puntos[0] > puntos[1]:
        return "¡Jugador gana con más puntos!"
    elif puntos[1] > puntos[0]:
        return "¡Máquina gana con más puntos!"
    else:
        return "¡Es un empate!"

# Función para que la máquina elija un movimiento
def elegir_movimiento_maquina(tablero):
    # Implementa una estrategia simple para la máquina
    movimientos = ['w', 'a', 's', 'd']
    for movimiento in movimientos:
        nuevo_tablero, movido, _ = mover(tablero, movimiento, 0)
        if movido:
            return movimiento
    return random.choice(movimientos)

# Mover el tablero basado en la dirección
def mover(tablero, direccion, puntos):
    if direccion == 'w':
        return mover_arriba(tablero, puntos)
    elif direccion == 'a':
        return mover_izquierda(tablero, puntos)
    elif direccion == 's':
        return mover_abajo(tablero, puntos)
    elif direccion == 'd':
        return mover_derecha(tablero, puntos)
    return tablero, False, puntos

# Función para mostrar las instrucciones de juego
def mostrar_instrucciones():
    print("""
    Bienvenido al juego 2048!
    
    Instrucciones:
    1. El juego se juega en un tablero de 4x4.
    2. Cada turno, puedes mover los números en el tablero en una de cuatro direcciones: arriba (W), abajo (S), izquierda (A), derecha (D).
    3. Cuando dos números iguales se tocan, se combinan en uno solo (por ejemplo, 2 + 2 = 4).
    4. Después de cada movimiento, aparece un nuevo número (2 o 4) en una casilla vacía aleatoria.
    5. El objetivo es crear un bloque con el número 2048.
    6. El juego termina cuando no hay movimientos posibles y el tablero está lleno.
    7. Por cada número que se junte, se otorgan 5 puntos.
    
    Controles:
    - Usa W para mover hacia arriba.
    - Usa S para mover hacia abajo.
    - Usa A para mover hacia la izquierda.
    - Usa D para mover hacia la derecha.
    - Escribe 'exit' para salir del juego.
    - Escribe 'undo' para deshacer el último movimiento.
    
    ¡Buena suerte!
    """)
    input("Presiona ENTER para regresar al menú de selección.")

# Función para reproducir las jugadas
def reproducir_jugadas(historial_jugadas):
    print("\nReproduciendo las jugadas...\n")
    for jugada in historial_jugadas:
        movimiento, tablero, jugador = jugada if len(jugada) == 3 else (*jugada, "")
        print(f"Movimiento: {movimiento} {'- ' + jugador if jugador else ''}")
        mostrar_tablero(tablero)
        input("Presiona ENTER para continuar...")

# Función principal
def main():
    while True:
        seleccion = menu_seleccion()
        if seleccion == 1:
            jugar_1_jugador()
        elif seleccion == 2:
            jugar_jugador_vs_jugador()
        elif seleccion == 3:
            jugar_jugador_vs_maquina()
        elif seleccion == 4:
            mostrar_instrucciones()

# Verificar si hay movimientos posibles
def movimientos_posibles(tablero):
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == 0:
                return True
            if i < 3 and tablero[i][j] == tablero[i + 1][j]:
                return True
            if j < 3 and tablero[i][j] == tablero[i][j + 1]:
                return True
    return False

if __name__ == "__main__":
    main()import random
import sys

# Inicializar el tablero
def inicializar_tablero():
    tablero = [[0] * 4 for _ in range(4)]
    agregar_nuevo_numero(tablero)
    agregar_nuevo_numero(tablero)
    return tablero

# Mostrar el tablero
def mostrar_tablero(tablero):
    print("+------+------+------+------+") 
    for fila in tablero:
        print("| " + " | ".join(f"{num:4}" if num != 0 else "    " for num in fila) + " |")
        print("+------+------+------+------+")

# Agregar un nuevo número (2 o 4) en una casilla vacía
def agregar_nuevo_numero(tablero):
    filas_vacias = [(i, j) for i in range(4) for j in range(4) if tablero[i][j] == 0]
    if filas_vacias:
        i, j = random.choice(filas_vacias)
        tablero[i][j] = random.choice([2, 4])

# Funciones para mover y combinar números
def mover_izquierda(tablero, puntos):
    nuevo_tablero, movido = [], False
    for fila in tablero:
        nueva_fila, fila_movida, puntos_ganados = compactar_fila(fila)
        nuevo_tablero.append(nueva_fila + [0] * (4 - len(nueva_fila)))
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return nuevo_tablero, movido, puntos

def mover_derecha(tablero, puntos):
    nuevo_tablero, movido = [], False
    for fila in tablero:
        nueva_fila, fila_movida, puntos_ganados = compactar_fila(fila[::-1])
        nueva_fila.reverse()
        nuevo_tablero.append([0] * (4 - len(nueva_fila)) + nueva_fila)
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return nuevo_tablero, movido, puntos

def mover_arriba(tablero, puntos):
    return mover_vertical(tablero, True, puntos)

def mover_abajo(tablero, puntos):
    return mover_vertical(tablero, False, puntos)

def mover_vertical(tablero, hacia_arriba, puntos):
    nuevo_tablero, movido = list(map(list, zip(*tablero))), False
    for i in range(4):
        if hacia_arriba:
            nueva_fila, fila_movida, puntos_ganados = compactar_fila(nuevo_tablero[i])
            nuevo_tablero[i] = nueva_fila + [0] * (4 - len(nueva_fila))
        else:
            nueva_fila, fila_movida, puntos_ganados = compactar_fila(nuevo_tablero[i][::-1])
            nueva_fila.reverse()
            nuevo_tablero[i] = [0] * (4 - len(nueva_fila)) + nueva_fila
        puntos += puntos_ganados
        if fila_movida:
            movido = True
    return list(map(list, zip(*nuevo_tablero))), movido, puntos

def compactar_fila(fila):
    compactada = [num for num in fila if num != 0]
    combinada = []
    skip = False
    puntos_ganados = 0
    for i in range(len(compactada)):
        if skip:
            skip = False
            continue
        if i + 1 < len(compactada) and compactada[i] == compactada[i + 1]:
            combinada.append(compactada[i] * 2)
            puntos_ganados += 5
            skip = True
        else:
            combinada.append(compactada[i])
    return combinada, len(combinada) < len(fila), puntos_ganados

# Contar casillas vacías
def contar_casillas_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Obtener el número más grande en el tablero
def obtener_numero_mas_grande(tablero):
    return max(max(fila) for fila in tablero)

# Menú de selección de modalidad
def menu_seleccion():
    while True:
        print("Seleccione la modalidad de juego:")
        print("1. 1 Jugador")
        print("2. Jugador vs Jugador")
        print("3. Jugador vs Máquina")
        print("4. Como jugar")
        seleccion = input("Ingrese el número de la modalidad (1/2/3/4): ")
        if seleccion in ['1', '2', '3', '4']:
            return int(seleccion)
        else:
            print("Selección no válida. Inténtelo de nuevo.")

# Preguntar si el jugador quiere seguir jugando o salir
def preguntar_continuar():
    while True:
        respuesta = input("¿Deseas jugar otra partida? (si/no/replay): ").lower()
        if respuesta in ['si', 'no', 'replay']:
            return respuesta
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Función para deshacer el último movimiento
def undo_move(historial_movimientos, tablero, movimientos):
    if len(historial_movimientos) > 0:
        tablero = historial_movimientos.pop()
        movimientos -= 1
    return tablero, movimientos

# Función para preguntar si el jugador quiere jugar el nivel bonus
def preguntar_bonus():
    while True:
        respuesta = input("¡Has llegado a 2048! ¿Deseas jugar el nivel bonus y tratar de llegar a 4096? (si/no): ").lower()
        if respuesta == 'si':
            return True
        elif respuesta == 'no':
            return False
        else:
            print("Opción no válida. Inténtalo de nuevo.")

# Función para manejar el nivel bonus
def jugar_nivel_bonus(tablero, puntos, historial_movimientos):
    print("Nivel Bonus: ¡Intenta llegar a 4096!")
    movimientos = 0
    while True:
        mostrar_tablero(tablero)
        casillas_vacias = contar_casillas_vacias(tablero)
        numero_mas_grande = obtener_numero_mas_grande(tablero)
        print(f"Movimientos: {movimientos}")
        print(f"Casillas vacías: {casillas_vacias}")
        print(f"Número más grande: {numero_mas_grande}")
        print(f"Puntos: {puntos}")
        movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
        if movimiento == "exit":
            print("Gracias por jugar 2048!")
            sys.exit()
        if movimiento == "menu":
            return
        if movimiento == "undo":
            tablero, movimientos = undo_move(historial_movimientos, tablero, movimientos)
            continue
        if movimiento in ['w', 'a', 's', 'd']:
            historial_movimientos.append([fila[:] for fila in tablero])
            if movimiento == 'w':
                nuevo_tablero, movido, puntos = mover_arriba(tablero, puntos)
            elif movimiento == 'a':
                nuevo_tablero, movido, puntos = mover_izquierda(tablero, puntos)
            elif movimiento == 's':
                nuevo_tablero, movido, puntos = mover_abajo(tablero, puntos)
            elif movimiento == 'd':
                nuevo_tablero, movido, puntos = mover_derecha(tablero, puntos)
            
            if movido:
                agregar_nuevo_numero(nuevo_tablero)
                tablero = nuevo_tablero
                movimientos += 1
            else:
                historial_movimientos.pop()
                print("Movimiento inválido, no se puede mover en esa dirección.")
            
            if any(4096 in fila for fila in tablero):
                print("¡Ganaste! Llegaste a 4096.")
                mostrar_tablero(tablero)
                if preguntar_continuar() == 'menu':
                    return
            
            if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                print("¡Juego Terminado! No hay más movimientos posibles.")
                mostrar_tablero(tablero)
                if preguntar_continuar() == 'menu':
                    return
        else:
            print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de 1 Jugador
def jugar_1_jugador():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = 0
        puntos = 0
        while True:
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos: {movimientos}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos: {puntos}")
            movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
            if movimiento == "exit":
                print("Gracias por jugar 2048!")
                sys.exit()
            if movimiento == "menu":
                return
            if movimiento == "undo":
                tablero, movimientos = undo_move(historial_movimientos, tablero, movimientos)
                continue
            if movimiento in ['w', 'a', 's', 'd']:
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento, [fila[:] for fila in tablero]))
                if movimiento == 'w':
                    nuevo_tablero, movido, puntos = mover_arriba(tablero, puntos)
                elif movimiento == 'a':
                    nuevo_tablero, movido, puntos = mover_izquierda(tablero, puntos)
                elif movimiento == 's':
                    nuevo_tablero, movido, puntos = mover_abajo(tablero, puntos)
                elif movimiento == 'd':
                    nuevo_tablero, movido, puntos = mover_derecha(tablero, puntos)
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos += 1
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
                
                if any(2048 in fila for fila in tablero):
                    print("¡Ganaste! Llegaste a 2048.")
                    mostrar_tablero(tablero)
                    if preguntar_bonus():
                        jugar_nivel_bonus(tablero, puntos, historial_movimientos)
                    else:
                        respuesta = preguntar_continuar()
                        if respuesta == 'menu':
                            return
                        elif respuesta == 'replay':
                            reproducir_jugadas(historial_jugadas)
                            return
                
                if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                    print("¡Juego Terminado! No hay más movimientos posibles.")
                    mostrar_tablero(tablero)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
            else:
                print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de Jugador vs Jugador
def jugar_jugador_vs_jugador():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = [0, 0]
        puntos = [0, 0]
        jugadores = ["Jugador 1", "Jugador 2"]
        turno = 0
        while True:
            jugador_actual = jugadores[turno]
            print(f"Turno de {jugador_actual}")
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos de {jugador_actual}: {movimientos[turno]}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos de {jugador_actual}: {puntos[turno]}")
            movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
            if movimiento == "exit":
                print("Gracias por jugar 2048!")
                sys.exit()
            if movimiento == "menu":
                return
            if movimiento == "undo":
                tablero, movimientos[turno] = undo_move(historial_movimientos, tablero, movimientos[turno])
                continue
            if movimiento in ['w', 'a', 's', 'd']:
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento, [fila[:] for fila in tablero], jugador_actual))
                if movimiento == 'w':
                    nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                elif movimiento == 'a':
                    nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                elif movimiento == 's':
                    nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                elif movimiento == 'd':
                    nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos[turno] += 1
                    turno = 1 - turno  # Cambiar turno
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
                
                if any(2048 in fila for fila in tablero):
                    print(f"¡{jugador_actual} gana! Llegó a 2048.")
                    mostrar_tablero(tablero)
                    ganador = determinar_ganador(puntos)
                    print(ganador)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
                
                if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                    print("¡Juego Terminado! No hay más movimientos posibles.")
                    mostrar_tablero(tablero)
                    ganador = determinar_ganador(puntos)
                    print(ganador)
                    respuesta = preguntar_continuar()
                    if respuesta == 'menu':
                        return
                    elif respuesta == 'replay':
                        reproducir_jugadas(historial_jugadas)
                        return
            else:
                print("Movimiento no válido. Usa WASD para moverte.")

# Modalidad de Jugador vs Máquina
def jugar_jugador_vs_maquina():
    historial_movimientos = []
    historial_jugadas = []
    while True:
        tablero = inicializar_tablero()
        movimientos = [0, 0]
        puntos = [0, 0]
        jugadores = ["Jugador", "Máquina"]
        turno = 0
        while True:
            jugador_actual = jugadores[turno]
            print(f"Turno de {jugador_actual}")
            mostrar_tablero(tablero)
            casillas_vacias = contar_casillas_vacias(tablero)
            numero_mas_grande = obtener_numero_mas_grande(tablero)
            print(f"Movimientos de {jugador_actual}: {movimientos[turno]}")
            print(f"Casillas vacías: {casillas_vacias}")
            print(f"Número más grande: {numero_mas_grande}")
            print(f"Puntos de {jugador_actual}: {puntos[turno]}")
            
            if turno == 0:  # Turno del jugador
                movimiento = input("Movimiento (WASD, 'exit' para salir, 'undo' para deshacer, 'menu' para regresar al menú): ").lower()
                if movimiento == "exit":
                    print("Gracias por jugar 2048!")
                    sys.exit()
                if movimiento == "menu":
                    return
                if movimiento == "undo":
                    tablero, movimientos[turno] = undo_move(historial_movimientos, tablero, movimientos[turno])
                    continue
                if movimiento in ['w', 'a', 's', 'd']:
                    historial_movimientos.append([fila[:] for fila in tablero])
                    historial_jugadas.append((movimiento, [fila[:] for fila in tablero], jugador_actual))
                    if movimiento == 'w':
                        nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                    elif movimiento == 'a':
                        nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                    elif movimiento == 's':
                        nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                    elif movimiento == 'd':
                        nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                    
                    if movido:
                        agregar_nuevo_numero(nuevo_tablero)
                        tablero = nuevo_tablero
                        movimientos[turno] += 1
                        turno = 1 - turno  # Cambiar turno
                    else:
                        historial_movimientos.pop()
                        historial_jugadas.pop()
                        print("Movimiento inválido, no se puede mover en esa dirección.")
                else:
                    print("Movimiento no válido. Usa WASD para moverte.")
            else:  # Turno de la máquina
                input("Presiona ENTER para que la máquina realice su movimiento...")
                print("Turno de la máquina.")
                movimiento_maquina = elegir_movimiento_maquina(tablero)
                historial_movimientos.append([fila[:] for fila in tablero])
                historial_jugadas.append((movimiento_maquina, [fila[:] for fila in tablero], jugador_actual))
                if movimiento_maquina == 'w':
                    nuevo_tablero, movido, puntos[turno] = mover_arriba(tablero, puntos[turno])
                elif movimiento_maquina == 'a':
                    nuevo_tablero, movido, puntos[turno] = mover_izquierda(tablero, puntos[turno])
                elif movimiento_maquina == 's':
                    nuevo_tablero, movido, puntos[turno] = mover_abajo(tablero, puntos[turno])
                elif movimiento_maquina == 'd':
                    nuevo_tablero, movido, puntos[turno] = mover_derecha(tablero, puntos[turno])
                
                if movido:
                    agregar_nuevo_numero(nuevo_tablero)
                    tablero = nuevo_tablero
                    movimientos[turno] += 1
                    turno = 1 - turno  # Cambiar turno
                else:
                    historial_movimientos.pop()
                    historial_jugadas.pop()
                    print("Movimiento inválido, no se puede mover en esa dirección.")
            
            if any(2048 in fila for fila in tablero):
                print(f"¡{jugador_actual} gana! Llegó a 2048.")
                mostrar_tablero(tablero)
                ganador = determinar_ganador(puntos)
                print(ganador)
                respuesta = preguntar_continuar()
                if respuesta == 'menu':
                    return
                elif respuesta == 'replay':
                    reproducir_jugadas(historial_jugadas)
                    return
            
            if not any(0 in fila for fila in tablero) and not movimientos_posibles(tablero):
                print("¡Juego Terminado! No hay más movimientos posibles.")
                mostrar_tablero(tablero)
                ganador = determinar_ganador(puntos)
                print(ganador)
                respuesta = preguntar_continuar()
                if respuesta == 'menu':
                    return
                elif respuesta == 'replay':
                    reproducir_jugadas(historial_jugadas)
                    return

# Función para determinar el ganador basado en puntos
def determinar_ganador(puntos):
    if puntos[0] > puntos[1]:
        return "¡Jugador gana con más puntos!"
    elif puntos[1] > puntos[0]:
        return "¡Máquina gana con más puntos!"
    else:
        return "¡Es un empate!"

# Función para que la máquina elija un movimiento
def elegir_movimiento_maquina(tablero):
    # Implementa una estrategia simple para la máquina
    movimientos = ['w', 'a', 's', 'd']
    for movimiento in movimientos:
        nuevo_tablero, movido, _ = mover(tablero, movimiento, 0)
        if movido:
            return movimiento
    return random.choice(movimientos)

# Mover el tablero basado en la dirección
def mover(tablero, direccion, puntos):
    if direccion == 'w':
        return mover_arriba(tablero, puntos)
    elif direccion == 'a':
        return mover_izquierda(tablero, puntos)
    elif direccion == 's':
        return mover_abajo(tablero, puntos)
    elif direccion == 'd':
        return mover_derecha(tablero, puntos)
    return tablero, False, puntos

# Función para mostrar las instrucciones de juego
def mostrar_instrucciones():
    print("""
    Bienvenido al juego 2048!
    
    Instrucciones:
    1. El juego se juega en un tablero de 4x4.
    2. Cada turno, puedes mover los números en el tablero en una de cuatro direcciones: arriba (W), abajo (S), izquierda (A), derecha (D).
    3. Cuando dos números iguales se tocan, se combinan en uno solo (por ejemplo, 2 + 2 = 4).
    4. Después de cada movimiento, aparece un nuevo número (2 o 4) en una casilla vacía aleatoria.
    5. El objetivo es crear un bloque con el número 2048.
    6. El juego termina cuando no hay movimientos posibles y el tablero está lleno.
    7. Por cada número que se junte, se otorgan 5 puntos.
    
    Controles:
    - Usa W para mover hacia arriba.
    - Usa S para mover hacia abajo.
    - Usa A para mover hacia la izquierda.
    - Usa D para mover hacia la derecha.
    - Escribe 'exit' para salir del juego.
    - Escribe 'undo' para deshacer el último movimiento.
    
    ¡Buena suerte!
    """)
    input("Presiona ENTER para regresar al menú de selección.")

# Función para reproducir las jugadas
def reproducir_jugadas(historial_jugadas):
    print("\nReproduciendo las jugadas...\n")
    for jugada in historial_jugadas:
        movimiento, tablero, jugador = jugada if len(jugada) == 3 else (*jugada, "")
        print(f"Movimiento: {movimiento} {'- ' + jugador if jugador else ''}")
        mostrar_tablero(tablero)
        input("Presiona ENTER para continuar...")

# Función principal
def main():
    while True:
        seleccion = menu_seleccion()
        if seleccion == 1:
            jugar_1_jugador()
        elif seleccion == 2:
            jugar_jugador_vs_jugador()
        elif seleccion == 3:
            jugar_jugador_vs_maquina()
        elif seleccion == 4:
            mostrar_instrucciones()

# Verificar si hay movimientos posibles
def movimientos_posibles(tablero):
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == 0:
                return True
            if i < 3 and tablero[i][j] == tablero[i + 1][j]:
                return True
            if j < 3 and tablero[i][j] == tablero[i][j + 1]:
                return True
    return False

if __name__ == "__main__":
    main()
