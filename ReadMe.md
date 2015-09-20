# Simulation Templates for SMTK and CMB

This repository hosts [SMTK]() workflow descriptions describing what inputs
are required to run a variety of open-source simulation packages.
The workflow descriptions include

+ template files holding definitions of physics models, boundary conditions,
  initial conditions, solver termination conditions, and more.
+ export scripts written in Python that take information from a
  filled-out template and generate an input deck for a simulation.

Together, these can be used
in the [CMB]() application suite
or as part of a custom application built on SMTK
to prepare a simulation scenario.

[SMTK]: https://smtk.readthedocs.org/
[CMB]: http://computationalmodelbuilder.org/

## Supported simulations

We currently target the following simulation packages.

+ [Adaptive Hydraulics (AdH)](http://adh.usace.army.mil/new_webpage/main/main_page.htm):
   a 2d flow simulator aimed at hydrological models.
+ [Albany](https://github.com/gahansen/Albany/wiki):
  a high-performance, parallel, mutliphysics solver
+ [Hydra](http://www.casl.gov/Hydra.shtml):
  a hybrid finite-element/finite-volume incompressible/low-Mach flow solver
  built on the [Hydra toolkit](https://get-hydra.lanl.gov/).
