# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:58:46 2021

@author: atharva.tanksale
"""

import streamlit as st
import pandas as pd
import numpy as np
import perf 

# ----------------------------
st.set_page_config(layout="wide")
# ----------------------------


st.title('Performance Views Webapp')
# st.write("Upload data using the function available in the side pane")
# Comment sidebar dev block when making the upload button active

# ------------------ Helper Functions ----------------

@st.cache(allow_output_mutation=True)
def load_data(file):
    """
    Cached function to ensure low load time for datasets
    """
    df = pd.read_csv(file, encoding='utf-8')
    return df

@st.cache(allow_output_mutation=True)
def make_plot(plotdata, plotindex, plotseries, viewtitle):
    """
    Helper function to return a matplotlib object that serves as the input to
    st.plotly method
    """
    ax = plotdata.plot(x = plotindex[0], y = plotseries, title = viewtitle)
    fig = ax.get_figure()
    ax.set_xlabel(plotindex[0])
    return fig

@st.cache(allow_output_mutation=True)
def filtered_data(data, filter_list):
    for i in filter_list.keys():
        data = data[data[i].isin(list(filter_list[i]))]
        return data
    else:
        return data
    
    
@st.cache(allow_output_mutation=True)
def custom_filter(col_name, display_string):
    if len(df[col_name].unique()) <= 10:
        return st.multiselect(display_string, df[col_name].unique(), df[col_name].unique())
    else:
        return st.slider(display_string, int(df[col_name].min()),
                                         int(df[col_name].max()), 
                                         value = (int(df[col_name].quantile(.25)), round(df[col_name].quantile(.75))))




@st.cache(allow_output_mutation=True)
def addtn_filter(df, condition_check, counter, dropdownlist, filterlist):
    drop = st.selectbox("Choose column on which to filter", dropdownlist,
                        key = "filter_drop"+ str(counter)) 
    a = custom_filter(drop, str(drop))
    if type(a) == tuple:
        a_values = np.arange(a[0], a[1]+1)
    else:
        a_values = a
    filterlist[drop] = a_values
    df = filtered_data(df, filterlist)
    condition_check = True
    continue_option = st.checkbox('Add Custom Filter ' + str(count), value = False,
                                  key = "filter"+ str(counter))
    return df, continue_option, condition_check, filterlist, dropdownlist


# ----------- App Layout ------------------

uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv", key='file_uploader')

if uploaded_file is not None:
    df = load_data(uploaded_file)
else: 
    st.write("""**Upload a file before proceeding/Select Dev version from sidebar**""")
    df = pd.DataFrame(columns = ['POP_DESC', 'SUM'])

if st.sidebar.checkbox("Dev Version"):
    df = pd.read_csv('tf_data.csv')
    preview = st.sidebar.checkbox("Preview Data")
    if preview: 
        st.subheader('Data Preview')
        st.dataframe(df.head(10))

st.markdown("""
            #### Set up Views
            """
            )

# ----------- Global non-app Declaratives ----------
index = ['MOB']
filter_list = {}

# --------------------------------------------------


# ----------- Global Settings part : App Layout ----------

pop_col1, pop_col2, pop_col3 = st.columns(3)

# Applying Global Filters

st.write("""**Apply Filters**""")

addt_options = st.sidebar.expander("Additional Options")
with addt_options:
    cust_filters = st.checkbox("Enable Custom Filters (beta)")
    combine_pop = st.checkbox("Enable Combining Populations")
    

# ------------------ Custom Filters Logic -------------
if cust_filters is True:
    add_filters_dict = {}
    exp = st.expander("Create custom filters")
    with exp:        
        count = 1
        condition_check = False
        drop_down_list = set(df.columns) - set(filter_list.keys())
        continue_option = st.checkbox('Add Custom Filter ' + str(count), value = False,
                              key = "filter"+ str(count))
        if continue_option is True:
            while condition_check is False:
                count = count + 1
                df, continue_option, condition_check, add_filters_dict, drop_down_list = addtn_filter(df, condition_check, 
                                                                                 count, drop_down_list, add_filters_dict)
                
                drop_down_list = set(df.columns) - set(add_filters_dict.keys())
                if continue_option is True:
                    condition_check = False
    # st.write(add_filters_dict)
    filter_list = {**add_filters_dict, **filter_list}
    df = filtered_data(df, filter_list)

# --------------------------------------------------



# ------------------ BAU Filters Logic -------------
filter_expander = st.expander(" List of filters")
with filter_expander:
    left_col1, mid_col1 = st.columns(2)    
    

    with left_col1:
        
        # Gen3 LT Filter
        filter_gen3lt = st.checkbox("Gen3LT")
        if filter_gen3lt is True:
            st.write("Gen3 LT Filter")
            gen3lt_values = st.slider('Select the Range of Gen3LT Ventiles', 1, 20, (1, 13))
            gen3lt_values_all = np.arange(gen3lt_values[0], gen3lt_values[1]+1)
            filter_list['GEN3_LT'] = gen3lt_values_all
            df = filtered_data(df, filter_list)
          
    
        # Gen3.2 LT Filter
        filter_gen32lt = st.checkbox("Gen3.2LT")
        if filter_gen32lt is True:
            st.write("Gen3.2 LT Filter")
            gen32lt_values = st.slider('Select the Range of Gen3.2LT Ventiles', 1, 20, (1, 13))
            gen32lt_values_all = np.arange(gen32lt_values[0], gen32lt_values[1]+1)
            filter_list['LTG3_2'] = gen32lt_values_all
            df = filtered_data(df, filter_list)
    
        # Gen4.2 LT Filter
        filter_gen42lt = st.checkbox("Gen4.2LT")
        if filter_gen42lt is True:
            st.write("Gen4.2 LT Filter")
            gen42lt_values = st.slider('Select the Range of Gen4.2LT Deciles', 1, 10, (1, 7))
            gen42lt_values_all = np.arange(gen42lt_values[0], gen42lt_values[1]+1)
            filter_list['LTG42_DECILE'] = gen42lt_values_all
            df = filtered_data(df, filter_list)
            
        # Gen4.1 LT Filter
        filter_gen41lt = st.checkbox("Gen4.1LT")
        if filter_gen41lt is True:
            st.write("Gen4.1 LT Filter")
            gen41lt_values = st.slider('Select the Range of Gen4.1LT Ventiles', 1, 10, (1, 7))
            gen41lt_values_all = np.arange(gen41lt_values[0], gen41lt_values[1]+1)
            filter_list['LTG41_DECILE'] = gen41lt_values_all
            df = filtered_data(df, filter_list)
        
        
    with mid_col1:    
        
        # FiCO score filter
        filter_fico = st.checkbox("FICO")
        if filter_fico is True:
            st.write("FICO (FSF_CURR_FICO_SCORE) Range Filter")
            fico_values = st.slider('Select the Range of FICO', 550, 720, (600, 680))
            fico_values_all = np.arange(fico_values[0], fico_values[1]+1)
            filter_list['SUM_CURRENT_FICO'] = fico_values_all
            df = filtered_data(df, filter_list)
          
        # Inquiry Flag filter    
        filter_inquiry = st.checkbox("Inquiry Flag")
        if filter_inquiry is True:
            # st.write("Inquiry Flag (IQT9421) filter")
            inquiryflag_values = st.multiselect('Add/drop values for IQT9421', 
                                                df.INQUIRY_FLAG.unique(), df.INQUIRY_FLAG.unique())
            filter_list['INQUIRY_FLAG'] = inquiryflag_values
            df = filtered_data(df, filter_list)   
            
        # SSSNI flag filter
        filter_ssni = st.checkbox("SSN Code")
        if filter_ssni is True:
            # st.write("Inquiry Flag (IQT9421) filter")
            ssni_values = st.multiselect('Add/drop values for SSN Code', 
                                                df.SSSNI.unique(), df.SSSNI.unique())
            filter_list['SSSNI'] = ssni_values
            df = filtered_data(df, filter_list)
    
    

        
# ------------- Combine Population Logic------------

with pop_col2:
    if combine_pop is True:
        st.write("""**Combine Series** """)
        st.write("""*(Allows for only one new combined series at present)*""")
        pop_subset = st.multiselect("Add or drop series present in the dataset",
                                    df.POP_DESC.unique())
        df2  = perf.combine_pop(df, pop_subset)
        df = pd.concat([df, df2], ignore_index = True)
        
    
        
# Selecting Series
with pop_col1:
    st.markdown("""##### Select Population Series""")
    df = filtered_data(df, filter_list)
    select_series = st.multiselect("Add or drop series present in the dataset",
                                   df.POP_DESC.unique(), df.POP_DESC.unique())
    population_list = []
    for i in select_series:
        population_list.append(i)
        

