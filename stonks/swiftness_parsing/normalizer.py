from stonks.models import SwiftnessProduct, SwiftnessDeposit, SwiftnessInsurance

# noinspection PyUnresolvedReferences,PyProtectedMember
normalize_swiftness_products_mapping = {
    field.name: field.swiftness_value_parser
    for field in SwiftnessProduct._meta.get_fields()
    if hasattr(field, "swiftness_value_parser")
}
normalize_swiftness_products_reverse_mapping = {
    v.heb_field_name: k for k, v in normalize_swiftness_products_mapping.items()
}

# noinspection PyUnresolvedReferences,PyProtectedMember
normalize_swiftness_deposits_mapping = {
    field.name: field.swiftness_value_parser
    for field in SwiftnessDeposit._meta.get_fields()
    if hasattr(field, "swiftness_value_parser")
}
normalize_swiftness_deposits_reverse_mapping = {
    v.heb_field_name: k for k, v in normalize_swiftness_deposits_mapping.items()
}

# noinspection PyUnresolvedReferences,PyProtectedMember
normalize_swiftness_insurances_mapping = {
    field.name: field.swiftness_value_parser
    for field in SwiftnessInsurance._meta.get_fields()
    if hasattr(field, "swiftness_value_parser")
}
normalize_swiftness_insurances_reverse_mapping = {
    v.heb_field_name: k for k, v in normalize_swiftness_insurances_mapping.items()
}

normalize_swiftness_mapping_categories = {
    "products": (
        "פרטי המוצרים שלי",
        normalize_swiftness_products_mapping,
        normalize_swiftness_products_reverse_mapping,
    ),
    "deposits": (
        "מעקב הפקדות",
        normalize_swiftness_deposits_mapping,
        normalize_swiftness_deposits_reverse_mapping,
    ),
    "insurances": (
        "כיסויים ביטוחיים",
        normalize_swiftness_insurances_mapping,
        normalize_swiftness_insurances_reverse_mapping,
    ),
}

normalize_swiftness_mapping_reverse_categories = {
    v[0]: norm_name for norm_name, v in normalize_swiftness_mapping_categories.items()
}


def normalize_swiftness_dict(src: dict):
    assert sorted(src.keys()) == sorted(normalize_swiftness_mapping_reverse_categories.keys()), "Unexpected categories"

    dst = {}
    for eng_category, (
        heb_category,
        mapping,
        rev_mapping,
    ) in normalize_swiftness_mapping_categories.items():
        assert sorted(src[heb_category][0].keys()) == sorted(rev_mapping.keys()), "Unexpected header"
        # For each column, parse the value according to the type specified in the mapping,
        # and store it using the normalized (english) name
        dst[eng_category] = [
            {rev_mapping[k]: mapping[rev_mapping[k]].parse(str(v)) for k, v in entry.items()}
            for entry in src[heb_category]
        ]

    return dst
