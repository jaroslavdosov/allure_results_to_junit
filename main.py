from sys import argv
import os
import glob

from allure_result import AllureResult
from metaData import MetaData
from report_creator import ReportCreator


def main():
    work_path = argv[1]
    results = list()

    # Получаем отсортированный список файлов
    sorted_files = get_sorted_json_files(work_path)

    #  Получаем данные по всем тестам
    for file in sorted_files:
        results.append(AllureResult(file, work_path))

    # Убираем повторы перезапусков
    unique_results = delete_retries(results)

    # Получаем meta данные
    metaData = MetaData(unique_results)


    # формируем xml
    reportCreator = ReportCreator()
    reportCreator.createReport(metaData, unique_results, work_path)

def delete_retries(results):
    filtered_results = {}
    for result in results:
        if result.fullName not in filtered_results or filtered_results[result.fullName].status != "passed":
            filtered_results[result.fullName] = result

    return list(filtered_results.values())


def get_sorted_json_files(directory):
    files = glob.glob(os.path.join(directory, "*.json"))
    files.sort(key=os.path.getctime, reverse=True)
    return files

if __name__ == "__main__":
    main()