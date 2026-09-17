
from collections import *

def compute_largest_cc_size(g: dict) -> int:
    """
    Find the size of largest connected component of a given graph
    
    Arguments:
    g -- a graph as dictionary
    
    Returns:
    size of largest connected component
    """
    traverse=set()
    nodes=g.keys()
    largest_com=0
    for node in nodes:
        #skip code already traversed
        if node in traverse:
            continue
        queue=[]
        queue.append(node)
        traverse.add(node)
        comp=0
        #use BFS to reach all connected node
        while len(queue)!=0:
            current=queue.pop(0)
            comp+=1
            for neighbor in g[current]:
                if neighbor not in traverse:
                    queue.append(neighbor)
                    traverse.add(neighbor)

        if comp>=largest_com:
            largest_com=comp

    return largest_com