import math
import operator

# global variables for bfs
bfs_PR = {}
bfs_M = {}
bfs_L = {}

# global variables for dfs
dfs_PR = {}
dfs_M = {}
dfs_L = {}
damping = 0.85


'''
    Given: a file name and a dictionary to store the in-links/out-links
    Effect: populates the given dictionary with the links extracted from the given file name.
'''
def get_links(file_name, dict):
    with open(file_name, 'r') as file:
        lines = file.readlines()                    # read file
        for l in lines:
            line = str(l).strip().split()           # strip line of end breaks and split
            dict[line[0]] = list(line[1:])          # first word is the key and rest are values


'''
    Given: a dictionary with link to out-links mapping
    Returns: a list of links that have no out-links
'''
def get_sink_links(outlink_dict):
    sinks = []                                      # stores sink links
    for page, olinks in outlink_dict.items():       # for each link to  out-links mapping
        if len(olinks) == 0:
            sinks.append(page)                      # add sink links
    return sinks


'''
    Given: a list of links and a dictionary to store page ranks
    Effect: initialises the page rank to 1/N for each link
'''
def initialise_PR(links, PR):
    N = len(links)                                  # number of unique links
    for l in links:
        PR[l] = 1/N                                 # initial PR value


'''
    Effect: initialises the global variables for bfs & dfs
'''
def initialise_dicts():
    global bfs_M, bfs_L, bfs_PR
    global dfs_M, dfs_L, dfs_PR
    get_links('bfs_inlinks_graph.txt', bfs_M)       # extract in-links from graph file
    get_links('bfs_outlinks_graph.txt', bfs_L)      # extract out-links from graph file
    bfs_P = bfs_M.keys()                            # get unique crawled links
    initialise_PR(bfs_P, bfs_PR)                    # initialise PR for each link

    get_links('dfs_inlinks_graph.txt', dfs_M)       # extract in-links from graph file
    get_links('dfs_outlinks_graph.txt', dfs_L)      # extract out-links from graph file
    dfs_P = dfs_M.keys()                            # get unique crawled links
    initialise_PR(dfs_P, dfs_PR)                    # initialise PR for each link


'''
    Given: a dictionary with page ranks and a list of unique links
    Returns: the perplexity value for all the links
'''
def compute_perplexity(PR, P):
    entropy = 0                                     # entropy sum
    for page in P:
        entropy += PR[page] * math.log2(PR[page])   # e = - sum(PR + lg(PR)
    entropy *= -1
    perplexity = 2**entropy                         # p = 2^e
    return perplexity


'''
    Given: a list of perplexities and a file name
    Effect: writes all the perplexity values to the given filename.
'''
def write_perplexities(list, file_name):
    with open(file_name, 'w') as outfile:
        for i in range(len(list)):
            outfile.write("Round %s" %i)
            outfile.write(" perplexity: %s\n" %list[i])


'''
    Given: a dictionary of in-links, out-links, page ranks, the dampening factor and a filename
    Returns: computes the page rank for each link.
'''
def compute_page_rank(M, L, PR, d, file_name):
    converge_count = 0                              # counts when page ranks are converged
    P = M.keys()                                    # unique links
    N = len(P)                                      # number of unique links
    perplexities = []                               # perplexity list
    perplexity = compute_perplexity(PR, P)          # initial perplexity
    S = get_sink_links(L)                           # sink links list
    # count = 0
    while converge_count < 4:                       # stop when PR has converged for 4 iterations
        perplexities.append(perplexity)             # add perplexity to perplexity list
        # print("Convergence: ",converge_count)
        newPR = {}                                  # dictionary to store new PR values
        sinkPR = 0
        for page in S:
            sinkPR += PR[page]                      # distributing the PR values for sink links
        # print("Sink PR: ",sinkPR)
        for page in P:                              # PR = (1 -d)/N + (d * sinkPR)/N + sum(d * PR(In-Links))
            newPR[page] = (1 - d)/N
            newPR[page] += (d * sinkPR)/N
            for q in M[page]:
                newPR[page] += d * (PR[q]/len(L[q]))
        for p in P:                                 # assign new PR values
            PR[p] = newPR[p]
        new_perplexity = compute_perplexity(PR, P)  # compute new perplexity
        change = abs(perplexity - new_perplexity)   # compute difference in old and new perplexity
        perplexity = new_perplexity                 # assign new perplexity value
        if change < 1:                              # increase convergence count if change less than one
            converge_count += 1
        else:
            converge_count = 0                      # else restart the counter
        # count += 1
        # if count > 3:
        #     break
    write_perplexities(perplexities, file_name)     # write the perplexities to a file
    return PR


