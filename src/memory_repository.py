import pandas as pd
import os


class MemoryRepository:
    def __init__(
        self,
        current_data_path="data/drug_file.xlsx",
        previous_data_path="data/prev_drug_file.xlsx",
    ):
        """메모리 DB (이전 데이터 비교 후 새로운 데이터만 저장)"""
        self.data = set()  # 새로운 데이터 저장소
        self.previous_data_path = previous_data_path
        self.previous_data = set()  # 이전 데이터 저장소

        # 기존 데이터 불러오기
        if os.path.exists(previous_data_path):
            self.load_previous_data(previous_data_path)

        # 현재 데이터 읽어서 변경된 데이터만 저장
        self.load_new_data(current_data_path)

    def load_previous_data(self, file_path):
        """이전 데이터를 Excel에서 불러와 set으로 저장 (중복 방지)"""
        df = pd.read_excel(file_path, dtype=str).fillna("")
        for _, row in df.iterrows():
            key = (
                row["company_name"],
                row["brand_name"],
                row["inn_name"],
                row["code_name"],
            )
            self.previous_data.add(key)  # 기존 데이터 저장

    def load_new_data(self, file_path):
        """현재 데이터를 읽고, 이전 데이터에 없는 새로운 데이터만 저장"""
        df = pd.read_excel(file_path, dtype=str).fillna("")
        for _, row in df.iterrows():
            key = (
                row["company_name"],
                row["brand_name"],
                row["inn_name"],
                row["code_name"],
            )
            if key not in self.previous_data:
                self.data.add(key)  # 새로운 데이터만 저장

    def save_updated_data(self, data, output_path):
        """변경된 데이터를 Excel 파일로 저장"""
        df = pd.DataFrame(
            data,
            columns=["company_name", "brand_name", "inn_name", "code_name"],
        )
        df.to_excel(output_path, index=False)

        # 새로운 데이터를 previous_drug_file.xlsx에 추가
        all_data = list(self.previous_data | self.data)  # 기존 데이터 + 새로운 데이터
        prev_df = pd.DataFrame(
            all_data, columns=["company_name", "brand_name", "inn_name", "code_name"]
        )
        prev_df.to_excel(self.previous_data_path, index=False)
