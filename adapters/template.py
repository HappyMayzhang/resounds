import re, json

def codeBlock(lang, code):
    return [
        '```' + lang,
        json.dumps(code, ensure_ascii=False),
        '```'
    ]

def template(example, model_type):
    instructions = example['instructions']
    if model_type == 'chat':
        instructions = "Return answer in json format, key is 'xiaoya'. " + instructions
    prompt = [
        [
            '### Instructions',
            instructions
        ]
    ]
    if model_type == 'text' and 'tools' in example:
        prompt.append([
            '### Functions that can be called',
            '- JSON Schema:',
            *codeBlock('JSON Schema', example['tools'])
        ])
    if 'context' in example:
        prompt.append([
            '### Please answer the questions based on the following knowledge',
            example['context']
        ] if isinstance(example['context'], str) else
        [
            '### Please answer the questions based on the following knowledge',
            '- JSON Schema:',
            *codeBlock('JSON Schema', example['context']["schema"]),
            '- Value:',
            *codeBlock('json', example['context']["kwargs"])
        ])
    prompt.extend([
        [
            '### Input',
            '- JSON Schema:',
            *codeBlock('JSON Schema', example['inputs']["schema"]),
            '- Value:',
            *codeBlock('json', example['inputs']["kwargs"])
        ],
        [
            '### Output',
            '- JSON Schema:',
            *codeBlock('JSON Schema', example['output']["schema"]),
            '- Value:',
        ]
    ])
    return '\n\n'.join(['\n'.join(part) for part in prompt])

def extract(choice, model_type):
    results = []
    code_block = r'```.*\n([^\0]+?)\n```'
    m = re.findall(code_block, choice)
    if not m:
        results.append(choice)
    else:
        results.extend(m)

    answers = []
    for result in results:
        try:
            answer = json.loads(result)
            if model_type == 'chat':
                answer = answer["xiaoya"]
        except KeyError:
            print("Where has 'xiaoya' gone?")
        except:
            answer = result
        answers.append(answer)
    return answers
