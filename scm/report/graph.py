
from pygraphviz import AGraph
import pandas as pd

from collections import defaultdict


def _draw_vertex(module_id, course_graph_dot, graph_layout, base_url, advanced=False, level=False, penwidth=1, draw_labels=False):
    pos = graph_layout[module_id]
    x, y = pos["x"], pos["y"]
    x, y = x/120, -y/120

    pos = f'{x},{y}!'

    size = '0.35' if level else '0.7'

    course_graph_dot.add_node(
        str(module_id),
        id = str(module_id), 
        label = str(module_id) if draw_labels else "",
        href = base_url+str(module_id),
        style = 'filled', 
        fontsize = '12.0', 
        fixedsize = 'true',
        penwidth = 1*penwidth,
        width = size,
        height = size, 
        fillcolor = "white" if not level else "#ffffffcc", 
        shape = "ellipse" if not advanced else "pentagon",
        pos = pos
    )


def _draw_edges(course_graph_dot, edges_in, penwidth):
    for y, xs in edges_in.items():
        for x, type in xs:
            if type=="extension": continue
            course_graph_dot.add_edge(str(x), str(y), color='black', penwidth=1.*penwidth, arrowhead="normal" )



def draw_graph(course, bold=False, draw_labels=False, selected_node=None):
    penwidth = 1.5 if bold else 1
    
    course_graph_dot = AGraph(directed=True)
    course_graph_dot.graph_attr.update(dpi='72.0')

    edges_in = defaultdict(list)

    for edge in course.graph:
        edges_in[ edge.to_module_id ].append( ( edge.from_module_id, edge.type ) )

    for i in course.graph_layout.keys():
        is_selected = i==selected_node
        
        _draw_vertex(
            i, 
            course_graph_dot, 
            course.graph_layout, 
            base_url = "#module_info_", 
            advanced = course.modules[i].is_advanced, 
            level = course.modules[i].level==2,
            penwidth = penwidth*4 if is_selected else penwidth,
            draw_labels = draw_labels
        )    


    # adding starting node
    for x in course.graph_layout.keys():
        if len(edges_in[int(x)]) == 0:
            edges_in[x].append( ( -1, "ordinary" ))

    course_graph_dot.add_node(str(-1), label='', style='filled', fillcolor="white", pos="0,0!")

    _draw_edges(course_graph_dot, edges_in, penwidth)


    course_graph_dot.layout()

    svg_bytes = course_graph_dot.draw(format="svg:svg:core")

    return svg_bytes.decode("utf-8")
