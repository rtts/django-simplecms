import os, re, argparse, shutil, example, cms
from pip._internal.operations import freeze as pip


def main():
    parser = argparse.ArgumentParser(description='SimpleCMS')
    parser.add_argument('project_name', nargs='?', default='.')
    project_name = parser.parse_args().project_name
    if project_name == '.':
        project_dir = os.getcwd()
        project_name = os.path.basename(project_dir)
    else:
        project_dir = os.path.join(os.getcwd(), project_name)
    if re.match(r'^\w+$', project_name):
        if input(f'Do you want to create a new project in `{project_dir}` ?\033[1D') in 'Yy':
            create_project(project_name, project_dir)
    else:
        print(f'Invalid project name: {project_name}')


def create_project(project_name, project_dir):
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
        for line in pip.freeze():
            if 'django_simplecms' in line:
                line = f'django-simplecms=={cms.__version__}'
            print(line, file=f)

    shutil.copytree(os.path.dirname(example.__file__),os.path.join(project_dir, project_name), dirs_exist_ok=True)
    with open(os.open(os.path.join(project_dir, 'manage.py'), os.O_CREAT|os.O_WRONLY, 0o755), 'w') as f:
        print('#!/usr/bin/env python',
              'import os, sys',
              f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')",
              'from django.core.management import execute_from_command_line',
              'execute_from_command_line(sys.argv)',
              sep='\n', file=f)
    with open(os.path.join(project_dir, project_name, 'wsgi.py'), 'w') as f:
        print('import os',
              'from django.core.wsgi import get_wsgi_application',
              f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')",
              'application = get_wsgi_application()',
              sep='\n', file=f)
    with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
        print('*.pyc\n__pycache__/', file=f)

    print(f'Successfully created project "{project_name}"',
          '',
          'Things to do next:',
          '- create a database',
          '- ./manage.py makemigrations',
          '- ./manage.py migrate',
          '- ./manage.py createsuperuser',
          '- ./manage.py runserver',
          sep='\n')


if __name__ == '__main__':
    main()
