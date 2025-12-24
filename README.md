# 0.py
Takes a csv file of agroculture related Yahoo Finance tickers from one directory back and outputs s1_values.csv and violation_pct.csv. s1_values.csv contains Date, PairA (ticker), PairB (second ticker), and S1. violations_pct.csv contains Date, ViolationsPct (ViolationCounts/Total Pairs), Total Pairs, and ViolationCounts.

S1 is defined as $\begin{equation}\notag S_1= \mathbb{E}(a,b)+\mathbb{E}(a,b')+\mathbb{E}(a',b)-\mathbb{E}(a',b') \end{equation}$ with expectations calculated as the average sign product $\begin{equation}\notag  \mathbb{E}(a,b)=\frac{\sum_{i\in w}a_ib_im_i}{\sum_{i\in w}m_i}\end{equation}$ and $m_i$ being masks.

0.py calculates percent change for adjusted returns (returns) of Yahoo Finance tickers in a given date range. Then, it creates rolling windows of 20 trading days. Within these windows, expectations as calculated as aboce and summed to find the S1 value with the masked defined such that $\mathbb{E}(a,b)$ corresponds to dates where both Ticker A and Ticker B have returns greater than the fixed threshold of 0.05. This mask is then negated to calculate the other terms. For example, $\mathbb{E}(a',b')$ corresponds to dates where both Ticker A and Ticker B have returns less than the fixed threshold of 0.05. The $S_1$ values are then saved as well as the violation percent defined as the number of $S_1$ values greater than 2 on a given day.
# 1.py
Requires violation_pct.csv from 0.py as input and outputs Results/volatility_traces, Figures/Established_Methods_&_S1_matplotlib.png, and Figures/Established_Methods_&_S1.html. It calculates rolling volatility, GARCH volatility, and regime switching volatility for the S&P GSCI. The S&P GSCI is a weighted commodity futures index of 24 physically delivered futures contracts. It is comprised of Brent Crude Oil, West Texas Intermediate (WTI) Crude Oil, Heating Oil, RBOB Gasoline, Gasoil, Natural Gas, Aluminum, Copper, Nickel, Lead, Zinc, Gold, Silver, Corn, Soybeans, Chicago Wheat, Kansas Wheat, Cotton, Sugar, Coffee, Cocoa, Live Cattle, Feeder Cattle, and Lean Hogs. WTI is weighted at approximately 25%, Brent Crude at 18%, Corn at 5%, and Live Cattle at 4%. The rolling volatility is calculated as the standard deviation of a rolling window of 20 days times $\sqrt{252}$ to annualize the daily voltaility. GARCH(1,1) is calculated using the python arch_models package and similarly annualized. The equation for GARCH(1,1) is $\begin{equation}\notag \sigma _t^2=\omega+\alpha_1 \epsilon_{t-1}^2+\beta _1 \sigma^2_{t-1} \end{equation}$. For more details, see the documentation at https://arch.readthedocs.io/en/stable/univariate/introduction.html.

All of these are then plotted along with $S_1$ violation percentage defined as in 0.py. Thresholds for period classification are displayed on the html output plot. One can select Percentiles, StdDev, Absolute, or All. The output png only displays a threshold for the 95th percentile. 
# 2.py
Requires s1_values.csv from 0.py and outputs undirected networks for each day in s1_values.csv in Results/networks and Figures/networks. The number of nodes in the networks are held constant at the total number of 54 tickers used to create s1_values.csv. The condition for an edge is the $S_1$ value between two tickers be greater than 2. The equation for density is

$\begin{equation}\notag
d = \frac{2m}{n(n-1)}
\end{equation}$

where $m$ is the number of edges and $n$ is the number of nodes. Giant component size is calculated as the number of nodes in the largest connected component divided by the total number of nodes

$\begin{equation}\notag
\mathcal{G} = \frac{\max_i |C_i|}{|N|}
\end{equation}$

where $|C_i|$ denotes the number of nodes in a connected component $C_i$. The average clustering coefficient is calculated as

$\begin{equation}\notag
C = \frac{1}{n} \sum_{v \in G} c_v
\end{equation}$

where $c_v$ is the local clustering coefficient of node $v$. The global clustering coefficient, or transitivity, is calculated as the fraction of all possible triangles present in $G$. Global efficiency is calculated as the average of the inverse shortest path lengths between all pairs of nodes in the largest connected component

