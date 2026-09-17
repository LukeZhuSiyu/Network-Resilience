
import matplotlib.pyplot as plt
import pylab
import types
import time
import math
import copy
import numpy
import random

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
def copy_graph(g):
    """
    Return a copy of the input graph, g

    Arguments:
    g -- a graph

    Returns:
    A copy of the input graph that does not share any objects.
    """
    return copy.deepcopy(g)

def upa(n, m):
    """
    Generate an undirected graph with n node and m edges per node
    using the preferential attachment algorithm.

    Arguments:
    n -- number of nodes
    m -- number of edges per node

    Returns:
    undirected random graph in UPAG(n, m)
    """
    g = {}
    if m <= n:
        g = make_complete_graph(m)
        for new_node in range(m, n):
            # Find <=m nodes to attach to new_node
            totdeg = float(total_degree(g))
            nodes = list(g.keys())
            probs = []
            for node in nodes:
                probs.append(len(g[node]) / totdeg)
            mult = distinct_multinomial(m, probs)

            # Add new_node and its random neighbors
            g[new_node] = set()
            for idx in mult:
                node = nodes[idx]
                g[new_node].add(node)
                g[node].add(new_node)
    return g            

def erdos_renyi(n, p):
    """
    Generate a random Erdos-Renyi graph with n nodes and edge probability p.

    Arguments:
    n -- number of nodes
    p -- probability of an edge between any pair of nodes

    Returns:
    undirected random graph in G(n, p)
    """
    g = {}

    ### Add n nodes to the graph
    for node in range(n):
        g[node] = set()

    ### Iterate through each possible edge and add it with 
    ### probability p.
    for u in range(n):
        for v in range(u+1, n):
            r = random.random()
            if r < p:
                g[u].add(v)
                g[v].add(u)

    return g


def total_degree(g):
    """
    Compute total degree of the undirected graph g.

    Arguments:
    g -- undirected graph

    Returns:
    Total degree of all nodes in g
    """
    return sum(map(len, g.values()))

def make_complete_graph(num_nodes):
    """
    Returns a complete graph containing num_nodes nodes.
 
    The nodes of the returned graph will be 0...(num_nodes-1) if num_nodes-1 is positive.
    An empty graph will be returned in all other cases.
 
    Arguments:
    num_nodes -- The number of nodes in the returned graph.
 
    Returns:
    A complete graph in dictionary form.
    """
    result = {}
         
    for node_key in range(num_nodes):
        result[node_key] = set()
        for node_value in range(num_nodes):
            if node_key != node_value: 
                result[node_key].add(node_value)
 
    return result

def distinct_multinomial(ntrials, probs):
    """
    Draw ntrials samples from a multinomial distribution given by
    probs.  Return a list of indices into probs for all distinct
    elements that were selected.  Always returns a list with between 1
    and ntrials elements.

    Arguments:
    ntrials -- number of trials
    probs   -- probability vector for the multinomial, must sum to 1

    Returns: 
    A list of indices into probs for each element that was chosen one
    or more times.  If an element was chosen more than once, it will
    only appear once in the result.  
    """
    ### select ntrials elements randomly
    mult = numpy.random.multinomial(ntrials, probs)

    ### turn the results into a list of indices without duplicates
    result = [i for i, v in enumerate(mult) if v > 0]
    return result

def read_graph(filename):
    """
    Read a graph from a file.  The file is assumed to hold a graph
    that was written via the write_graph function.

    Arguments:
    filename -- name of file that contains the graph

    Returns:
    The graph that was stored in the input file.
    """
    with open(filename) as f:
        g = eval(f.read())
    return g


def _plot_dict_line(d, label=None):
    """
    Plot data in the dictionary d on the current plot as a line.

    Arguments:
    d     -- dictionary
    label -- optional legend label

    Returns:
    None
    """
    xvals, yvals = _dict2lists(d)
    if label:
        pylab.plot(xvals, yvals, label=label)
    else:
        pylab.plot(xvals, yvals)

def _dict2lists(data):
    """
    Convert a dictionary into a list of keys and values, sorted by
    key.  

    Arguments:
    data -- dictionary

    Returns:
    A tuple of two lists: the first is the keys, the second is the values
    """
    xvals = list(data.keys())
    xvals.sort()
    yvals = []
    for x in xvals:
        yvals.append(data[x])
    return xvals, yvals

