"""
Template/Options file for altering the structure of the .csv flatfile output.

"""

import collections
headermeasurements = [
    ('observation',            "OBS"), 
    ('data_marking',           "DATAMARKER"), 
    ('statistical_unit_eng',   "STATUNIT"),      'statistical_unit_cym', 
    ('measure_type_eng',       "MEASURETYPE"),   'measure_type_cym', 'observation_type', 'empty', 'obs_type_value', 
    ('unit_multiplier',        "UNITMULTIPLIER"),
    ('unit_of_measure_eng',    "UNITOFMEASURE"), 'unit_of_measure_cym', 'confidentuality', 'empty1', 
    ('geographic_area',        "GEOG"),          'empty2', 'empty3', 
    ('time_dim_item_id',       "TIME"),               
    ('time_dim_item_label_eng',"TIME"),          'time_dim_item_label_cym', 
    ('time_type',              "TIMEUNIT"),      'empty4', 
    ('statistical_population_id',       "STATPOP"),
    ('statistical_population_label_eng',"STATPOP"),
            'statistical_population_label_cym', 'cdid', 'cdiddescrip', 'empty5', 'empty6', 'empty7', 'empty8', 'empty9', 'empty10', 'empty11', 'empty12'
]

headeradditionals = [ 
    ("dim_id",      "NAME"),  ("dimension_label_eng",      "NAME"),  "dimension_label_cym",
    ("dim_item_id", "VALUE"), ("dimension_item_label_eng", "VALUE"), "dimension_item_label_cym",  
    "is_total", "is_sub_total"
]

conversionsegmentnumbercolumn = "empty11"

# Do we want to create a TIMEUNIT dimension using a TIME dimension - ONS specific
SH_Create_ONS_time = True

# Do you want to split the OBS, placing non float data into your next column.
SH_Split_OBS = "DATAMARKER"  # see value set to int value below


####  Below this point is derived data (used in old code) from the above tables


# derive the elements of the headernames above into the values below 
headermeasurementnames = list(collections.OrderedDict.fromkeys(k[1]  for k in headermeasurements  if isinstance(k, tuple)))
dimension_names = headermeasurementnames  # for now

# OLD WAY (to delete and will be over-written)
# we are going to try and convert the values OBS=-9 to use OBS="OBS"
if False:
    headermeasurementnumvalues = dict((item, -i)  for i, item in enumerate(reversed(headermeasurementnames)))
    headermeasurementnumvaluesSet = set(headermeasurementnumvalues.values())


    # Create variables (This is terrible!)
    exec("%s = %s" % (", ".join(headermeasurementnumvalues.keys()), ", ".join(map(str, headermeasurementnumvalues.values()))))
    exec("SH_Split_OBS = %s" % SH_Split_OBS)

# this will be using strings instead of numbers soon, which will remove this one dereference and make things more meaningful
# NEW WAY
else:
    headermeasurementnumvalues = dict((item, item)  for i, item in enumerate(reversed(headermeasurementnames)))
    headermeasurementnumvaluesSet = set(headermeasurementnumvalues.values())
    # Create variables (This is terrible!)
    exec("%s = '%s'" % (", ".join(headermeasurementnames), "', '".join(map(str, headermeasurementnames))))
    exec("SH_Split_OBS = %s" % SH_Split_OBS)


####  Below this point is derived data only used in old code

start = ",".join((k[0] if isinstance(k, tuple) else k) for k in headermeasurements)

SKIP_AFTER = { }
hm = None
for hn in headermeasurements:
    if isinstance(hn, tuple):
        hm = headermeasurementnumvalues[hn[1]]
        SKIP_AFTER[hm] = 0
    elif hm is not None:
        SKIP_AFTER[hm] += 1


# = verify the calculations are the same ========
Dstart = "observation,data_marking,statistical_unit_eng,statistical_unit_cym,measure_type_eng,measure_type_cym,observation_type,empty,obs_type_value,unit_multiplier,unit_of_measure_eng,unit_of_measure_cym,confidentuality,empty1,geographic_area,empty2,empty3,time_dim_item_id,time_dim_item_label_eng,time_dim_item_label_cym,time_type,empty4,statistical_population_id,statistical_population_label_eng,statistical_population_label_cym,cdid,cdiddescrip,empty5,empty6,empty7,empty8,empty9,empty10,empty11,empty12"
assert Dstart == start

# Dimension names (as strings!)
Ddimension_names = ['OBS', 'DATAMARKER', 'STATUNIT', 'MEASURETYPE', 'UNITMULTIPLIER', 'UNITOFMEASURE', 'GEOG', 'TIME', 'TIMEUNIT', 'STATPOP']
assert headermeasurementnames == Ddimension_names

# [Check] Create variables (This is terrible!)
if isinstance(OBS, int):
    for i, item in enumerate(reversed(headermeasurementnames)):
        exec("assert "+item+"==-i")

__all__ = list(headermeasurementnames) # don't expose unnecessary items when using `from foo import *`


# used in the old code
DSKIP_AFTER = {OBS: 0,           # 1..2  MANDATORY, must be here, must be called OBS
              DATAMARKER: 0,     # 2..3
              STATUNIT: 1,       # 3..5
              MEASURETYPE: 4,    # 5..10
              UNITMULTIPLIER: 0, # 10..11
              UNITOFMEASURE: 3,  # 11..15
              GEOG: 2,           # 15..18/19
              TIME: 1,           # 18/19..21
              TIMEUNIT: 1,       # 21..23/24
              STATPOP:11}        # 23/24..36/37

assert SKIP_AFTER == DSKIP_AFTER, (SKIP_AFTER, DSKIP_AFTER)


# = Topic Dimensions ========

# Repeat - list of headers to be repeated for each topic dimension
repeat = "dim_id_{num},dimension_label_eng_{num},dimension_label_cym_{num},dim_item_id_{num},dimension_item_label_eng_{num},dimension_item_label_cym_{num},is_total_{num},is_sub_total_{num}"


# Where in the repeat do you want to output the dimensions name and value?
def get_topic_headers(name, value):  # DONT alter this
    return ([name, name, '', value, value, '', '', ''])   # Change this line

# Where are the values? (should match the above (minus the 'name entries)
value_spread = get_topic_headers('', 'value')
Dvalue_spread = ['', '', '', 'value', 'value', '', '', '']
assert value_spread == Dvalue_spread

# do you want to output the 'name' value in the header of the value columns?
topic_headers_as_dims = False



# ====================== S-P-E-C-I-A-L handling ========================== (..fallout much?)
# Use the following to decide which STANDARD dimensionss should get special handling

# Standard Dimensions that need to be outputted twice in a row (i.e item|label combos)
SH_Repeat = [TIME, STATPOP]

