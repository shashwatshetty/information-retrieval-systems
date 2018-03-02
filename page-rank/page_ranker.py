import math

bfs_PR = {}
bfs_M = {}
bfs_L = {}

dfs_PR = {}
dfs_M = {}
dfs_L = {}
damping = 0.85


def get_links(file_name, dict):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for l in lines:
            line = str(l).strip().split()
            dict[line[0]] = list(line[1:])

def get_sink_links(outlink_dict):
    sinks = []
    for page, olinks in outlink_dict.items():
        if len(olinks) == 0:
            sinks.append(page)
    return sinks

def initialise_PR(links, PR):
    N = len(links)
    for l in links:
        PR[l] = 1/N

def initialise_dicts():
    global bfs_M, bfs_L, bfs_PR
    global dfs_M, dfs_L, dfs_PR
    get_links('bfs_inlinks_graph.txt', bfs_M)
    get_links('bfs_outlinks_graph.txt', bfs_L)
    bfs_P = bfs_M.keys()
    initialise_PR(bfs_P, bfs_PR)

    get_links('dfs_inlinks_graph.txt', dfs_M)
    get_links('dfs_outlinks_graph.txt', dfs_L)
    dfs_P = dfs_M.keys()
    initialise_PR(dfs_P, dfs_PR)


def compute_perplexity(PR, P):
    entropy = 0
    for page in P:
        entropy += PR[page] * math.log2(PR[page])
    entropy *= -1
    perplexity = 2**entropy
    return perplexity


def compute_page_rank(M, L, PR, d):
    converge_count = 0
    P = M.keys()
    N = len(P)
    perplexity = compute_perplexity(PR, P)
    S = get_sink_links(L)
    while converge_count < 4:
        #print("Convergence: ",converge_count)
        newPR = {}
        sinkPR = 0
        for page in S:
            sinkPR += PR[page]
        #print("Sink PR: ",sinkPR)
        for page in P:
            newPR[page] = (1 - d)/N
            newPR[page] += (d * sinkPR)/N
            for q in M[page]:
                newPR[page] += d * (PR[q]/len(L[q]))
        for p in P:
            PR[p] = newPR[p]
        new_perplexity = compute_perplexity(PR, P)
        change = abs(perplexity - new_perplexity)
        perplexity = new_perplexity
        if change < 1:
            converge_count += 1
        else:
            converge_count = 0
    return PR
