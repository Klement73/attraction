# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:26:43 2020

@author: Yael
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import time

#CHANGE THIS TO WORKING DIRECTORY
MAIN_PATH = r"C:\Temp\"
CSV_PATH = f'{MAIN_PATH}\SimulatedDataCSV\SIM_V2_{int(time.time())}.csv'

def dumpToCSV(arr,title,mode):
        if mode==None:
                mode = "REAL_RESULTS"
        with open(CSV_PATH,'a') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(arr+[title,mode])




def generateEmptyGenerationDF():
        df = pd.DataFrame(index = ['herm self','male self','herm cross','male cross'],columns=['green hom','green het','black'])
        df = df.fillna(0)
        return df

self_offspring = 330 
crossed_offspring_total = 550
self_when_crossed = 100
crossed_offspring_just_crossed = crossed_offspring_total-self_when_crossed;
male_self_rate = 10**-3;
#male_self_rate=0


#the input dataframe is the same shape as the output dataframe
#rows: herm self, male self, herm cross, male cross
#columns: 'green hom','green het','black'
def G_next(df_prev, mating_rate_green,mating_rate_nongreen,green_relative_fitness,ADD_MALES):
        df_g_next = generateEmptyGenerationDF()
        
        total_herms= pd.Series(df_prev.loc['herm self'],dtype="float64") + pd.Series(df_prev.loc['herm cross'],dtype="float64")
        
        #FITNESS ADJUSTMENT
        total_herms[0] = total_herms[0]*green_relative_fitness
        total_herms[1] = total_herms[1]*green_relative_fitness
        #
       
        total_males= pd.Series(df_prev.loc['male self'],dtype="float64") + pd.Series(df_prev.loc['male cross'],dtype="float64")
        
        #add 25 black males
        if ADD_MALES:
                total_males[2]+=25
        
        #FITNESS ADJUSTMENT FOR MALES AS WELL. WE ASSUME MALES ARE ALSO
        #SICKLY IN THE SAME WAY HERMS ARE SICKLIY
        total_males[0] = total_males[0]*green_relative_fitness
        total_males[1] = total_males[1]*green_relative_fitness
        
        
        if sum(total_males)!=0 :
                fraction_males = total_males/sum(total_males)
        else:
                fraction_males = total_males
       
        het_offspring = crossed_offspring_just_crossed*\
                (total_herms[0]*mating_rate_green*fraction_males[0]*0+\
                 total_herms[2]*mating_rate_nongreen*fraction_males[2]*0+\
                         total_herms[0]*mating_rate_green*fraction_males[2]*1+\
                                 total_herms[2]*mating_rate_nongreen*fraction_males[0]*1+\
                                         total_herms[1]*mating_rate_green*fraction_males[1]*0.5+\
                                                 total_herms[0]*mating_rate_green*fraction_males[1]*0.5+\
                                                         total_herms[1]*mating_rate_green*fraction_males[0]*0.5+\
                                                                 total_herms[1]*mating_rate_green*fraction_males[2]*0.5+\
                                                                         total_herms[2]*mating_rate_nongreen*fraction_males[1]*0.5);
                
        hom_offspring = crossed_offspring_just_crossed*\
                (total_herms[0]*mating_rate_green*fraction_males[0]*1+\
                 total_herms[2]*mating_rate_nongreen*fraction_males[2]*0+\
                         total_herms[0]*mating_rate_green*fraction_males[2]*0+\
                                 total_herms[2]*mating_rate_nongreen*fraction_males[0]*0+\
                                         total_herms[1]*mating_rate_green*fraction_males[1]*0.25+\
                                                 total_herms[0]*mating_rate_green*fraction_males[1]*0.5+\
                                                         total_herms[1]*mating_rate_green*fraction_males[0]*0.5+\
                                                                 total_herms[1]*mating_rate_green*fraction_males[2]*0+\
                                                                         total_herms[2]*mating_rate_nongreen*fraction_males[1]*0); 
                        
                        
        black_offspring = crossed_offspring_just_crossed*\
                (total_herms[0]*mating_rate_green*fraction_males[0]*0+\
                 total_herms[2]*mating_rate_nongreen*fraction_males[2]*1+\
                         total_herms[0]*mating_rate_green*fraction_males[2]*0+\
                                 total_herms[2]*mating_rate_nongreen*fraction_males[0]*0+\
                                         total_herms[1]*mating_rate_green*fraction_males[1]*0.25+\
                                                 total_herms[0]*mating_rate_green*fraction_males[1]*0+\
                                                         total_herms[1]*mating_rate_green*fraction_males[0]*0+\
                                                                 total_herms[1]*mating_rate_green*fraction_males[2]*0.5+\
                                                                         total_herms[2]*mating_rate_nongreen*fraction_males[1]*0.5);
        
        total_crossed_offspring = pd.Series([hom_offspring,het_offspring,black_offspring],dtype="float64")
                        
        new_herms_crossed = total_crossed_offspring*0.5
        
        #same as crossed_herms
        new_males_crossed = total_crossed_offspring*0.5


        mating_rate_arr = pd.Series([mating_rate_green,mating_rate_green,mating_rate_nongreen],dtype="float64")
        #mating_rate_arr = [mating_rate_green,mating_rate_green,mating_rate_nongreen]


        #THIS IS TRUE ONLY FOR THE HOMOZYGOTES (GREEN AND BLACK)
        df_g_next.loc['herm self']=total_herms*(1-mating_rate_arr).tolist()*self_offspring+\
                total_herms*mating_rate_arr.tolist()*self_when_crossed
                
        #CORRECTING SELFING PROPORTIONS FOR HETROZYGOTES
        hets_self = df_g_next.loc['herm self','green het']
        df_g_next.loc['herm self','green hom'] += 0.25*hets_self
        df_g_next.loc['herm self','black'] += 0.25*hets_self
        df_g_next.loc['herm self','green het'] = hets_self*0.5

                

        df_g_next.loc['male self']=total_herms*(1-mating_rate_arr).tolist()*self_offspring*male_self_rate+\
                total_herms*mating_rate_arr.tolist()*self_when_crossed*male_self_rate
                
        males_self = df_g_next.loc['male self','green het']
        df_g_next.loc['male self','green hom'] += 0.25*males_self
        df_g_next.loc['male self','black'] += 0.25*males_self
        df_g_next.loc['male self','green het'] = males_self*0.5
        
        
        df_g_next.loc['herm cross']=new_herms_crossed.tolist()
        df_g_next.loc['male cross']=new_males_crossed.tolist()
        

        
        
        return df_g_next
 
        

