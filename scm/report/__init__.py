import json

import numpy as np
import pandas as pd
import dominate
from dominate.tags import *

import scm.report.graph
import scm.report.chart
import scm.consts


def get_fill_color(x, metric_id, knowledge_area_id):
    if metric_id not in scm.consts.metrics_minmax[knowledge_area_id]:
        return scm.consts.default_color
    
    minmax = scm.consts.metrics_minmax[knowledge_area_id][metric_id]
    return scm.utils.color_to_hex(
        scm.utils.multiple_colors_lerp(
            scm.utils.clip_to_1(
                scm.utils.normalize_minmax(
                    x, 
                    minmax
                )
            ),
            scm.consts.fillcolors
        ) 
    )


def _render_value_td(metric_result, metric_id=None, knowledge_area=None, color=True):
    kwargs = {}
    
    if pd.notna(metric_result.sample):
        kwargs["tooltip"] = f"Количество учеников: {metric_result.sample}"
    
    if color:
        kwargs["style"] = "background: " + get_fill_color(metric_result.value, metric_id, knowledge_area)
    
    
    if pd.notna(metric_result.value):
        td(
            f"{metric_result.value:.2f}".rstrip('0').rstrip('.'),
            **kwargs
        )
    else:
        td(_class="nan-cell")

def _render_metric_header_th(metric):
    th(
        metric.name, 
        tooltip = metric.description,
        _class = "have-tooltip"
    )


