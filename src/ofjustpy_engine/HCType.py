from aenum import Enum

class HCType(Enum):
    passive = "passive"  # implies static div/hc; for div implies passive/active childs
    active = "active"  # implies active div/hc; for div imples passive/active childs
    mutable = (
        "css_mutable"  # implies mutable div/hc; if div then imples css-mutable childs
    )
    hcc_mutable_div = "hcc_mutable"  # for div only; twstags is static/unmutable; only childs are mutable
    hcc_static_div = "static_hcc_div"  # for div only; twstags of div is mutable; but childs are static/active
