"""
A simple national energy system modelled as a dependency graph.

Structure:
  oil_supply
      └── fuel_produced     (oil_supply × efficiency)
              └── energy_output   (fuel_produced × energy_per_unit)
              └── emissions       (fuel_produced × emission_factor)
                      └── carbon_tax  (emissions × tax_rate)

We run three scenarios:
  Baseline   — current values
  Scenario A — oil supply drops 20% (supply shock)
  Scenario B — emission factor cut 30% (cleaner technology)
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from graph_engine import Node, DependencyGraph


def build_graph():
    """Build and return the energy dependency graph."""
    g = DependencyGraph()

    # ── Input nodes (no dependencies)
    oil_supply      = g.add(Node("oil_supply"))        # million barrels
    efficiency      = g.add(Node("efficiency"))        # fraction
    energy_per_unit = g.add(Node("energy_per_unit"))   # GJ per unit fuel
    emission_factor = g.add(Node("emission_factor"))   # tonnes CO2 per unit fuel
    tax_rate        = g.add(Node("tax_rate"))           # $ per tonne CO2

    # ── Computed nodes
    fuel_produced = g.add(Node(
        "fuel_produced",
        inputs=[oil_supply, efficiency],
        fn=lambda oil, eff: oil * eff
    ))

    energy_output = g.add(Node(
        "energy_output",
        inputs=[fuel_produced, energy_per_unit],
        fn=lambda fuel, epj: fuel * epj
    ))

    emissions = g.add(Node(
        "emissions",
        inputs=[fuel_produced, emission_factor],
        fn=lambda fuel, ef: fuel * ef
    ))

    carbon_tax = g.add(Node(
        "carbon_tax",
        inputs=[emissions, tax_rate],
        fn=lambda em, tr: em * tr
    ))

    return g


def set_baseline(g):
    """Set baseline input values."""
    g.nodes["oil_supply"].set(100.0)
    g.nodes["efficiency"].set(0.85)
    g.nodes["energy_per_unit"].set(6.0)
    g.nodes["emission_factor"].set(0.25)
    g.nodes["tax_rate"].set(50.0)
    g.compute_all()


def run_scenarios():
    print("=" * 56)
    print("  Energy System — Dependency Graph Scenario Analysis")
    print("=" * 56)

    # ── Baseline ──────────────────────────────────────
    g = build_graph()
    set_baseline(g)
    g.snapshot("Baseline")
    baseline = g.fork()

    # ── Scenario A: oil supply drops 20% ──────────────
    print("\n  Scenario A: oil supply drops 20% (supply shock)")
    g.update("oil_supply", 80.0)   # was 100, now 80
    g.snapshot("Scenario A")
    scenario_a = g.fork()

    # ── Scenario B: cleaner tech — emissions factor -30% ─
    print("\n  Scenario B: cleaner technology (emission factor -30%)")
    set_baseline(g)                           # reset to baseline first
    g.update("emission_factor", 0.175)        # was 0.25, now 0.175
    g.snapshot("Scenario B")
    scenario_b = g.fork()

    return baseline, scenario_a, scenario_b


def make_figure(baseline, scenario_a, scenario_b):
    metrics = ["fuel_produced", "energy_output", "emissions", "carbon_tax"]
    labels  = ["Fuel\nProduced", "Energy\nOutput", "Emissions", "Carbon\nTax"]
    x = np.arange(len(metrics))
    w = 0.26

    b_vals = [baseline[m]   for m in metrics]
    a_vals = [scenario_a[m] for m in metrics]
    c_vals = [scenario_b[m] for m in metrics]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.patch.set_facecolor('#0f1117')

    BLUE   = '#4FC3F7'
    ORANGE = '#FFB74D'
    GREEN  = '#81C784'

    def style_ax(ax, title, ylabel):
        ax.set_facecolor('#1a1d27')
        ax.tick_params(colors='#aaaaaa', labelsize=9)
        ax.set_ylabel(ylabel, color='#cccccc', fontsize=10)
        ax.set_title(title, color='white', fontsize=11, fontweight='bold', pad=8)
        for sp in ax.spines.values():
            sp.set_edgecolor('#333344')
        ax.grid(True, linestyle='--', alpha=0.2, color='#555566', axis='y')

    # Panel 1: absolute values across scenarios
    ax1 = axes[0]
    ax1.bar(x - w, b_vals, width=w, color=BLUE,   alpha=0.85, label='Baseline')
    ax1.bar(x,     a_vals, width=w, color=ORANGE, alpha=0.85, label='Scenario A: -20% oil')
    ax1.bar(x + w, c_vals, width=w, color=GREEN,  alpha=0.85, label='Scenario B: -30% emissions factor')
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels, fontsize=9)
    ax1.legend(fontsize=8, labelcolor='#cccccc', facecolor='#22253a', edgecolor='#333344')
    style_ax(ax1, "Scenario Comparison — All Metrics", "Value (model units)")

    # Panel 2: % change from baseline
    ax2 = axes[1]
    a_delta = [(a - b) / b * 100 for a, b in zip(a_vals, b_vals)]
    c_delta = [(c - b) / b * 100 for c, b in zip(c_vals, b_vals)]
    ax2.bar(x - w/2, a_delta, width=w, color=ORANGE, alpha=0.85, label='Scenario A vs Baseline')
    ax2.bar(x + w/2, c_delta, width=w, color=GREEN,  alpha=0.85, label='Scenario B vs Baseline')
    ax2.axhline(0, color='white', lw=0.6, alpha=0.4)
    ax2.set_xticks(x)
    ax2.set_xticklabels(labels, fontsize=9)
    ax2.legend(fontsize=8, labelcolor='#cccccc', facecolor='#22253a', edgecolor='#333344')
    style_ax(ax2, "% Change from Baseline\n(propagated through dependency graph)", "% Change")

    fig.suptitle(
        "Dependency Graph Scenario Analysis — Energy System\n"
        "Upstream changes automatically propagate through dependent nodes",
        color='white', fontsize=12, fontweight='bold', y=1.01
    )

    plt.tight_layout()
    out = '/mnt/user-data/outputs/scenario_graph_results.png'
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#0f1117')
    plt.close()
    print(f"\n  Figure saved.")


if __name__ == "__main__":
    baseline, scenario_a, scenario_b = run_scenarios()
    make_figure(baseline, scenario_a, scenario_b)

    print("\n\nKey result:")
    print(f"  Scenario A (-20% oil): emissions drop from "
          f"{baseline['emissions']:.1f} to {scenario_a['emissions']:.1f} "
          f"({(scenario_a['emissions']-baseline['emissions'])/baseline['emissions']*100:.1f}%)")
    print(f"  Scenario B (-30% emission factor): emissions drop from "
          f"{baseline['emissions']:.1f} to {scenario_b['emissions']:.1f} "
          f"({(scenario_b['emissions']-baseline['emissions'])/baseline['emissions']*100:.1f}%)")
    print(f"\n  Carbon tax impact:")
    print(f"    Baseline:   ${baseline['carbon_tax']:.1f}")
    print(f"    Scenario A: ${scenario_a['carbon_tax']:.1f}")
    print(f"    Scenario B: ${scenario_b['carbon_tax']:.1f}")
