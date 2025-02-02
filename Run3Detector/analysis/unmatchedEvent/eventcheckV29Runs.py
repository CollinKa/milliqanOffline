#ver 1.0
#1/12/2023 Collin Zheng  Zheng.1947@buckeyemail.osu.edu
#the code needs to be run with python2
#dont worry if you see the errors.
#Here are two ways to run the code
#1.'python2 eventcheckV29Runs.py all_run'  this is for make the plots for unmatched event counting with different runs from version 29
#2.'python2 eventcheckV29Runs.py single_run --runNum MilliQan_Run570' this is for specific run


#------------------------------------------------------------------------------------------------------------------------------------
import ROOT as r
import os
import sys
import numpy as np

from array import array
from multiprocessing import Process, Manager
import argparse




def initializeTree(run):

    treeChain = r.TChain("t")
    treeChain.Add('/store/user/mcarrigan/trees/v29/' + run + '.*_v29_firstPedestals.root')
    return treeChain


def count(run,variables):
    TDCtime=[] #used for storing the all unique TDCtime including matched and unmatched time 
    trees = initializeTree(run)
    uniqueUnmatchedTDC = [] #use for storing the unique unmatched events. 
    Counstructable = [] #use for storing the contrutable unmatched events.
    repeated_index_event = []
    NumCounstructable = 0 #use for the contrutable unmatched events counting
 
    for ievent, event in enumerate(trees):
        a = np.array(event.v_groupTDC_g0)
        MaxTDC = max(a)
        TDCtime.append(MaxTDC)

    #check empty event Run
    if TDCtime == []:
        print('run number ' + str(run) + ' has no event')
        p = 0.0
        i1 = 0.0
        i2 = 0.0
        i3 = 0.0
        i4 = 0.0
        i5 = 0.0
        N_unmatched=0.0
        N_repeated = 0.0
        p3 =0 #the ratio of unique unmatched event out of unique total event.
        
    else:
        uniqueTDC = np.unique(TDCtime,axis=0)# unique TDC time is used for checking repeated event
        #start counting the unmatched event
        N_unmatched=0.0
        N_repeated = 0.0
        #record the position zero TDC on specific index
        i1 = 0.
        i2 = 0.
        i3 = 0.
        i4 = 0.
        i5 = 0.

        for ievent, event in enumerate(trees):
            b = np.array(event.v_groupTDC_g0)   #b is TDCtime for each digitizer in the format [time1 time2 time3 time4 time5]
            if min(b) == 0 :    #unmatched event
                #count the number of position of zero index
                if b[0] == 0:
                    i1 += 1
                if b[1] == 0:
                    i2 += 1
                if b[2] == 0:
                    i3 += 1
                if b[3] == 0:
                    i4 += 1
                if b[4] == 0:                                 
                    i5 += 1
                
                
                #check repeatedness
                maxTDC = max(b)
                if maxTDC in uniqueTDC:   #if the unmatched event is not repeated, it return ture
                    uniqueTDC=list(uniqueTDC)
                    uniqueTDC.remove(maxTDC)
                    uniqueTDC = np.array(uniqueTDC)
                    
                    uniqueUnmatchedTDC.extend([maxTDC]) #for construtabal
                    N_unmatched += 1.0 #count the unique umatched event

                else:  #count the repeated unmatched event
                    N_repeated += 1.0

                            
                #counstrutable unmatched event counting
                repeated_index_event=list(b) 

                repeated_index_event.extend([maxTDC])  #I want to construct a list that looks like [time1 time2 time3 time4 time5 max TDCtime]
                                                        #the maxTDCtime is used as an indication of unique TDCtime.
            
                Counstructable.extend([repeated_index_event]) #create an list of list that save the information of TDCtime(5 pulse)
                                                              # and the maxTDC time as an indication.
        
        #used for debugging
        #print("Counstructable" + str(Counstructable))
        #print("uniqueUnmatchedTDC" + str(uniqueUnmatchedTDC))
        
        
        for maxNum in uniqueUnmatchedTDC:
            
            result = [0,0,0,0,0,0]
            
            for element in Counstructable:
                if element[5] == maxNum:
                    #LIST.extend(element)
                    emptyList = []
                    loopNum = 0
                    for x,y in zip(result,element):
                        if loopNum < 5:            #only do the summation for first five TDCtime
                            emptyList.append(x+y)  # the last one can be used as indication of which unmatched event can
                                                   # be reconstructed.
                                              
                            result = emptyList
                            loopNum += 1
                        else:
                            result.append(maxNum)
                        
            
            #print("result is " + str(result))
            
            if 0 not in result: #if there is no zero in the result list, it means events are constructable.
                
                #for debugging only
                #print("unmatched event " + str(event.event) + " tdctime " + str(result[5]) + " pulse is constructable " )
                NumCounstructable += 1
                
    
                        
    if N_unmatched ==0:
        p1 = 0
        p2 = 0
        p3 = 0
    else:
        p1 = N_repeated/N_unmatched  #number of unmatched repeated events out of total number of unmatched event
        p2 = NumCounstructable/N_unmatched
        N_uniqueTDC = len(uniqueTDC) #number of unique TDC time can be used for the counting the totoal number of unique event
        p3 = N_unmatched/N_uniqueTDC
        
    runnumE = float(run.split('Run')[1])

    variables.append((i1,i2,i3,i4,i5,p1,runnumE,p2,p3,N_unmatched,N_repeated)) #append the data into a share variable



