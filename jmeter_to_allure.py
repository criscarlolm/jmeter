import xml.etree.ElementTree as ET
import json
import os

def convert_jtl_to_allure(jtl_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tree = ET.parse(jtl_file)
    root = tree.getroot()

    for index, sample in enumerate(root.findall(".//sampleResult")):
        test_case = {
            "name": sample.attrib.get("label", f"Test {index + 1}"),
            "status": "passed" if sample.attrib.get("success") == "true" else "failed",
            "start": int(sample.attrib.get("ts", "0")),
            "stop": int(sample.attrib.get("ts", "0")) + int(sample.attrib.get("t", "0")),
            "parameters": {
                "responseCode": sample.attrib.get("rc", "N/A"),
                "responseMessage": sample.attrib.get("rm", "N/A"),
                "threadName": sample.attrib.get("tn", "N/A"),
            },
        }

        with open(os.path.join(output_dir, f"result-{index}.json"), "w") as f:
            json.dump(test_case, f, indent=4)

if __name__ == "__main__":
    jtl_file = "/path/to/results.jtl"
    output_dir = "/path/to/allure-results"
    convert_jtl_to_allure(jtl_file, output_dir)
