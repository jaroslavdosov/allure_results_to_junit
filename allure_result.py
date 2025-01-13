import json

class AllureResult:
    def __init__(self, file, path):
        self.time = ""
        self.name = ""
        self.status = ""
        self.message = ""
        self.trace = ""
        self.fullName = ""
        self.automation_id = ""
        self.testClass = ""
        self.testMethod = ""
        self.steps = list()
        self.attachments = list()
        with open(file) as f:
            result = json.load(f)
        self.name = result["name"]
        self.fullName = result["fullName"]
        self.time = int(result["stop"] - result["start"])/1000
        self.status = result["status"]

        for step in result["steps"]:
            self.steps.append(step["status"] + ": " + step["name"])
        for label in result["labels"]:
            if label["name"] == "testClass":
                self.testClass = label["value"]
        for label in result["labels"]:
            if label["name"] == "testMethod":
                self.testMethod = label["value"]
        self.automation_id = self.testClass + "." + self.testMethod

        if self.status != "passed":
            self.trace = result["statusDetails"]["trace"]
            self.message = result["statusDetails"]["message"]
            for attachment in result["attachments"]:
                self.attachments.append(path + attachment["source"])


