import unittest
from src.aggregator import merge_all_data
from src.aggregator import merge_once


class TestAggregator(unittest.TestCase):

    def test_case_1_merge_on_company_and_inn(self):
        """Case 1: Company Name과 Inn Name이 같은 경우 병합되는지 확인"""
        data = [
            ("CompanyA", "BrandX", "Inn1__Inn2", "CodeA"),
            ("CompanyA", "BrandY", "Inn2__Inn3", "CodeB"),
        ]
        expected = [
            {
                "company_name": "CompanyA",
                "brand_name": "BrandX__BrandY",
                "inn_name": "Inn1__Inn2__Inn3",
                "code_name": "CodeA__CodeB",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_case_2_merge_on_company_and_brand_or_code(self):
        """Case 2: Company Name이 같고 Brand Name 또는 Code Name이 같은 경우 병합되는지 확인"""
        data = [
            ("CompanyB", "BrandX__BrandY", "Inn1", "CodeA"),
            ("CompanyB", "BrandX", "Inn2", "CodeB"),
            ("CompanyB", "BrandY", "Inn3", "CodeA"),  # CodeA가 겹침 → 병합
        ]
        expected = [
            {
                "company_name": "CompanyB",
                "brand_name": "BrandX__BrandY",
                "inn_name": "Inn1__Inn2__Inn3",
                "code_name": "CodeA__CodeB",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_no_merge_different_companies(self):
        """서로 다른 회사의 경우 병합되지 않아야 함"""
        data = [
            ("CompanyA", "BrandX", "Inn1", "CodeA"),
            ("CompanyB", "BrandY", "Inn2", "CodeB"),
        ]
        expected = [
            {
                "company_name": "CompanyA",
                "brand_name": "BrandX",
                "inn_name": "Inn1",
                "code_name": "CodeA",
            },
            {
                "company_name": "CompanyB",
                "brand_name": "BrandY",
                "inn_name": "Inn2",
                "code_name": "CodeB",
            },
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_edge_case_empty_values(self):
        """빈 값이 있는 경우 정상적으로 병합되는지 확인"""
        data = [
            ("CompanyA", "BrandX", "Inn1", ""),
            ("CompanyA", "BrandY", "Inn1", "CodeA"),
        ]
        expected = [
            {
                "company_name": "CompanyA",
                "brand_name": "BrandX__BrandY",
                "inn_name": "Inn1",
                "code_name": "CodeA",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_multiple_merges(self):
        """여러 개의 데이터가 병합되는지 확인"""
        data = [
            ("CompanyC", "BrandX", "Inn1", "CodeA"),
            ("CompanyC", "BrandY", "Inn1", ""),
            ("CompanyC", "BrandZ", "Inn2", "CodeB"),
            ("CompanyC", "BrandW", "Inn2", "CodeA"),  # CodeA가 겹침 → 병합
        ]
        expected = [
            {
                "company_name": "CompanyC",
                "brand_name": "BrandW__BrandX__BrandY__BrandZ",
                "inn_name": "Inn1__Inn2",
                "code_name": "CodeA__CodeB",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_merge_with_multiple_values_in_each_field(self):
        """각 필드가 __로 연결된 경우 병합이 올바르게 수행되는지 확인"""
        data = [
            ("CompanyD__CompanyE", "Brand1__Brand2", "InnA__InnB", "CodeX"),
            ("CompanyD", "Brand1", "InnA", "CodeY"),
            ("CompanyE", "Brand3", "InnB", "CodeZ"),
        ]
        expected = [
            {
                "company_name": "CompanyD__CompanyE",
                "brand_name": "Brand1__Brand2__Brand3",
                "inn_name": "InnA__InnB",
                "code_name": "CodeX__CodeY__CodeZ",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)

    def test_merge_with_large_overlap(self):
        """여러 개의 값이 겹치는 경우 병합이 정상적으로 수행되는지 확인"""
        data = [
            ("CompanyF", "BrandA__BrandB", "InnX__InnY", "Code1__Code2"),
            ("CompanyF", "BrandB__BrandC", "InnY__InnZ", "Code2__Code3"),
        ]
        expected = [
            {
                "company_name": "CompanyF",
                "brand_name": "BrandA__BrandB__BrandC",
                "inn_name": "InnX__InnY__InnZ",
                "code_name": "Code1__Code2__Code3",
            }
        ]
        result = merge_all_data(data)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
