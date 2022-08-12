import random


WIDTH = 3
HEIGHT = 3
AMOUNT_OF_CELLS = WIDTH * HEIGHT
MAX_NUM = 5
END_INDEX = AMOUNT_OF_CELLS - 1


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
        self.neighbours: list[Cell] = []

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

    def addNeigbours(self, full_grid: list):

        if self.row > 0:
            self.neighbours.append(full_grid[self.index - WIDTH])

        if self.column < WIDTH - 1:
            self.neighbours.append(full_grid[self.index + 1])

        if self.row < HEIGHT - 1:
            self.neighbours.append(full_grid[self.index + WIDTH])

        if self.column > 0:
            self.neighbours.append(full_grid[self.index - 1])

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


def predictDistanceSimpleGame(cell1: Cell, cell2: Cell):
    horizontal_distance = abs(cell1.column - cell2.column)
    vertical_distance = abs(cell1.row - cell2.row)
    return horizontal_distance + vertical_distance


grid_of_cells: list[Cell] = []

# Making the cells
for index, number in enumerate(grid_of_numbers):
    newCell = Cell(calculateColumn(index), calculateRow(
        index), number, grid_of_numbers)
    grid_of_cells.append(newCell)

# Give each cell neigbours
for cell in grid_of_cells:
    cell.addNeigbours(grid_of_cells)

current_cell = grid_of_cells[0]
path_taken = [0]

algorithm_choice = "1" # Only 1 gets used
while not algorithm_choice in ["1", "2"]:
    algorithm_choice = input(
        "Do you want to use the simple algorithm (1) or the Dijkstra's algorithm (2)? \nChoose 1 or 2: ")

if algorithm_choice == "1":

    game_choice = ""
    while not game_choice in ["1", "2"]:
        game_choice = input(
            "Do you want to use the time spent on each cell game (1) or time spent is time difference game (2)? \nChoose 1 or 2: ")


    # Current cell is the cell we have currently arrived at. We start at the topleft and finish at the bottom right. As long as we have not reached the bottom right, we have not finished the game.
    while current_cell.index != END_INDEX:
        next_step = -1
        if game_choice == "1":
            # Each cell will calculate the next best step by looking at their east and south neighbour and check which one has the lowest value. This way there is always a straight path to the finish.
            next_step = current_cell.decideNextStepFirstGameSimple()
        elif game_choice == "2":
            # Each cell calculates the difference between it's value and it's neigbour's value and sees which one has the least absolute difference
            next_step = current_cell.decideNextStepSecondGameSimple()

        path_taken.append(next_step)
        current_cell = grid_of_cells[next_step]

        

if algorithm_choice == "2":

    open_set: list[Cell] = [grid_of_cells[0]]
    closed_set: list[Cell] = []

    while len(open_set) > 0:
        print("open set:", len(open_set))
        print("closed set:", len(closed_set))

        best_scoring_index: int = 0
        for current_open_cell_index, current_open_cell in enumerate(open_set):
            if(current_open_cell.f_value < open_set[best_scoring_index].f_value):
                best_scoring_index = current_open_cell_index

        current_cell = open_set[best_scoring_index]
        if current_cell.index == END_INDEX:
            print("Reached the end.")
            break

        # Remove from the open set
        for i in range(len(open_set)):
            if i == current_cell.index:
                open_set.pop(i)
                break
        closed_set.append(current_cell)

        for neighbour in current_cell.neighbours:
            if not neighbour in closed_set:
                expected_g_value = current_cell.g_value + neighbour.value

                if neighbour in open_set:
                    if neighbour.g_value > expected_g_value:
                        neighbour.g_value = expected_g_value
                else:
                    neighbour.g_value = expected_g_value
                    open_set.append(neighbour)

                neighbour.h_value = predictDistanceSimpleGame(current_cell, neighbour)
                neighbour.f_value = neighbour.g_value + neighbour.f_value


print("FINISHED")
print(path_taken)
