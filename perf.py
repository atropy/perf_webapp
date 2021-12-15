# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 23:49:46 2021

Function Module file for perf views

@author: atharva.tanksale
"""
import pandas as pd

# ---------------------------------------------------

def calc_field(data, x_ax, fields, view, factor = 1, agg_func = 'sum'):
    """
    Takes filtered data and outputs a pivot table with calculated field
    x_ax   = Field that forms the x axis of the view; MOB for example
    fields = A list of fields used as input that are used to create 
            the calculated field 
            Also requires a minimum of 2 fields
    agg_func= The aggregate function to be used; for example 'sum'/'average'
    view   = a string with the name of the calculated field 
    
    
    Note : Input data must contain the columns passed as fields
    
    """
    # Data Checks
    cols = data.columns
    if len(set(fields) - set(fields).intersection(list(data.columns))) > 0:
#         print(len(set(fields) - set(fields).intersection(list(data.columns))))
        raise Exception('Data is missing a column')
    if len(fields) < 2:
        raise Exception('Check the number of fields used as inputs; should be at least 2')
    
    # Operative part
    k = pd.pivot_table(data, index = x_ax[0], aggfunc=agg_func).reset_index()

    # Formula for calculated field (Edit as required)
    k[view] = k[fields[0]]/k[fields[1]] * factor * 100
    
    return k[[x_ax[0], view]]

# ------------------------------------------------


def data_merge(outputs, index):
    """
    Driver function to merge outputs of the calc_field function
    outputs : list of outputs from calc_field func
    index : the column on which to join the df
    """
    k = outputs[0]
    for i in range(1, len(outputs)):
        k = k.merge(outputs[i], on = index[0], how = 'inner')
    return k

# ------------------------------------------------


def view_generator(data, field_list, index, view_type, population_list):
    """
    Function to obtain input dataframe for plotting charts. Output used as the 
    input to a plotting function
    """
    columns = field_list + index
    out = []
    plot_series = []
    for i in population_list:
        tmp = data[(data.POP_DESC == i)][columns]
        v = i + '_'+ view_type
        plot_series.append(v)
        out.append(calc_field(tmp, index, field_list, view = v))
    k = data_merge(out, index)
    return k, index, plot_series

# ------------------------------------------------        

def combine_pop(data, combinelist):
    """
    Function to help combine populations
    """
    s = ''
    print(s)
    for i in range(len(combinelist)):
        s = s + str(combinelist[i]) + '+'
    s = s[:-1]
    
    tmp = data[data.POP_DESC.isin(combinelist)].reset_index(drop = True)
    tmp['POP_DESC'] = s
    return tmp

























