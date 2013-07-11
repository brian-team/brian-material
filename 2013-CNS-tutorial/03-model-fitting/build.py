from IPython.nbconvert.exporters import RevealExporter
from IPython.config import Config

from IPython.nbformat import current as nbformat

infile = "slides.ipynb" # load the name of your slideshow
outfile = "slides.reveal.html"

notebook = open(infile).read()
notebook_json = nbformat.reads_json(notebook)

# This is the config object I talked before, in the 'url_prefix', 
# you can set you proper location of your local reveal.js library,
# i.e. if the reveal.js is located in the same directory as your 
# your_slideshow.reveal.html, then set 'url_prefix':'reveal.js'.
c = Config({
            'RevealHelpTransformer':{
                'enabled':True,
                'url_prefix':'reveal.js',
                },                
            })

exportHtml = RevealExporter(config=c)
(body,resources) = exportHtml.from_notebook_node(notebook_json)

open(outfile, 'w').write(body.encode('utf-8'))
