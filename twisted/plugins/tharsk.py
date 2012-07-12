# -*- coding: utf-8 -*-
from twisted.application.service import ServiceMaker


TharskService = ServiceMaker(
    "Tharsk Web Server",
    "tharsk.app",
    "The φarsk dictionary web server.",
    "tharsk")
