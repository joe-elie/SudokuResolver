import extracter
import solver

def solve(im):
    # Pre process (remove noise, treshold image, get contours)
    pre_processed = extracter.preProcess(im)

    # Find corners based on the biggest contour
    corners = extracter.findCorners(pre_processed)

    # Fix the perspective based on the 4 corners found
    sudoku = fixPerspective(pre_processed, corners)

    # Match a grid to the image
    squares = grid(sudoku)

    # Convert to int
    squares_int = [[tuple(int(x) for x in tup) for tup in square] for square in squares]

    im_squares = cv.cvtColor(sudoku.copy(), cv.COLOR_GRAY2RGB)

    # Get individual cells 
    cells = extractCells(sudoku, squares_int)

    # Get each digit 
    extractedCells = []
    for cell in cells:
        h, w = cell.shape[:2]
        margin = int(np.mean([h, w]) / 2.5)
        _, bbox, seed = findLargestConnectedComponent(cell, [margin, margin], [w - margin, h - margin])
        extractedCells.append(extractDigit(cell, bbox, 28))

    # Get matrix by using CNN to recognize digits
    sudoku = readSudoku(extractedCells)
    print("Extracted sudoku :")
    print(sudoku)

    # Resolve sudoku
    resolved = sudoku.copy()
    solver.solveSudoku(resolved)