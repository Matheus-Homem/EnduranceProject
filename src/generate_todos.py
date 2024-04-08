import os

def find_todos(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                full_file_path = os.path.join(root, file)
                if os.path.abspath(full_file_path) == os.path.abspath(__file__):
                    continue
                with open(full_file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '#TODO' in line:
                            yield full_file_path, line

def write_todos_to_md_file(todos, md_file_path):
    with open(md_file_path, 'w') as f:
        for file_path, todo in todos:
            f.write(f'- [ ] **{file_path}**: {todo}\n')

todos = list(find_todos('.'))
write_todos_to_md_file(todos, '../TODO.md')