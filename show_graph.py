import pickle
from sys import argv

# Load pickle files

fig = pickle.load(open(argv[1], "rb"))
fig.show()
input()