def reduceGeneration(df,how_many,ADD_MALES):
               
        total_worms = df.sum().sum()
        df = df*how_many/total_worms
        
        
        #add 25 black males
        # if ADD_MALES:
        #         df.loc['male cross','black']+=25
               
        return df
        
        

def makeGenerationsFromRealData(treatment):
        generations=[]
        df= pd.read_excel(r"C:\Users\Yael\Dropbox\PhD\Collabs\Oded Rechavi\Itai data 0320\AllData2020_STATS.xlsx")
        new_df = df[df["Treatment"]==treatment].groupby(["Generation"]).mean()
        for ind,row in new_df.iterrows():
                g_next = generateEmptyGenerationDF()
                g_next.loc["herm cross","green hom"]=row["Herm Green"]
                g_next.loc["herm cross","black"]=row["Herm Black"]
                g_next.loc["male cross","green hom"]=row["Male Green"]
                g_next.loc["male cross","black"]=row["Male Black"]
                generations.append(g_next)
        return generations


def getGreenPercentages(dfs):
        green_in_herms=[]
        green_in_males =[]
        male_freq=[]
        green_in_population =[]
        
        for df in dfs:
                total_herms= pd.Series(df.loc['herm self'],dtype="float64") + pd.Series(df.loc['herm cross'],dtype="float64")
                sum_herms = total_herms.sum()
                green_herms_perc = (total_herms[0]+total_herms[1])/sum_herms
                green_in_herms.append(green_herms_perc)
                
                total_males= pd.Series(df.loc['male self'],dtype="float64") + pd.Series(df.loc['male cross'],dtype="float64")
                sum_males = total_males.sum()
                green_males_perc = (total_males[0]+total_males[1])/sum_males
                green_in_males.append(green_males_perc)
                
                male_freq.append(sum_males/ (sum_males+sum_herms));
                                     
                green = df["green hom"] + df["green het"]
                green_in_population.append(green.sum()/df.sum().sum())
                
        return green_in_herms,green_in_males,green_in_population, male_freq
        


