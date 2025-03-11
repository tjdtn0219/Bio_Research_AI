from memory_repository import MemoryRepository
from aggregator import merge_all_data
import pandas as pd
import time


def process_excel(output_path):
    """새로운 데이터만 저장"""
    repo = MemoryRepository()  # 변경된 데이터만 저장됨

    if not repo.data:
        print("데이터의 변경사항이 없습니다.")
        return

    start_time = time.time()

    aggregated_data = merge_all_data(list(repo.data))

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"⏱ 실행 시간: {execution_time:.4f} seconds")

    repo.save_updated_data(aggregated_data, output_path)

    print(f"✅ 파일이 성공적으로 저장되었습니다: {output_path}")
