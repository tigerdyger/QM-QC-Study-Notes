"""Reproduce the section 7.3 figures: python figures/07-03-oscillator.py.

Requires Python 3, NumPy >= 2, and Matplotlib >= 3.8.
All plotted coordinates and functions are dimensionless. Outputs are written
beside this script; no textbook images or external data are used.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def oscillator_state(n, y):
    """Normalized Hermite function, evaluated by its stable recurrence."""
    previous = np.pi ** (-0.25) * np.exp(-y * y / 2)
    if n == 0:
        return previous
    current = np.sqrt(2) * y * previous
    for j in range(1, n):
        previous, current = current, (
            np.sqrt(2 / (j + 1)) * y * current
            - np.sqrt(j / (j + 1)) * previous
        )
    return current


def verify_states():
    y = np.linspace(-14, 14, 40001)
    for n in (0, 1, 2, 3, 11):
        state = oscillator_state(n, y)
        assert np.isclose(np.trapezoid(state**2, y), 1, atol=1e-9)
        assert np.allclose(state[::-1], (-1) ** n * state, atol=1e-12)
        assert np.isclose(
            np.trapezoid(y**2 * state**2, y), n + 0.5, atol=1e-9
        )
    for n, m in ((0, 2), (1, 2)):
        assert abs(np.trapezoid(oscillator_state(n, y) * oscillator_state(m, y), y)) < 1e-9
    right = y[y >= 0]
    assert np.isclose(np.trapezoid(2 * oscillator_state(1, right)**2, right), 1, atol=1e-9)


def make_figures():
    output = Path(__file__).resolve().parent
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                         "axes.spines.right": False, "savefig.dpi": 220})
    teal, red = "#16756b", "#b63c48"
    y = np.linspace(-4.5, 4.5, 1801)
    fig, axes = plt.subplots(2, 2, figsize=(8, 4.8), sharex=True, sharey=True,
                             constrained_layout=True)
    for n, ax in enumerate(axes.flat):
        ax.axhline(0, color="0.65", lw=0.7)
        ax.axvline(0, color="0.85", lw=0.7)
        ax.plot(y, oscillator_state(n, y), color=teal, lw=1.8)
        ax.set(title=rf"$n={n}$", xlim=(-4.5, 4.5), ylim=(-0.85, 0.85))
        ax.set_xlabel(r"$y=x/b$")
        ax.set_ylabel(r"$\chi_n(y)$")
    fig.savefig(output / "07-03-eigenfunctions.png")
    plt.close(fig)

    q = np.linspace(-1.6, 1.6, 2401)
    classical_q = np.linspace(-0.995, 0.995, 2001)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.1), sharey=True,
                             constrained_layout=True)
    for n, ax in zip((0, 11), axes):
        turning_point = np.sqrt(2 * n + 1)
        density = turning_point * oscillator_state(n, turning_point * q)**2
        ax.axvspan(-1.6, -1, color="0.94")
        ax.axvspan(1, 1.6, color="0.94")
        ax.plot(q, density, color=teal, lw=1.6, label="Quantum")
        ax.plot(classical_q, 1 / (np.pi * np.sqrt(1 - classical_q**2)),
                "--", color=red, lw=1.4, label="Classical")
        ax.set(title=rf"$n={n}$", xlim=(-1.6, 1.6), ylim=(0, 2.35),
               xlabel=r"$q=x/x_{\rm turn}$")
        ax.legend(loc="upper center", fontsize=9, frameon=False)
    axes[0].set_ylabel("Probability density in q")
    fig.savefig(output / "07-03-classical-limit.png")
    plt.close(fig)


if __name__ == "__main__":
    verify_states()
    make_figures()
    print("Normalization, parity, moments, overlaps, and half-axis norm verified.")
