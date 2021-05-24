ISI_TEMPLATE = """
AU Wodarz, S
   Hasegawa, T
AF Wodarz, Siggi
   Hasegawa, Takashi
TI Structural control of ultra-fine CoPt nanodot arrays via
   electrodeposition process
SO JOURNAL OF MAGNETISM AND MAGNETIC MATERIALS
DE Electrodeposition; Structural control; Nanodot array; Bit-patterned
   media; CoPt alloy
ID BIT-PATTERNED MEDIA; ELECTRON-BEAM LITHOGRAPHY; RECORDING MEDIA;
   MAGNETIC MEDIA; DENSITY; FILMS; ANISOTROPY; STORAGE
CR Albrecht TR, 2013, IEEE T MAGN, V49, P773, DOI 10.1109/TMAG.2012.2227303
   Gapin AI, 2006, J APPL PHYS, V99, DOI 10.1063/1.2163289
   Yua H., 2009, J APPL PHYS, V105
PU ELSEVIER SCIENCE BV
J9 J MAGN MAGN MATER
JI J. Magn. Magn. Mater.
PY 2017
VL 500
IS 2
BP 3000
DI 10.1016/j.jmmm.2017.01.061
ER
""".strip()

from wostools.sources.isi import parse_record, parse_label


def test_parses_basic_data():
    result = parse_record(ISI_TEMPLATE)
    assert (
        result.title
        == "Structural control of ultra-fine CoPt nanodot arrays via electrodeposition process"
    )
    assert result.authors == ["Wodarz S", "Hasegawa T"]
    assert result.year == 2017
    assert result.journal == "J MAGN MAGN MATER"


def test_parses_references():
    result = parse_record(ISI_TEMPLATE)
    first, *_ = result.references
    assert first.authors == ["Albrecht TR"]
    assert first.year == 2013
    assert first.journal == "IEEE T MAGN"


def test_parses_reference():
    result = parse_label(
        "Albrecht TR, 2013, IEEE T MAGN, V49, P773, DOI 10.1109/TMAG.2012.2227303"
    )
    assert result.authors == ["Albrecht TR"]
    assert result.year == 2013
    assert result.journal == "IEEE T MAGN"
    assert result.doi == "10.1109/TMAG.2012.2227303"
    assert result.volume == "49"
    assert result.page == "773"
