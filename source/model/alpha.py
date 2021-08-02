import os
import numpy as np

## User-defined macros
EMPTY_CELL = "*"

## Developer-defined variables
adjacent_cells = [(-1, 0), (0, -1), (0, 1), (1, 0)]

## The flow-free function
def flow_free(input_text_path):
    print(">> flow_free")

    ## Convert text data in the input path to a char array
    char_array = text2array(input_text_path)
    # print(char_array)

    ## Apply the forced-move algorithm
    char_array = forced_move(char_array)
    # print(char_array)

    ## Write char array data to the output solution based on the input text path
    output_solution_path = array2text(char_array, input_text_path)
    # print("|Solution path:", output_solution_path)

    print("<< flow_free")
    return output_solution_path

def text2array(input_text_path):
    print(" >> text2array")

    ## Open the output text to read and write data
    input_text = open(input_text_path, "r+")
    text_lines = input_text.readlines()
    input_text.close()

    ## Calculate the board size (grid size)
    global board_size
    board_size = len(text_lines)
    # print(" |Board size:", board_size)

    ## Create an output array to store input text data
    output_array = np.chararray([board_size, board_size])
    for index, text_line in enumerate(text_lines):
        output_array[index] = list(text_line.strip())

    print(" << text2array")
    return output_array

def array2text(input_array, input_text_path):
    print(" >> array2text")

    ## Create a output solution path based on the input text path
    output_solution_path = os.path.splitext(input_text_path)[0] + "_solution.txt"
    output_solution_path = output_solution_path.replace("text", "solution")

    ## Open the output solution to read and write data
    output_solution = open(output_solution_path, "w+")

    ## Write input array data to the output solution
    for i in range(board_size):
        input_array[i].tofile(output_solution, sep = "", format = "%s")
        output_solution.write("\n")

    output_solution.close()

    print(" >> array2text")
    return output_solution_path

def forced_move(input_array):
    print(" >> forced_move")

    ## Create cell and solved cell lists
    cells = [(y, x) for y in range(board_size) for x in range(board_size)]
    solved_cells = []

    ## Loop until no forced move is found
    while True:
        ## Create a list to store indexes of solved cells in the cell list
        solved_indexes = []

        ## Query all cells in the cell list
        for index, cell in enumerate(cells):
            ## Check the current cell is a color cell
            if EMPTY_CELL != input_array[cell[0]][cell[1]].decode("utf-8"):
                ## Create an available move list and a check variable
                moves = []
                is_solved = False

                ## The current cell is already solved
                if cell in solved_cells:
                    solved_indexes.insert(0, index)
                    continue

                # Create adjacent cells of the current cell
                for adjacent_cell in adjacent_cells:
                    # Update the adjacent cell position based on the current cell position
                    adjacent_cell = (cell[0] + adjacent_cell[0], cell[1] + adjacent_cell[1])

                    # Check the adjacent cell position within the puzzle board's range
                    if 0 <= adjacent_cell[0] < board_size and 0 <= adjacent_cell[1] < board_size:
                        # Check the adjacent cell is an empty cell
                        if EMPTY_CELL == input_array[adjacent_cell[0]][adjacent_cell[1]].decode("utf-8"):
                            # Append the adjacent cell to the available move list
                            moves.append(adjacent_cell)

                        ## Check that the adjacent cell gets the same color as the current cell
                        ## But doesnt exist in the solved cell list. It means that color flow is already solved
                        if input_array[cell[0]][cell[1]] == input_array[adjacent_cell[0]][adjacent_cell[1]] and \
                           adjacent_cell not in solved_cells:
                            solved_cells.append(adjacent_cell)
                            is_solved = True

                ## The current cell has no available move, so it is solved
                if 0 == len(moves):
                    solved_indexes.insert(0, index)

                ## The current cell is not solved and has one available move (a forced move)
                if 1 == len(moves) and is_solved == False:
                    # print(" |Forced move", input_array[cell[0]][cell[1]].decode("utf-8"), \
                    #       "from", cell, "to", moves[0])
                    ## Copy the current cell color to the forced move cell
                    input_array[moves[0][0]][moves[0][1]] = input_array[cell[0]][cell[1]]
                    solved_indexes.insert(0, index)

        # print(len(cells), len(solved_indexes))
        ## No forced move is found
        if 0 == len(solved_indexes): break

        ## Pop solved cells from the cell list to the solved cell list
        for index in solved_indexes:
            if cells[index] not in solved_cells:
                solved_cells.append(cells[index])
            cells.pop(index)
        # print(len(solved_cells))

    print(" << forced_move")
    return input_array
