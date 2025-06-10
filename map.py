import pandas as pd
import geopandas as gpd
from bokeh.plotting import figure, show
from bokeh.models import (ColumnDataSource, HoverTool, CustomJS, TapTool, Select)
from bokeh.layouts import column

def create_static_map(file: str = 'data/ktn_data.json', gkzList: list[str] = 132*[''], bg_color: str = '#ffffff'):
    gdf = gpd.read_file(file) # read geojson file
    #gdf = gdf.explode(ignore_index=True) # make multipolygon to separate polygons
    #gdf = gdf.drop(index=179) # delete exclave hitzendorf
        
    # extract coordinates from gdf
    gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis=1)
    gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis=1)

    # prep data
    lenGDF = len(gdf)
    source = ColumnDataSource(data=dict(
            x=gdf['x'].tolist(),
            y=gdf['y'].tolist(),
            gemeinde=gdf['GEMNAM'].tolist(), 
            gkz=gdf['GKZ'].tolist(),
            line_color=['black'] * lenGDF,
            line_width=[0.5] * lenGDF,
            fill_color=['#CC79A7' if gkz in gkzList 
                        else "#fcfcfc" for gkz in gdf['GKZ']]#,
            #flag=[1 if gkz in gkzList else 0 for gkz in gdf['Gemeindenummer']]  
        ))

    # Create a Bokeh figure OG!!!
    p = figure(
            title="",
            tools="",
            x_axis_location=None, 
            y_axis_location=None,
            tooltips=[("", "@gemeinde")],
            width=1572,  #og width=1572//2,
            height=int(1572*0.68),  #og height=966//2,
            aspect_scale=0.68,
            match_aspect=True
        )

    p.grid.grid_line_color = None
        
    # Add patches to the figure
    patches = p.patches(
            'x', 
            'y', 
            source=source,
            fill_alpha=1,
            line_color='line_color', 
            line_width='line_width',
            fill_color='fill_color'
        )
        
    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [("", "@gemeinde")]
    hover.renderers = [patches]
    p.add_tools(hover)

    p.toolbar.logo = None
    p.toolbar_location = None
    p.outline_line_color = None          
    p.border_fill_color = None            
    p.min_border = 0                     
    p.min_border_left = 0
    p.min_border_right = 0
    p.min_border_top = 0
    p.min_border_bottom = 0
    p.min_border = 0
    p.background_fill_color = bg_color

    from bokeh.models import Range1d
    x_min, y_min, x_max, y_max = gdf.total_bounds
 
    #p.x_range = Range1d(x_min, x_max)
    #p.y_range = Range1d(y_min, y_max)

    pp = column(p, sizing_mode="stretch_width")
    return pp

