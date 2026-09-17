analysis.py analyze a graph of the measured network topology of an Internet Service Provider(rf7.repr) by removing 20% of nodes using random attack and targeted attack. 
To show comparison, it also generated two random graph using Undirected Preferential Attachment(UPA) and Erdős–Rényi, and remove 20% of nodes in each using random attack and targeted attack.
After each removal of node, the size of largest connected component of each graph is computed and stored. 
Finally, the size of largest connected component as function of number of nodes removed is shown by using matplotlib.pyplot.

test.py is used to test the correctness of computing largest connected component size of a graph.
