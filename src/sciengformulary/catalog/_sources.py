"""Bibliographic records shared by catalog formulas.

Each builder fills only fields read from the source itself: title pages, attribution
blocks, page metadata, or the publisher's citation page. A formula module adds the
locator (section, equation, figure) at which its relationship was checked.
"""

from sciengformulary.core import ReferenceSpec

# Date on which the URLs below were opened to verify the cited relationships.
ACCESSED = "2026-10-01"

# Date on which the sources added in the OpenStax provenance audit were opened.
ACCESSED_AUDIT = "2026-10-09"

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
    title: str,
    page: str,
    year: int,
    locator: str | None = None,
    accessed: str = ACCESSED,
) -> ReferenceSpec:
    """One page of NASA Glenn's Beginner's Guide to Aeronautics.

    Args:
        title: Page title as shown on the page.
        page: URL slug under ``/beginners-guide-to-aeronautics/``.
        year: Year of the page's "Last Updated" date.
        locator: Optional section of the page.
        accessed: Date the page was opened, ``"YYYY-MM-DD"``.
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
        accessed=ACCESSED_AUDIT,
    )


def us_standard_atmosphere_1976(locator: str) -> ReferenceSpec:
    """*U.S. Standard Atmosphere, 1976* (NOAA, NASA and U.S. Air Force), as held on NTRS."""
    return nasa_technical_report(
        title="U.S. Standard Atmosphere, 1976",
        authors=(),
        report_number="NASA-TM-X-74335; NOAA-S/T-76-1562",
        year=1976,
        url="https://ntrs.nasa.gov/citations/19770009539",
        locator=locator,
        organization="NOAA, NASA and U.S. Air Force",
    )


def nasa_cr_2005_213034(locator: str) -> ReferenceSpec:
    """Brunner's lunar-sample-return relay satellite study (NASA/CR-2005-213034)."""
    return nasa_technical_report(
        title="Conceptual Design of a Communications Relay Satellite for a Lunar Sample "
        "Return Mission",
        authors=("C. W. Brunner",),
        report_number="NASA/CR-2005-213034",
        year=2005,
        url="https://ntrs.nasa.gov/citations/20050232849",
        locator=locator,
    )


_DOE_HANDBOOK_URL = "https://www.energy.gov/sites/default/files/2026-04"

_DOE_FUNDAMENTALS_HANDBOOKS = {
    # report number: (subject title, volume line or None, year, file name)
    "DOE-HDBK-1010-92": ("Classical Physics", None, 1992, "DOE-HDBK-1010-92.pdf"),
    "DOE-HDBK-1012/1-92": (
        "Thermodynamics, Heat Transfer, and Fluid Flow",
        "Volume 1 of 3",
        1992,
        "DOE-HDBK-1012-92_VOL1.pdf",
    ),
    "DOE-HDBK-1017/1-93": (
        "Material Science",
        "Volume 1 of 2",
        1993,
        "DOE-HDBK-1017-93_VOL1.pdf",
    ),
    "DOE-HDBK-1019/1-93": (
        "Nuclear Physics and Reactor Theory",
        "Volume 1 of 2",
        1993,
        "DOE-HDBK-1019-93_VOL1.pdf",
    ),
}


def doe_fundamentals_handbook(report_number: str, locator: str) -> ReferenceSpec:
    """One DOE Fundamentals Handbook (U.S. Department of Energy, training handbook series).

    The handbooks carry a public-release distribution statement and no copyright notice,
    but they were prepared for DOE with contractor help, so the maintainers should review
    their reuse status (see ``docs/provenance/openstax-audit.md``).

    Args:
        report_number: Report number as printed on the title page, a key of the table above,
            e.g. ``"DOE-HDBK-1010-92"``.
        locator: Module, equation and page, e.g. ``"module 5, eq. (5-2), p. 2 (CP-05)"``.
    """
    subject, volume, year, file_name = _DOE_FUNDAMENTALS_HANDBOOKS[report_number]
    title = f"DOE Fundamentals Handbook: {subject}"
    if volume:
        title = f"{title}, {volume}"
    return ReferenceSpec(
        source_type="technical_report",
        title=title,
        organization="U.S. Department of Energy",
        place="Washington, DC, USA",
        report_number=report_number,
        year=year,
        locator=locator,
        url=f"{_DOE_HANDBOOK_URL}/{file_name}",
        accessed=ACCESSED_AUDIT,
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
