"""
Six-species non-equilibrium H/He chemistry and cooling network.

Species: HI, HII, HeI, HeII, HeIII, e-
Processes: collisional ionization, radiative + dielectronic recombination,
collisional excitation cooling, ionization cooling, recombination cooling,
and free-free (bremsstrahlung) cooling. No UV background (pure collisional).

Rate coefficients and cooling rates follow the standard fits compiled in
Katz, Weinberg & Hernquist (1996), ApJS 105, 19 (their Tables 1 and 2,
originally from Cen 1992 and Black 1981). All quantities are in cgs units.
"""

import numpy as np
from scipy.integrate import solve_ivp

# ----------------------------------------------------------------------
# Physical constants (cgs)
# ----------------------------------------------------------------------
k_B = 1.380649e-16      # erg/K
m_p = 1.67262192369e-24  # g
X_H = 0.76              # hydrogen mass fraction
Y_He = 1.0 - X_H        # helium mass fraction

# Floor values to keep the ODE system well-behaved
T_FLOOR = 1.0e3         # K
X_FLOOR = 1.0e-12       # minimum ionization fraction


# ----------------------------------------------------------------------
# Rate coefficients [cm^3 s^-1]  (KWH96 Table 2)
# ----------------------------------------------------------------------
def k_ci_HI(T):
    """Collisional ionization of HI by electrons."""
    return 5.85e-11 * np.sqrt(T) * np.exp(-157809.1 / T) \
        / (1.0 + np.sqrt(T / 1.0e5))


def k_ci_HeI(T):
    """Collisional ionization of HeI by electrons."""
    return 2.38e-11 * np.sqrt(T) * np.exp(-285335.4 / T) \
        / (1.0 + np.sqrt(T / 1.0e5))


def k_ci_HeII(T):
    """Collisional ionization of HeII by electrons."""
    return 5.68e-12 * np.sqrt(T) * np.exp(-631515.0 / T) \
        / (1.0 + np.sqrt(T / 1.0e5))


def alpha_HII(T):
    """Radiative recombination of HII."""
    return 8.4e-11 / np.sqrt(T) * (T / 1.0e3) ** -0.2 \
        / (1.0 + (T / 1.0e6) ** 0.7)


def alpha_HeII(T):
    """Radiative recombination of HeII."""
    return 1.5e-10 * T ** -0.6353


def alpha_d_HeII(T):
    """Dielectronic recombination of HeII."""
    return 1.9e-3 * T ** -1.5 * np.exp(-470000.0 / T) \
        * (1.0 + 0.3 * np.exp(-94000.0 / T))


def alpha_HeIII(T):
    """Radiative recombination of HeIII."""
    return 3.36e-10 / np.sqrt(T) * (T / 1.0e3) ** -0.2 \
        / (1.0 + (T / 1.0e6) ** 0.7)


# ----------------------------------------------------------------------
# Cooling rates [erg cm^-3 s^-1]  (KWH96 Table 1)
# Each function takes number densities in cm^-3 and returns a volumetric
# cooling rate. n_e is the electron number density.
# ----------------------------------------------------------------------
def cool_exc_HI(T, n_e, n_HI):
    """Collisional excitation of HI (Lyman-alpha)."""
    return 7.50e-19 * np.exp(-118348.0 / T) \
        / (1.0 + np.sqrt(T / 1.0e5)) * n_e * n_HI


def cool_exc_HeII(T, n_e, n_HeII):
    """Collisional excitation of HeII (n=2)."""
    return 5.54e-17 * T ** -0.397 * np.exp(-473638.0 / T) \
        / (1.0 + np.sqrt(T / 1.0e5)) * n_e * n_HeII


def cool_ci(T, n_e, n_HI, n_HeI, n_HeII):
    """Collisional ionization cooling (HI, HeI, HeII)."""
    common = 1.0 / (1.0 + np.sqrt(T / 1.0e5))
    c = 1.27e-21 * np.sqrt(T) * np.exp(-157809.1 / T) * common * n_e * n_HI
    c += 9.38e-22 * np.sqrt(T) * np.exp(-285335.4 / T) * common * n_e * n_HeI
    c += 4.95e-22 * np.sqrt(T) * np.exp(-631515.0 / T) * common * n_e * n_HeII
    return c


def cool_rec(T, n_e, n_HII, n_HeII, n_HeIII):
    """Recombination cooling (radiative + dielectronic)."""
    c = 8.70e-27 * np.sqrt(T) * (T / 1.0e3) ** -0.2 \
        / (1.0 + (T / 1.0e6) ** 0.7) * n_e * n_HII
    c += 1.55e-26 * T ** 0.3647 * n_e * n_HeII
    c += 3.48e-26 * np.sqrt(T) * (T / 1.0e3) ** -0.2 \
        / (1.0 + (T / 1.0e6) ** 0.7) * n_e * n_HeIII
    # dielectronic
    c += 1.24e-13 * T ** -1.5 * np.exp(-470000.0 / T) \
        * (1.0 + 0.3 * np.exp(-94000.0 / T)) * n_e * n_HeII
    return c


def cool_ff(T, n_e, n_HII, n_HeII, n_HeIII):
    """Free-free (bremsstrahlung) cooling."""
    g_ff = 1.1 + 0.34 * np.exp(-((5.5 - np.log10(T)) ** 2) / 3.0)
    return 1.42e-27 * g_ff * np.sqrt(T) * (n_HII + n_HeII + 4.0 * n_HeIII) * n_e


