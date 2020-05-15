
def earliest_ancestor(ancestors, starting_node):
    vertices = {}

    def add_relationship(pair):
        for node in pair:
            add_vertex(node)
        add_edge(*pair)

    def add_vertex(v):
        if v not in vertices:
            vertices[v] = set()

    def add_edge(ancestor, child):
        vertices[child].add(ancestor)
    # populate our graph
    for pair in ancestors:
        add_relationship(pair)
    oldest_ancestor = -1
    max_length = 0
    if not len(vertices[starting_node]):
        return oldest_ancestor
    visited = set()
    stack = []
    current = starting_node
    # until stack is empty and current has no unvisited neighbours
    stack.append(starting_node)
    while len(stack):
        # visit current vertex if it wasn't visited
        if current not in visited:
            visited.add(current)
        # look for unvisited neihgbours
        unvisited_neighbours = [
            v for v in vertices[current] if v not in visited]
        if unvisited_neighbours:
            # If it has an unvisited neighbour, push current vertex on stack, make neighbour current
            stack.append(current)
            current = unvisited_neighbours[0]
        else:
            # If it has no unvisited neighbors, pop off stack and set as current
            if len(stack) >= max_length:
                # do depth first traversal of the graph
                # each time we have to go back, compare against max length
                # if bigger, put current ancestor as oldest
                oldest_ancestor = current
                max_length = len(stack)
            current = stack.pop()
    return oldest_ancestor