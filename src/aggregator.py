def merge_all_data(data):
    """집계 규칙에 맞춰 데이터를 병합"""
    while True:
        result, updated = merge_once(data)  # 병합 실행
        data = result  # 새로운 데이터로 업데이트
        print("result", result)
        print("updated", updated)
        if not updated:  # 병합이 더 이상 일어나지 않으면 종료
            print("✅ No further updates. Returning final data.")

            # ✅ 최종 데이터 매핑 (튜플 -> 딕셔너리 변환)
            return [
                {
                    "company_name": company,
                    "brand_name": brand,
                    "inn_name": inn,
                    "code_name": code,
                }
                for company, brand, inn, code in data
            ]


def merge_once(data):
    """단일 병합 실행 후 결과 반환 (반환값은 항상 튜플 리스트)"""
    updated = False  # 병합이 일어났는지 추적
    new_aggregated = []

    for company, brand, inn, code in data:
        company_set = set(company.split("__"))
        brand_set = set(brand.split("__"))
        inn_set = set(inn.split("__"))
        code_set = set(code.split("__")) if code else set()

        merged = False

        for i, (agg_company, agg_brand, agg_inn, agg_code) in enumerate(new_aggregated):
            agg_company_set = set(agg_company.split("__"))
            agg_brand_set = set(agg_brand.split("__"))
            agg_inn_set = set(agg_inn.split("__"))
            agg_code_set = set(agg_code.split("__")) if agg_code else set()

            # Case 1: Company Name과 Inn Name이 같은 경우
            if company_set & agg_company_set and inn_set & agg_inn_set:
                new_aggregated[i] = (
                    "__".join(sorted(agg_company_set | company_set)),
                    "__".join(sorted(agg_brand_set | brand_set)),
                    "__".join(sorted(agg_inn_set | inn_set)),
                    (
                        "__".join(sorted(agg_code_set | code_set))
                        if code_set
                        else agg_code
                    ),
                )
                updated = True
                merged = True
                break

            # Case 2: Company Name이 같고 Brand Name 또는 Code Name이 같은 경우
            if company_set & agg_company_set and (
                brand_set & agg_brand_set or code_set & agg_code_set
            ):
                new_aggregated[i] = (
                    "__".join(sorted(agg_company_set | company_set)),
                    "__".join(sorted(agg_brand_set | brand_set)),
                    "__".join(sorted(agg_inn_set | inn_set)),
                    (
                        "__".join(sorted(agg_code_set | code_set))
                        if code_set
                        else agg_code
                    ),
                )
                updated = True
                merged = True
                break

        if not merged:
            new_aggregated.append(
                (
                    "__".join(sorted(company_set)),
                    "__".join(sorted(brand_set)),
                    "__".join(sorted(inn_set)),
                    "__".join(sorted(code_set)) if code_set else "",
                )
            )

    return new_aggregated, updated  # ✅ 항상 튜플 리스트로 반환
