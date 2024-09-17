import os
import subprocess


def read_cmds_from_file(file_path):
    """Читает переменную CMDS из файла и возвращает её значение."""
    with open(file_path, 'r') as file:
        content = file.read()
        local_vars = {}
        exec(content, {}, local_vars)
        return local_vars.get('CMDS', [])


def execute_commands(commands):
    """Выполняет команды, пропуская уже выполненные."""
    executed_commands = set()
    for cmd in commands:
        if cmd in executed_commands:
            print(f'команда "{cmd}" уже выполнялась')
        else:
            subprocess.run(cmd, shell=True)
            executed_commands.add(cmd)


def main(directory):
    all_commands = []

    directories = sorted([d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))])

    for dir_name in directories:
        dir_path = os.path.join(directory, dir_name)
        for file in sorted(os.listdir(dir_path)):
            if file.endswith('.py'):
                file_path = os.path.join(dir_path, file)
                commands = read_cmds_from_file(file_path)
                all_commands.extend(commands)

    for file in sorted(os.listdir(directory)):
        if file.endswith('.py'):
            file_path = os.path.join(directory, file)
            commands = read_cmds_from_file(file_path)
            all_commands.extend(commands)
    execute_commands(all_commands)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <dir>")
    else:
        main(sys.argv[1])