def plot_lines(data, title, xlabel, ylabel, labels=None, filename=None):
    """
    Plot a line graph with the provided data.

    Arguments: 
    data     -- a list of dictionaries, each of which will be plotted 
                as a line with the keys on the x axis and the values on
                the y axis.
    title    -- title label for the plot
    xlabel   -- x axis label for the plot
    ylabel   -- y axis label for the plot
    labels   -- optional list of strings that will be used for a legend
                this list must correspond to the data list
    filename -- optional name of file to which plot will be
                saved (in png format)

    Returns:
    None
    """
    ### Check that the data is a list
    if not isinstance(data, list):
        msg = "data must be a list, not {0}".format(type(data).__name__)
        raise TypeError(msg)

    ### Create a new figure
    fig = pylab.figure()

    ### Plot the data
    if labels:
        mylabels = labels[:]
        for _ in range(len(data)-len(labels)):
            mylabels.append("")
        for d, l in zip(data, mylabels):
            _plot_dict_line(d, l)
        # Add legend
        pylab.legend(loc='best')
        gca = pylab.gca()
        legend = gca.get_legend()
        pylab.setp(legend.get_texts(), fontsize='medium')
    else:
        for d in data:
            _plot_dict_line(d)

    ### Set the lower y limit to 0 or the lowest number in the values
    mins = [min(l.values()) for l in data]
    ymin = min(0, min(mins))
    pylab.ylim(ymin=ymin)

    ### Label the plot
    pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)

    ### Draw grid lines
    pylab.grid(True)

    ### Show the plot
    fig.show()

    ### Save to file
    if filename:
        pylab.savefig(filename)

def random_attack(g):
    """
    removing nodes randomly to perform random attack on graph g 
    
    Arguments:
    g -- graph as dictionary
    
    Returns:
    the largest connected component size after the attack
    """
    graph = copy_graph(g)
    nodes = list(graph.keys())
    num_node=len(nodes)
    #record the largest connected component before the attack as first element
    largest_comp = [compute_largest_cc_size(graph)]
    #repeat until 20% of node is removed
    while len(nodes)>=0.8*num_node:
        removal=random.choice(nodes)
        nodes.remove(removal)
        graph[removal]={}
        for node in graph.keys():
            if removal in graph[node]:
                graph[node].remove(removal)
        #push the new largest connected component size to the list
        largest_comp.append(compute_largest_cc_size(graph))
    return largest_comp

def targeted_attack(g):
    """
    removing most-connected nodes to perform targeted attack on graph g 
        
    Arguments:
    g -- graph as dictionary
        
    Returns:
    the largest connected component size after the attack
    """
    graph = copy_graph(g)
    nodes = list(graph.keys())
    num_node=len(nodes)
    #record the largest connected component before the attack as first element
    largest_comp = [compute_largest_cc_size(graph)]
    sorted_nodes = sorted(graph, key=lambda node: len(graph[node]), reverse=True)
    #repeat until 20% of node is removed
    while len(nodes)>=0.8*num_node:
        removal=sorted_nodes.pop(0)
        nodes.remove(removal)
        graph[removal]={}
        for node in graph.keys():
            if removal in graph[node]:
                graph[node].remove(removal)
        #push the new largest connected component size to the list
        largest_comp.append(compute_largest_cc_size(graph))
    return largest_comp

#sample test code
graph=read_graph("rf7.repr")
#set the number of node n to 1200 so that these graphs have the same number of node,
#make p=2m/n, m=2 so that these graphs have approximately the same degree for each node
graph_upa=upa(1200,2)
graph_erdos=erdos_renyi(1200,0.0034)
graph_random = dict(zip(range(1, len(graph.keys()) + 1), random_attack(graph)))
graph_target = dict(zip(range(1, len(graph.keys()) + 1), targeted_attack(graph)))
upa_random = dict(zip(range(1, len(graph.keys()) + 1), random_attack(copy_graph(graph_upa))))
upa_target = dict(zip(range(1, len(graph.keys()) + 1), targeted_attack(copy_graph(graph_upa))))
erdos_random = dict(zip(range(1, len(graph.keys()) + 1), random_attack(copy_graph(graph_erdos))))
erdos_target = dict(zip(range(1, len(graph.keys()) + 1), targeted_attack(copy_graph(graph_erdos))))
plot_lines([graph_random,graph_target,upa_random,upa_target,erdos_random,erdos_target],
"size of largest connected component as function of number of nodes removed",
"'nodes removed","size of largest connected component",
["graph_random","graph_target","upa_random","upa_target","erdos_random","erdos_target"],"plot")

plt.show()

