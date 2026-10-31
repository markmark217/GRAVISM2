"""
Astronomical Objects Catalog and Real Gravitational Lens Database
================================================================

Curated catalog of observed gravitational lenses and compact objects
from public archives (NASA/NED, MAST, SDSS, ESA/Hubble).
Conforms to Core Data Models specification (Section 11).
"""

from typing import List, Dict, Any, Optional
import json
import pandas as pd


ASTRONOMICAL_CATALOG: List[Dict[str, Any]] = [
    {
        "id": "LENS-001",
        "name": "Q2237+0305 (Einstein's Cross)",
        "objectType": "Gravitational Lens System",
        "lensName": "ZW 2237+030 (Huchra's Lens)",
        "lensType": "Galaxy (Spiral Core)",
        "rightAscensionDeg": 339.8458,
        "declinationDeg": 3.3583,
        "zLens": 0.0394,
        "zSource": 1.695,
        "estimatedMassSolar": 1.2e10,
        "massUncertaintySolar": 0.2e10,
        "einsteinRadiusArcsec": 0.89,
        "sourceType": "Quasar",
        "survey": "HST / W. M. Keck Observatory",
        "observationDate": "1990-08-15",
        "sourceUrl": "https://esahubble.org/images/heic0511a/",
        "citation": "Huchra et al. (1985); Yee (1988); HST ACS/WFC3",
        "description": "Four bright quasar images surrounding a low-redshift spiral galactic nucleus.",
        "recommendedModel": "sie_galaxy",
        "modelParameters": {"q": 0.72, "phi_deg": 45.0, "theta_e": 0.89, "source_x": 0.05, "source_y": 0.03}
    },
    {
        "id": "LENS-002",
        "name": "SDSS J0946+1006 (The Cosmic Horseshoe)",
        "objectType": "Gravitational Lens System",
        "lensName": "SDSS J0946+1006 Lens Galaxy",
        "lensType": "Luminous Red Galaxy (LRG)",
        "rightAscensionDeg": 146.6183,
        "declinationDeg": 10.1111,
        "zLens": 0.444,
        "zSource": 2.007,
        "estimatedMassSolar": 1.1e12,
        "massUncertaintySolar": 0.15e12,
        "einsteinRadiusArcsec": 2.11,
        "sourceType": "Star-Forming Galaxy",
        "survey": "Sloan Digital Sky Survey (SDSS) / Hubble Space Telescope",
        "observationDate": "2007-06-20",
        "sourceUrl": "https://esahubble.org/images/potw1151a/",
        "citation": "Belokurov et al. (2007); Dye et al. (2008)",
        "description": "Nearly complete 300-degree Einstein ring with a radius of 2.11 arcseconds around a giant elliptical galaxy.",
        "recommendedModel": "sie_galaxy",
        "modelParameters": {"q": 0.90, "phi_deg": 15.0, "theta_e": 2.11, "source_x": 0.08, "source_y": 0.05}
    },
    {
        "id": "LENS-003",
        "name": "SDSS J1004+4112",
        "objectType": "Gravitational Lens System",
        "lensName": "Cluster SDSS J1004+4112",
        "lensType": "Galaxy Cluster",
        "rightAscensionDeg": 151.0512,
        "declinationDeg": 41.2128,
        "zLens": 0.680,
        "zSource": 1.734,
        "estimatedMassSolar": 5.4e13,
        "massUncertaintySolar": 0.8e13,
        "einsteinRadiusArcsec": 7.3,
        "sourceType": "Quasar",
        "survey": "SDSS / Subaru / HST",
        "observationDate": "2003-12-18",
        "sourceUrl": "https://archive.stsci.edu/",
        "citation": "Inada et al. (2003); Oguri et al. (2004)",
        "description": "The first quintuply lensed quasar discovered, produced by a foreground rich galaxy cluster.",
        "recommendedModel": "cluster",
        "modelParameters": {"cluster_theta_e": 7.3, "core_radius": 2.0, "source_x": 0.8, "source_y": 0.4}
    },
    {
        "id": "LENS-004",
        "name": "MACS J1149.5+2223 (Supernova Refsdal System)",
        "objectType": "Gravitational Lens System",
        "lensName": "MACS J1149.5+2223",
        "lensType": "Galaxy Cluster + Cluster Elliptical",
        "rightAscensionDeg": 177.3987,
        "declinationDeg": 22.3989,
        "zLens": 0.542,
        "zSource": 1.488,
        "estimatedMassSolar": 2.5e14,
        "massUncertaintySolar": 0.4e14,
        "einsteinRadiusArcsec": 14.2,
        "sourceType": "Type Ia Supernova / Spiral Galaxy",
        "survey": "Hubble Frontier Fields",
        "observationDate": "2014-11-10",
        "sourceUrl": "https://esahubble.org/news/heic1525/",
        "citation": "Kelly et al. (2015), Science; Refsdal (1964)",
        "description": "First gravitationally lensed supernova with observed multiple images and predicted reappearance time delay.",
        "recommendedModel": "cluster",
        "modelParameters": {"cluster_theta_e": 14.0, "core_radius": 3.0, "source_x": 1.2, "source_y": 0.8}
    },
    {
        "id": "BH-001",
        "name": "M87* (Messier 87 Central Supermassive Black Hole)",
        "objectType": "Supermassive Black Hole",
        "lensName": "M87*",
        "lensType": "Kerr / Schwarzschild Black Hole",
        "rightAscensionDeg": 187.7059,
        "declinationDeg": 12.3911,
        "zLens": 0.00428,
        "zSource": None,
        "estimatedMassSolar": 6.5e9,
        "massUncertaintySolar": 0.7e9,
        "einsteinRadiusArcsec": None,
        "sourceType": "Relativistic Accretion Flow",
        "survey": "Event Horizon Telescope (EHT)",
        "observationDate": "2017-04-11",
        "sourceUrl": "https://eventhorizontelescope.org/",
        "citation": "Event Horizon Telescope Collaboration (2019), ApJL",
        "description": "First black hole ever directly resolved. Measured angular diameter of shadow is 42 +/- 3 microarcsec.",
        "recommendedModel": "schwarzschild",
        "modelParameters": {"mass_solar": 6.5e9}
    },
    {
        "id": "BH-002",
        "name": "Sagittarius A* (Milky Way Galactic Center)",
        "objectType": "Supermassive Black Hole",
        "lensName": "Sgr A*",
        "lensType": "Compact Supermassive Black Hole",
        "rightAscensionDeg": 266.4168,
        "declinationDeg": -29.0078,
        "zLens": 0.0,
        "zSource": None,
        "estimatedMassSolar": 4.15e6,
        "massUncertaintySolar": 0.01e6,
        "einsteinRadiusArcsec": None,
        "sourceType": "Inner Accretion Ring",
        "survey": "Event Horizon Telescope (EHT) / Keck / VLT GRAVITY",
        "observationDate": "2022-05-12",
        "sourceUrl": "https://eventhorizontelescope.org/",
        "citation": "Event Horizon Telescope Collaboration (2022), ApJL",
        "description": "Supermassive black hole at the center of the Milky Way, at a distance of ~8.2 kpc.",
        "recommendedModel": "schwarzschild",
        "modelParameters": {"mass_solar": 4.15e6}
    }
]


def get_catalog_dataframe() -> pd.DataFrame:
    """Return catalog as a pandas DataFrame."""
    return pd.DataFrame(ASTRONOMICAL_CATALOG)


def get_object_by_id(object_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full astronomical record by ID."""
    for obj in ASTRONOMICAL_CATALOG:
        if obj["id"] == object_id:
            return obj
    return None

