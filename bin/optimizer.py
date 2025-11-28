import argparse, sys, os
from ..core.config import move_from_save_dir_to_read_dir
from ..core.sample import Sample
from ..tools import induce_instruction

def testsuite(func_name):
    sys.path.append(os.getcwd())
    return __import__(func_name.split('.')[-1])

def color(s, c):
    f = {
        'red'   : "1",
        'green' : "2",
        'yellow': "3",
        'blue'  : "4",
        'violet': "5",
        'cyan'  : "6"
    }
    return f"\033[1;3{f[c]}m{s}\033[0m"

def maintain():
    parser = argparse.ArgumentParser(description="Semantic function optimizer")
    parser.add_argument('func_name', help="module.func_name")
    options = parser.parse_args()

    move_from_save_dir_to_read_dir()
    samples = Sample(options.func_name, testsuite(options.func_name))
    return samples

def show_sample(sample, indent = 0):
    for key, value in sample.items():
        print(' ' * indent + '-', key)
        if indent < 4 and isinstance(value, dict):
            indent += 2
            show_sample(value, indent)
            indent -= 2
        else:
            print(' ' * indent + ' ', value)

def show_info(info):
    print("\n===\n")
    if isinstance(info, dict):
        show_sample(info)
    if isinstance(info, list):
        print("\n".join(info))
    print("\n===\n")

def show_tips(text):
    print(color('Answer:', 'cyan'), color(text, 'blue'))
    print("\n---\n")

def show_menu(level):
    menu = {
        "0": "\n".join([
            color("Menu:", 'red'),
            "",
            color("1) Modify Function Description", 'green'),
            color("2) Summarize Function Descriptions", 'green'),
            color("3) Evaluate Semantic Functions", 'green'),
            "",
            color("Press ^D to return.", 'yellow'),
            color("Press ^C to abort.", 'yellow')
        ]),
        "11": color("Enter New Function Description", 'green'),
        "12": color("Press Enter to Execute Summarization", 'green'),
        "13": color("Enter New Function Description and Press Enter to Evaluate", 'green')
    }
    print(menu[level])

def gets(prompt):
    s = []
    while(True):
        a = input(prompt + ' ')
        b = a.rstrip('\\')
        s.append(b)
        if len(a) == len(b): break
    return '\n'.join(s)

def main():
    samples = maintain()
    level = "0"
    while True:
        show_menu(level)
        try:
            text = gets(color('I pick:', 'violet'))
        except EOFError:
            print("^D")
            if level != "0":
                show_tips("Return to the previous level.")
                level = "0"
                continue
            print('Answer:', "Bye!")
            break
        except KeyboardInterrupt:
            print("")
            print('Answer:', "ByeBye!")
            return
        if level == "0":
            if text == '1':
                try:
                    sample = samples.choice()
                except IndexError:
                    show_tips("There are no samples to be processed.")
                else:
                    show_info(sample)
                    level = "11"
            elif text == '2':
                instructions = samples.instructions()
                if not instructions:
                    show_tips("There are no instructions to be processed.")
                else:
                    show_info(instructions)
                    if len(instructions) > 1:
                        level = "12"
            elif text == '3':
                if not samples.stats['instructions']:
                    show_tips("There is no evaluation record.")
                else:
                    show_info(samples.stats['instructions'])
                level = "13"
            else:
                show_tips("Please enter 1-3.")
        elif level == "11":
            sample['instructions'] = text
            try:
                samples.submit(sample)
                show_info(sample)
            except:
                show_tips("LLM don't work.")
            level = "0"
        elif level == "12":
            try:
                show_tips(induce_instruction(list(instructions.keys())))
            except:
                show_tips("LLM don't work.")
            level = "0"
        elif level == "13":
            try:
                samples.stats['instructions'][text] = samples.evaluate(text)
                show_info(samples.stats['instructions'])
            except:
                show_tips("LLM don't work.")
            level = "0"
    samples.save()

if __name__ == '__main__':
    main()
