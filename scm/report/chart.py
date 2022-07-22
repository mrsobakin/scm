from io import StringIO

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import scm.consts
import scm.report

# TODO:
# [?] 1. Local object for plot
# [ ] 2. Optimize
# [*] 3. Plot ALL metrics


def plot_metrics(module, knowledge_area):
    sns.set_theme(style="whitegrid")

    metrics = module.get_multimetrics() # TODO: get_child_metrics

    df = metrics.element.df.merge( 
        pd.DataFrame( {
            "id": module.elements_order, 
            "order": range(len(module.elements_order)),
            "name": [ str(element.element_id)+("*" if element.is_advanced else "") for element in scm.utils.sublist(module.elements, module.elements_order) ]
            }
        ),
        how="outer"
    ).sort_values("order")

    svgs = {}
    for metric in metrics.element.metrics.values():
        fig, ax = plt.subplots()

        minmax = scm.consts.metrics_minmax[knowledge_area].get(metric.id, (0, 1))


        heights = df[metric.id].apply(lambda x: x.value)
        
        max_height = heights.max()
        if pd.isna(max_height): max_height = max(minmax)
        
        heights = heights.fillna(max_height)

        sns.barplot(
            ax = ax,
            x = df["name"], 
            y = heights, 
            order = df["name"],
            edgecolor = "black",
            linewidth = 1
        )
        
        for i, bar in enumerate(ax.patches):
            element = module.elements[module.elements_order[i]]
            if pd.notna( df[metric.id].iloc[i].value ):
                
                bar.set(facecolor = scm.report.get_fill_color(bar.get_height(), metric.id, knowledge_area))
                
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() * 0.2, 
                    df[metric.id].iloc[i].sample, 
                    ha='center', 
                    va='bottom', 
                    color='black'
                )
            else:
                bar.set(color = scm.consts.chart_disabled)
                if element.element_type != "task":
                    ax.text(
                        bar.get_x() + bar.get_width() / 2, 
                        bar.get_height() / 2, 
                        scm.consts.emojis[element.element_type], 
                        ha='center', 
                        va='center'
                    )

        ax.axhline(
            minmax[1], 
            linestyle = "--",
            color = "k"
        )
        
        
        direction = -1 if (minmax[1] > minmax[0]) else 1
        ax.annotate(
            "",
            xytext = (
                len(ax.patches)-0.5, 
                minmax[1] + 0.00000001 * direction
                #           ^ Yes. It works.
            ),
            xy = (
                len(ax.patches)-0.5, 
                minmax[1]
            ),
            arrowprops=dict(facecolor='black', linewidth=0, width=2)
        )
        
        ax.set_title(metric.name, loc='left')
        fig.set_size_inches(scm.consts.chart_size)
        ax.tick_params(axis="x", labelrotation=45)
        ax.set(xlabel=None, ylabel=None)

        io = StringIO()
        with plt.rc_context({'svg.fonttype': 'none'}):
            fig.savefig(io, format="svg", bbox_inches='tight')

        plt.close(fig)

        svgs[metric.id] = io.getvalue()

    return svgs