def plotDiffGraphs(dfsWT, dfsSRD,c,fig=None,mode=None):
        
        if dfsWT==[] and dfsSRD==[]:
                dfsSRD = runExperimentSRD(mode)
                dfsWT = runExperimentWT(mode)
                
        
        
        def substractLists(a,b):
                return [i - j for i, j in zip(a, b)]
        
        def divideLists(a,b):
                return [0 if j==0 else i/j for i, j in zip(a, b)]
                
        
        green_in_herms1,green_in_males1,green_in_population1,male_freq1 = getGreenPercentages(dfsWT)       
        green_in_herms2,green_in_males2,green_in_population2,male_freq2 = getGreenPercentages(dfsSRD)
                
        if not fig:                  
                f, (ax1, ax2,ax3) = plt.subplots(1,3);
        else:
                f=fig
                ax1,ax2,ax3 = fig.axes
        
        #width,height
        f.set_size_inches(9,2.5,forward=True)
        
        makesubplot2(ax1,substractLists(green_in_population1,green_in_population2),"All population",c,mode)
        makesubplot2(ax2,substractLists(green_in_herms1,green_in_herms2),"Herms only",c,mode)
        makesubplot2(ax3,substractLists(green_in_males1,green_in_males2),"Males only",c,mode)
        
        # makesubplot2(ax1,divideLists(green_in_population2,green_in_population1),"All population",c,mode)
        # makesubplot2(ax2,divideLists(green_in_herms2,green_in_herms1),"Herms only",c,mode)
        # makesubplot2(ax3,divideLists(green_in_males2,green_in_males1),"Males only",c,mode)
        
        
        
        f.tight_layout()
        plt.show()

        
        return f
        

def makesubplot2(ax,arr,title,c,mode):
        
        #PATCH LOSE G0
        arr = arr[1:]
        X_LABELS = ('G1', 'G2', 'G3','G4','G5','G6')
        
        #X_LABELS = ('G0', 'G1', 'G2', 'G3','G4','G5','G6')
        
        
        ax.plot(arr,color=c,marker=".")
        
        #ax.plot(arr,color=c,marker="o")
        #ax.set_ylim(-0.3,0.05)
        ax.set_ylim(-0.05,0.35)
        #ax.set_ylim(0.3,1.1)
        
        ax.set_title(title)
        plt.sca(ax)
        plt.xticks(np.arange(6), X_LABELS)
        #plt.yticks(np.arange(0.3,1.1,0.1))
        plt.yticks(np.arange(0,0.35,0.05))

        #plt.ylabel('srd %green / WT %green')
        
        plt.ylabel('WT %green - srd %green')
        
        plt.xlabel("Generation")
        
        
        #WRITE TO CSV
        dumpToCSV(arr,title,mode)

        



def makesubplot(ax,arr,title,c,mode):
        
        X_LABELS = ('G0', 'G1', 'G2', 'G3','G4','G5','G6')
        
        ax.plot(arr,color=c,marker="o")
        ax.set_ylim(0,0.6)
        #ax1.set_title("%Males")
        ax.set_title(title)
        plt.sca(ax)
        plt.xticks(np.arange(7), X_LABELS)
        plt.yticks(np.arange(6)*0.1)
        plt.ylabel('%green')
        plt.xlabel("Generation")
        
        dumpToCSV(arr,title,mode)

        


def plotGenerations(dfs,c,mode,fig=None):
     
        green_in_herms,green_in_males,green_in_population,male_freq = getGreenPercentages(dfs)
        
                
        if not fig:                  
                f, (ax1, ax2,ax3) = plt.subplots(1,3);
        else:
                f=fig
                ax1,ax2,ax3 = fig.axes
                
        #width,height
        f.set_size_inches(9,2.5,forward=True)
        #f.set_size_inches(10,8,forward=True)
 
        
        #X_LABELS = ('G0', 'G1', 'G2', 'G3','G4','G5','G6')
        makesubplot(ax1,green_in_population,"All population",c,mode)
        makesubplot(ax2,green_in_herms,"Herms only",c,mode)
        makesubplot(ax3,green_in_males,"Males only",c,mode)


       # f.suptitle("Simulation Results")
        f.tight_layout()

        plt.show()
        return f
        
        
        
