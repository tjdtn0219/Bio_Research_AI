from processor import process_excel

if __name__ == "__main__":
    output_file = "data/Organized_Drug_Profile.xlsx"

    print("======== 실행 중 ========")

    process_excel(output_file)
    print(f"✅ 파일이 성공적으로 저장되었습니다: {output_file}")
