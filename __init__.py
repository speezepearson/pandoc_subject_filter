import os
import glob
import subprocess

FILTER_PATH=os.path.join(os.path.dirname(__file__), 'subject_filter.py')

def collect_relevant_sections_from_file(path:str, query:str, output_format:str='markdown') -> str:
  p = subprocess.Popen(['pandoc', '--to', output_format, '--filter', FILTER_PATH, '--metadata=subject-query:{}'.format(query), path], stdout=subprocess.PIPE)
  out, err = p.communicate()
  if p.returncode != 0:
    raise subprocess.SubprocessError()
  return out.decode()

def collect_relevant_sections_from_dir(path:str, *args, **kwargs) -> str:
  return '\n\n'.join(
    collect_relevant_sections_from_file(path=filepath, *args, **kwargs)
    for filepath in
    list(glob.glob(os.path.join(path, '*.md'))) +
    list(glob.glob(os.path.join(path, '*.markdown'))))
