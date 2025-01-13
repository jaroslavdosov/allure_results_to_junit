import xml.etree.ElementTree as ET

class ReportCreator:
    def createReport(self, metaData, results, work_path):
        testsuite = createTestSuite(metaData.name, metaData.tests, metaData.failures, metaData.errors, metaData.time, metaData.skipped, metaData.timestamp, results)

        tree = ET.ElementTree(testsuite)
        with open(work_path + "junit_report.xml", "wb") as f:
            tree.write(f, encoding="UTF-8", xml_declaration=True)


def createTestSuite(name, tests, failures, errors, time, skipped, timestamp, results):
    # мета инфа
    testsuite = ET.Element(
    "testsuite",
    {
        "xsi:noNamespaceSchemaLocation": "https://raw.githubusercontent.com/jenkinsci/xunit-plugin/ae25da5089d4f94ac6c4669bf736e4d416cc4665/src/main/resources/org/jenkinsci/plugins/xunit/types/model/xsd/junit-10.xsd",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "name": f"{name}",
        "tests": f"{tests}",
        "failures": f"{failures}",
        "errors": f"{errors}",
        "time": f"{time}",
        "skipped": f"{skipped}",
        "timestamp": f"{timestamp}",
    },
)
    for result in results:
        testcase = ET.SubElement(
            testsuite,
            "testcase",
            {
                "name": f"{result.testMethod}",
                "time": f"{result.time}",
                "classname": f"{result.testClass}",
            },
        )

        # добавляем проперти для теста
        properties = ET.SubElement(testcase, "properties")
        property_list = list()
        property_list.append({"name": "testrail_case_field", "value": "type_name:Automated"})

        if result.status != "passed":
            ET.SubElement(testcase, "failure", {
                "message": f"{result.message}",
                "type": "error"
            }).text = result.trace

        for step in result.steps:
            property_list.append({"name": "testrail_result_step", "value": f"{step}"})

        for attachment in result.attachments:
            property_list.append({"name": "testrail_attachment", "value": f"{attachment}"})

        for prop in property_list:
            ET.SubElement(properties, "property", prop)
        property_list.clear()
    return testsuite