def from_course(course):
    metrics = course.get_multimetrics()

    ## TODO: remove; some metrics CAN calc info for advanced modules
    
    isadv = {}
    for module in course.modules.values():
        isadv.update( { element.id: element.is_advanced for element in module.elements.values() } )
    
    for _, row in metrics.element.df.iterrows():
        if isadv[row["id"]]:
            for cell in row[1:]:
                cell.value = np.nan


    isadv = {}
    for module in course.modules.values():
        isadv[module.id] = module.is_advanced
    
    for _, row in metrics.module.df.iterrows():
        if isadv[row["id"]]:
            for cell in row[1:]:
                cell.value = np.nan
                
    ##

    metrics.element.df.set_index("id", drop=False, inplace=True)
    metrics.module.df.set_index("id", drop=False, inplace=True)
    metrics.course.df.set_index("id", drop=False, inplace=True)
    
    module_order = scm.utils.sort_nodes( course.graph )

    course_graph = scm.report.graph.draw_graph(course)
    course_graphs_map = { 
        module.id: scm.report.graph.draw_graph(course, bold=True, draw_labels=False, selected_node = module.id) 
            for module in course.modules.values() 
    }
    
    charts = { module.id: scm.report.chart.plot_metrics(module, course.knowledge_area_id) for module in course.modules.values() }

    doc = dominate.document(title="Report")

    with doc.head:
        meta(charset="utf-8")
        style().add_raw_string("""
            table, th, td {
              border: 1px solid #b6afac;
              border-collapse: collapse;
            }

            th, td {
                padding: 5px;
            }
            
            th {
                text-align: right;
            }

            select {
                font-size: 18px;            
            }

            td {
                text-align: center;
                vertical-align: middle;
            }
            
            caption {
                text-align: left;
            }
            
            .nan-cell {
                background-image:url("data:image/svg+xml,<svg version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' width='100%' height='100%' xml:space='preserve'><defs><pattern id='stripePattern' patternTransform='rotate(45 0 0)' patternUnits='userSpaceOnUse' height='10' width='5'><line x1='0' y1='0' x2='0' y2='10' style='stroke:rgb(192,192,192); stroke-width:4'></line></pattern></defs><rect fill='url(%23stripePattern)' width='100%' height='100%'/></svg>");
                /* background: #d3d3d3; */
            }
            
            .have-tooltip {
                cursor: help;
            }
            
            .minimap-container {
                padding-left: 24px;
                width: 300px;
                height: 300px;
            }
            
            .minimap-container > svg {
                width: 100%;
                height: 100%;
            }
            
            [tooltip] .tooltip {
                position: fixed;
                margin: 8px;
                padding: 8px;
                border: 1px solid black;
                background: white;
                
                pointer-events: none;
                visibility: hidden;
                opacity: 0;
                transition: opacity 0.2s, visibility 0.2s;
                font-weight: normal;
            }

            [tooltip]:hover .tooltip {
                visibility: visible;
                opacity: 1;
            }
            
            """)
        script(type='text/javascript').add_raw_string("""
window.onload = function() {
    var svg = document.getElementById("course_graph_svg_container").getElementsByTagName("svg")[0];

    svg.insertAdjacentHTML("afterbegin", "<style>.node:hover { filter: drop-shadow(0px 0px 5px rgba(0, 0, 0, 0.25)); }</style>");

    svg.insertAdjacentHTML("afterbegin", "<defs><pattern id=\\"stripePattern\\" patternTransform=\\"rotate(45 0 0)\\" patternUnits=\\"userSpaceOnUse\\" height=\\"10\\" width=\\"5\\"><line x1=\\"0\\" y1=\\"0\\" x2=\\"0\\" y2=\\"10\\" style=\\"stroke:rgb(192,192,192); stroke-width:4\\"></line></pattern></defs>");

    document.getElementById("graph_metric_select").value = "none";

    renderTooltips();
}

function renderTooltips() {
    Array.from(document.querySelectorAll("[tooltip]")).forEach( (element) => {
        let tooltip = document.createElement("div");
        tooltip.classList.add("tooltip");
        tooltip.innerText = element.getAttribute("tooltip");
        element.appendChild(tooltip);

        element.onmousemove = (e) => {
            tooltip.style.left = e.clientX + 'px'
            tooltip.style.top = e.clientY + 'px';
        };
    } ); 
}

function colorLerp(x, c1, c2) {
    return "#"+c1.map( (component1, i) => {
        var component = Math.round(component1*(1-x)+c2[i]*x);
            return component.toString(16).padStart(2, "0");
    } ).join("");
}

function multiColorLerp(x, colors) {
    var bigx = x*(colors.length-1);
    var i = Math.floor(bigx);
    if(i >= (colors.length-1)) return colorLerp(1, colors[colors.length-1], colors[colors.length-1]);
    return colorLerp(bigx%1, colors[i], colors[i+1]);
}

function normalizeMinMax(x, min, max) {
    return (x-min)/(max-min);
}

function clipTo1(x) {
    return Math.max(0, Math.min(1, x));
}

function colorCourseGraphSvg(svg, colors) {
    Object.entries(colors).forEach( ([id, color]) => {
        var nodeBase = svg.getElementById( id );
        var nodeShape = ( nodeBase.getElementsByTagName("ellipse")[0] || nodeBase.getElementsByTagName("polygon")[0] );
        
        nodeShape.style.fill = color;
    } );
}

function changeGraphMetric(metricId) {
    var metricRow = document.getElementById(metricId+"_row");
    var idRow = document.getElementById("modules_metrics").rows[0];

    
    var nodeColors = {};

    for(var i=1; i<idRow.cells.length; i++) {
        var moduleId = idRow.cells[i].textContent.replace(/\\D+/g, '');
        var metricVal = metricRow.cells[i].innerText;

        var minmax = metricsMinMaxes[metricId];
        if(minmax) {
            var style = metricVal ? multiColorLerp(clipTo1(normalizeMinMax(metricVal, minmax[0], minmax[1])), fillColors) : "url(#stripePattern)";
        
            nodeColors[moduleId] = style;
        } else {
            nodeColors[moduleId] = "#ffffff";
        }
    }
    
    var bigCourseGraphSvg = document.getElementById("course_graph_svg_container").getElementsByTagName("svg")[0];
    colorCourseGraphSvg(bigCourseGraphSvg, nodeColors);
    
    document.querySelectorAll(".minimap-container").forEach( (container) => {
        colorCourseGraphSvg(
            container.getElementsByTagName("svg")[0],
            nodeColors
        );
    } );
}

var metricsMinMaxes = """ + json.dumps(scm.consts.metrics_minmax[course.knowledge_area_id]) + "; var fillColors = " + json.dumps(scm.consts.fillcolors))

    with doc:
        with h1(course.course_name, style="display: inline"):
            a(
                scm.consts.emojis["link"], 
                href = f"{scm.consts.base_url}/{course.id}",
                target="_blank"
            )
        br()
        br()

        with table(id="course_info"):
            with tr():
                th("Область знаний")
                td(scm.consts.knowledge_areas[course.knowledge_area_id])
            
            with tr():
                th("Дата открытия")
                td(course.date_start)

            with tr():
                th("Дата закрытия")
                td(course.close_date)

            for infometric in metrics.course.info_metrics.values():
                with tr():
                    _render_metric_header_th(infometric)
                    _render_value_td(metrics.course.df.loc[course.id][infometric.id], color=False)

        br()
        
        with table(id="course_metrics"):
            caption("Метрики курса")
            with tr():
                th("Метрика")
                th("Значение")
            
            for metric in metrics.course.metrics.values():
                with tr():
                    _render_metric_header_th(metric)
                    _render_value_td(
                        metrics.course.df[metric.id][course.id], 
                        metric.id, 
                        course.knowledge_area_id
                    )

        br()

        with table(id="modules_metrics"):
            caption("Метрики модулей")

            with tr():
                th("Модуль")
                for module in scm.utils.sublist(course.modules, module_order):
                    level_indicator = ("*" if module.is_advanced else "")
                    td( 
                        a(
                            f"{module.id}{level_indicator}", 
                            href=f"#module_info_{module.id}"
                        ) 
                    )
            
            for metric in metrics.module.metrics.values():
                with tr(id=f"{metric.id}_row"):
                    _render_metric_header_th(metric)
                    for module_id in module_order:
                        _render_value_td(
                            metrics.module.df.loc[module_id][metric.id], 
                            metric.id, 
                            course.knowledge_area_id
                        )
        
        br()

        with div(id="course_graph"):

            with select(id="graph_metric_select", onchange="changeGraphMetric(this.value);"):
                option("Выберите метрику...", value="none", hidden=True, selected=True)
                for metric in metrics.module.metrics.values():
                    option( metric.name, value=metric.id )

            div(id="course_graph_svg_container").add_raw_string(course_graph)
            
            
        with div(id="modules_infos_section"):
            for module in scm.utils.sublist(course.modules, module_order):
                # TODO replace with something like `get_child_metrics`
                elements_metrics = module.get_multimetrics().element

                with div(id=f"module_info_{module.id}"):
                    a("[↑]", style="display: inline", href="#modules_metrics")

                    level_indicator = ("*" if module.is_advanced else "")
                    with h2(f"{module.id}. {module.title}{level_indicator}", style="display: inline"):
                        a(
                            scm.consts.emojis["link"], 
                            href = f"{scm.consts.base_url}/{course.id}/{module.id}",
                            target="_blank"
                        )

                    br()
                    br()

                    with div(style="display: flex;"):
                        with div():
                            with table():
                                for infometric in module.metrics.info_metrics.values():
                                    with tr():
                                        _render_metric_header_th(infometric)
                                        _render_value_td( metrics.module.df.loc[module.id][infometric.id], color=False )
                                        # render_value_td

                            br()

                            with table():
                                caption("Метрики модуля")
            
                                with tr():
                                    th("Метрика")
                                    th("Значение")

                                for metric in module.metrics.metrics.values():
                                    with tr():                            
                                        _render_metric_header_th(metric)
                                        _render_value_td(
                                            metrics.module.df.loc[module.id][metric.id], 
                                            metric.id, 
                                            course.knowledge_area_id
                                        )

                            br()
                        with div():
                            div(_class="minimap-container").add_raw_string( course_graphs_map[module.id] )
            
                    br()

                    with table():
                        caption("Метрики элементов")
                        with tr():
                            th("Элемент")
                            for element in scm.utils.sublist(module.elements, module.elements_order):
                                level_indicator = ("*" if element.is_advanced else "")                             
                                with td():
                                    a(
                                        f"{element.element_id}{level_indicator}",
                                        href = f"{scm.consts.base_url}/{course.id}/{module.id}/{element.element_type}_{element.element_id}",
                                        target="_blank"
                                    )
                                
                        metrics_iter = iter(elements_metrics.metrics.values())
                        rows_total = len(elements_metrics.metrics.values())
                        
                        if rows_total > 0:
                            metric = next(metrics_iter)
                            with tr():
                                _render_metric_header_th(metric)
                                
                                for element in scm.utils.sublist(module.elements, module.elements_order):
                                    if element.element_type == "task":
                                        _render_value_td(
                                            metrics.element.df.loc[element.id][metric.id], 
                                            metric.id, 
                                            course.knowledge_area_id
                                        )
                                    else:
                                        td(scm.consts.emojis[element.element_type], rowspan=rows_total)

                            for metric in metrics_iter:
                                with tr():
                                    _render_metric_header_th(metric)
                                    
                                    for element in scm.utils.sublist(module.elements, module.elements_order):
                                        if element.element_type != "task": continue
                                        
                                        _render_value_td(
                                            metrics.element.df.loc[element.id][metric.id], 
                                            metric.id, 
                                            course.knowledge_area_id
                                        )

                    br()
                    
                    with div():
                        for chart in charts[module.id].values():                       
                            with div() as svg_container:
                                svg_container.add_raw_string(chart)
        
        h1("Описание метрик")
        
        for metric_type, metric_type_name in zip(["course", "module", "element"], ["Курс", "Модуль", "Элемент"]):
            for metric_info in ["metrics"]:
                metrics_dct = getattr(getattr(metrics, metric_type), metric_info)
                
                br()
                with table():
                    caption(metric_type_name)
                    
                    with tr(id=f"{metric.id}_description_row"):
                        th("Метрика", style="text-align: center;")
                        th("Описание", style="text-align: center;")
                        
                    for metric in metrics_dct.values():
                        with tr():
                            td(metric.name, style="text-align: left;")
                            td(metric.description, style="text-align: left;")
            

    return doc
