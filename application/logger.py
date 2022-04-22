from datetime import datetime
import re


def logger(path_to_logs):

    def logger_(function):

        def add_info_file(*args, **kwargs):
            func_name = str(function.__name__)
            old_function = function(*args, **kwargs)
            regex = r"(\d*\-\d*\-\d*)[\s](\d*\:\d*\:\d*)(\.\d*)"
            subst = "date: \\1 | time: \\2"
            time = str(datetime.today())
            sub = re.sub(regex, subst, time)
            name = str(f"function called - {sub} | name:'{func_name}' | arguments: {args} {kwargs} | result: {old_function}" + "\n")
            with open(f'{path_to_logs}', 'a', encoding="utf-8") as file:
                file.write(name)

            return old_function

        return add_info_file

    return logger_
