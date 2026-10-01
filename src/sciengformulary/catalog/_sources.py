"""Bibliographic records shared by catalog formulas.

Each builder fills only fields read from the source itself: title pages, attribution
blocks, page metadata, or the publisher's citation page. A formula module adds the
locator (section, equation, figure) at which its relationship was checked.
"""

from sciengformulary.core import ReferenceSpec

# Date on which the URLs below were opened to verify the cited relationships.
ACCESSED = "2026-10-01"

_OPENSTAX_UNIVERSITY_PHYSICS = {
    # volume: (authors in the order of the book's attribution block, year)
    1: (("W. Moebs", "S. J. Ling", "J. Sanny"), 2016),
    2: (("S. J. Ling", "W. Moebs", "J. Sanny"), 2016),
    3: (("S. J. Ling", "J. Sanny", "W. Moebs"), 2016),
}


def openstax_university_physics(volume: int, page: str, locator: str) -> ReferenceSpec:
    """OpenStax *University Physics* (Rice University), one section page.

    Args:
        volume: Volume number, 1 to 3.
        page: Section page slug, e.g. ``"15-5-damped-oscillations"``.
        locator: Section and equation, e.g. ``"sec. 15.5, eq. (15.26)"``.
    """
    authors, year = _OPENSTAX_UNIVERSITY_PHYSICS[volume]
    return ReferenceSpec(
        source_type="book",
        title=f"University Physics Volume {volume}",
        authors=authors,
        publisher="OpenStax",
        place="Houston, TX, USA",
        year=year,
        locator=locator,
        url=f"https://openstax.org/books/university-physics-volume-{volume}/pages/{page}",
        accessed=ACCESSED,
    )


def naca_report_1135(locator: str) -> ReferenceSpec:
    """NACA Report 1135, the Ames compilation of compressible-flow relations."""
    return ReferenceSpec(
        source_type="technical_report",
        title="Equations, Tables, and Charts for Compressible Flow",
        organization="Ames Research Staff",
        report_number="NACA Rep. 1135",
        year=1953,
        locator=locator,
        url="https://ntrs.nasa.gov/citations/19930091059",
        accessed=ACCESSED,
    )


def nasa_glenn(title: str, page: str, year: int, locator: str | None = None) -> ReferenceSpec:
    """One page of NASA Glenn's Beginner's Guide to Aeronautics.

    Args:
        title: Page title as shown on the page.
        page: URL slug under ``/beginners-guide-to-aeronautics/``.
        year: Year of the page's "Last Updated" date.
        locator: Optional section of the page.
    """
    return ReferenceSpec(
        source_type="official_web",
        title=title,
        organization="NASA Glenn Research Center",
        year=year,
        locator=locator,
        url=f"https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/{page}/",
        accessed=ACCESSED,
    )


_ROYLANCE_COURSE_URL = "https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999"


def roylance(title: str, resource: str, year: int, locator: str) -> ReferenceSpec:
    """A module of D. Roylance's MIT 3.11 *Mechanics of Materials* notes on MIT OCW.

    Args:
        title: Module title as printed on its first page.
        resource: OCW resource slug, e.g. ``"mit3_11f99_torsion"``.
        year: Year printed under the author's affiliation.
        locator: Equation, figure or page in the module.
    """
    return ReferenceSpec(
        source_type="course_material",
        title=title,
        authors=("D. Roylance",),
        organization="Massachusetts Institute of Technology",
        year=year,
        locator=locator,
        url=f"{_ROYLANCE_COURSE_URL}/resources/{resource}/",
        accessed=ACCESSED,
    )


def lienhard_heat_transfer(locator: str) -> ReferenceSpec:
    """Lienhard and Lienhard, *A Heat Transfer Textbook*, 6th ed. (version 6.00)."""
    return ReferenceSpec(
        source_type="book",
        title="A Heat Transfer Textbook",
        authors=("J. H. Lienhard V", "J. H. Lienhard IV"),
        edition="6th",
        publisher="Phlogiston Press",
        place="Cambridge, MA, USA",
        year=2024,
        locator=locator,
        url="https://ahtt.mit.edu",
        accessed=ACCESSED,
    )


def nist_codata(quantity: str, symbol: str) -> ReferenceSpec:
    """NIST page for one CODATA 2022 recommended value.

    Args:
        quantity: Name in the page title, e.g. ``"Boltzmann constant"``.
        symbol: Query key of the page, e.g. ``"k"``.
    """
    return ReferenceSpec(
        source_type="official_web",
        title=f"CODATA Value: {quantity}",
        organization="National Institute of Standards and Technology",
        locator="2022 CODATA recommended value",
        url=f"https://physics.nist.gov/cgi-bin/cuu/Value?{symbol}",
        accessed=ACCESSED,
    )


def nist_dlmf(section: str, locator: str) -> ReferenceSpec:
    """A section of the NIST Digital Library of Mathematical Functions (release 1.2.8)."""
    return ReferenceSpec(
        source_type="official_web",
        title="NIST Digital Library of Mathematical Functions",
        organization="National Institute of Standards and Technology",
        year=2026,
        locator=locator,
        url=f"https://dlmf.nist.gov/{section}",
        accessed=ACCESSED,
    )


def nist_statistics_handbook(path: str, locator: str) -> ReferenceSpec:
    """A page of the NIST/SEMATECH e-Handbook of Statistical Methods."""
    return ReferenceSpec(
        source_type="official_web",
        title="NIST/SEMATECH e-Handbook of Statistical Methods",
        organization="National Institute of Standards and Technology",
        locator=locator,
        url=f"https://www.itl.nist.gov/div898/handbook/{path}",
        accessed=ACCESSED,
    )
