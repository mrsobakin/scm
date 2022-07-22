
import itertools
from collections import defaultdict

import pandas as pd


first_or_none = lambda x: next(iter(x), None)


def collapse_columns(df, keep, name, f):
    df = df.copy()
    
    # TODO: KOSTYL to preserve column types.
    df = df.astype("O")

    df[name] = df.apply(f, axis=1)

    df = df[keep + [name]]

    return df


def collapse_and_group(df, id_name, comb_name, func, agg_func=list):
    df = collapse_columns(df, [id_name], comb_name, func)

    df = df.groupby(id_name).agg(agg_func)

    return df


def dict_from_list(lst, key):
    return { getattr(e, key): e for e in lst }


def chain_element(itr, element):
    for e in itr:
        yield e
    yield element


def filter_nan(itr):
    return (e for e in itr if not pd.isna(e))


def dict_keys_map(dct, f):
    return { f(k): v for k,v in dct.items() }


def get_column(lst, i):
    return ( row[i] for row in lst )


# TODO: replace with better toposort
def calc_graph_sum_in_edges(edges_list): 
    in_edges = defaultdict(list)    
    out_edges = defaultdict(list)

    for edge in edges_list:
        out_edges[ edge.from_module_id ].append( edge.to_module_id )
        in_edges[ edge.to_module_id ].append( edge.from_module_id )

    next_nodes = []
    for node in out_edges.keys() - in_edges.keys():
        next_nodes.append(node)

    nodes_before = defaultdict(set)
    
    while next_nodes:
        next_node = next_nodes.pop(0)
        
        nodes_before[ next_node ].update( in_edges[ next_node ] )
        for in_node in in_edges[ next_node ]:
            nodes_before[ next_node ].update( nodes_before[ in_node ] )

        nodes_before[ next_node ].update( nodes_before[ next_node ] )

        next_nodes.extend( out_edges[ next_node ] )

    return { node: len(in_nodes) for node, in_nodes in nodes_before.items() }
        

def sort_nodes(edges_list):
    nodes_path_len = calc_graph_sum_in_edges(edges_list)

    extension_edges = {}
    for edge in edges_list:
        if edge.type == "extension":
            extension_edges[edge.from_module_id] = edge.to_module_id

    nodes = []
    for node in get_column(sorted(nodes_path_len.items(), key=lambda x: x[1]), 0):
        if node in extension_edges.values():
            continue

        nodes.append(node)

        if node in extension_edges:
            nodes.append(extension_edges[node])
    
    return nodes


def sublist(itr, ind_lst):
    return ( itr[i] for i in ind_lst)


def color_to_hex(c):
    return "#%02x%02x%02x" % c


def color_lerp(x, c1, c2):
    return tuple( ( int( (1-x)*comp1+x*comp2 ) for comp1, comp2 in zip(c1, c2) ) )


def multiple_colors_lerp(x, colors):
    bigx = x*(len(colors)-1)
    i = int(bigx)
    
    if i >= len(colors)-1: return colors[-1]
    
    return color_lerp(bigx%1, colors[i], colors[i+1])


def normalize_minmax(x, minmax):
    return (x-minmax[0]) / (minmax[1]-minmax[0])


def clip_to_1(x):
    return max(0, min(1, x))
