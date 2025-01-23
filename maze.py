from cell import Cell
import random
import time

class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None, # None for tests
        seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self,i,j):
        if self._win is None:
            return
        x1_pos = self._x1 + (i * self._cell_size_x)
        y1_pos = self._y1 + (j * self._cell_size_y)
        x2_pos = x1_pos + self._cell_size_x
        y2_pos = y1_pos + self._cell_size_y
        self._cells[i][j].draw(x1_pos, y1_pos, x2_pos, y2_pos)
        self._animate()


    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(.01)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols -1][self._num_rows -1].has_bottom_wall =  False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_moves = []
            # checking possible cells to visit next
            # left
            if i > 0 and not self._cells[i-1][j].visited: 
                possible_moves.append((i-1,j))
            # right
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                possible_moves.append((i+1,j))
            # up
            if j > 0 and not self._cells[i][j-1].visited:
                possible_moves.append((i,j-1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                possible_moves.append((i,j+1))

            # nowhere else to go
            if len(possible_moves) == 0:
                self._draw_cell(i,j)
                return
            
            # randomly choose next direction
            choice_rand = random.randrange(0,len(possible_moves))
            next_i, next_j = possible_moves[choice_rand]
            # self._cells[next_i][next_j].visited = True
            
            # remove walls between traversed cells
            # right
            if next_i == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][j].has_left_wall = False
            # left
            elif next_i == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][j].has_right_wall = False
            # down
            elif next_j == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][next_j].has_top_wall = False
            # up
            elif next_j == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][next_j].has_bottom_wall = False

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False
    
    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # base case
        if i == self._num_cols -1 and j == self._num_rows - 1:
            return True
        
        # search left
        if (i > 0
            and not self._cells[i][j].has_left_wall
            and not self._cells[i - 1][j].visited):

            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        
        # search right
        if (i < self._num_cols
            and not self._cells[i][j].has_right_wall
            and not self._cells[i + 1][j].visited):

            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        
        # search up
        if (j > 0
            and not self._cells[i][j].has_top_wall
            and not self._cells[i][j - 1].visited):

            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        
        if (j < self._num_rows
            and not self._cells[i][j].has_bottom_wall
            and not self._cells[i][j + 1].visited):

            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False
        
    def solve(self):
        return self._solve_r(0,0)