##
# Author: Justin A. Hathaway
# Class: CS 391
# Assignment: Final Project
##

import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

# Load our data into a dataframe
df = pd.read_csv("data\wine\winemag-data_first150k.csv")
df_2 = pd.read_csv("data\wine\winemag-data-130k-v2.csv")

print(df)