def create_interactive_map(file: str = 'data/ktn_data.json', gkzList: list[str] = ['']*132, bg_color: str = '#000000'):
    selected: str = "#F56D8D"
    unselected: str = "#ffffff"

    # Read the shapefile using GeoPandas
    gdf = gpd.read_file(file)

    # Extract x and y coordinates from the geometry
    gdf['x'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[0]), axis=1)
    gdf['y'] = gdf.apply(lambda row: list(row.geometry.exterior.coords.xy[1]), axis=1)

    # Prepare data for Bokeh
    n = len(gdf)
    source = ColumnDataSource(data=dict(
        x=gdf['x'].tolist(),
        y=gdf['y'].tolist(),
        gemeinde=gdf['GEMNAM'].tolist(),  # Adjust the column name if different
        gkz=gdf['GKZ'].tolist(),
        line_color=['black'] * n,
        line_width=[0.5] * n,
        fill_color=[selected if gkz in gkzList else unselected for gkz in gdf['GKZ']],
        selected_gkz=gkzList  # Pass the initial selected GKZs
    ))

    # Create a Bokeh figure
    p = figure(
        #title="Kärnten Karte mit Gemeinden"
        title="", 
        tools="reset,save,tap", #tools="pan,wheel_zoom,reset,save,tap",
        x_axis_location=None, 
        y_axis_location=None,
        tooltips=[("", "@gemeinde")],
        width=1872//4, 
        height=966//4,
        aspect_scale=0.68,
        match_aspect=True
    )
    p.grid.grid_line_color = None

    # Add patches to the figure
    patches = p.patches(
        'x', 'y', source=source,
        fill_alpha=1, line_color='line_color', line_width='line_width',
        fill_color='fill_color'
    )

    # Customize the selection and non-selection glyphs - to overwrite "auto-transparency"
    patches.selection_glyph = patches.glyph.clone()
    patches.selection_glyph.fill_alpha = 1  
    patches.selection_glyph.line_width = 0.5    

    patches.nonselection_glyph = patches.glyph.clone()
    patches.nonselection_glyph.fill_alpha = 1  
    patches.nonselection_glyph.line_width = 0.5    

    # Add hover tool
    hover = HoverTool()
    hover.tooltips = [("", "@gemeinde")]
    hover.renderers = [patches]
    p.add_tools(hover)

    with open("js/callback2.js", "r") as f:
        js_code = f.read()

    # Define the callback for the tap tool
    callback = CustomJS(args=dict(source=source), code=js_code)
    taptool = p.select(type=TapTool)
    taptool.callback = callback
    p.toolbar.logo = None
    p.toolbar_location = None
    p.outline_line_color = None          
    p.border_fill_color = None            
    p.min_border = 0                     
    p.min_border_left = 0
    p.min_border_right = 0
    p.min_border_top = 0
    p.min_border_bottom = 0
    p.min_border = 0
    p.background_fill_color = bg_color

    df = pd.read_csv('data/l_gkz.csv', sep=';')
    df = df[df["id"] != 99999] 
    df.rename(columns={'id': 'Gkz', 
                       'gemeinde': 'Gemeinde', 
                       'bezirk': 'Bezirk', 
                       'nuts3': 'NUTS3', 
                       'bundesland': 'Bundesland', 
                       'tourismusregion': 'Tourismusregion'}, inplace=True)
    
    list_data = df.to_dict(orient='records')

    level_two_options = {'Gemeinde': sorted(df['Gemeinde'].unique()), 
                         'Bezirk': sorted(df['Bezirk'].unique()), 
                         'NUTS3': sorted(df['NUTS3'].unique()), 
                         'Bundesland': sorted(df['Bundesland'].unique()), 
                         'Tourismusregion': sorted(df['Tourismusregion'].unique())} 

    #Create two dropdowns (Category and another for the values from the categories)
    select_category = Select(title="", options=["Bundesland", "NUTS3", "Bezirk", "Gemeinde", "Tourismusregion"], value='Gemeinde')
    select_secondchoice = Select(title="", options=level_two_options['Gemeinde'], value='')

    #Implements function to change options from select_secondschoice
    select_category.js_on_change('value', 
                                 CustomJS(args={"select_secondchoice": select_secondchoice, "options": level_two_options}, code="""
        var value = this.value;
        var listOptions = options[value];
        select_secondchoice.value = '';
        select_secondchoice.options = listOptions;
        select_secondchoice.change.emit();
            """))
    
    #Open and read file callback_choice.js
    with open("js/callback_choice.js", "r") as f:
        js_code_choice = f.read()
    
    #Implements function to select a gemeinde or bezirk via dropdown
    select_secondchoice.js_on_change("value", CustomJS(args={"select_category": select_category, "source": source, "list_data": list_data}, code=js_code_choice))
    pp = column(column(select_category, select_secondchoice, p), sizing_mode="stretch_both")
    
    # Return the Bokeh layout
    return pp

if __name__ == '__main__':
    #IMPORTANT!!! To update javascript in Bokeh uncomment show() and run this python file
    layout = create_interactive_map(bg_color='#8f44a3')
    #layout = create_static_map()
    show(layout)
    pass