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


def nasa_glenn(
    title: str, page: str, year: int, locator: str | None = None, accessed: str = ACCESSED
) -> ReferenceSpec:
    """One page of NASA Glenn's Beginner's Guide to Aeronautics.

    Args:
        title: Page title as shown on the page.
        page: URL slug under ``/beginners-guide-to-aeronautics/``.
        year: Year of the page's "Last Updated" date.
        locator: Optional section of the page.
        accessed: Date the source was opened, if not ``ACCESSED``.
    """
    return ReferenceSpec(
        source_type="official_web",
        title=title,
        organization="NASA Glenn Research Center",
        year=year,
        locator=locator,
        url=f"https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/{page}/",
        accessed=accessed,
    )


_ROYLANCE_COURSE_URL = "https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999"


def roylance(
    title: str, resource: str, year: int, locator: str, accessed: str = ACCESSED
) -> ReferenceSpec:
    """A module of D. Roylance's MIT 3.11 *Mechanics of Materials* notes on MIT OCW.

    Args:
        title: Module title as printed on its first page.
        resource: OCW resource slug, e.g. ``"mit3_11f99_torsion"``.
        year: Year printed under the author's affiliation.
        locator: Equation, figure or page in the module.
        accessed: Date the source was opened, if not ``ACCESSED``.
    """
    return ReferenceSpec(
        source_type="course_material",
        title=title,
        authors=("D. Roylance",),
        organization="Massachusetts Institute of Technology",
        year=year,
        locator=locator,
        url=f"{_ROYLANCE_COURSE_URL}/resources/{resource}/",
        accessed=accessed,
    )


def lienhard_heat_transfer(locator: str, accessed: str = ACCESSED) -> ReferenceSpec:
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
        accessed=accessed,
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


def nist_statistics_handbook(path: str, locator: str, accessed: str = ACCESSED) -> ReferenceSpec:
    """A page of the NIST/SEMATECH e-Handbook of Statistical Methods.

    Args:
        path: Page path under ``/div898/handbook/``, e.g. ``"eda/section3/eda3667.htm"``.
        locator: Section number and topic shown on the page.
        accessed: Date the page was opened, if not ``ACCESSED``.
    """
    return ReferenceSpec(
        source_type="official_web",
        title="NIST/SEMATECH e-Handbook of Statistical Methods",
        organization="National Institute of Standards and Technology",
        locator=locator,
        url=f"https://www.itl.nist.gov/div898/handbook/{path}",
        accessed=accessed,
    )


# Mathlib is cited at one pinned commit so every locator stays stable.
MATHLIB_COMMIT = "4a3cff2c9216262b3e173547a543e524f5d6be6e"
# Date on which the Mathlib, Selinger and newer NIST pages were opened.
MATH_ACCESSED = "2026-10-08"


def mathlib(path: str, locator: str) -> ReferenceSpec:
    """A theorem or definition in the Lean mathematical library (mathlib4) at a pinned commit.

    Mathlib states each relation formally; the catalog cites the statement only and does not
    claim to have re-checked its proof.

    Args:
        path: File path in the repository, optionally with a ``#L<line>`` anchor, e.g.
            ``"Mathlib/Data/Nat/Choose/Basic.lean"``.
        locator: Declaration kind and name, e.g.
            ``"theorem Nat.choose_eq_factorial_div_factorial"``.
    """
    return ReferenceSpec(
        source_type="official_web",
        title="mathlib4",
        organization="The mathlib Community",
        year=2026,  # commit date of MATHLIB_COMMIT: 2026-10-08
        locator=locator,
        url=f"https://github.com/leanprover-community/mathlib4/blob/{MATHLIB_COMMIT}/{path}",
        accessed=MATH_ACCESSED,
    )


def selinger_linear_algebra(locator: str) -> ReferenceSpec:
    """P. Selinger, *Matrix Theory and Linear Algebra* (CC BY 4.0), 1st ed., revision Dal 2018 A.

    The text names no publisher, so it is cited as university teaching material. Section
    numbers follow the book's chapter order; labels are given where printed numbers were not
    derived.

    Args:
        locator: Section and item, e.g. ``"sec. 7.1, Def. 7.1"``.
    """
    return ReferenceSpec(
        source_type="course_material",
        title="Matrix Theory and Linear Algebra",
        authors=("P. Selinger",),
        year=2018,
        locator=f"1st ed., rev. Dal 2018 A, {locator}",
        url="https://www.mathstat.dal.ca/~selinger/linear-algebra/",
        accessed=MATH_ACCESSED,
    )


# Date on which the engineering sources below, and newly cited pages of the builders above, were
# opened to verify the cited relationships.
ENGINEERING_ACCESSED = "2026-10-09"


def usgs_report(
    title: str,
    authors: tuple[str, ...],
    report_number: str,
    year: int,
    url: str,
    locator: str,
) -> ReferenceSpec:
    """A numbered U.S. Geological Survey report (e.g. a Water-Supply Paper).

    Args:
        title: Title as printed on the report.
        authors: Personal authors in IEEE name form.
        report_number: Series and number as printed, e.g. ``"Water-Supply Paper 1898-B"``.
        year: Year of publication.
        url: Stable USGS publications URL.
        locator: Page and equation, e.g. ``"p. B8, eq. (6)"``.
    """
    return ReferenceSpec(
        source_type="technical_report",
        title=title,
        authors=authors,
        organization="U.S. Geological Survey",
        report_number=report_number,
        place="Washington, DC, USA",
        year=year,
        locator=locator,
        url=url,
        accessed=ENGINEERING_ACCESSED,
    )


def nasa_technical_report(
    title: str,
    authors: tuple[str, ...],
    report_number: str,
    year: int,
    url: str,
    locator: str,
    organization: str = "National Aeronautics and Space Administration",
) -> ReferenceSpec:
    """A NASA technical report on the NASA Technical Reports Server (NTRS).

    Use it only for documents whose NTRS record gives the rights determination
    ``GOV_PUBLIC_USE_PERMITTED``. Every field comes from the report's title page or its
    NTRS record; pass ``authors=()`` when the report names no personal author.

    Args:
        title: Title as printed on the report.
        authors: Personal authors in IEEE name form.
        report_number: Report number, e.g. ``"NASA TM-87572"``.
        year: Year of publication.
        url: NTRS citation URL.
        locator: Section, equation and page checked.
        organization: Issuing body when it is not NASA alone.
    """
    return ReferenceSpec(
        source_type="technical_report",
        title=title,
        authors=authors,
        organization=organization,
        report_number=report_number,
        year=year,
        locator=locator,
        url=url,
        accessed=ENGINEERING_ACCESSED,
    )
