#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time
import os
import signal
from fonctions import *

#On efface la console
os.system('clear')

#On lit les cartes ou tags en continue
read()