def single_run(run):

    manager = Manager()
    variables = manager.list() #created shared variable
    processes = []
    
    
    #for run in unique_run:

    #p = Process(target = count, args=('MilliQan_Run570',variables))
    p = Process(target = count, args=(run,variables))
    processes.append(p)
    p.start()
    p.join()
    i1=variables[0][0]
    i2=variables[0][1]
    i3=variables[0][2]
    i4=variables[0][3]
    i5=variables[0][4]
    N_unmatched = variables[0][9]
    N_repeated = variables[0][10]
    p1 = variables[0][5]
    p2 = variables[0][7]
    p3 = variables[0][8]


    print( str(run) + " number of unmatched events on each digitizer " + " i1:" + str(i1) + " i2:" + str(i2)
         +" i3:" + str(i3) + " i4:" + str(i4) + " i5:" + str(i5) + "\n  number of unmatched event:" +
          str(N_unmatched) + "\n number of repeated unmatched events:" + str(N_repeated)
          + "\n number of unmatched repeated events out of total number of unmatched event:" + str(p1)
          + "\n number of construtable repeated events out of total number of unmatched event:" + str(p2)
          +"\n ratio of unique unmatched events over total unique events:" + str(p3) )


def mutiple_run(unique_run):
    print('start mutiple run in multiple_run method')
    manager = Manager()
    variables = manager.list() #created shared variable
    processes = []
    
    
    for run in unique_run:

        p = Process(target = count, args=(run,variables))
        processes.append(p)
        #p.start()
        
    for p in processes:
        p.start()
        
    for p in processes:
        p.join()
    
    plot1(variables) # number of constructible unmatched event / number of unique unmatched event(based on TDCtime)
    plot2(variables) # number of repeated event / number of unique event
    plot3(variables) # number of repeated event / number of unique unmatched event

def plot1(variables):
    # number of constructible unmatched event / number of unique matched event(based on TDCtime)
    c=len(variables)
    runNum_list, constructable_list = array('d'),array('d')

    for i in range(c):
        runNum_list.append(0)
        constructable_list.append(0)

    
    for i in range(c):
        runNum_list[i] = variables[i][6]
        constructable_list[i] = variables[i][7]
    

    gr = r.TGraph(c,runNum_list,constructable_list)
    c1 = r.TCanvas("c1","graph",200,10,600,400)
    gr.SetMarkerColor(2)
    gr.SetTitle( 'constructible unmatched event / unique unmatched event(based on TDCtime)' )
    gr.Draw("*")
    c1.Draw()
    f=r.TFile.Open("unmatched_constructible_ratio.root","recreate");
    gr.Write()
    f.Close()
    print("plot is save as " + "unmatched_constructible_ratio.root ")



def plot2(variables):
    #plot the ration of number of repeated event out of number of unmatched event
    c=len(variables)
    runNum_list, unmatched_list = array('d'),array('d')

    for i in range(c):
        runNum_list.append(0)
        unmatched_list.append(0)

    
    for i in range(c):
        runNum_list[i] = variables[i][6]
        unmatched_list[i] = variables[i][8]
       

    gr2 = r.TGraph(c,runNum_list,unmatched_list)
    c1 = r.TCanvas("c1","graph",200,10,600,400)
    gr2.SetTitle( 'number of unique unmatched events / number of unique events' )
    gr2.SetMarkerColor(1)
    gr2.Draw("*")
    c1.Draw()
    f=r.TFile.Open("unmatched_unique_ratio.root","recreate");
    gr2.Write()
    f.Close()
    print("plot is save as unmatched_unique_ratio.root ")

def plot3(variables):
    #plot the ration of number of repeated event out of number of unmatched event
    c=len(variables)
    runNum_list, repeated_list = array('d'),array('d')

    for i in range(c):
        runNum_list.append(0)
        repeated_list.append(0)

    
    for i in range(c):
        runNum_list[i] = variables[i][6]
        repeated_list[i] = variables[i][5]
    
    gr1 = r.TGraph(c,runNum_list,repeated_list)
    c1 = r.TCanvas("c1","graph",200,10,600,400)
    gr1.SetTitle( 'number of repeated event / number of unique unmatched event' )
    gr1.SetMarkerColor(1)
    gr1.Draw("*")
    c1.Draw()
    f=r.TFile.Open("unmatched_repeated_ratio.root","recreate");
    gr1.Write()
    f.Close()
    print("plot is save as unmatched_repeated_ratio.root")







def Main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    single_run_arg = subparser.add_parser('single_run')
    all_run = subparser.add_parser('all_run')
    #kai: make a make the unique run be default argument, TBD
    single_run_arg.add_argument('--runNum',type = str, required = True)
    args = parser.parse_args()
    if args.command == 'single_run':
        print(args.runNum)
        runNum = args.runNum
        single_run(args.runNum)
        #run with python eventcheck1_1V29.py single_run --runNum 'MilliQan_Run570'
    if args.command == 'all_run':
        A=os.listdir('/store/user/mcarrigan/trees/v29/')
        #extract the run number
        b = [s.split(".")[0] for s in A]
        # keep the unique elements in array with 'set()' and sort them base on run number.
        unique_run = sorted(list(set(b)))
        tot_run=len(unique_run)
        mutiple_run(unique_run)
        #print("mutiple run start") #test

if __name__ == "__main__":
    Main()
