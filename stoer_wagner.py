def stoer_wagner(G, min_partition_fraction=0.05, verbose=False):
    best_cut = (float("inf"), None, None)
    g = G.copy()

    total_vol = sum(d["weight"] for u, v, d in G.edges(data=True)) * 2
    min_vol = min_partition_fraction * total_vol
    n_phases = g.number_of_nodes() - 1

    if verbose:
        print(f"starting: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
        print(f"total_vol={total_vol:.2f}, min_vol={min_vol:.2f}\n")

    for node in g.nodes():
        g.nodes[node]["merged"] = {node}
        g.nodes[node]["vol"] = sum(d["weight"] for _, _, d in g.edges(node, data=True))

    phase = 0
    while g.number_of_nodes() > 1:
        phase += 1
        cut_weight, s, t = _phase(g)

        vol_t = g.nodes[t]["vol"]
        vol_s = total_vol - vol_t
        passes = min(vol_t, vol_s) >= min_vol

        if passes:
            score = cut_weight / min(vol_t, vol_s)
            is_best = score < best_cut[0]
            if is_best:
                side_t = g.nodes[t]["merged"].copy()
                side_s = set(G.nodes()) - side_t
                best_cut = (score, side_s, side_t)
        else:
            score = None
            is_best = False

        if verbose:
            status = "BEST" if is_best else ("skip" if not passes else "    ")
            print(f"phase {phase:>4}/{n_phases}  "
                  f"nodes={g.number_of_nodes():>4}  "
                  f"cut={cut_weight:>8.2f}  "
                  f"vol_t={vol_t:>8.2f}  "
                  f"{status}")

        _merge(g, s, t)

    if verbose:
        _, sa, sb = best_cut
        print(f"\ndone. best partition: {len(sa)} / {len(sb)}")

    return best_cut[1], best_cut[2]


def _phase(g):
    start = next(iter(g.nodes()))
    in_A = {start}
    key = {n: 0.0 for n in g.nodes()}

    for _, nbr, data in g.edges(start, data=True):
        key[nbr] = data.get("weight", 1.0)

    order = [start]
    remaining = set(g.nodes()) - {start}

    while remaining:
        v = max(remaining, key=lambda n: key[n])
        remaining.remove(v)
        order.append(v)
        in_A.add(v)

        for _, nbr, data in g.edges(v, data=True):
            if nbr not in in_A:
                key[nbr] += data.get("weight", 1.0)

    t = order[-1]
    s = order[-2]
    return key[t], s, t


def _merge(g, s, t):
    for nbr in list(g.neighbors(t)):
        if nbr == s:
            continue
        w = g[t][nbr].get("weight", 1.0)
        if g.has_edge(s, nbr):
            g[s][nbr]["weight"] += w
        else:
            g.add_edge(s, nbr, weight=w)

    g.nodes[s]["merged"] = g.nodes[s]["merged"] | g.nodes[t]["merged"]
    g.nodes[s]["vol"] += g.nodes[t]["vol"]
    g.remove_node(t)