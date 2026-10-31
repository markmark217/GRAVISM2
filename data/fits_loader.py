"""
Astronomical FITS Image and Metadata Loader
===========================================

Loads and parses Flexible Image Transport System (FITS) astronomical files
using Astropy FITS module.
"""

from typing import Dict, Any, Tuple, Optional
import io
import numpy as np


def read_fits_data(file_bytes_or_path) -> Dict[str, Any]:
    """
    Read FITS image data and primary header keywords.
    """
    from astropy.io import fits

    try:
        with fits.open(file_bytes_or_path) as hdul:
            # Find first HDU with 2D image data
            image_data = None
            header_dict = {}
            for hdu in hdul:
                if hdu.data is not None and len(hdu.data.shape) == 2:
                    image_data = np.array(hdu.data, dtype=np.float32)
                    for key, val in hdu.header.items():
                        if key and key not in ["COMMENT", "HISTORY"]:
                            header_dict[str(key)] = str(val)
                    break

            if image_data is None:
                raise ValueError("No 2D image data found in FITS HDUs.")

            # Basic statistics
            stats = {
                "min": float(np.min(image_data)),
                "max": float(np.max(image_data)),
                "mean": float(np.mean(image_data)),
                "shape": list(image_data.shape)
            }

            return {
                "data": image_data,
                "header": header_dict,
                "stats": stats,
                "success": True
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def create_sample_fits_buffer(name: str = "Einstein_Cross_Sim") -> io.BytesIO:
    """
    Create an in-memory sample FITS file for testing and educational import.
    """
    from astropy.io import fits

    # Generate sample 100x100 quadrupole image
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    xx, yy = np.meshgrid(x, y)
    r = np.hypot(xx, yy)

    # Core galaxy
    img = 100.0 * np.exp(-r / 0.8)
    # 4 lensed quasar images
    for qx, qy in [(1.1, 0.0), (-1.1, 0.0), (0.0, 1.1), (0.0, -1.1)]:
        rq = np.hypot(xx - qx, yy - qy)
        img += 150.0 * np.exp(-0.5 * (rq / 0.15)**2)

    # Add Gaussian noise
    img += np.random.normal(0, 2.0, img.shape)

    hdu = fits.PrimaryHDU(data=img.astype(np.float32))
    hdu.header["OBJECT"] = name
    hdu.header["TELESCOP"] = "HST-WFC3"
    hdu.header["INSTRUME"] = "WFC3-UVIS"
    hdu.header["FILTER"] = "F814W"
    hdu.header["EXPTIME"] = 1200.0
    hdu.header["BUNIT"] = "ELECTRONS/S"

    buf = io.BytesIO()
    hdu.writeto(buf)
    buf.seek(0)
    return buf