#MAIN

def runGenerations(G0,mating_rates_green,mating_rates_nongreen,green_relative_fit):
        
        generations=[G0];
        for i in range(0,1):
                G = G_next(generations[i],mating_rates_green[i],\
                           mating_rates_nongreen[i],green_relative_fit[i],False);
                G = reduceGeneration(G,GEN_SIZE,True)
                G = G.apply(np.floor)
                generations.append(G)
                
                
        for i in range(1,6):
                G = G_next(generations[i],mating_rates_green[i],\
                           mating_rates_nongreen[i],green_relative_fit[i],True);
                G = reduceGeneration(G,GEN_SIZE,True)
                G = G.apply(np.floor)
                generations.append(G)

        return generations


def runExperimentWT(mode):
        G0=generateEmptyGenerationDF();
        
        #green hom, green het, black
        G0.loc['herm cross'] = [7,0,7];
        G0.loc['male cross'] = [0,0,11];
        
        default_mode=True
        
        if default_mode or mode=="MATCH_REAL":
        #BEST MATCH FOR REAL RESULTS
                mating_rates_green = [0.5, 0.25,0.33,0.39,0.72,0.70]
                mating_rates_nongreen =[0.55,0.55,0.6,0.95,0.83,0.99]
                green_relative_fit= [1.09,0.67,0.7,0.84,0.72,1.12]
        #
        
        
        if mode=="JUST_LOWER_FITNESS_85":
                G0.loc['male cross'] = [0,0,0];
                mating_rates_green =[0]*6
                mating_rates_nongreen =[0]*6

                #green_relative_fit= [1.09,0.7,0.7,0.7,0.7,0.7,0.7]
                green_relative_fit= [0.85,0.85,0.85,0.85,0.85,0.85,0.85]
                
        if mode=="JUST_LOWER_FITNESS_70":
                G0.loc['male cross'] = [0,0,0];
                mating_rates_green =[0]*6
                mating_rates_nongreen =[0]*6
                
                green_relative_fit= [0.85,0.7,0.7,0.7,0.7,0.7,0.7]
                #green_relative_fit= [1.09,0.85,0.85,0.85,0.85,0.85,0.85]
                
                
        
        if mode=="MEG_FITNESS_NO_CHANGE":
                green_relative_fit= [1.09,0.67,0.67,0.67,0.67,0.67]
                
        if mode=="MEGTYPE_FITNESS_LIKE_WT":                
                green_relative_fit= [1.09,1,1,1,1,1]
                
        if mode=="MEGTYPE_MATING_LIKE_WT":
                mating_rates_green =[0.55,0.55,0.6,0.95,0.83,0.99]
                
                
        if mode=="MEG_DOESNT_IMPROVE":
                mating_rates_green = [0.5, 0.25,0.25,0.25,0.25,0.25]
                green_relative_fit= [1.09,0.67,0.67,0.67,0.67,0.67]
                
                
                
        if mode=="GO_THEN_NULL":
                mating_rates_green =[0.5,0.55,0.6,0.95,0.83,0.99]
                mating_rates_nongreen =[0.55,0.55,0.6,0.95,0.83,0.99]
                #green_relative_fit= [1.15,1,1,1,1,1.1]
                green_relative_fit= [1.09,0.67,0.67,0.67,0.67,0.67]
               
        return runGenerations(G0,mating_rates_green,mating_rates_nongreen,green_relative_fit)