$\begin{equation}\notag
E(G) = \frac{1}{n(n-1)} \sum_{i \ne j \in G} \frac{1}{d(i,j)}
\end{equation}$

where $d(i,j)$ is the shortest path length between nodes $i$ and $j$. The average shortest path length is the mean distance between all node pairs in the largest connected component

$\begin{equation}\notag
L(G) = \frac{1}{n(n-1)} \sum_{i \ne j \in G} d(i,j)
\end{equation}$

and the diameter is the maximum of these shortest path lengths. Degree centralization measures the extent to which a single node dominates the network in terms of degree and is defined as

$\begin{equation}\notag
C_D = \frac{\sum_{i=1}^{n} (k_{\max} - k_i)}{(n-1)(n-2)}
\end{equation}$

where $k_i$ is the degree of node $i$ and $k_{\max}$ is the maximum degree observed in the network. Betweenness centralization captures how unequally betweenness centrality is distributed among nodes and is calculated as

$\begin{equation}\notag
C_B = \frac{\sum_{i=1}^{n} (b_{\max} - b_i)}{(n-1)(n-2)}
\end{equation}$

where $b_i$ is the betweenness centrality of node $i$ and $b_{\max}$ is its maximum value in the network. Modularity is calculated using the greedy modularity optimization algorithm and is defined as

$\begin{equation}\notag
Q = \frac{1}{2m} \sum_{i,j} \left[A_{ij} - \frac{k_i k_j}{2m}\right] \delta(c_i, c_j)
\end{equation}$

where $A_{ij}$ is the adjacency matrix, $k_i$ is the degree of node $i$, and $\delta(c_i, c_j)$ equals 1 if nodes $i$ and $j$ belong to the same community and 0 otherwise. Community size entropy quantifies the heterogeneity of community sizes as

$\begin{equation}\notag
H = -\sum_{i} p_i \log(p_i)
\end{equation}$

where $p_i$ is the fraction of nodes in community $i$. The number of communities is given by the total count of detected clusters. The assortativity coefficient measures the Pearson correlation between the degrees of connected nodes and is given by

$\begin{equation}\notag
r = \frac{\sum_{ij} (A_{ij} - \frac{k_i k_j}{2m}) k_i k_j}{\sum_{ij} (k_i \delta_{ij} - \frac{k_i k_j}{2m}) k_i k_j}
\end{equation}$

The scale-free exponent $\alpha$ is estimated by fitting a power-law distribution to the node degree sequence using the method of moments

$\begin{equation}\notag
P(k) \propto k^{-\alpha}
\end{equation}$

Node-level metrics are computed for all 54 nodes as follows: Degree ($k_i$): The number of edges connected to node $i$.

$\begin{equation}\notag
k_i = \sum_j A_{ij}
\end{equation}$

Clustering coefficient ($c_i$): The fraction of node $i$’s neighbors that are also connected to each other.

$\begin{equation}\notag
c_i = \frac{2e_i}{k_i(k_i - 1)}
\end{equation}$

where $e_i$ is the number of edges between the neighbors of node $i$. Betweenness centrality ($b_i$): The fraction of all shortest paths between pairs of nodes that pass through node $i$.

$\begin{equation}\notag
b_i = \sum_{s \ne i \ne t} \frac{\sigma_{st}(i)}{\sigma_{st}}
\end{equation}$

where $\sigma_{st}$ is the total number of shortest paths from node $s$ to node $t$, and $\sigma_{st}(i)$ is the number of those paths passing through $i$. Closeness centrality ($c_i^{(close)}$): The inverse of the average shortest path distance from node $i$ to all other nodes.

$\begin{equation}\notag
c_i^{(close)} = \frac{n-1}{\sum_{j} d(i,j)}
\end{equation}$

Eigenvector centrality ($x_i$): A measure of node influence based on the principle that connections to highly connected nodes contribute more to a node’s score.

$\begin{equation} \notag
x_i = \frac{1}{\lambda} \sum_j A_{ij} x_j
\end{equation}$

