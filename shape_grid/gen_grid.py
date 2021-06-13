from itertools import product

def generateGrid(cellsize=100, canvasSize=100, buffer=0):
    """
    Generate a grid of points with a resolution of cellsize assuming
    a square canvas of size canvasSize.
    """
    cellList = [x * cellsize + cellsize/2.0 for x in range(0-buffer, int(canvasSize/cellsize)+buffer)]
    return list(product(cellList, cellList))