# --------------------------------------------------


# ------------------  Perf Views ----------------------

# Begin Views Part
st.markdown("""
            ####  Views
            """)

a1, a2 = st.columns(2)

with a1:  
    a1_expander = st.expander("Views/Open", True)
    with a1_expander:
    # st.write("""**Views/Open**""")
    
        open_v1 = st.checkbox('Util/Open')
        if open_v1 is True:
            view_title = 'Util/Open'        
            fields = ['ADB_CURRENT_BALANCE_SUM', 'CREDIT_LIMIT_SUM']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
        open_v2 = st.checkbox('Revolve_Rate/Open')
        if open_v2 is True:
            view_title = 'Revolve_Rate/Open'        
            fields = ['REVOLVING_BALANCE_ADB', 'ADB_CURRENT_BALANCE_SUM']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
    
        open_v3 = st.checkbox('Credit Limit/Open')
        if open_v3 is True:
            view_title = 'Credit Limit/Open'        
            fields = ['CREDIT_LIMIT_SUM', 'SUM_OPEN_ACCOUNTS']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))
    
        open_v4 = st.checkbox('DQ30+($)/Open')
        if open_v4 is True:
            view_title = 'DQ30+($)/Open'        
            fields = ['DQ$30_NUMERATOR', 'DQ$30_DENOMINATOR']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
        open_v5 = st.checkbox('DQ60+($)/Open')
        if open_v5 is True:
            view_title = 'DQ60+($)/Open'        
            fields = ['DQ$60_NUMERATOR', 'DQ$60_DENOMINATOR']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
    
        open_v6 = st.checkbox('DQ30+(#)/Open')
        if open_v6 is True:
            view_title = 'DQ30+(#)/Open'        
            fields = ['DQ30SUMNUM_NUMERATOR', 'DQ30SUMNUM_DENOMINATOR']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
        open_v7 = st.checkbox('DQ60+(#)/Open')
        if open_v7 is True:
            view_title = 'DQ60+(#)/Open'        
            fields = ['DQ60SUMNUM_NUMERATOR', 'DQ60SUMNUM_DENOMINATOR']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))


        open_v8 = st.checkbox('BRM/Open')
        if open_v8 is True:
            view_title = 'BRM/Open'        
            fields = ['BRM_RISK_NEW', 'SUM_OPEN_ACCOUNTS']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))


