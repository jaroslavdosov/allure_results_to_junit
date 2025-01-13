from datetime import datetime

class MetaData:
    def __init__(self, allureResults):
        self.name = "auto tests"
        self.tests = 0
        self.failures = 0
        self.errors = 0
        self.time = 0
        self.skipped = 0
        self.timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        for result in allureResults:
            self.tests =  self.tests + 1
            self.time = self.time + result.time
            if result.status == "broken" or result.status == "failed":
                self.failures = self.failures + 1
            if result.status == "skipped":
                self.skipped = self.skipped + 1


