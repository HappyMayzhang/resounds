from .config import read_example, save_example, read_stats, save_stats
from jsonschema import validate
import json, random # secrets
from time import sleep

class Sample:
    def __init__(self, func_name, testsuite):
        self.sample = {}
        for example in read_example(func_name, ext = '.sample'):
            if "return" not in example['output']: continue
            uid = json.dumps(example['inputs']["kwargs"], ensure_ascii=False)
            if 'context' in example:
                uid += example['context'] \
                       if isinstance(example['context'], str) else \
                       json.dumps(example['context']["kwargs"], ensure_ascii=False)
            if 'tools' in example:
                uid += json.dumps(example['tools'], ensure_ascii=False)
            if 'tool_choice' in example:
                uid += json.dumps(example['tool_choice'], ensure_ascii=False)
            self.sample[uid] = example
        for example in read_example(func_name):
            if "return" not in example['output']: continue
            uid = json.dumps(example['inputs']["kwargs"], ensure_ascii=False)
            if 'context' in example:
                uid += example['context'] \
                       if isinstance(example['context'], str) else \
                       json.dumps(example['context']["kwargs"], ensure_ascii=False)
            if 'tools' in example:
                uid += json.dumps(example['tools'], ensure_ascii=False)
            if 'tool_choice' in example:
                uid += json.dumps(example['tool_choice'], ensure_ascii=False)
            if uid not in self.sample or testsuite.verify(example):
                self.sample[uid] = example
        self.stats = read_stats(func_name)
        self.testsuite = testsuite

    def save(self):
        for example in self.sample.values():
            save_example(example, ext = '.sample')
        save_stats(self.stats)

    def submit(self, example):
        results = self.testsuite.request(example)
        sleep(30)
        for answer in results:
            try:
                validate(instance=answer, schema=example['output']["schema"])
            except:
                pass
            else:
                example['output']["return"] = answer
                return answer
        raise ValueError("Invalid format string")

    def choice(self):
        return random.choice([
            sample
            for sample in self.sample.values()
            if not self.testsuite.verify(sample)
        ])

    def instructions(self):
        report = {}
        for sample in self.sample.values():
            key = sample['instructions']
            value = report.get(key, [0, 0])
            if self.testsuite.verify(sample):
                value[1] += 1
            else:
                value[0] += 1
            report[key] = value
        return report

    def evaluate(self, instructions):
        value = [0, 0]
        for sample in self.sample.values():
            example = sample.copy()
            example['instructions'] = instructions
            example['output'] = sample['output'].copy()
            self.submit(example)
            if self.testsuite.verify(example):
                sample['instructions'] = example['instructions']
                sample['output'] = example['output']
                value[1] += 1
            else:
                value[0] += 1
        return value
