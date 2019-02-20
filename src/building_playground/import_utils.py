import networkx as nx
from eppy.modeleditor import IDF

from building_playground.EpBunchWrapper import get_wrapper, EPBunchWrapperParent, matches

def idf_to_graph(fname1):
    idf = IDF(fname1)
    object_list = idf_to_object_list(idf)
    g = object_list_to_graph(object_list)
    return g

def idf_to_object_list(idf2):
    # produce a list of nicely wrapped objects
    object_list = []
    for key, value in idf2.idfobjects.items():
        print(key)
        for num, item in enumerate(value): # will not execute anyway if len(value)==0
            if len(value) == 1:
                fallback_name = ''
            else:
                fallback_name = '[' + str(num) + ']'

            object_list.append(get_wrapper(item, fallback_name))
    return object_list


def create_node_properties(x):
    props ={}
    if isinstance(x,str):
        props['viz'] = {'color': {'r': 0, 'g': 255, 'b': 0, 'a': 1.0}}
        props['key'] = ''
        props['name'] = x
    else:
        props['viz'] = {'color': {'r': 255, 'g': 0, 'b': 255, 'a': 1.0}}
        props['key'] = x.key
        props['name'] = x.name
    props['str'] = str(x)

    return props


def nice_short_string(name):
    if type(name) == tuple:
        return nice_short_string(name[0]) + '#' + nice_short_string(name[1])
    elif isinstance(name, EPBunchWrapperParent):
        return nice_short_string(name.key) + '#' + nice_short_string(name.name)
    elif type(name) == str:
        return name#name.replace(':', '@') # for some reason export to dot fails if I don't do this.
    else:
        raise ValueError("Can only handle tuples, strings, and EPBunchWrappers")


def object_list_to_graph(object_list):
    G = nx.DiGraph()
    for parent in object_list:
        parent_id = nice_short_string(parent)
        if parent_id not in G.node:
            # Add parent as graph node
            G.add_node(parent_id, **create_node_properties(parent))
        for fn, child_name in parent.references.items():
            if child_name == '': # empty names are null references
                continue
            # search for the child with that name
            for child_candidate in object_list:
                found = False
                # parent_name = make_nice(parent_name)
                if matches(child_name, child_candidate):
                    found = True
                    child = child_candidate
                    break
            if not found:
                assert(child_name != 'SPACE3-1')
                child = child_name
            child_id = nice_short_string(child)
            if child_id not in G.node:
                G.add_node(child_id, **create_node_properties(child))

            G.add_edge(parent_id, child_id, name=fn)
    return G