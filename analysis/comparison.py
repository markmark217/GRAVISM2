"""
Multi-Model Comparison Engine
=============================

Compares different gravitational lens models (Point Mass, SIS, SIE, Binary Lens,
Galaxy Cluster) side by side under identical source conditions.
"""

from typing import Dict, Any, List
from simulation.point_mass import PointMassSimulation
from simulation.galaxy_lens import GalaxyLensSimulation
from simulation.binary_lens import BinaryLensSimulation
from simulation.cluster_lens import ClusterLensSimulation


def compare_all_models(source_x: float = 0.3, source_y: float = 0.2, resolution: int = 120) -> Dict[str, Any]:
    """
    Execute simulations across the core lens models for side-by-side scientific comparison.
    """
    p_sim = PointMassSimulation(source_x=source_x, source_y=source_y, resolution=resolution).run()
    sis_sim = GalaxyLensSimulation(is_elliptical=False, source_x=source_x, source_y=source_y, resolution=resolution).run()
    sie_sim = GalaxyLensSimulation(is_elliptical=True, source_x=source_x, source_y=source_y, resolution=resolution).run()
    bin_sim = BinaryLensSimulation(source_x=source_x, source_y=source_y, resolution=resolution).run()

    return {
        "point_mass": p_sim,
        "sis": sis_sim,
        "sie": sie_sim,
        "binary": bin_sim
    }

