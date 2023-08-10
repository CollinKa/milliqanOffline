 #########################################################################################################################################################
 # Original Author: Ryan De Los Santos                                                                                                                   #
 # Use: Use to handle the data files and apply any necessary cuts for your analysis. When using this function make sure that you instantiate DataHandler #
 # then input what cuts you would like to use in applyCuts(). Call DataHandler.applyCuts() to apply all of your cuts.
 # Example:
 # data = DataHandler("datapath")          # Replace datapath with where your data is stored
 # data.applyCuts([data.npeCut, data.timingCut])       # Any of the functions within the class containing cut in the name can be used
 #
 #   # The code should return a few events that pass all of the cuts we expect small numbers for printed to screen for the number of events
 # Edit the  timingCut() by Collin
 # Add muonSelection() Based on NeHa's idea by Collin 2/10/23                               
 # NeHa's idea see https://indico.cern.ch/event/1216209/contributions/5115893/attachments/2537208/4366944/Milliqan_cosmics_eventdisplay_Run469-1.pdf
 # Add threeinaline() cut by Collin 2/12/23  
 # modified applycut to make it work without using cut  8/5/23
 #########################################################################################################################################################

import ROOT as r
from DetectorGeometry import *

# Create Data Class
class DataHandler():
    def __init__(self, dataPath, debug=False):
        self.data = self.initializeData(dataPath)
        self.debug = debug
    # Create TChain with all data you will need for your analysis
    # wildcards can be used in datapath
    def initializeData(self, datapath):
       treeChain = r.TChain('t')
       treeChain.Add(datapath)
       return treeChain

    """
    # Print out certain datafile statistics
    # FIXME: Implement way to viewData or get rid of function
    def viewData(self):
        return

    # For a millicharged particle it is expected that the ratio between the maximum and minimum nPE is less than 10
    # This function removes events that don't satisfy this cut
    def npeCut(self, event, cut_ratio):
        # FIXME: How do we reconcile the issue where some values are negative
        nPEratio = max(event.nPE)/min(event.nPE)
        if nPEratio > cut_ratio:
            return
        if self.debug:
            print(event.nPE)
            print(nPEratio)
        return event

    # Removes events that have a hit in the cosmic veto panels labeled by channel 68, 69, 70, 72, 73, 74.
    def cosmicPanelVeto(self, event):
        # Getting list of channels for each event
        channels = event.chan
        # vetoPanels is defined in DetectorGeometry.py
        if any(veto in channels for veto in vetoPanels):
            return
        if self.debug:
            print(channels)
        return event


    # Removes events that have more than a single hit per layer, ensuring particle travels in straight line
    def singleHitPerLayer(self, event):
        layers = event.layer
        # Sets have no repeated values so if the lenghts are not the same, there is some repeated value
        if len(set(layers)) != len(layers):
            return
        if self.debug:
            print(layers)
        return event


    #MuonSelection is base on NeHa's idea
    #this will not work in run 591 because there is not much hit in the end pannels
    def muonSelection(self,event, height_threshold):
        
        height_list = event.height
        chan_list = event.chan

        # if there is no hit on the end pannels, then we can't claims that this 
        # event is muon event
        if 71 not in chan_list:
            return
        elif 75 not in chan_list:
            return
        frontPannelHeight = []
        backPannelHeight = []
        #She claim if both end pannals has a big hit(>1.1V), then it is muon event
        for chan, height in zip(chan_list,height_list):

            if chan == 71:  
                frontPannelHeight.append(height)
            elif chan == 75:
                backPannelHeight.append(height)
            
            if any(x >= height_threshold for x in frontPannelHeight) and any(x >= height_threshold for x in backPannelHeight):
                return event
            else:
                return

    def npeCheck(self,event):
        nPE_list = event.nPE
        DAQNum = event.DAQEventNumber
        #nPEthreashold is define in DetectorGeometry.py
        if min(nPE_list) >= nPEthreashold:
            #print(DAQNum)
            return event
        else:
            return None


    #this method is used with ThreeInLine()
    def layerCheck(self,lists):
        i = 0 
        for list in lists:
            if len(set(list)) >= 3: #return true if it contain 3 unique layers(3 in a line)
                i += 1
        return i


    
    def ThreeInLine(self,event):
        row_list = event.row
        column_list = event.column
        layer_list = event.layer

        # four in a line is very rare impossible to find in run 591
        # use three in a line instead!
        if len(set(layer_list)) >= 3:  #three in a line
            pass
        else:
            return

        
        # the list at below save the information about the pulse passing through difference layers
        # For example, List0 is used for saving the infomation pulse passing through the position of
        # row is three and column is one. "0" correspond to the position of the 0th channal, whose location
        # is at the third row and first column.

        #numbers at below are index number. So 3rd(index) row mean the 4th row in my notation
        list0 = [] # correspond to 3rd row, 0st column
        list1 = [] # correspond to 3rd row, 1st column
        list2 = [] # correspond to 2rd row, 0th column
        list3 = [] # correspond to 2rd row, 1st column
        list4 = [] #list 4-7 should not contain any hit in run 591 due to the last Super model is yet to install
        list5 = []
        list6 = [] 
        list7 = [] 
        list8 = []
        list9 = []
        list10 = []
        list11 = []
        list12 = []
        list13 = []
        list14 = []
        list15 = []

        for row, column, layer in zip(row_list,column_list,layer_list):
            if row == 3 and column == 0:
                list0.append(layer)
            elif row == 3 and column == 1:
                list1.append(layer)
            elif row == 2 and column == 0:
                list2.append(layer)
            elif row == 2 and column == 1:
                list3.append(layer)
            elif row == 3 and column == 2:
                list4.append(layer)
            elif row == 3 and column == 3:
                list5.append(layer)
            elif row == 2 and column == 2:
                list6.append(layer)
            elif row == 2 and column == 3:
                list7.append(layer)
            elif row == 1 and column == 0:
                list8.append(layer)
            elif row == 1 and column == 1:
                list9.append(layer)
            elif row == 0 and column == 0:
                list10.append(layer)
            elif row == 0 and column == 1:
                list11.append(layer)
            elif row == 1 and column == 2:
                list12.append(layer)
            elif row == 1 and column == 3:
                list13.append(layer)
            elif row == 0 and column == 2:
                list14.append(layer)
            elif row == 0 and column == 3:
                list15.append(layer)
        
        # check where does the 4 in a row locate
        lists=[list0,list1,list2,list3,list4,list5,list6,list7,list8,list9,list10,list11,list12,list13,list14,list15]
        #print("lists:"+str(lists)) #for debugs
        i = self.layerCheck(lists) #i is the number list in lists are 3 in a row
        if i >= 1:
            return event
        
        else:
            return
        
    def noPickup(self, event):
        height_list = event.height
        if any(height >= 500 for height in height_list):
            return event
        else:
            return
        

    def timingCut(self, event):
        time = event.time_module_calibrated


        if len(time) >= 2:
            #print("len(time):"+str(len(time))) #debug
            sorted_time = sorted (enumerate(time),key=lambda x: x[1])   #return (index,time)
            #print("sorted_time"+str(sorted_time)) #debug
            time = []
            index_list = []
            for index,t in sorted_time:
                time.append(t)
                index_list.append(index)

            ajacent_time = [y - x for x, y in zip(time[:], time[1:])]
            #print("ajacent_time"+str(ajacent_time)) # debug
        else:  # it requires at least two hit to find the time passing two layers.
            return 
        
        if self.debug:
            print("Adjacent Time", ajacent_time)

        # check if the particle passing through ajecent layer is 15 ns
        # if the minimun value of time passing through ajcent layers is bigger than 15ns, 
        # then it is different from the expected data.

        #timebL: timebl:time it take for particle pass through layer. Defined in DetectorGeometry.py
        if min(ajacent_time) > timebL: 
            #print("ajacent time is not satified") #debug
            return
        
        
        if self.debug:
            print(time)

        return event
    """
    
    #def applyCuts(self, cuts):
        #lc=len(cuts)
        #cutData = []

        # Run over all events

    def applyCuts(self):

        #empty list
        #h_list = []
        #a_list = []
        #c_list = []
        #t_list = []
        

        num_lists = 12
        #h_list_of_lists = []
        a_list_of_lists = []
        nun_chan_E_lists = []
        t_list_of_lists = []
        for _ in range(num_lists):
            #h_list_of_lists.append([])
            a_list_of_lists.append([])
            nun_chan_E_lists.append([])
            t_list_of_lists.append([])

        count = 0# for test only chose first 50 events
        for event in self.data:
            if event is None: continue
            
            height_list = event.height
            area_list = event.area
            channels = event.chan
            time_info = event.timeFit
            count += 1
            #energy cut from 100 to 1100 kev with 100 kev interval
            for i in range(num_lists):
                nun_chan_E = [] #used to collect channel information for each pulse
                for height,area,channel,time in zip(height_list,area_list,channels,time_info):
                    #if height >= height_cut:
                    if height >= 100 + i*100:
                        a_list_of_lists[i].append(area)
                        t_list_of_lists[i].append(time)
                        nun_chan_E.append(channel)

                    Num_event = len(set(nun_chan_E))
                    nun_chan_E_lists[i].append(Num_event)

            """
            # Run over all cuts in list given to applyCuts
            None_check = []
            for cut in cuts:

                event= cut(event) # Apply given cut
                if event is None: 
                    break
                None_check.append(event.DAQEventNumber)


            if None in None_check:
                break
            if len(None_check) == lc: # if there are two cuts then len(None_check) should be 2
                cutData.append(None_check[0])
            """
                
            
        #return cutData
            #if count > 500:
        return a_list_of_lists,nun_chan_E_lists,t_list_of_lists

