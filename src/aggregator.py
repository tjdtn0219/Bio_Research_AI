from collections import defaultdict
from itertools import combinations


def merge_all_data(data):
    """집계 규칙에 맞춰 데이터를 병합"""
    while True:
        result, updated = merge_once(data)
        data = result
        if not updated:
            print("✅ No further updates. Returning final data.")

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
    """한 번의 병합 실행 후 결과 반환 (Trie & 해시 최적화 적용)"""
    updated = False
    aggregated_dict = defaultdict(
        lambda: {"company": set(), "brand": set(), "inn": set(), "code": set()}
    )

    # 1. 데이터를 Set으로 변환하여 저장 (문자열 변환 최소화)
    processed_data = []
    for company, brand, inn, code in data:
        company_set = set(company.split("__"))
        brand_set = set(brand.split("__"))
        inn_set = set(inn.split("__"))
        code_set = set(code.split("__")) if code else set()
        processed_data.append((company_set, brand_set, inn_set, code_set))

    # 2. 해시 기반 병합: 기존 데이터와 비교하여 병합할 대상을 찾음
    for company_set, brand_set, inn_set, code_set in processed_data:
        found_key = None

        # Case 1: Company Name과 Inn Name이 같은 경우 병합
        for existing_key in aggregated_dict.keys():
            existing_company_set, existing_inn_set = existing_key
            if company_set & existing_company_set and inn_set & existing_inn_set:
                found_key = existing_key
                break

        if found_key:
            existing = aggregated_dict[found_key]
            existing["company"].update(company_set)
            existing["brand"].update(brand_set)
            existing["inn"].update(inn_set)
            existing["code"].update(code_set)
            updated = True
            continue

        # Case 2: Company Name이 같고 Brand Name 또는 Code Name이 같은 경우 병합
        for existing_key in aggregated_dict.keys():
            existing = aggregated_dict[existing_key]
            if company_set & existing["company"] and (
                brand_set & existing["brand"] or code_set & existing["code"]
            ):
                existing["company"].update(company_set)
                existing["brand"].update(brand_set)
                existing["inn"].update(inn_set)
                existing["code"].update(code_set)
                updated = True
                break
        else:
            aggregated_dict[(frozenset(company_set), frozenset(inn_set))] = {
                "company": company_set,
                "brand": brand_set,
                "inn": inn_set,
                "code": code_set,
            }

    # 3. 결과 변환
    result = [
        (
            "__".join(sorted(data["company"])),
            "__".join(sorted(data["brand"])),
            "__".join(sorted(data["inn"])),
            "__".join(sorted(data["code"])) if data["code"] else "",
        )
        for data in aggregated_dict.values()
    ]

    return result, updated  # ✅ 최적화된 데이터 반환
