from app import db
from src.models.puzzle_solver_log import PuzzleSolverLog


class PuzzleSolver:
    def __init__(self, n, grid):
        self.n = n
        self.grid = grid
        self.mario = None
        self.peach = None
        self.obstacles = []
        self.free_cells = []
        self.complete_paths = []
        self.possible_paths = []
        self.shortest_paths = []
        self.error_flag = False

        self.__convert_grid()
        self.__check_input()

    def solve_puzzle(self):
        """
        calls all the necessary methods in order to solve the current puzzle
        """
        starting_paths = self.__get_free_cells_around_position(self.mario)
        for path in starting_paths:
            result = self.__find_path_recursively(path, [self.mario], [self.mario])
            clean_path = self.__clean_path(result)
            complete_path = self.__get_last_move(clean_path)
            if complete_path[len(complete_path) - 1]['move']:
                self.complete_paths.append(complete_path)

        self.__get_shortest_paths()

    def log(self, time_elapsed):
        """
        log the current puzzle result into the database
        :param time_elapsed: the execution time of the solution
        """
        log = PuzzleSolverLog(
            n=self.n,
            grid=str(self.grid),
            paths=str(self.shortest_paths),
            error_flag=self.error_flag,
            request_time=time_elapsed
        )
        db.session.add(log)
        db.session.commit()

    def __get_shortest_paths(self):
        """
        determines the shortest paths from the complete paths list and set the shortest_path variable with a
        list of just moves
        :return:
        """
        try:
            if self.complete_paths:
                min_len = min(map(len, self.complete_paths))
                shortest_paths = [lst for lst in self.complete_paths if len(lst) == min_len]

                for shortest_path in shortest_paths:
                    shortest_path.pop(0)
                    self.shortest_paths.append([p['move'] for p in shortest_path])

        except Exception as e:
            raise e

    def __convert_grid(self):
        """
        convert the input grid into a series of usable variables
        """
        try:
            for i in range(0, self.n):
                for j in range(0, self.n):
                    if self.grid[i][j] == 'm':
                        self.mario = {'i': i,
                                      'j': j}
                    elif self.grid[i][j] == 'p':
                        self.peach = {'i': i,
                                      'j': j}
                    elif self.grid[i][j] == 'x':
                        self.obstacles.append(dict(i=i, j=j))
                    elif self.grid[i][j] == '-':
                        self.free_cells.append(dict(i=i, j=j))
        except Exception as e:
            raise e

    def __get_free_cells_around_position(self, current_position):
        """
        get all the free cells around a specific position
        :param current_position: the position to search for surrounding free cells for
        :return: the free cells around the current position
        """
        free_cells_around_mario = []
        for free_cell in self.free_cells:
            if abs(free_cell['i'] - current_position['i']) <= 1 and abs(free_cell['j'] - current_position['j']) <= 1:
                if current_position != free_cell:
                    move = self.__get_move(current_position, free_cell)
                    if not move:
                        continue
                    free_cells_around_mario.append(dict(i=free_cell['i'], j=free_cell['j'], move=move))

        return free_cells_around_mario

    def __get_last_move(self, path):
        """
        get the last move for the selected path
        :param path: the path to find the last move for
        :return: the complete path
        """
        move = self.__get_move(path[len(path) - 1], self.peach)
        path.append(dict(i=self.peach['i'], j=self.peach['j'], move=move))
        return path

    def __find_path_recursively(self, current_position, visited, visited_with_position):
        """
        recursive function to find a path based on a starting current position
        :param current_position: the position from where to start
        :param visited: the visited paths
        :param visited_with_position: the visited path with the position
        :return: the visited path with position
        """
        position_to_check = dict(i=current_position['i'], j=current_position['j'])
        if self.__get_move(position_to_check, self.peach):
            visited.append(dict(i=current_position['i'], j=current_position['j']))
            visited_with_position.append(current_position)
            return visited_with_position

        if position_to_check in visited:
            return visited_with_position

        if abs(visited[len(visited) - 1]['i'] - position_to_check['i']) >= 1 \
                and abs(visited[len(visited) - 1]['j'] - position_to_check['j']) >= 1:
            return visited_with_position

        visited.append(dict(i=current_position['i'], j=current_position['j']))
        visited_with_position.append(current_position)

        for path in self.__get_free_cells_around_position(dict(i=current_position['i'], j=current_position['j'])):
            test = self.__find_path_recursively(path, visited, visited_with_position)
            if test not in self.possible_paths:
                self.possible_paths.append(test)

        return visited_with_position

    @staticmethod
    def __get_move(current_position, free_cell):
        """
        Define which move will be the next
        :param current_position: the current mario position
        :param free_cell: the free cell to get the movement direction too
        :return: the direction to which to move
        """
        difference_column = current_position['j'] - free_cell['j']
        difference_row = current_position['i'] - free_cell['i']
        if difference_row == 0 and difference_column == 1:
            move = 'LEFT'
        elif difference_row == 0 and difference_column == -1:
            move = 'RIGHT'
        elif difference_row == -1 and difference_column == 0:
            move = 'DOWN'
        elif difference_row == 1 and difference_column == 0:
            move = 'UP'
        else:
            move = None
        return move

    def __clean_path(self, path):
        """
        removes the duplicated/double jumps from the path
        :param path: the path to clean
        :return: the clean and stipped path
        """
        indexes_to_remove = []
        final_path = []
        for i in range(0, len(path)):
            if not self.__get_move(path[i], self.peach):
                final_path.append(path[i])
            else:
                final_path.append(path[i])
                break

        for i in range(0, len(final_path) - 1):
            if abs(final_path[i]['i'] - final_path[i + 1]['i']) > 1 \
                    or abs(final_path[i]['j'] - final_path[i + 1]['j']) > 1:
                indexes_to_remove.append(i)

        for ele in sorted(indexes_to_remove, reverse=True):
            del final_path[ele]

        if path != final_path:
            self.__clean_path(final_path)
        return final_path

    def __check_input(self):
        """
        validates the game input setting an error flag in case of wrong input
        """
        try:
            for i in range(0, len(self.grid)):
                assert self.n == len(self.grid) == len(self.grid[i])

            assert self.mario
            assert self.peach
            assert self.obstacles
            assert self.free_cells
        except AssertionError:
            self.error_flag = True
