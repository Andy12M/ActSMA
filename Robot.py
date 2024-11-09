"""
Simulación de robots de limpieza reactivos en una habitación de MxN espacios.
El programa simula el comportamiento de agentes de limpieza que aspiran celdas sucias y
se mueven aleatoriamente cuando una celda está limpia.

Integrantes: 
Andrea Doce Murillo- A01799931
Israel Rocha Ramírez- A01798126

Fecha de entrega:
8 de noviembre de 2024
"""

import numpy as np
import random


class Room:
    """
    Representa la habitación donde los agentes operan. Cada celda puede estar limpia o sucia.
    """

    def __init__(self, numRows, numCols, dirtyPercentage):
        """
        Inicializa la habitación con celdas sucias en posiciones aleatorias según el porcentaje dado.

        Parámetros:
        numRows (int): Número de filas en la habitación.
        numCols (int): Número de columnas en la habitación.
        dirtyPercentage (float): Porcentaje de celdas que estarán inicialmente sucias.
        """
        self.numRows = numRows
        self.numCols = numCols
        self.cells = np.zeros((numRows, numCols), dtype=int)

        totalCells = numRows * numCols
        numDirtyCells = int(totalCells * dirtyPercentage)
        dirtyIndices = random.sample(range(totalCells), numDirtyCells)
        for index in dirtyIndices:
            row, col = divmod(index, numCols)
            self.cells[row, col] = 1  # 1 representa una celda sucia

    def isDirty(self, x, y):
        """
        Verifica si la celda en las coordenadas (x, y) está sucia.

        Parámetros:
        x (int): Fila de la celda.
        y (int): Columna de la celda.

        Retorna:
        bool: True si la celda está sucia, False en caso contrario.
        """
        return self.cells[x, y] == 1

    def clean(self, x, y):
        """
        Limpia la celda en las coordenadas (x, y).

        Parámetros:
        x (int): Fila de la celda.
        y (int): Columna de la celda.
        """
        self.cells[x, y] = 0  # 0 representa una celda limpia

    def getCleanPercentage(self):
        """
        Calcula el porcentaje de celdas limpias en la habitación.

        Retorna:
        float: Porcentaje de celdas limpias.
        """
        totalCleanCells = np.sum(self.cells == 0)
        totalCells = self.numRows * self.numCols
        return totalCleanCells / totalCells * 100

    def display(self):
        """
        Muestra el estado actual de la habitación en la consola, con [X] para celdas sucias y [ ] para celdas limpias.
        """
        for row in self.cells:
            print(" ".join("[X]" if cell == 1 else "[ ]" for cell in row))
        print("\n")


class Agent:
    """
    Representa un agente de limpieza que puede moverse y limpiar celdas en la habitación.
    """

    def __init__(self, room):
        """
        Inicializa la posición del agente en la esquina superior izquierda de la habitación.

        Parámetros:
        room (Room): La habitación donde el agente se moverá y limpiará.
        """
        self.room = room
        self.posX = 0
        self.posY = 0
        self.moves = 0

    def move(self):
        """
        Mueve al agente a una celda adyacente aleatoria en una de las ocho direcciones posibles.
        Si el movimiento excede los límites de la habitación, el agente se queda en su celda actual.
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        dx, dy = random.choice(directions)
        newX, newY = self.posX + dx, self.posY + dy

        if 0 <= newX < self.room.numRows and 0 <= newY < self.room.numCols:
            self.posX, self.posY = newX, newY
        self.moves += 1

    def act(self):
        """
        Ejecuta la acción del agente: limpia la celda si está sucia o se mueve si está limpia.
        """
        if self.room.isDirty(self.posX, self.posY):
            self.room.clean(self.posX, self.posY)
        else:
            self.move()


def runSimulation(numRows, numCols, dirtyPercentage, maxTime, numAgents):
    """
    Ejecuta la simulación de agentes de limpieza en la habitación.

    Parámetros:
    numRows (int): Número de filas en la habitación.
    numCols (int): Número de columnas en la habitación.
    dirtyPercentage (float): Porcentaje inicial de celdas sucias.
    maxTime (int): Tiempo máximo de ejecución de la simulación.
    numAgents (int): Número de agentes en la habitación.

    Retorna:
    tuple: Tiempo transcurrido, porcentaje de celdas limpias y número total de movimientos de todos los agentes.
    """
    room = Room(numRows, numCols, dirtyPercentage)
    agents = [Agent(room) for _ in range(numAgents)]
    timeElapsed = 0
    allClean = False

    while timeElapsed < maxTime and not allClean:
        for agent in agents:
            agent.act()

        allClean = room.getCleanPercentage() == 100
        timeElapsed += 1

        # Muestra el estado de la habitación en cada paso de tiempo
        print(f"Tiempo: {timeElapsed}")
        room.display()

    cleanPercentage = room.getCleanPercentage()
    totalMoves = sum(agent.moves for agent in agents)

    return timeElapsed, cleanPercentage, totalMoves


# Solicitar al usuario los parámetros de la simulación
numRows = int(input("Ingresa el número de filas de la habitación: "))
numCols = int(input("Ingresa el número de columnas de la habitación: "))
dirtyPercentage = float(input("Ingresa el porcentaje inicial de celdas sucias (0.0 a 1.0): "))
maxTime = int(input("Ingresa el tiempo máximo de ejecución: "))
numAgents = int(input("Ingresa el número de agentes: "))

# Ejecución de la simulación
timeElapsed, cleanPercentage, totalMoves = runSimulation(numRows, numCols, dirtyPercentage, maxTime, numAgents)

# Resultados de la simulación
print(f"\nTiempo hasta que todas las celdas estén limpias (o se agotó el tiempo): {timeElapsed}")
print(f"Porcentaje de celdas limpias al finalizar: {cleanPercentage:.2f}%")
print(f"Número total de movimientos realizados por los agentes: {totalMoves}")
