#Generates timeseries of network metrics 
#Requires Results/networks from 2.py. Outputs Figures/network_metrics_timeseries.html

import os
import glob
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

METRICS_DIR = "Results/networks"
OUTPUT_HTML = "Figures/network_metrics_timeseries.html"
os.makedirs("Figures", exist_ok=True)

metric_files = sorted(glob.glob(os.path.join(METRICS_DIR, "*_metrics.csv")))

if not metric_files:
    raise FileNotFoundError("No *_metrics.csv files found in Results/networks")

dfs = []
for f in metric_files:
    df = pd.read_csv(f)
    dfs.append(df)

metrics_df = pd.concat(dfs, ignore_index=True)
metrics_df["Date"] = pd.to_datetime(metrics_df["Date"])
metrics_df = metrics_df.sort_values("Date").reset_index(drop=True)

metrics = [
    "NumNodes","NumEdges","Density","GiantComponentSizePct","AvgClusteringCoeff",
    "GlobalClustering","Efficiency","AvgShortestPathLength","Diameter",
    "DegreeCentralization","BetweennessCentralization","Modularity",
    "CommunitySizeEntropy","NumCommunities","Assortativity","ScaleFreeAlpha"
]

metrics = [m for m in metrics if m in metrics_df.columns]

rows = len(metrics)
fig = make_subplots(rows=rows, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    subplot_titles=metrics)

for i, metric in enumerate(metrics, start=1):
    fig.add_trace(
        go.Scatter(
            x=metrics_df["Date"],
            y=metrics_df[metric],
            mode="lines",
            name=metric,
            line=dict(width=2)
        ),
        row=i, col=1
    )

fig.update_layout(
    title=dict(
        text="Network Metrics Over Time",
        x=0.5,
        font=dict(size=18)
    ),
    showlegend=False,
    height=250 * len(metrics),
    template="plotly_white",
    margin=dict(l=60, r=20, t=60, b=60)
)

for i in range(1, len(metrics) + 1):
    fig.update_xaxes(showticklabels=True, title_text="Date", row=i, col=1)


fig.write_html(OUTPUT_HTML)
print(f"Saved interactive dashboard to {OUTPUT_HTML}")
