import random


WIDTH = 3
HEIGHT = 3
AMOUNT_OF_CELLS = WIDTH * HEIGHT
MAX_NUM = 5


def calculateColumn(index: int) -> int:
    return index % (WIDTH)


def calculateRow(index: int) -> int:
    return index // WIDTH


# first make the grid with just numbers
grid_of_numbers = []

for x in range(HEIGHT):
    for y in range(WIDTH):
        grid_of_numbers.append(random.randint(0, MAX_NUM))


# grid_of_numbers = [6, 5, 4, 3, 2, 1]


for i, num in enumerate(grid_of_numbers):
    print(num, end="\t")
    if calculateColumn(i) >= WIDTH - 1:
        print("\n")


print(grid_of_numbers)


class Cell:

    def __init__(self, _column: int, _row: int, _value: int, grid: list[int]) -> None:
        self.column = _column
        self.row = _row
        self.index = self.column + self.row * WIDTH
        self.value = _value

        # dijkstra numbers
        self.f_value = 0
        self.g_value = 0
        self.h_value = 0

        self.visitedNeighbours = [False, False, False, False]

        # NORTH
        self.north_index = self.index - WIDTH
        if calculateRow(self.north_index) >= 0:
            self.north_value = grid[self.north_index]
            self.north_difference = abs(self.value - self.north_value)
        else:
            self.north_value = -1
            self.north_difference = -1

        # EAST
        self.east_index = self.index + 1
        if calculateColumn(self.east_index) < WIDTH and self.index != WIDTH*HEIGHT - 1:
            self.east_value = grid[self.east_index]
            self.east_difference = abs(self.value - self.east_value)
        else:
            self.east_difference = -1
            self.east_value = -1

        # SOUTH
        self.south_index = self.index + WIDTH
        if calculateRow(self.south_index) < HEIGHT:
            self.south_value = grid[self.south_index]
            self.south_difference = abs(self.value - self.south_value)
        else:
            self.south_value = -1
            self.south_difference = -1

        # WEST
        self.west_index = self.index - 1
        if calculateColumn(self.west_index) >= 0 and self.index != 0:
            self.west_value = grid[self.west_index]
            self.west_difference = abs(self.value - self.west_value)
        else:
            self.west_value = -1
            self.west_difference = -1

    # This function has the issue that if the path is not rightly setup, it will always go to the lowest neighbour. This can make an infinite loop (test function)
    def decideNextStep(self) -> int:

        values = self.getAllNeigbouringValues()
        minValue = MAX_NUM + 1
        lowestValueIndex = -1
        direction = -1

        for dir, v in enumerate(values):
            if v != -1 and v <= minValue and not self.visitedNeighbours[dir]:
                lowestValueIndex = self.getIndexFromDirection(dir)
                minValue = v
                direction = dir

        self.visitedNeighbours[direction] = True
        return lowestValueIndex

    # decide the next step by always moving to the corner by moving to the lowest number
    def decideNextStepFirstGameSimple(self) -> int:
        all_values = self.getAllNeigbouringValues()
        rightValue = all_values[1]
        southValue = all_values[2]

        # if one of values is -1, return the other
        if rightValue == -1:
            return self.index + WIDTH
        if southValue == -1:
            return self.index + 1

        if rightValue < southValue:
            return self.index + 1
        return self.index + WIDTH

    def decideNextStepSecondGameSimple(self) -> int:
        all_values = self.getAllNeigbouringValues()

        rightValue = all_values[1]
        southValue = all_values[2]

        rightValueDifference = abs(self.value - all_values[1])
        southValueDifference = abs(self.value - all_values[2])

        # if one of values is -1, return the other
        if rightValue == -1:
            return self.index + WIDTH
        if southValue == -1:
            return self.index + 1

        if rightValueDifference < southValueDifference:
            return self.index + 1
        return self.index + WIDTH

    def getIndexFromDirection(self, direction: int) -> int:
        if direction == 0:
            return self.index - WIDTH
        elif direction == 1:
            return self.index + 1
        elif direction == 2:
            return self.index + WIDTH
        elif direction == 3:
            return self.index - 1

    def getAllNeigbouringValues(self) -> list[int]:
        return [self.north_value, self.east_value, self.south_value, self.west_value]

    def __str__(self) -> str:
        return f"Cell: index: {self.index} column: {self.column} row: {self.row} values: {[self.north_difference, self.east_difference, self.south_difference, self.west_difference]} indexes: {[self.north_index, self.east_index, self.south_index, self.west_index]}"


grid_of_cells: list[Cell] = []

# Making the cells
for index, number in enumerate(grid_of_numbers):
    newCell = Cell(calculateColumn(index), calculateRow(
        index), number, grid_of_numbers)
    grid_of_cells.append(newCell)


current_cell = grid_of_cells[0]
path_taken = [0]

algorithm_choice = ""
while not algorithm_choice in ["1", "2"]:
    algorithm_choice = input(
        "Do you want to use the simple algorithm (1) or the Dijkstra's algorithm (2)? \nChoose 1 or 2: ")

if algorithm_choice == "1":

    while not game_choice in ["1", "2"]:
        game_choice = input(
            "Do you want to use the time spent on each cell game (1) or time spent is time difference game (2)? \nChoose 1 or 2: ")

    if game_choice == "1":
        while current_cell.index != WIDTH*HEIGHT-1:
            next_step = current_cell.decideNextStepFirstGameSimple()
            path_taken.append(next_step)
            current_cell = grid_of_cells[next_step]

    if game_choice == "2":
        while current_cell.index != WIDTH*HEIGHT-1:
            next_step = current_cell.decideNextStepSecondGameSimple()
            path_taken.append(next_step)
            current_cell = grid_of_cells[next_step]

if algorithm_choice == "2":

    open_set = []
    closed_set = []

    while current_cell.index != WIDTH*HEIGHT-1:
        pass


print("FINISHED")
print(path_taken)
