# GH Gym

# download or load data
from CBData import CBData
can = CBData.loadData()
CBData.cleanData(can)
can = can.drop_duplicates()
can 

# benedict_bornder_constants critical=True
