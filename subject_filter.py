#!/home/spencer/.virtualenv/3.4/bin/python

import re
import pandocfilters

class SubjectFilter:
  def __init__(self):
    self.subjects = None
    self.level_of_current_matching_section = None

  def __call__(self, key, value, format, meta):
    if self.subjects is None:
      self.subjects = set(meta['subject-query']['c'].split(' '))

    if key == 'Header':
      level, (identifier, classes, attrs), content = value
      normalized_header = ' '.join(v['c'].lower() for v in content if v['t'] == 'Str')
      header_matches_subjects = any(
        any(subject in c for c in classes) or subject in normalized_header
        for subject in self.subjects)
      if self.level_of_current_matching_section is None:
        if header_matches_subjects:
          self.level_of_current_matching_section = level
      elif level <= self.level_of_current_matching_section:
        self.level_of_current_matching_section = (level if header_matches_subjects else None)

    return (pandocfilters.Null() if self.level_of_current_matching_section is None else None)

_f = SubjectFilter()
_m = {'subject-query': {'t':'MetaString', 'c':'good'}}
_doc = [
  ('Header', [1, ['', ['good'], []], {}]),
  ('Header', [2, ['', ['good'], []], {}]),
  ('Header', [2, ['', [], []], {}]),
  ('Header', [1, ['', [], []], {}]),
  ('Header', [2, ['', ['good'], []], {}])]
assert [0,1,2,4] == [i for i,(k,v) in enumerate(_doc) if _f(k,v,'html',_m) is None]

if __name__ == '__main__':
  pandocfilters.toJSONFilter(SubjectFilter())
