#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import shutil


class ReleaseAssignment(object):

    def __init__(self, dir_name):
        self.course_id = 'info490-fa16'
        self.export_root = '/export'
        self.dir_name = dir_name
        self.student_list = 'studentlist'

    @property
    def hw_dir(self):
        return os.path.join(self.dir_name, 'assignments')

    def _hw_dir_exists(self):
        if os.path.exists(self.dir_name) and os.path.exists(self.hw_dir):
            return True

    @property
    def hw_dir_files(self):
        if self._hw_dir_exists():
            return os.listdir(self.hw_dir)

    @property
    def num_notebooks(self):
        files = self.hw_dir_files
        notebooks = [nb for nb in files if nb.endswith('.ipynb')]
        return len(notebooks)

    def is_draft_in_readme(self):
        if self._hw_dir_exists():
            readme_path = os.path.join(self.hw_dir, 'README.md')
            result = ['Draft_Version_picture.png' in line
                for line in open(readme_path)]
            return any(result)

    def is_warning_a_file(self):
        files = self.hw_dir_files
        if 'WARNING_DRAFT_VERSION_DO_NOT_START' in files:
            return True

    def is_ready(self):
        if (self.num_notebooks == 3 and
            not self.is_draft_in_readme() and
            not self.is_warning_a_file()):
            return True

    @property
    def students(self):
        names = []
        with open(self.student_list) as f:
            for line in f:
                if line.isspace():
                    continue
                parts = line.strip().split()
                name = parts[0]
                names.append(name)
        return names

    def copy(self, assignment):
        if self.is_ready():
            for student in self.students:
                target_path = os.path.join(
                    self.export_root, 'exchange', student,
                    self.course_id, 'outbound', assignment
                )
                shutil.copytree(self.hw_dir, target_path)
                sys.stdout.write(
                "Released assignments for {} from {}\n".format(student, self.hw_dir)
                )
        else:
            raise RuntimeError("Not ready yet.")

def main(arg1, arg2):

    hw = ReleaseAssignment(arg1)
    try:
        hw.copy(arg2)
    except Exception, err:
        sys.stderr.write("Assignments: {}\n".format(str(err)))

if __name__ == '__main__':

    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except IndexError:
        sys.stderr.write("Usage: release_assignment.py </path/to/WeekX> <hw01>\n")
        sys.exit(1)

    main(arg1, arg2)

