from processor import process_excel

if __name__ == "__main__":
    output_file = "data/aggregated_drug_file.xlsx"

    print("======프로그램 시작======")

    process_excel(output_file)

    print("======프로그램 종료======")