# ----------------------------------------------------------------------
# State helpers
#
# The state vector is y = [x_HII, x_HeII, x_HeIII, T]:
#   x_HII   = n_HII / n_H          (ionized H fraction, 0..1)
#   x_HeII  = n_HeII / n_He        (singly ionized He fraction)
#   x_HeIII = n_HeIII / n_He       (doubly ionized He fraction)
#   T       = temperature in K
# Fractions guarantee species conservation by construction.
# ----------------------------------------------------------------------

def number_densities(y, n_H):
    """Convert state vector to species number densities [cm^-3]."""
    x_HII, x_HeII, x_HeIII, T = y
    n_He = n_H * (Y_He / X_H) / 4.0   # He nuclei per unit volume

    n_HI = n_H * np.clip(1.0 - x_HII, X_FLOOR, 1.0)
    n_HII = n_H * np.clip(x_HII, X_FLOOR, 1.0)
    n_HeI = n_He * np.clip(1.0 - x_HeII - x_HeIII, X_FLOOR, 1.0)
    n_HeII = n_He * np.clip(x_HeII, X_FLOOR, 1.0)
    n_HeIII = n_He * np.clip(x_HeIII, X_FLOOR, 1.0)
    n_e = n_HII + n_HeII + 2.0 * n_HeIII
    return n_HI, n_HII, n_HeI, n_HeII, n_HeIII, n_e


def total_particle_density(y, n_H):
    """Total particle number density including electrons [cm^-3]."""
    n_HI, n_HII, n_HeI, n_HeII, n_HeIII, n_e = number_densities(y, n_H)
    return n_HI + n_HII + n_HeI + n_HeII + n_HeIII + n_e


def cooling_rate(y, n_H):
    """Total volumetric cooling rate Lambda_tot [erg cm^-3 s^-1]."""
    x_HII, x_HeII, x_HeIII, T = y
    T = max(T, T_FLOOR)
    n_HI, n_HII, n_HeI, n_HeII, n_HeIII, n_e = number_densities(y, n_H)
    lam = cool_exc_HI(T, n_e, n_HI)
    lam += cool_exc_HeII(T, n_e, n_HeII)
    lam += cool_ci(T, n_e, n_HI, n_HeI, n_HeII)
    lam += cool_rec(T, n_e, n_HII, n_HeII, n_HeIII)
    lam += cool_ff(T, n_e, n_HII, n_HeII, n_HeIII)
    return lam


def rhs(t, y, n_H, evolve_T=True):
    """Right-hand side of the chemistry + cooling ODE system."""
    x_HII, x_HeII, x_HeIII, T = y
    T = max(T, T_FLOOR)
    n_HI, n_HII, n_HeI, n_HeII, n_HeIII, n_e = number_densities(y, n_H)
    n_He = n_H * (Y_He / X_H) / 4.0

    # Ionization fraction ODEs
    dx_HII = (k_ci_HI(T) * n_e * n_HI - alpha_HII(T) * n_e * n_HII) / n_H
    dx_HeII = (k_ci_HeI(T) * n_e * n_HeI
               - (alpha_HeII(T) + alpha_d_HeII(T)) * n_e * n_HeII
               - k_ci_HeII(T) * n_e * n_HeII
               + alpha_HeIII(T) * n_e * n_HeIII) / n_He
    dx_HeIII = (k_ci_HeII(T) * n_e * n_HeII
                - alpha_HeIII(T) * n_e * n_HeIII) / n_He

    if evolve_T:
        # (3/2) n_tot k_B dT/dt = -Lambda_tot  (isochoric cooling; we neglect
        # the small dT/dt correction from the changing particle count)
        n_tot = n_HI + n_HII + n_HeI + n_HeII + n_HeIII + n_e
        dT = -cooling_rate(y, n_H) / (1.5 * n_tot * k_B)
        # Don't cool below the floor
        if T <= T_FLOOR and dT < 0:
            dT = 0.0
    else:
        dT = 0.0

    return [dx_HII, dx_HeII, dx_HeIII, dT]


def integrate_cell(y0, n_H, dt, evolve_T=True, rtol=1e-6, atol=1e-10):
    """
    Integrate one gas cell forward by dt seconds with a stiff (BDF) solver.

    Parameters
    ----------
    y0 : sequence of 4 floats -- initial [x_HII, x_HeII, x_HeIII, T]
    n_H : float -- hydrogen number density [cm^-3]
    dt : float -- timestep [s]

    Returns
    -------
    y1 : ndarray of 4 floats -- state after dt
    nfev : int -- number of RHS evaluations (a cost proxy)
    """
    sol = solve_ivp(rhs, (0.0, dt), y0, args=(n_H, evolve_T),
                    method="BDF", rtol=rtol, atol=atol)
    if not sol.success:
        raise RuntimeError(f"solver failed: {sol.message}")
    y1 = sol.y[:, -1]
    # Clip tiny over/undershoots from the solver
    y1[0] = np.clip(y1[0], 0.0, 1.0)
    y1[1] = np.clip(y1[1], 0.0, 1.0)
    y1[2] = np.clip(y1[2], 0.0, 1.0 - y1[1])
    y1[3] = max(y1[3], T_FLOOR)
    return y1, sol.nfev


def equilibrium_state(T, n_H, t_relax=1.0e17):
    """
    Collisional ionization equilibrium (CIE) fractions at fixed T,
    found by integrating the chemistry with the temperature held constant.
    """
    x0 = [0.5, 0.3, 0.3, T]
    y_eq, _ = integrate_cell(x0, n_H, t_relax, evolve_T=False)
    return y_eq
