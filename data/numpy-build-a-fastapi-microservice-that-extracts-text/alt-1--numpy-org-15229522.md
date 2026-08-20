---
library: "numpy"
query: "Build a FastAPI microservice that extracts text from uploaded PDF resumes, embeds them with sentence-transformers, and ranks them against a job description"
url: "https://numpy.org/"
role: "alternate"
rank: 1
fetched_at: "2026-08-20T15:09:56.602692+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "696e46c82759a06257ab7e4fbf2626838e331f203bdf677692c78c59b4d1c6c6"
---

NumPy ![NumPy logo. ](/images/logo.svg)

The fundamental package for scientific computing with Python

[NumPy 2.5.0 released!](/news)

[2026-06-21](/news)

Powerful N-dimensional arrays

Fast and versatile, the NumPy vectorization, indexing, and broadcasting concepts are the de-facto standards of array computing today.

Numerical computing tools

NumPy offers comprehensive mathematical functions, random number generators, linear algebra routines, Fourier transforms, and more.

Open source

Distributed under a liberal [BSD license](https://github.com/numpy/numpy/blob/main/LICENSE.txt) , NumPy is developed and maintained [publicly on GitHub](https://github.com/numpy/numpy) by a vibrant, responsive, and diverse [community](/community/) .

Interoperable

NumPy supports a wide range of hardware and computing platforms, and plays well with distributed, GPU, and sparse array libraries.

Performant

The core of NumPy is well-optimized C code. Enjoy the flexibility of Python with the speed of compiled code.

Easy to use

NumPy’s high level syntax makes it accessible and productive for programmers from any background or experience level.

Try NumPy

Use the interactive shell to try NumPy in the browser

```
"""
To try the examples in the browser:
1. Type code in the input cell and press
   Shift + Enter to execute
2. Or copy paste the code, and click on
   the "Run" button in the toolbar
"""

# The standard way to import NumPy:
import numpy as np

# Create a 2-D array, set every second element in
# some rows and find max per row:

x = np.arange(15, dtype=np.int64).reshape(3, 5)
x[1:, ::2] = -99
x
# array([[  0,   1,   2,   3,   4],
#        [-99,   6, -99,   8, -99],
#        [-99,  11, -99,  13, -99]])

x.max(axis=1)
# array([ 4,  8, 13])

# Generate normally distributed random numbers:
rng = np.random.default_rng()
samples = rng.normal(size=2500)
samples
```

# ECOSYSTEM

Nearly every scientist working in Python draws on the power of NumPy.

NumPy brings the computational power of languages like C and Fortran to Python, a language much easier to learn and use. With this power comes simplicity: a solution in NumPy is often clear and elegant.

* ![A computer chip.](/images/content_images/sc_dom_img/quantum_computing.svg)+ [QuTiP](https://qutip.org)
  + [PyQuil](https://pyquil-docs.rigetti.com/en/stable)
  + [Qiskit](https://qiskit.org)
  + [PennyLane](https://pennylane.ai)
* ![A line graph with the line moving up.](/images/content_images/sc_dom_img/statistical_computing.svg)+ [Pandas](https://pandas.pydata.org/)
  + [statsmodels](https://www.statsmodels.org/)
  + [Xarray](https://xarray.pydata.org/en/stable/)
  + [Seaborn](https://seaborn.pydata.org/)
* ![A bar chart with positive and negative values.](/images/content_images/sc_dom_img/signal_processing.svg)+ [SciPy](https://scipy.org)
  + [PyWavelets](https://pywavelets.readthedocs.io/)
  + [python-control](https://python-control.org/)
  + [HyperSpy](https://hyperspy.org/)
* ![A photograph of the mountains.](/images/content_images/sc_dom_img/image_processing.svg)+ [Scikit-image](https://scikit-image.org/)
  + [OpenCV](https://opencv.org/)
  + [Mahotas](https://mahotas.rtfd.io/)
* ![A simple graph.](/images/content_images/sc_dom_img/sd6.svg)+ [NetworkX](https://networkx.org/)
  + [graph-tool](https://graph-tool.skewed.de/)
  + [igraph](https://igraph.org/python/)
  + [PyGSP](https://pygsp.rtfd.io/)
* ![A telescope.](/images/content_images/sc_dom_img/astronomy_processes.svg)+ [AstroPy](https://www.astropy.org/)
  + [SunPy](https://sunpy.org/)
  + [SpacePy](https://spacepy.github.io/)
* ![A human head with gears.](/images/content_images/sc_dom_img/cognitive_psychology.svg)+ [PsychoPy](https://www.psychopy.org/)
* ![A strand of DNA.](/images/content_images/sc_dom_img/bioinformatics.svg)+ [BioPython](https://biopython.org/)
  + [Scikit-Bio](http://scikit-bio.org/)
  + [PyEnsembl](https://github.com/openvax/pyensembl)
  + [ETE](http://etetoolkit.org/)
* ![A graph with a bell-shaped curve.](/images/content_images/sc_dom_img/bayesian_inference.svg)+ [PyStan](https://pystan.readthedocs.io/en/latest/)
  + [PyMC](https://docs.pymc.io/)
  + [ArviZ](https://arviz-devs.github.io/arviz/)
  + [emcee](https://emcee.readthedocs.io/)
* ![Four mathematical symbols.](/images/content_images/sc_dom_img/mathematical_analysis.svg)+ [SciPy](https://scipy.org)
  + [SymPy](https://www.sympy.org/)
  + [cvxpy](https://www.cvxpy.org/)
  + [FEniCS](https://fenicsproject.org/)
* ![A test tube.](/images/content_images/sc_dom_img/chemistry.svg)+ [Cantera](https://cantera.org/)
  + [MDAnalysis](https://www.mdanalysis.org/)
  + [RDKit](https://github.com/rdkit/rdkit)
  + [PyBaMM](https://www.pybamm.org/)
* ![The Earth.](/images/content_images/sc_dom_img/geoscience.svg)+ [Pangeo](https://pangeo.io/)
  + [Simpeg](https://simpeg.xyz/)
  + [ObsPy](https://github.com/obspy/obspy/wiki)
  + [Fatiando a Terra](https://www.fatiando.org/)
* ![A map.](/images/content_images/sc_dom_img/GIS.svg)+ [Shapely](https://shapely.readthedocs.io/)
  + [GeoPandas](https://geopandas.org/)
  + [Folium](https://python-visualization.github.io/folium)
* ![A microprocessor development board.](/images/content_images/sc_dom_img/robotics.svg)+ [COMPAS](https://compas.dev/)
  + [City Energy Analyst](https://cityenergyanalyst.com/)
  + [Sverchok](https://nortikin.github.io/sverchok/)

NumPy's API is the starting point when libraries are written to exploit innovative hardware, create specialized array types, or add capabilities beyond what NumPy provides.

|  |  |  |
| --- | --- | --- |
|  | Array Library | Capabilities & Application areas |
| Dask | [Dask](https://dask.org/) | Distributed arrays and advanced parallelism for analytics, enabling performance at scale. |
| CuPy | [CuPy](https://cupy.dev) | NumPy-compatible array library for GPU-accelerated computing with Python. |
| JAX | [JAX](https://docs.jax.dev) | Composable transformations of NumPy programs: differentiate, vectorize, just-in-time compilation to GPU/TPU. |
| xarray | [Xarray](https://xarray.pydata.org/en/stable/index.html) | Labeled, indexed multi-dimensional arrays for advanced analytics and visualization. |
| sparse | [Sparse](https://sparse.pydata.org/en/latest/) | NumPy-compatible sparse array library that integrates with Dask and SciPy's sparse linear algebra. |
| PyTorch | [PyTorch](https://pytorch.org/) | Deep learning framework that accelerates the path from research prototyping to production deployment. |
| TensorFlow | [TensorFlow](https://www.tensorflow.org) | An end-to-end platform for machine learning to easily build and deploy ML powered applications. |
| arrow | [Arrow](https://arrow.apache.org/) | A cross-language development platform for columnar in-memory data and analytics. |
| xtensor | [xtensor](https://github.com/xtensor-stack/xtensor-python) | Multi-dimensional arrays with broadcasting and lazy computing for numerical analysis. |
| awkward | [Awkward Array](https://awkward-array.org/) | Manipulate JSON-like data with NumPy-like idioms. |
| uarray | [uarray](https://uarray.org/en/latest/) | Python backend system that decouples API from implementation; unumpy provides a NumPy API. |
| tensorly | [tensorly](http://tensorly.org/stable/home.html) | Tensor learning, algebra and backends to seamlessly use NumPy, PyTorch, TensorFlow or CuPy. |
| blosc2 | [Blosc2](https://www.blosc.org/python-blosc2/) | Accelerated computation for in-memory, on-disk, or remote compressed arrays. |

[![Diagram of Python Libraries. The five catagories are 'Extract, Transform, Load', 'Data Exploration', 'Data Modeling', 'Data Evaluation' and 'Data Presentation'.](/images/content_images/ds-landscape.png)](/images/content_images/ds-landscape.png)

NumPy lies at the core of a rich ecosystem of data science libraries. A typical exploratory data science workflow might look like:

* **Extract, Transform, Load:**  [Pandas](https://pandas.pydata.org) , [Intake](https://intake.readthedocs.io) , [PyJanitor](https://pyjanitor-devs.github.io/pyjanitor/)
* **Exploratory analysis:**  [Jupyter](https://jupyter.org) , [Seaborn](https://seaborn.pydata.org) , [Matplotlib](https://matplotlib.org) , [Altair](https://altair-viz.github.io)
* **Model and evaluate:**  [scikit-learn](https://scikit-learn.org) , [statsmodels](https://www.statsmodels.org/stable/index.html) , [PyMC](https://docs.pymc.io) , [spaCy](https://spacy.io)
* **Report in a dashboard:**  [Dash](https://plotly.com/dash) , [Panel](https://panel.holoviz.org) , [Voila](https://voila.readthedocs.io/)

For high data volumes, [Dask](https://dask.org) and [Ray](https://ray.io/) are designed to scale. Stable deployments rely on data versioning ( [DVC](https://dvc.org) ), experiment tracking ( [MLFlow](https://mlflow.org) ), and workflow automation ( [Airflow](https://airflow.apache.org) , [Dagster](https://dagster.io) and [Prefect](https://www.prefect.io) ).

![Diagram of three overlapping circles. The circles are labeled 'Mathematics', 'Computer Science' and 'Domain Expertise'. In the middle of the diagram, which has the three circles overlapping it, is an area labeled 'Data Science'.](/images/content_images/data-science.png)

[![An animated gif showing a three-dimensional graph of embeddings made in Tensorflow.](/images/content_images/ml_img/tensorflow-ml-anim.gif)](https://ai.googleblog.com/2016/12/open-sourcing-embedding-projector-tool.html)

*[Source: Google AI Blog](https://ai.googleblog.com/2016/12/open-sourcing-embedding-projector-tool.html)*

NumPy forms the basis of powerful machine learning libraries like [scikit-learn](https://scikit-learn.org) and [SciPy](https://scipy.org) . As machine learning grows, so does the list of libraries built on NumPy. [TensorFlow’s](https://www.tensorflow.org) deep learning capabilities have broad applications — among them speech and image recognition, text-based applications, time-series analysis, and video detection. [PyTorch](https://pytorch.org) , another deep learning library, is popular among researchers in computer vision and natural language processing.

Statistical techniques called [ensemble methods](https://scikit-learn.org/stable/modules/ensemble.html) such as binning, bagging, stacking, and boosting are among the ML algorithms implemented by tools such as [XGBoost](https://xgboost.readthedocs.io/) , [LightGBM](https://lightgbm.readthedocs.io/en/latest/) , and [CatBoost](https://catboost.ai) — one of the fastest inference engines. [Yellowbrick](https://www.scikit-yb.org/en/latest/) and [Eli5](https://eli5.readthedocs.io/en/latest/) offer machine learning visualizations.

[![A streamplot made in matplotlib](/images/content_images/v_matplotlib.png)](https://www.fusioncharts.com/blog/best-python-data-visualization-libraries)

[![A scatter-plot graph made in ggpy](/images/content_images/v_ggpy.png)](https://github.com/yhat/ggpy)

[![A box-plot made in plotly](/images/content_images/v_plotly.png)](https://www.journaldev.com/19692/python-plotly-tutorial)

[![A streamgraph made in altair](/images/content_images/v_altair.png)](https://altair-viz.github.io/gallery/streamgraph.html)

[![A pairplot of two types of graph, a plot-graph and a frequency graph made in seaborn"](/images/content_images/v_seaborn.png)](https://seaborn.pydata.org)

[![A 3D volume rendering made in PyVista.](/images/content_images/v_pyvista.png)](https://pyvista.org)

[![A multi-dimensionan image made in napari.](/images/content_images/v_napari.png)](https://napari.org)

[![A Voronoi diagram made in vispy.](/images/content_images/v_vispy.png)](https://vispy.org/gallery/index.html)

NumPy is an essential component in the burgeoning [Python visualization landscape](https://pyviz.org/overviews/index.html) , which includes [Matplotlib](https://matplotlib.org) , [Seaborn](https://seaborn.pydata.org) , [Plotly](https://plot.ly) , [Altair](https://altair-viz.github.io) , [Bokeh](https://docs.bokeh.org/en/latest/) , [Holoviz](https://holoviz.org) , [Vispy](http://vispy.org) , [Napari](https://napari.org/) , and [PyVista](https://pyvista.org) , to name a few.

NumPy’s accelerated processing of large arrays allows researchers to visualize datasets far larger than native Python could handle.

# CASE STUDIES

[First Image of a Black Hole

![First image of a black hole. It is an orange circle in a black background.](/images/content_images/case_studies/blackhole.png)

How NumPy, together with libraries like SciPy and Matplotlib that depend on NumPy, enabled the Event Horizon Telescope to produce the first ever image of a black hole](/case-studies/blackhole-image) [Detection of Gravitational Waves

![Two orbs orbiting each other. They are displacing gravity around them.](/images/content_images/case_studies/gravitional.png)

In 1916, Albert Einstein predicted gravitational waves; 100 years later their existence was confirmed by LIGO scientists using NumPy.](/case-studies/gw-discov) [Sports Analytics

![Cricket ball on green field.](/images/content_images/case_studies/sports.jpg)

Cricket Analytics is changing the game by improving player and team performance through statistical modelling and predictive analytics. NumPy enables many of these analyses.](/case-studies/cricket-analytics) [Pose Estimation using deep learning

![Cheetah pose analysis](/images/content_images/case_studies/deeplabcut.png)

DeepLabCut uses NumPy for accelerating scientific studies that involve observing animal behavior for better understanding of motor control, across species and timescales.](/case-studies/deeplabcut-dnn)
