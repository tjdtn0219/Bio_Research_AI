from memory_repository import MemoryRepository
from aggregator import merge_all_data
import pandas as pd


def process_excel(output_path):
    """새로운 데이터만 저장"""
    repo = MemoryRepository()  # 변경된 데이터만 저장됨

    if not repo.data:
        print("✅ 변경된 데이터가 없습니다.")
        return

    # 변경된 데이터를 집계하여 저장
    aggregated_data = merge_all_data(list(repo.data))
    repo.save_updated_data(aggregated_data, output_path)
