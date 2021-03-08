import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
SAINE=0
CYTO=100
PROLI=100

MORT=20
#BLEU = VIVANT, ROUGE = PROLI et CYTO ,BLEU CLAIR = MORT
vals = [SAINE, CYTO,PROLI, MORT]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N * N, p=[0.996, 0.002,0.002,0]).reshape(N, N)
def update(frameNum, img, grid, N):

    newGrid = grid.copy()
    for i in range(2,N-1):
        for j in range(2,N-1):

            newGrid[i,j]= grid[i,j]
            if (grid[i,j]==MORT):
                if ((grid[i-1,j]==PROLI) or (grid[i+1,j]==PROLI) or (grid[i,j-1]==PROLI) or (grid[i,j+1]==PROLI) or (grid[i-1,j-1]==PROLI)
                or (grid[i-1,j+1]==PROLI) or (grid[i+1,j+1]==PROLI) or (grid[i+1,j-1]==PROLI)):
                    newGrid[i,j]=PROLI

            if ((grid[i,j]== SAINE) or (grid[i,j]==PROLI)):
                if ((grid[i - 1, j]==CYTO) or (grid[i+1, j]==CYTO) or (grid[i, j-1]==CYTO )or (grid[i, j+1]==CYTO )or (grid[i-1, j-1]==CYTO)
                or (grid[i - 1, j + 1] ==CYTO) or (grid[i + 1, j + 1] ==CYTO) or (grid[i + 1, j - 1] ==CYTO)) :
                    newGrid[i,j]=MORT

                # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    # Command line arg’s are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # set animation update interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)


    grid = np.array([])


    grid = randomGrid(N)

    # set up animation
    fig, ax = plt.subplots()
    assert isinstance(ax.imshow, object)
    img = ax.imshow(grid,cmap=cm.jet, interpolation='nearest') #Montre l'image
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # # of frames?
    # set output file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# call main
if __name__ == '__main__':
    main()



