
class PieceBoard:

    def __init__(self, h_int, v_int, h_off, v_off):
        self.coordinate = [[0] * 15 for _ in range(15)]

        self.horizontal_interval = h_int
        self.vertical_interval = v_int
        self.horizontal_offset = h_off
        self.vertical_offset = v_off

        self.blackOnBoard = []  # use list for undo
        self.whiteOnBoard = []

        self.over = False   # a flag to show if game has ended

    def judge(self, x, y):
        # this function is to judge if a user has won
        # notice that in gobang game, last piece in 5 continuous pieces must locate at one end

        x_bound = y_bound = 15
        directions = [[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1]]

        for move in directions:
            count = 0
            temp_x, temp_y = x, y
            for i in range(1, 5, 1):
                temp_x, temp_y = temp_x + move[0], temp_y + move[1]
                if temp_x < 0 or temp_x >= x_bound or temp_y < 0 or temp_y >= y_bound:
                    continue
                if self.coordinate[x][y] == self.coordinate[temp_x][temp_y] :
                    count += 1
            if count == 4:
                self.over = True
                break

    def getCoordinate(self, position, black_turn):
        """
        this function get the standard position of a piece
        and add this piece to the chessboard map
        """

        x = (position[0] - self.horizontal_offset) // self.horizontal_interval
        y = (position[1] - self.vertical_offset) // self.vertical_interval

        if self.coordinate[x][y] != 0:
            # chosen position has been covered by another piece
            # return -1, -1 as sign of covered position
            return -1, -1

        # a piece has landed
        self.coordinate[x][y] = 1 if black_turn else -1
        self.judge(x, y)

        horizontal_pos = self.horizontal_offset + self.horizontal_interval * x
        vertical_pos = self.vertical_offset + self.vertical_interval * y

        return horizontal_pos, vertical_pos

    def getStdPosition(self, position):
        """
        this function get the standard position of a piece
        without add it to the chessboard map
        """
        x = max(min((position[0] - self.horizontal_offset) // self.horizontal_interval, 14), 0)
        y = max(min((position[1] - self.vertical_offset) // self.vertical_interval, 14), 0)

        if self.coordinate[x][y] != 0:
            # chosen position has been covered by another piece
            # return -1, -1 as sign of covered position
            return -1, -1

        horizontal_pos = self.horizontal_offset + self.horizontal_interval * x
        vertical_pos = self.vertical_offset + self.vertical_interval * y

        return horizontal_pos, vertical_pos

    def ifOver(self):
        return self.over

    def reset(self):
        self.blackOnBoard.clear()
        self.whiteOnBoard.clear()

        for x in range(15):
            for y in range(15):
                self.coordinate[x][y] = 0

        self.over = False
