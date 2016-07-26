#!/usr/bin/python

import bottle

from markdown_subject_filter import collect_relevant_sections_from_file

@bottle.get('/')
def get_index():
  return '''
    <input id="queryField" placeholder="keywords" oninput="updateResultsSoon(this.value)" />
    <div id="results" />

    <script>
      function updateResults(query) {
        var request = new XMLHttpRequest();
        request.open('get', '/search?q='+query);
        request.onload = function() {
          document.getElementById('results').innerHTML = this.responseText;
        }
        request.send();
      }

      var lastUpdateResultsSoonTime;
      function updateResultsSoon(query) {
        var calledAt = new Date().getTime();
        lastUpdateResultsSoonTime = calledAt;
        setTimeout(function(){if (lastUpdateResultsSoonTime==calledAt) updateResults(query);}, 300);
      }

      updateResults('');
      document.getElementById('queryField').focus();
    </script>
    '''

@bottle.get('/search')
def get_search():
  return collect_relevant_sections_from_file(
    path=args.file,
    query=bottle.request.query['q'],
    output_format='html')

if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('file')
  args = parser.parse_args()

  bottle.run(host='localhost', port=8080, debug=True)
