** part of my application for RO297 **
# Dependency Graph Scenario Analysis

This project is a small prototype exploring how **dependency graphs can be used for scenario analysis**.

In many scientific, engineering, and policy models, outputs depend on multiple upstream inputs. When one parameter changes, all downstream quantities must be recomputed. This project demonstrates a simple way to represent those relationships using a graph structure.

---

## Idea

Each quantity in the model is represented as a **node in a graph**.

Some nodes are **inputs** (for example oil supply), while others are **computed from upstream nodes**.

Example structure:
oil_supply
↓
fuel_produced
↓
energy_output
↓
emissions
↓
carbon_tax

When an upstream value changes, the graph automatically recomputes all dependent nodes.

---

## Example Model

The example models a simplified national energy system.

Relationships:

- **Fuel produced** depends on oil supply and efficiency
- **Energy output** depends on fuel produced
- **Emissions** depend on fuel produced and emission intensity
- **Carbon tax** depends on emissions and a tax rate

The script runs three scenarios:

**Baseline**  
Current system parameters.

**Scenario A — Supply shock**  
Oil supply decreases by 20%.

**Scenario B — Cleaner technology**  
Emission factor decreases by 30%.

The outputs of each scenario are compared using a simple visualization.

---

## Files

### `graph_engine.py`

Implements a minimal dependency graph system:

- `Node`
- `DependencyGraph`
- automatic recomputation of dependent nodes when inputs change

### `energy_model_example.py`

Demonstrates how the dependency graph can be used to run scenario analysis on a simplified energy system model.

---

## Purpose

This project was built as a small learning prototype to explore:

- dependency graphs
- propagation of updates through computational models
- scenario comparison using simple simulations

The implementation is intentionally minimal and focuses on illustrating the core idea rather than building a full modeling framework.

---

## Running the Example

```bash
python energy_model_example.py