def runExperimentSRD(mode):
          
        G0=generateEmptyGenerationDF();
        
        #green hom, green het, black
        G0.loc['herm cross'] = [7,0,7];
        G0.loc['male cross'] = [0,0,11];
                       
        default_mode=True
        
        if default_mode or mode=="MATCH_REAL":
        #BEST MATCH FOR REAL RESULTS
                mating_rates_green = [0.15,0.25,0.25,0.3,0.41,0.59]
                mating_rates_nongreen =[0.5,0.52,0.68,0.9,0.92,0.91]       
                green_relative_fit= [0.88,0.61,0.68,0.91,0.85,1.12]
        #
        
        if mode=="MEG_DOESNT_IMPROVE":
                mating_rates_green = [0.15,0.25,0.25,0.25,0.25,0.25]
                green_relative_fit= [0.88,0.61,0.61,0.61,0.61,0.61]
                
        
        if mode=="MEG_FITNESS_NO_CHANGE":
                green_relative_fit= [0.88,0.61,0.61,0.61,0.61,0.61]
               
                
        if mode=="MEG_MATING_SRD_LIKE_WT":
                mating_rates_green = [0.5, 0.25,0.33,0.39,0.72,0.70]
                
        if mode=="MEGTYPE_FITNESS_LIKE_WT":                
                green_relative_fit= [0.88,1,1,1,1,1]
                
        if mode=="MEGTYPE_MATING_LIKE_WT":
                mating_rates_green =[0.5,0.52,0.68,0.9,0.92,0.91]       
                
        if mode=="GO_THEN_NULL":
                mating_rates_green =[0.15,0.52,0.68,0.9,0.92,0.91]       
                mating_rates_nongreen =[0.5,0.52,0.68,0.9,0.92,0.91]       
                #green_relative_fit= [0.9,1,1,1,1,1.1]
                green_relative_fit= [0.88,0.61,0.61,0.61,0.61,0.61]
             
    
        return runGenerations(G0,mating_rates_green,mating_rates_nongreen,green_relative_fit)





GEN_SIZE = 300    


realGenWT = makeGenerationsFromRealData("WT")
realGenSRD = makeGenerationsFromRealData("SRD")

# generationsSRD2 = runExperimentSRD("MEG_FITNESS_NO_CHANGE")
# generationsWT2 = runExperimentWT("MEG_FITNESS_NO_CHANGE")
# f1 = plotGenerations(generationsSRD2,c="red",fig=None)
# f2 = plotGenerations(generationsWT2,c="gray",fig=f1)

# generationsSRD = runExperimentSRD("MATCH_REAL")
# generationsWT = runExperimentWT("MATCH_REAL")



generationsWT_85 = runExperimentWT("JUST_LOWER_FITNESS_85")
generationsWT_70 = runExperimentWT("JUST_LOWER_FITNESS_70")

#f1 = plotGenerations(realGenWT,c="black",mode="REAL_RESULTS",fig=None)
f2 = plotGenerations(generationsWT_85,c="green",mode="JUST_LOWER_FITNESS_85",fig=None)
f3 = plotGenerations(generationsWT_70,c="blue",mode="JUST_LOWER_FITNESS_70",fig=f2)


# f1 = plotGenerations(generationsSRD,c="red",fig=None)
# f2 = plotGenerations(generationsWT,c="gray",fig=f1)
# f3 = plotGenerations(realGenSRD,c="red",fig=None)
# f4 = plotGenerations(realGenWT,c="gray",fig=f3)


###PLOT ALL DIFF GRAPHS
# f1 = plotDiffGraphs(realGenWT, realGenSRD,'black',fig=None,mode=None)
# f2 = plotDiffGraphs([], [],'gray',fig=f1,mode="MATCH_REAL")
# f3 = plotDiffGraphs([], [],'green',fig=f1,mode="MEG_FITNESS_NO_CHANGE")
# f4 = plotDiffGraphs([], [],'blue',fig=f1,mode="MEG_MATING_SRD_LIKE_WT")
# f5 = plotDiffGraphs([], [],'orange',fig=f1,mode="MEGTYPE_FITNESS_LIKE_WT")
# f6 = plotDiffGraphs([], [],'purple',fig=f1,mode="MEGTYPE_MATING_LIKE_WT")
###

#f7 = plotDiffGraphs([], [],'red',fig=f1,mode="GO_THEN_NULL")
#f8 = plotDiffGraphs([], [],'orange',fig=f1,mode="MEG_DOESNT_IMPROVE")

####

ax1,ax2,ax3 = f1.axes
# ax1.legend(['real results','full model','no epigenetic dilution',\
#             'no mating advantage in wt vs srd',\
#                     'same brood size megtype as wt','same mating megtype as wt'],loc="best")

#f, (ax1, ax2,ax3) = plt.subplots(1,3);
#ax1.legend(['real results','meg brood size doesnt improve','no mating advantage in wt vs srd'])