where $\lambda$ is the largest eigenvalue of the adjacency matrix $A$.
All node-level results are saved to Results/networks, and network visualizations are output to Figures/networks.
# 2Bootstrap.py
Requires Results/volatility_traces/regime_vol.csv and Results/networks and outputs to Results/event_tables. Periods of time at least 40 trading days in length and with regime switching volaility greater than 40% are identified as extreme and compared to the normal periods directly preceding them. These events correspond to the 2008 Financial Crisis (Event 1), COVID-19 (Event 2), and Ukraine War (Event 3). The daily network metrics for these periods of time are averaged and compared and a bootstrap procedure is used to calculate 95% confidence intervals for the metrics. The boostrap algorithm is as follows:
For each metric $ m \in \text{metrics} $:
All non-NaN values of that metric are extracted as

$\begin{equation}\notag
\text{arr} = \text{values\_df}[m].\text{dropna()}
\end{equation}$

The observed mean is calculated as

$\begin{equation}\notag
\text{obs} = \frac{1}{n} \sum_{i=1}^{n} \text{arr}_i
\end{equation}$

where n is the number of available observations for metric m .

Bootstrap resampling is then performed. For each of $ n_{\text{iter}} $ iterations, 
a random sample with replacement of size n is drawn from $\text{arr}$, 
and its mean is stored in $\text{boot\_means}[i]$.

Confidence bounds are computed as percentile values of the bootstrap distribution:

$\begin{equation}\notag
\text{lo} = \text{percentile}(\text{boot\_means}, 100 \times \tfrac{\alpha}{2})
\end{equation}$

$\begin{equation}\notag
\text{med} = \text{percentile}(\text{boot\_means}, 50)
\end{equation}$

$\begin{equation}\notag
\text{hi} = \text{percentile}(\text{boot\_means}, 100 \times (1 - \tfrac{\alpha}{2}))
\end{equation}$

where $ \alpha $ denotes the significance level, typically $ \alpha = 0.05 $.
# 3.py
Requires Results/volatility_traces/regime_vol.csv and Results/networks and outputs Figures/event_tables and Results/event_tables. For each metric, the null hypothesis is that both samples come from the same distribution Extreme and normal blocks are first identified from the volatility trace Results/volatility_traces/regime_vol.csv. Blocks where volatility exceeds a fixed threshold are labeled as extreme. Each extreme block is then paired with its immediately preceding normal block. Network metrics corresponding to those date ranges are loaded from Results/networks. For each paired period and each metric, the observed difference in means is computed as

$\begin{equation}
\notag
\Delta_{\text{obs}} = \bar{x} - \bar{y}
\end{equation}$

where $\bar{x}$ and $\bar{y}$ denote the sample means of the extreme and normal periods, respectively. To assess statistical significance, a permutation test is performed. Combine all observations into a single pooled sample of size

$\begin{equation}
\notag
n = n_x + n_y
\end{equation}$

Randomly permute the pooled values. Split the permuted sample into two groups of sizes $n_x$ and $n_y$. Compute the permuted difference in means

$\begin{equation}
\notag
\Delta^{(k)} = \bar{x}^{(k)} - \bar{y}^{(k)}
\end{equation}$

Repeat the procedure for $N_{\text{perm}} = 100{,}000$ permutations to form a null distribution. The two-sided p-value is then calculated as

$\begin{equation}
\notag
p = \frac{\#\{\,|\Delta^{(k)}| \geq |\Delta_{\text{obs}}|\,\} + 1}{N_{\text{perm}} + 1}
\end{equation}$

The smaller the p-value, the less likely it is that the observed difference arose by chance under the null hypothesis. For each metric, Cohen’s d is also computed to quantify the standardized effect size:

$\begin{equation}
\notag
d = \frac{\bar{x} - \bar{y}}{s_p}
\end{equation}$

where

$\begin{equation}
\notag
s_p = \sqrt{\frac{(n_x - 1)s_x^2 + (n_y - 1)s_y^2}{n_x + n_y - 2}}
\end{equation}$

and $s_x^2$ and $s_y^2$ are the sample variances of each group. After computing raw p-values for all metrics, Benjamini--Hochberg false discovery rate (FDR) correction is applied to obtain adjusted q-values:

$\begin{equation}
\notag
q_i = \min_{j \ge i} \left( \frac{m}{j} p_{(j)} \right)
\end{equation}$

where $p_{(j)}$ are the sorted p-values and m is the total number of tests. Metrics with p < 0.05 or q < 0.05 are highlighted as statistically significant in the output tables and figures saved to Figures/event_tables and Results/event_tables.

