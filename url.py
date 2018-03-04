#!/usr/bin/env python

from handler.node import Main
from handler.api import SweepCodeCeriticationBefore,SweepCodeCeriticationAfter



urls = [
	(r"/",Main),
	(r"/sweepcodeceriticationbefore",SweepCodeCeriticationBefore),
	(r"/sweepcodeceriticationafter",SweepCodeCeriticationAfter),
]