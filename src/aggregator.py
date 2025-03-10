def aggregate_data(data):
    """집계 규칙에 맞춰 데이터를 병합"""
    aggregated = []  # 집계된 데이터 저장소

    for company, brand, inn, code in data:  # 새로운 데이터를 하나씩 가져옴
        company_set = set(company.split("__"))
        brand_set = set(brand.split("__"))
        inn_set = set(inn.split("__"))
        code_set = set(code.split("__")) if code else set()

        merged = False

        for agg in aggregated:  # 기존 집계 데이터와 비교하여 병합 수행
            agg_company_set = set(agg["company_name"].split("__"))
            agg_brand_set = set(agg["brand_name"].split("__"))
            agg_inn_set = set(agg["inn_name"].split("__"))
            agg_code_set = (
                set(agg["code_name"].split("__")) if agg["code_name"] else set()
            )

            # Case 1: Company Name과 Inn Name이 같은 경우
            if company_set & agg_company_set and inn_set & agg_inn_set:
                agg["company_name"] = "__".join(sorted(agg_company_set | company_set))
                agg["brand_name"] = "__".join(sorted(agg_brand_set | brand_set))
                agg["inn_name"] = "__".join(sorted(agg_inn_set | inn_set))
                agg["code_name"] = (
                    "__".join(sorted(agg_code_set | code_set))
                    if code_set
                    else agg["code_name"]
                )
                merged = True
                break

            # Case 2: Company Name이 같고 Brand Name 또는 Code Name이 같은 경우
            if company_set & agg_company_set and (
                brand_set & agg_brand_set or code_set & agg_code_set
            ):
                agg["company_name"] = "__".join(sorted(agg_company_set | company_set))
                agg["brand_name"] = "__".join(sorted(agg_brand_set | brand_set))
                agg["inn_name"] = "__".join(sorted(agg_inn_set | inn_set))
                agg["code_name"] = (
                    "__".join(sorted(agg_code_set | code_set))
                    if code_set
                    else agg["code_name"]
                )
                merged = True
                break

        # 병합되지 않은 경우 새로운 row 추가
        if not merged:
            aggregated.append(
                {
                    "company_name": "__".join(sorted(company_set)),
                    "brand_name": "__".join(sorted(brand_set)),
                    "inn_name": "__".join(sorted(inn_set)),
                    "code_name": "__".join(sorted(code_set)) if code_set else "",
                }
            )

    return aggregated
