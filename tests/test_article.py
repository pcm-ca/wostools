from copy import deepcopy
from dataclasses import dataclass
from typing import Optional, List

from pytest import fixture
from pytest_bdd import scenarios, scenario, given, then, when, parsers

from wostools.article import Article


ISI_TEMPLATE = """
PT J
AU {author}
   {second_author}
AF {author}
   {second_author}
TI {title}
SO JOURNAL OF MAGNETISM AND MAGNETIC MATERIALS
LA English
DT Article
DE Electrodeposition; Structural control; Nanodot array; Bit-patterned
   media; CoPt alloy
ID BIT-PATTERNED MEDIA; ELECTRON-BEAM LITHOGRAPHY; RECORDING MEDIA;
   MAGNETIC MEDIA; DENSITY; FILMS; ANISOTROPY; STORAGE
AB CoPt nanodot arrays were fabricated by combining electrodeposition and electron beam lithography (EBL) for the use of bit-patterned media (BPM). To achieve precise control of deposition uniformity and coercivity of the CoPt nanodot arrays, their crystal structure and magnetic properties were controlled by controlling the diffusion state of metal ions from the initial deposition stage with the application of bath agitation. Following bath agitation, the composition gradient of the CoPt alloy with thickness was mitigated to have a near-ideal alloy composition of Co:Pt =80:20, which induces epitaxial-like growth from Ru substrate, thus resulting in the improvement of the crystal orientation of the hcp (002) structure from its initial deposition stages. Furthermore, the cross-sectional transmission electron microscope (TEM) analysis of the nanodots deposited with bath agitation showed CoPt growth along its c-axis oriented in the perpendicular direction, having uniform lattice fringes on the hcp (002) plane from the Ru underlayer interface, which is a significant factor to induce perpendicular magnetic anisotropy. Magnetic characterization of the CoPt nanodot arrays showed increase in the perpendicular coercivity and squareness of the hysteresis loops from 2.0 kOe and 0.64 (without agitation) to 4.0 kOe and 0.87 with bath agitation. Based on the detailed characterization of nanodot arrays, the precise crystal structure control of the nanodot arrays with ultra-high recording density by electrochemical process was successfully demonstrated.
C1 [Wodarz, Siggi; Homma, Takayuki] Waseda Univ, Dept Appl Chem, Shinjuku Ku, Tokyo 1698555, Japan.
   [Hasegawa, Takashi; Ishio, Shunji] Akita Univ, Dept Mat Sci, Akita 0108502, Japan.
RP Homma, T (reprint author), Waseda Univ, Dept Appl Chem, Shinjuku Ku, Tokyo 1698555, Japan.
EM t.homma@waseda.jp
OI Hasegawa, Takashi/0000-0002-8178-4980
FU JSPS KAKENHI Grant [25249104]
FX This work was supported in part by JSPS KAKENHI Grant Number 25249104.
CR Albrecht TR, 2013, IEEE T MAGN, V49, P773, DOI 10.1109/TMAG.2012.2227303
   BUSCHOW KHJ, 1983, J MAGN MAGN MATER, V38, P1, DOI 10.1016/0304-8853(83)90097-5
   Gapin AI, 2006, J APPL PHYS, V99, DOI 10.1063/1.2163289
   Homma Takayuki, 2015, ECS Transactions, V64, P1, DOI 10.1149/06431.0001ecst
   Kryder MH, 2008, P IEEE, V96, P1810, DOI 10.1109/JPROC.2008.2004315
   Kubo T, 2005, J APPL PHYS, V97, DOI 10.1063/1.1855572
   Lodder JC, 2004, J MAGN MAGN MATER, V272, P1692, DOI 10.1016/j.jmmm.2003.12.259
   Mitsuzuka K, 2007, IEEE T MAGN, V43, P2160, DOI 10.1109/TMAG.2007.893129
   Ouchi T, 2010, ELECTROCHIM ACTA, V55, P8081, DOI 10.1016/j.electacta.2010.02.073
   Pattanaik G, 2006, J APPL PHYS, V99, DOI 10.1063/1.2150805
   Pattanaik G, 2007, ELECTROCHIM ACTA, V52, P2755, DOI 10.1016/j.electacta.2006.07.062
   Piramanayagam SN, 2009, J MAGN MAGN MATER, V321, P485, DOI 10.1016/j.jmmm.2008.05.007
   Ross CA, 2008, MRS BULL, V33, P838, DOI 10.1557/mrs2008.179
   Shiroishi Y, 2009, IEEE T MAGN, V45, P3816, DOI 10.1109/TMAG.2009.2024879
   Sirtori V, 2011, ACS APPL MATER INTER, V3, P1800, DOI 10.1021/am200267u
   Sohn JS, 2009, NANOTECHNOLOGY, V20, DOI 10.1088/0957-4484/20/2/025302
   Sun SH, 2000, SCIENCE, V287, P1989, DOI 10.1126/science.287.5460.1989
   Terris BD, 2007, MICROSYST TECHNOL, V13, P189, DOI 10.1007/s00542-006-0144-9
   Wang JP, 2008, P IEEE, V96, P1847, DOI 10.1109/JPROC.2008.2004318
   Weller D, 1999, IEEE T MAGN, V35, P4423, DOI 10.1109/20.809134
   Weller D, 2000, IEEE T MAGN, V36, P10, DOI 10.1109/20.824418
   Wodarz S, 2016, ELECTROCHIM ACTA, V197, P330, DOI 10.1016/j.electacta.2015.11.136
   Xu X, 2012, J ELECTROCHEM SOC, V159, pD240, DOI 10.1149/2.090204jes
   Yang X, 2007, J VAC SCI TECHNOL B, V25, P2202, DOI 10.1116/1.2798711
   Yang XM, 2009, ACS NANO, V3, P1844, DOI 10.1021/nn900073r
   Yasui N, 2003, APPL PHYS LETT, V83, P3347, DOI 10.1063/1.1622787
   Yua H., 2009, J APPL PHYS, V105
   Zhu JG, 2008, IEEE T MAGN, V44, P125, DOI 10.1109/TMAG.2007.911031
NR 28
TC 0
Z9 0
U1 21
U2 21
PU ELSEVIER SCIENCE BV
PI AMSTERDAM
PA PO BOX 211, 1000 AE AMSTERDAM, NETHERLANDS
SN 0304-8853
EI 1873-4766
J9 {journal}
JI J. Magn. Magn. Mater.
PD MAY 15
PY {year}
VL {volume}
BP {page}
EP 58
DI {doi}
PG 7
WC Materials Science, Multidisciplinary; Physics, Condensed Matter
SC Materials Science; Physics
GA EP2GP
UT WOS:000397201600008
ER
""".strip()


