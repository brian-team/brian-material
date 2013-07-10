Brian Modelfitting tutorial
===========================

Notes and slides of the [Brian Model Fitting Tutorial](http://briansimulator.org/brian-tutorial-cns-2013/) at [CNS 2013](http://www.cnsorg.org/cns-2013-paris)


## Required dependencies

  * pip install markdown
  * pip install jinja2
  

## Building the slides

Here are the instructions to convert the `.ipynb` notebook file into an HTML slideshow. You need the development versions of IPython and nbconvert:

  * git clone https://github.com/ipython/ipython.git
  * cd ipython
  * python setupegg.py develop
  * extract https://github.com/hakimel/reveal.js/archive/2.4.0.zip in the folder where `slides.ipynb` is in, and rename the folder to `reveal.js`.
  * ipython nbconvert reveal slides.ipynb
  * the slides will then be in `slides.reveal.html`. Dependencies are reveal.js folder and slides_files folder.