with a2:
    
    a2_expander = st.expander("Views/Active", True)
    with a2_expander:
        active_v1 = st.checkbox('Util/Active')
        if active_v1 is True:
            view_title = 'Util/Active'        
            fields = ['ADB_CURRENT_BALANCE_SUM_ACTIVE', 'CREDIT_LIMIT_SUM_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
        
        active_v2 = st.checkbox('Revolve_Rate/Active')
        if active_v2 is True:
            view_title = 'Revolve_Rate/Active'        
            fields = ['REVOLVING_BALANCE_ADB_ACTIVE', 'ADB_CURRENT_BALANCE_SUM_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
    
        # Add the /100 part in the last line to fix the non% error
        active_v3 = st.checkbox('Credit Limit/Active')
        if active_v3 is True:
            view_title = 'Credit Limit/Active'        
            fields = ['CREDIT_LIMIT_SUM_ACTIVE', 'BALANCE_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))        

        active_v4 = st.checkbox('DQ30+($)/Active')
        if active_v4 is True:
            view_title = 'DQ30+($)/Active'        
            fields = ['DQ$30_NUMERATOR_ACTIVE', 'DQ$30_DENOMINATOR_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))   


        active_v5 = st.checkbox('DQ60+($)/Active')
        if active_v5 is True:
            view_title = 'DQ60+($)/Active'        
            fields = ['DQ$60_NUMERATOR_ACTIVE', 'DQ$60_DENOMINATOR_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))   

        active_v6 = st.checkbox('DQ30+(#)/Active')
        if active_v6 is True:
            view_title = 'DQ30+(#)/Active'        
            fields = ['DQ30SUMNUM_NUMERATOR_ACTIVE', 'DQ30SUMNUM_DENOMINATOR_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))   


        active_v7 = st.checkbox('DQ60+(#)/Active')
        if active_v7 is True:
            view_title = 'DQ60+(#)/Active'        
            fields = ['DQ60SUMNUM_NUMERATOR_ACTIVE', 'DQ60SUMNUM_DENOMINATOR_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))   

        active_v8 = st.checkbox('BRM/Active')
        if active_v8 is True:
            view_title = 'BRM/Active'        
            fields = ['BRM_RISK_NEW_ACTIVE', 'BALANCE_ACTIVE']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))   
            

# a3 = st.expander("""**Additional Views**""")

a3, a4 = st.columns(2)

with a3:
    a3_expander = st.expander("Additional Views", True)
    with a3_expander:
    
        # Add the /100 part in the last line to fix the non% error
        misc_v1 = st.checkbox('Avg. FICO/Active')
        if misc_v1 is True:
            view_title = 'Avg. FICO/Active'        
            fields = ['SUM_CURRENT_FICO_ACT', 'COUNT_VALID_CURRENT_FICO_ACT']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))
    
        # Add the /100 part in the last line to fix the non% error
        misc_v2 = st.checkbox('Avg. FICO/Open')
        if misc_v2 is True:
            view_title = 'Avg. FICO/Open'        
            fields = ['SUM_CURRENT_FICO', 'COUNT_VALID_CURRENT_FICO']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data/100, plot_index, plot_series, view_title))
    
    
        misc_v3 = st.checkbox('Pvol/OS (ADB)')
        if misc_v3 is True:
            view_title = 'Pvol/OS (ADB)'        
            fields = ['PURCHASES_SUM', 'ADB_CURRENT_BALANCE_SUM']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title))
     
        
        misc_v4 = st.checkbox('Active/Open Accounts')
        if misc_v4 is True:
            view_title = 'Active/Open Accounts'        
            fields = ['BALANCE_ACTIVE', 'SUM_OPEN_ACCOUNTS']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title)) 

        misc_v5 = st.checkbox('PBad')
        if misc_v5 is True:
            view_title = 'PBad'        
            fields = ['SUM_CHARGEOFF', 'SUM_OPEN_ACCOUNTS']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            plot_data = plot_data*12
            plot_data[plot_index[0]] = plot_data[plot_index[0]]/12
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title)) 

        misc_v6 = st.checkbox('PBad 6M Moving Avg.')
        if misc_v6 is True:
            view_title = 'PBad 6M. MA'        
            fields = ['SUM_CHARGEOFF', 'SUM_OPEN_ACCOUNTS']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            plot_data = plot_data*12
            plot_data[plot_index[0]] = plot_data[plot_index[0]]/12
            ind_ext = plot_data[plot_index[0]]
            plot_data = plot_data.rolling(6).mean()
            plot_data[plot_index[0]] = ind_ext
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title)) 
            
        misc_v7 = st.checkbox('$ GUCO (ADB)')
        if misc_v7 is True:
            view_title = '$ GUCO (ADB)'        
            fields = ['CHARGEOFF_NUMERATOR', 'ADB_CURRENT_BALANCE_SUM']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            plot_data = plot_data*12
            plot_data[plot_index[0]] = plot_data[plot_index[0]]/12
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title)) 

        misc_v8 = st.checkbox('$ GUCO (ADB) 6M Moving Avg.')
        if misc_v8 is True:
            view_title = '$ GUCO (ADB) 6M MA'        
            fields = ['CHARGEOFF_NUMERATOR', 'ADB_CURRENT_BALANCE_SUM']
            columns = fields + index
            plot_data, plot_index, plot_series = perf.view_generator(df, fields, index, view_title, population_list)
            plot_data = plot_data*12
            plot_data[plot_index[0]] = plot_data[plot_index[0]]/12
            ind_ext = plot_data[plot_index[0]]
            plot_data = plot_data.rolling(6).mean()
            plot_data[plot_index[0]] = ind_ext
            st.plotly_chart(make_plot(plot_data, plot_index, plot_series, view_title)) 





# --------------------------------------------------

#----------------------Hide Streamlit footer----------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
#--------------------------------------------------------------------