@dataclass
class Context:
    article: Optional[Article]
    label: Optional[str] = None
    expected_label: Optional[str] = None
    error: Optional[Exception] = None


@dataclass
class ParseContext:
    history: Optional[List[Article]] = None
    error: Optional[Exception] = None
    article: Optional[Article] = None

    def push(self, article: Article):
        if self.history is None:
            self.history = []
        self.history.append(article)
        self.article = article
        self.error = None


scenarios("features/article.feature")


@fixture
def attributes():
    return {
        "title": "some title",
        "author": "John Doe",
        "second_author": "Jane Doe",
        "authors": ["John Doe", "Jane Doe"],
        "year": 1994,
        "page": "1330-5",
        "journal": "J MAGN MAGN MATER",
        "volume": "1000",
        "doi": "10.1016/j.jmmm.2017.01.061",
    }


@fixture
def parse_context():
    return ParseContext()


@given("a complete article missing <field>", target_fixture="context")
def article_missing(field: str):
    article = Article(
        title=None, authors=["L, Robertson"], year=1999, journal="Science"
    )
    setattr(article, field, None)
    return Context(article=article)


@given("a complete article", target_fixture="context")
@given("an article with authors, year and journal", target_fixture="context")
def article_with_authors_year_and_journal():
    return Context(
        article=Article(
            title=None, authors=["L, Robertson"], year=1999, journal="Science"
        ),
        expected_label="L Robertson, 1999, Science",
    )


@given("theres a similar article that includes a doi", target_fixture="other")
def similar_article_with_doi(context: Context):
    assert context.article, "missing article to copy"
    article = deepcopy(context.article)
    article.doi = "somedoi/123"
    if context.expected_label:
        return Context(
            article=article,
            expected_label=", ".join([context.expected_label, article.doi]),
        )
    return Context(article=article)


@given("some valid isi text", target_fixture="isi_text")
def valid_isi_text(attributes):
    return ISI_TEMPLATE.format(**attributes)


@when("I merge the two articles")
def merge_articles(context: Context, other: Context):
    assert context.article, "Missing article for this step"
    assert other.article, "Missing other article for this step"
    context.article = context.article.merge(other.article)
    context.expected_label = None


@when("I try to compute the label for the article")
@when("I compute the label for the article")
def try_to_compute_label(context: Context):
    assert context.article, "Missing article for this step"
    try:
        context.label = context.article.label
    except Exception as e:
        context.error = e


@when("I create an article from the isi text")
def create_article_from_isi_text(isi_text, parse_context):
    article = Article.from_isi_text(isi_text)
    parse_context.push(article)


@then("the label is a proper string")
def then_label_is_a_proper_string(context: Context):
    assert context.expected_label
    assert context.label
    assert context.label == context.expected_label


@then("the label contains the doi of the other")
def label_matches_other(context: Context, other: Context):
    assert context.label, "You didn't get a label in the then block"
    assert other.article and other.article.doi, "There's no doi in the other article"
    assert other.article.doi in context.label


@then("There's no error computing the label")
@then("there's no error computing the label")
def no_error_computing_label(context: Context):
    assert context.label
    assert not context.error


@then("There's an error computing the label")
def error_computing_label(context: Context):
    assert not context.label
    assert context.error
    assert isinstance(context.error, ValueError)


@then(parsers.parse("the article matches the {field:w} of the other"))
@then(parsers.parse("the article's {field:w} matches the other"))
def contais_others_field(context: Context, other: Context, field: str):
    assert context.article
    assert other.article
    assert getattr(context.article, field) == getattr(other.article, field)


@then("the values in the isi text are part of the article")
def values_make_it_to_the_article(parse_context: ParseContext, attributes: dict):
    assert parse_context.article, "no article parsed yet"
    for field in [
        "title",
        "authors",
        "year",
        "page",
        "journal",
        "volume",
        "doi",
    ]:
        assert getattr(parse_context.article, field)
        assert getattr(parse_context.article, field) == attributes[field]


@then("the isi text itself is part of the articles sources")
def isi_text_in_sources(parse_context: ParseContext, isi_text: str):
    assert parse_context.article, "no article parsed yet"
    assert isi_text in parse_context.article.sources