if __name__ == "__main__":
    Run_num = 1039
    data = DataHandler(f'/store/user/milliqan/trees/v31/MilliQan_Run{Run_num}.*_v31_firstPedestals.root')
    #1098(dont use, contain none data)
    #1032(long run) 
    #1026 (nisarg's old run)
    #1039 (beam & magnetic off) 2 minish finish -pure cosmic is at around 3-4 channel

    #height_cut = 100
    a_list_of_lists,nun_chan_E_lists,t_list_of_lists = data.applyCuts()
    #for area in a_list_of_lists:
    #    print(area)
    #print(a_list)
    #print(nun_chan_E_lists)
    #print(t_list_of_lists)
    #print(len(nun_chan_E_lists))
    #print(len(t_list_of_lists))
    #a_bins_max = max(a_list)
    #a_bins_min = min(a_list)
    #t_list_min = min(t_list)
    #t_list_max = max(t_list)
    #"""
    def height_histogram(height,xtitle,data,nBins, xMin, xMax):
        HistogramTitle = f"{xtitle} with {height}kev cut "
        #hisarea = r.TH1D(f"{height}kev", "My Histogram", nBins, xMin, xMax)
        hist = r.TH1D(f"{height}kev data:{xtitle}", "My Histogram", nBins, xMin, xMax)
        hist.SetTitle(HistogramTitle)
        hist.GetXaxis().SetTitle(xtitle)
        for d in data:
            hist.Fill(d)
        hist.Scale(1.0 / hist.GetEntries()) # not working
        canvas = r.TCanvas("canvas", "Canvas Title", 800, 600)
        hist.Draw()
        hist.Write()
    
    
    fileName = f"run{Run_num}_heightcut.root"
    output_file = r.TFile(fileName, "RECREATE")
    
    for index,area_data in enumerate(a_list_of_lists):
        if area_data == None: continue
        height = 100 + index * 100
        height_histogram(height,"area",area_data,100, 0, max(area_data))

    for index,chan_data in enumerate(nun_chan_E_lists):
        if chan_data == None: continue
        height = 100 + index * 100
        height_histogram(height,"number of channel got hit",chan_data,75, 0, 75)

    for index,time_data in enumerate(t_list_of_lists):
        if time_data == None: continue
        height = 100 + index * 100
        height_histogram(height,"puse time",time_data,100, 0, 2500)

    output_file.Close()
    #"""






    #create histogram
