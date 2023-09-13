import pandas as pd
import matplotlib.pyplot as plt

class time:
    def __init__(self, h=0, m=0, hhmm=":"):
        self.h, self.m = list(map(int,hhmm.split(sep=":")))
        self.h+=h
        self.m+=m
        self.h = self.h % 24

    def as_m(self):
        return self.h * 60 + self.m
    
    def __eq__(self,_value) -> bool:
        return self.as_m() == _value.as_m()
    
    def __lt__(self,_value):
        return self.as_m() < _value.as_m()
    
    def __gt__(self,_value):
        return self.as_m() > _value.as_m()
    
    def __add__(self,_value):
        return time((self.h+_value.h+(self.m+_value.m)//60)%24,(self.m+_value.m)%60)
    
    def __iadd__(self,_value):
        self.h=(self.h+(self.m+_value)//60)%24
        self.m=(self.m+_value)%60
        return self
    
    def __sub__(self,_value):
        return time((24+self.h+_value.h+(self.m-_value.m)//60)%24,(self.m-_value.m)%60)
    
    def __isub__(self,_value):
        self.h=(24+self.h+(self.m-_value-59)//60)%24
        self.m=(60+self.m-_value)%60
        return self
    
    def hhmm(self):
        return "{:0>2d}:{:0>2d}".format(self.h,self.m)
    
    def __repr__(self):
        return self.hhmm()
 
class timer:
    def __init__(self, start="0:0", end="0:0"):
        self.start = time(hhmm=start)
        self.end = time(hhmm=end)
    
    def pomodoro_list(self):
        if self.start > self.end:
            self.end += 24*60

        table=[[],[],[]]
        now = self.start
        n_colu = 0

        while (now < self.end):
            table[0]+=["集中","休憩"]
            table[1].append(now.hhmm())
            now+=25
            table[1].append(now.hhmm())
            table[2].append(now.hhmm())
            now+=5
            table[2].append(now.hhmm())
            n_colu+=2
        #cf = [['gainsboro' for i in range(3)]]
        cf = [[['w','w','w'],['lawngreen' for i in range(3)]][j&1] for j in range(n_colu)]
        
        return [{'':table[0], '開始':table[1], '終了':table[2]},cf]
    
    def gen_pomodoro(self):
        plt.rcParams['font.family'] = 'Hiragino Sans'
        plt.rcParams['font.size'] = 48
        ls, cf = self.pomodoro_list()
        #names = ['区分','開始','終了']
        df = pd.DataFrame(ls)[['','開始','終了']]
        fig, ax = plt.subplots(figsize=(15,20))
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=df.values,
                 cellColours=cf,
                colLabels=df.columns,
                colColours=['gainsboro' for i in range(3)],
                bbox=[0,0,1,1],
                cellLoc='center',
                loc='center',)
        fig.tight_layout()
        plt.savefig('table.png')

        
if __name__=='__main__':
    timer("12:00","15:00").gen_pomodoro()