'''
    Given: a dictionary for page ranks and a file name
    Effect: writes all the page rank values sorted in decreasing value to the given filename.
'''
def write_page_ranks(PR, file_name):
    sorted_PR = sorted(PR.items(), key = operator.itemgetter(1), reverse = True)
    with open(file_name, 'w') as outfile:
        for k, v in sorted_PR:
            outfile.write("%s : " %k)
            outfile.write("%s\n" %v)


'''
    Given: a dictionary for in-links
    Returns: a dictionary with the count of in-links for each link
'''
def get_inlink_count(M):
    count = {}                                      # stores the count of in-links
    for k, v in bfs_M.items():
        count[k] = len(v)
    return count

# main method
def main():
    global bfs_PR, bfs_L, bfs_M, dfs_PR, dfs_L, dfs_M
    initialise_dicts()
    bfs_page_rank_085 = compute_page_rank(bfs_M, bfs_L, bfs_PR, damping, 'bfs_perplexities_085.txt')
    dfs_page_rank_085 = compute_page_rank(dfs_M, dfs_L, dfs_PR, damping, 'dfs_perplexities_085.txt')
    bfs_page_rank_055 = compute_page_rank(bfs_M, bfs_L, bfs_PR, 0.55, 'bfs_perplexities_055.txt')
    dfs_page_rank_055 = compute_page_rank(dfs_M, dfs_L, dfs_PR, 0.55, 'dfs_perplexities_055.txt')

    write_page_ranks(bfs_page_rank_085, 'bfs_page_ranks_085.txt')
    write_page_ranks(dfs_page_rank_085, 'dfs_page_ranks_085.txt')
    write_page_ranks(bfs_page_rank_055, 'bfs_page_ranks_055.txt')
    write_page_ranks(dfs_page_rank_055, 'dfs_page_ranks_055.txt')

    bfs_inlink_count = get_inlink_count(bfs_M)
    dfs_inlink_count = get_inlink_count(dfs_M)
    bfs_top_inlinks = sorted(bfs_inlink_count.items(), key = operator.itemgetter(1), reverse = True)
    dfs_top_inlinks = sorted(dfs_inlink_count.items(), key = operator.itemgetter(1), reverse = True)
    with open('inlink_counts.txt', 'w') as outfile:
        outfile.write("BFS In-link Count:\n")
        for k, v in bfs_top_inlinks:
            outfile.write("%s : " %k)
            outfile.write("%s\n" %v)
        outfile.write("\nDFS In-link Count:\n")
        for k, v in dfs_top_inlinks:
            outfile.write("%s : " % k)
            outfile.write("%s\n" % v)


if __name__ == '__main__':
    main()


# Test Graph
'''  
inl = {}
inl['A'] = ['D', 'E', 'F']
inl['B'] = ['A', 'F']
inl['C'] = ['A', 'B', 'D']
inl['D'] = ['B', 'C']
inl['E'] = ['B', 'C', 'D', 'F']
inl['F'] = ['A', 'B', 'D']
oul = {}
oul['A'] = ['B', 'C', 'F']
oul['B'] = ['C', 'D', 'E', 'F']
oul['C'] = ['D', 'E']
oul['D'] = ['A', 'C', 'E', 'F']
oul['E'] = ['A']
oul['F'] = ['A', 'B', 'E']
pgrk = {}
initialise_PR(inl.keys(), pgrk)
ans = compute_page_rank(inl, oul, pgrk, 0.85, 'test_perplexity.txt')
sans = sorted(ans.items(), key = operator.itemgetter(1), reverse = True)
for k,v in sans:
    print(k," : ",v)
'''