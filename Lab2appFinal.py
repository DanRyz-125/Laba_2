import pandas as pd
from spyre import server

class VHI_App(server.App):
    title = "Inputs"

    regions = ["Vinnitsya", "Volyn", "Dnipropetrovsk", "Donetsk", "Zhytomyr", 
               "Zakarpathia", "Zaporizhzhya", "Ivano-Frankivsk", "Kiev", 
               "Kirovohrad", "Luhansk", "Lviv", "Mykolayiv", "Odessa", "Poltava", 
               "Rivne", "Sumy", "Ternopil", "Kharkiv", "Kherson", "Khmelnytskyy", 
               "Cherkasy", "Chernivtsi", "Chernihiv", "Crimea", "Kiev City", "Sevastopol"]
    
    region_options = [{"label": region, "value": 
                       str(i + 1)} 
                      for i, region in enumerate(regions)]

    inputs = [{   "type":'dropdown',                
               "label": 'Index  ',                
               "options" : [ {"label": "VCI", "value":"VCI"},                                
                            {"label": "TCI", "value":"TCI"},                                
                            {"label": "VHI", "value":"VHI"},],
                "key": 'index',
                "action_id": "update_data"},

              { "type":'dropdown',
                "label": 'Region',
                "options" : region_options,
                "key": 'region',
                "action_id": "update_data"},

              { "input_type":"text",
                "variable_name":"year",
                "label": "Year",
                "value":1981,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'First week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'first',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Last week',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'last',
                "action_id": 'update_data'}]

    controls = [{   "type" : "hidden",
                  "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{  "type" : "plot",
                "id" : "plot",
                "control_id" : "update_data",
                "tab" : "Plot"},
              { "type" : "table",
                "id" : "table",
                "control_id" : "update_data",
                "tab" : "Table",
                "on_page_load" : True}]


    def getData(self, params):
            index = params['index']
            year = params['year']
            first = params['first']
            last = params['last']
            path = 'C:\\Users\\Home\\LabPython\\cleaned\\15_11_2022_14_vhi_id_{}.csv'.format(index)
            df = pd.read_csv(path, index_col=False, header=9,names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
            df1 = df[(df['year'] == float(year)) & (df['week'] >= float(first)) & (df['week'] <= float(last))]
            df1 = df1[['week', index]]
            return df

    def getPlot(self, params):
            index = params['index']
            year = params['year']
            first = params['first']
            last = params['last']
            df = self.table(params).set_index('week')
            plt_obj = df.plot()
            plt_obj.set_ylabel(index)
            plt_obj.set_title('Index {index} for {year} from {first} to {last} weeks'.format(index=index,year=float(year), first=float(first), last=float(last)))
            return  plt_obj.get_figure()
        
app = VHI_App()
app.launch(port=8080)