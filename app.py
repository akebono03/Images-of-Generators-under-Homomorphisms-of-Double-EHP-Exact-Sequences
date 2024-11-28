from re import A, template
from flask import Flask, render_template, request #追加
from jinja2 import Template
#from openpyxl import load_workbook
import sqlite3
import numpy as np
import pandas as pd
import sympy as sp

app=Flask(__name__)

n=2
k=2
HoGroup=[]
Arrow=[]
table_group=[[],[],[],[],[],[]]
table_gen=[[],[],[],[],[],[]]
table_arrow=[[],[],[],[],[],[]]
table_image=[[],[],[],[],[],[]]
table_ref=[[],[],[],[],[],[]]
m_d_sum=1

@app.route('/')
def homotopy_group():
  return render_template('homotopy_group.html', title='flask test', n=n, k=k, \
    HoGroup=HoGroup, Arrow=Arrow, \
    table_group=table_group, table_gen=table_gen, table_arrow=table_arrow, \
    table_image=table_image, table_ref=table_ref, m_d_sum=m_d_sum)

@app.route('/register', methods=['post'])
def register():
  n=request.form['n']
  k=request.form['k']
  n=int(n)
  k=int(k)

  db_name='sphere3.db'
  conn=sqlite3.connect(db_name)
  df=pd.read_csv('./sphere3.csv')
  df.to_sql('sphere',conn,if_exists='replace')
  df=pd.read_csv('./generator3.csv')
  df.to_sql('gen',conn,if_exists='replace')
  df=pd.read_csv('./fiber3.csv')
  df.to_sql('fiber3',conn,if_exists='replace')
 
  c=conn.cursor()

  inf=float('inf')

#dict_factoryの定義
  def dict_factory(cursor,row):
    d={}
    for idx,col in enumerate(cursor.description):
      d[col[0]]=row[idx]
    return d

#row_factoryの変更(dict_factoryに変更)
  c.row_factory=dict_factory

  def Dot(A,B):
    return sp.expand( (A.transpose()*B)[0,0])

  class Fiber:
    def __init__(self,n,k):
      self.n=int(n)
      self.k=int(k)

      if k<=-1:
        query=f'select*from fiber3 where n={0} and k={-1}'
        query_count=f'select count( * ) from fiber3 where n={0} and k={-1}'
      elif k+2>=n:
        query=f'select*from fiber3 where n={n} and k={k}'
        query_count=f'select count( * ) from fiber3 where n={n} and k={k}'
      else:
        if k%2==1:
          query=f'select*from fiber3 where n={k+2} and k={k}'
          query_count=f'select count( * ) from fiber3 where n={k+2} and k={k}'
        else:
          query=f'select*from fiber3 where n={k+2} and k={k}'
          query_count=f'select count( * ) from fiber3 where n={k+2} and k={k}'
      self.query = query
      self.query_count= query_count

    def direct_sum(self):
#直和成分の個数を与えるメソッド
      for row in c.execute( self.query_count):
        res=row['count( * )']
      return res

    def order_list(self):
#orderのリストを与えるメソッド
      try:res=[row['orders'] if row['orders']==inf else int(row['orders']) for row in c.execute(self.query)]
      except:res=[0]
      return res

    def group_order(self):
      res=max(self.order_list())
      return res


  class HomotopyGroup:
    def __init__(self,n,k):
      self.n=int(n)
      self.k=int(k)

      if k<=-1:
        query=f'select*from sphere where n={0} and k={-1}'
        query_count=f'select count( * ) from sphere where n={0} and k={-1}'
      elif k+2>=n:
        query=f'select*from sphere where n={n} and k={k}'
        query_count=f'select count( * ) from sphere where n={n} and k={k}'
      else:
        if k%2==1:
          query=f'select*from sphere where n={k+2} and k={k}'
          query_count=f'select count( * ) from sphere where n={k+2} and k={k}'
        else:
          query=f'select*from sphere where n={k+2} and k={k}'
          query_count=f'select count( * ) from sphere where n={k+2} and k={k}'
      self.query = query
      self.query_count= query_count

    def direct_sum(self):
#直和成分の個数を与えるメソッド
      for row in c.execute( self.query_count):
        res=row['count( * )']
      return res

    def order_list(self):
#orderのリストを与えるメソッド
      try:res=[row['orders'] if row['orders']==inf else int(row['orders']) for row in c.execute(self.query)]
      except:res=[0]
      return res

    def group_order(self):
      res=max(self.order_list())
      return res

    def max_direct_sum(self):
      nn=[self.n*2-1,self.n-1, self.n,self.n*2-1,self.n-1]
      kk=[self.k-self.n+2, self.k,self.k,self.k-self.n+1, self.k-1]
      m_d_sum=[HomotopyGroup( nn[i],kk[i]).direct_sum() for i in range(5)]
      return max(m_d_sum)

    def query_id(self,id):
      if self.k<=-1:res=f'select*from sphere where n={0} and k={-1} and id={id}'
      elif self.k+2>=self.n:res=f'select*from sphere where n={self.n} and k={self.k} and id={id}'
      else:res=f'select*from sphere where n={self.k+2} and k={self.k} and id={id}'
      return res

    def rep_list(self,id):
#表示元を合成で表示する際の数字のリストを与えるメソッド
      c.execute( self.query_id(id))
      res=list(map(int, c.fetchone()['Element'].split()))
      return res

    def gen_coe_list(self,id):
#生成元の表示元による一次結合の係数のリストを与えるメソッド
      for row in c.execute(self.query_id(id)):
        res=list(map(int, row['gen_coe'].split()))
      del res[self.direct_sum():]
#リストの長さをdirect_sumの数にする
      return res

    # def gen_coe_list(self, id): 
# 生成元の表示元による一次結合の係数のリストを与えるメソッド
    #   try:
    #     for row in c.execute(self.query_id(id)):
    #       int_list = list(map(int, row['gen_coe'].split()))
    #     del int_list[self.direct_sum():] 
# リストの長さを direct_sum の数にする
    #   except:
    #     int_list = []
    #   return int_list

    def el_dim_list(self, el_list):
#表示元の境目の次元のリストを与えるメソッド
      res=[self.n]
      for i,elem in enumerate(el_list):
        gen_query=f'select*from gen where id="{elem}"'
        for row in c.execute( gen_query):
          res.append( res[i]+row['k'])
      return res

    def pi_tex(self):
      res=f'\pi_{ {self.n+self.k} }^{ {self.n} }'
      return res

    def group_structure(self):
      group=[]
      for row in c.execute(self.query):
        if row['orders']==0:group.append('0')
        elif row['orders']==inf:group.append('Z')
        else:
          try:group.append(f"Z_{ {int(row['orders'])} }")
          except:group.append('0')
      self_direct_sum= self.direct_sum()
      group_gen= [self.rep_linear_tex( self.gen_coe_list(j)) for j in range(self_direct_sum)]
      group_tex_list= [gr+'\{'+gen+'\}' for (gr,gen) in zip(group,group_gen)]
      return ' \oplus '.join( group_tex_list)

    def el_tex(self,el_li):
#表示元のtex表示を与えるメソッド
      el_dim_li= self.el_dim_list(el_li)
      res=''
      sq_cnt=1
      for i,elem in enumerate(el_li):
        gen_query=f'select*from gen where id="{elem}"'
        for row in c.execute(gen_query):
          # if row['kinds']==2:
          #   res+='{ s }'
          if row['kinds']!=-1:
            if el_dim_li[i]< row['n']:res+='{'+row['latex'] +f'_{ {el_dim_li[i]} }'+'(Not Defined)}'
            elif i==0 or el_li[i-1]!=el_li[i]:sq_cnt=1
#一番最初か、前のidと違うとき、カウントを１にする。
            else:sq_cnt+=1
#前のidと同じときにカウントを＋１
            if i== len(el_li)-1:
#最後のときにtexを追加
              if el_dim_li[i] >=row['n']:
                if row['latex'][-1]=='(':
                  res+='{' +row['latex'] +f'{int(el_dim_li[i-sq_cnt+1])}' +') }'
                else:
                  res+='{' +row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'}'
                if sq_cnt>=2:
                  res= res[:-1]+f'^{ {sq_cnt} }'+'}'
            elif el_li[i]!= el_li[i+1]:
#次のidと違うときにtexを追加
              if el_dim_li[i] >=row['n']:
                if row['latex'][-1]=='(':
                  res+='{' +row['latex'] +f'{int(el_dim_li[i-sq_cnt+1])}' +') }'
                else:
                  res+='{'+ row['latex']+f'{ {el_dim_li[i-sq_cnt+1]} }'+') }'
                if sq_cnt>=2: 
                  res= res[:-1]+f'^{ {sq_cnt} }'+'}'
#カウントの数をべきにする。
#次のidと同じ場合は何もしない
          elif el_dim_li[i] <row['n']:
            res+='{'+' Ea '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'(Not Defined)}'
          elif el_dim_li[i] ==row['n']:
            res+='{' +row['latex']+'}'
          elif el_dim_li[i]== row['n']+1:
            res+='{'+' Eb '+row['latex']+'}'
          else:
            res+='{'+' Ec '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'}'
      if 0 in el_li:res='0'
      return res

    def el_coe_tex(self,elli,el_coeli=[1]*6):
      el_li,el_coe_li=self.delete_iota(elli,el_coeli)
      el_dim_li=self.el_dim_list(el_li)
      len_el_li=len(el_li)
      res=''
      sq_cnt=1
      for i,elem in enumerate(el_li):
        gen_query=f'select*from gen where id="{elem}"'
        for row in c.execute(gen_query):
          if row['kinds']==0:
            if el_dim_li[i]<row['n']:
              if el_coe_li[i]==1:res+='{'+row['latex']+f'_{ {el_dim_li[i]} }'+'(Not Defineda)}'
              elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i]} }'+'(Not Defineda)}'
              else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i]} }'+'(Not Defineda)})'
            elif i==0 or el_li[i-1]!=el_li[i] or (el_li[i-1]==el_li[i] and el_coe_li[i]!=1):sq_cnt=1
#一番最初か、前のidと違うとき、カウントを１にする。
            else:sq_cnt+=1;el_coe_li[i]=el_coe_li[i-1]
#前のidと同じときにカウントを＋1
            if i==len_el_li-1:
#最後のときにtexを追加
              # if el_dim_li[i]>=row['n']:
              if el_dim_li[i]<row['n']:continue
              if '{3,' in row['latex'] or '{4,' in row['latex']:
                if el_coe_li[i]==1:res+='{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} }'
                elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} }'
                else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} })'
              else:
                if el_coe_li[i]==1:res+='{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'}'
                elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'}'
                else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'})'
              if sq_cnt<2:continue
              if res[-1]==')':res=res[:-2]+f'^{ {sq_cnt} }'+'})'
              else:res=res[:-1]+f'^{ {sq_cnt} }'+'}'
            elif el_li[i]!=el_li[i+1] or (el_li[i]==el_li[i+1] and el_coe_li[i+1]!=1):
#次のidと違うときにtexを追加
              if el_dim_li[i]<row['n']:continue
              if '{3,' in row['latex'] or '{4,' in row['latex']:
                if el_coe_li[i]==1:res+='{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} }'
                elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} }'
                else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+f'{el_dim_li[i-sq_cnt+1]}'+'} })'
              else:
                if el_coe_li[i]==1:res+='{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'}'
                elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'}'
                else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+f'_{ {el_dim_li[i-sq_cnt+1]} }'+'})'
              if sq_cnt<2:continue
# カウントの数をべきにする。
              if res[-1]==')':res=res[:-2]+f'^{ {sq_cnt} }'+'})'
              else:res=res[:-1]+f'^{ {sq_cnt} }'+'}'
#次のidと同じ場合は何もしない
          elif el_dim_li[i]<row['n']:
            if el_coe_li[i]==1:res+='{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'(Not Defined)}'
            elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'(Not Defined)}'
            else:res+='('+f'{el_coe_li[i]}'+'{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'(Not Defined)})'
          elif el_dim_li[i]==row['n']:
            if el_coe_li[i]==1:res+='{'+row['latex']+'}'
            elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+row['latex']+'}'
            else:res+='('+f'{el_coe_li[i]}'+'{'+row['latex']+'})'
          elif el_dim_li[i]==row['n']+1:
            if el_coe_li[i]==1:res+='{'+' E '+row['latex']+'}'
            elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+' E '+row['latex']+'}'
            else:res+='('+f'{el_coe_li[i]}'+'{'+' E '+row['latex']+'})'
          else:
            if el_coe_li[i]==1:res+='{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'}'
            elif len_el_li==1:res+=f'{el_coe_li[i]}'+'{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'}'
            else:res+='('+f'{el_coe_li[i]}'+'{'+' E '+f"^{ {el_dim_li[i]-row['n']} }"+row['latex']+'})'
      return res

    def rep_linear_tex(self,coe,totalcoe=1):
      rep_coe=[c*totalcoe for c in coe]
      ord_li=self.order_list()
      direct_sum=self.direct_sum()
      if ord_li==[0]: res='0'
      elif rep_coe!=[]:
        symbol_li=['x00','x01','x02','x03','x04','x05','x06','x07','x08','x09','x10','x11']
        X=sp.Matrix([sp.Symbol(symbol_li[i]) for i in range(direct_sum)])
        def mod_coe(i):
          try:
            if ord_li[i]==inf: return rep_coe[i]
            elif rep_coe[i]%ord_li[i]>ord_li[i]//2: return rep_coe[i]%ord_li[i]-ord_li[i]
            else: return rep_coe[i]%ord_li[i]
          except: return rep_coe[i]
        A=sp.Matrix([mod_coe(i) for i in range(direct_sum)])
        res=str(Dot(X,A)).replace('*x','x')
        for i in range(direct_sum):
          res=res.replace(symbol_li[i],self.el_tex(self.rep_list(i)))
      else:res=''
      return res

    def rep_to_gen_matrix(self):
      matrix_li=[]
      d_sum=self.direct_sum()
      try:
        for id in range(d_sum):
          for row in c.execute(self.query_id(id)):
            int_li=list(map(int, row['gen_coe'].split()))
          del int_li[d_sum:]
          matrix_li.append(int_li)
      except: pass
      return_matrix=sp.Matrix(matrix_li)
      return return_matrix

    def P_image_tex(self,id):
      if self.n%2==1:
        P_hg=HomotopyGroup((self.n-1)//2,(self.n+2*self.k-3)//2)
        self_P_coe=self.P_coe(id)
        res=P_hg.rep_linear_tex(self_P_coe[0])
        res_ref=self_P_coe[1]
      else:res,res_ref='',''
      return res,res_ref

    def E_image_tex(self,id):
      # E_hg=HomotopyGroup(self.n+1,self.k)
      E_hg=HomotopyGroup(self.n+2,self.k)
      self_E_coe=self.E_coe(id)
      res=E_hg.rep_linear_tex(self_E_coe[0])
      res_ref=self_E_coe[1]
      return res,res_ref

    def H_image_tex(self,id):
      H_hg=HomotopyGroup(2*self.n-1,self.k-self.n+1)
      self_H_coe=self.H_coe(id)
      res=H_hg.rep_linear_tex(self_H_coe[0])
      res_ref=self_H_coe[1]
      return res,res_ref

    def rep_coe_to_id_list(self,repcoeli):
      res_id=[i for i in range(self.direct_sum()) if repcoeli[i]!=0]
      res_coe=[repcoeli[i] for i in res_id]
      return res_id,res_coe

    def rep_coe_to_el_list(self,repcoeli):
      id_li=self.rep_coe_to_id_list(repcoeli)
      res_el=[self.rep_list(i) for i in id_li[0]]
      res_coe=id_li[1]
      return res_el,res_coe

    def P_coe_matrix(self):
      matrix_li=[]
      d_sum=self.direct_sum()
      # hg_P=HomotopyGroup((self.n-1)//2,self.n+self.k-2-(self.n-1)//2)
      hg_P=HomotopyGroup(self.n-2, self.k)
      P_d_sum=hg_P.direct_sum()
      for id in range(d_sum):
        for row in c.execute(self.query_id(id)):
          int_li=list(map(int, row['P_coe'].split()))
        del int_li[P_d_sum:]
        matrix_li.append(int_li)
      return_P_coe_matrix=sp.Matrix(matrix_li)
      return return_P_coe_matrix

    def E_coe_matrix(self):
      matrix_li=[]
      d_sum=self.direct_sum()
      hg_E=HomotopyGroup(self.n+2,self.k)
      E_d_sum=hg_E.direct_sum()
      for id in range(d_sum):
        for row in c.execute(self.query_id(id)):
          try: int_li=list(map(int, row['E_coe'].split()))
          except: int_li=[0]*12
        del int_li[E_d_sum:]
        if int_li != []: matrix_li.append(int_li)
        else: matrix_li.append([0]*E_d_sum)
      return_E_coe_matrix=sp.Matrix(matrix_li)
      return return_E_coe_matrix

    def H_coe_matrix(self):
      matrix_li=[]
      d_sum=self.direct_sum()
      # hg_H=HomotopyGroup((self.n*2)-1,self.n+self.k-(self.n*2)+1)
      hg_H=HomotopyGroup(self.n-2, self.k-1)
      H_d_sum=hg_H.direct_sum()
      for id in range(d_sum):
        for row in c.execute(self.query_id(id)):
          try: int_li=list(map(int, row['H_coe'].split()))
          except: int_li=[0]*H_d_sum
        del int_li[H_d_sum:]
        matrix_li.append(int_li)
      return_H_coe_matrix=sp.Matrix(matrix_li)
      return return_H_coe_matrix

    def rep_coe_to_gen_coe(self, repcoelist):
      repcoematrix = sp.Matrix([repcoelist])
      if repcoematrix == sp.Matrix([[0]]):
        direct_sum = self.direct_sum()
        return_gen_coe_list = [0] * direct_sum
      else:
        try:
          return_gen_coe_list = (repcoematrix * self.rep_to_gen_matrix().inv()).tolist()[0]
        except:
          return_gen_coe_list = []
      return return_gen_coe_list

    def gen_coe_to_rep_coe(self, gencoelist):
      if gencoelist != []:
        gencoematrix = sp.Matrix([gencoelist])
        return_rep_coe_list = (gencoematrix * self.rep_to_gen_matrix()).tolist()[0]
      else:
        return_rep_coe_list = []
      return return_rep_coe_list

    def mod_gen_coe_list(self, gencoe):
      if gencoe != []:
        order_list = self.order_list()
        direct_sum = self.direct_sum()
        def mod_coe(i):
          if order_list[i] == 0:
            return gencoe[i]
          elif order_list[i] == inf:
            return gencoe[i]
          elif gencoe[i] % order_list[i] > order_list[i] /2:
            return gencoe[i] % order_list[i] - order_list[i]
          else:
            return gencoe[i] % order_list[i]
        return_mod_gen_coe_list = [mod_coe(i) for i in range(direct_sum)]
      else:
        return_mod_gen_coe_list = []
      return return_mod_gen_coe_list

    def gen_P_coe(self,id):
      res=[]
      ref_tex=''
      self_d_sum=self.direct_sum()
      order_li=self.order_list()
      try:
        if order_li==[0] or order_li==[]: res=[0]*12
        else:
          queryid=f'select*from sphere where n={self.n} and k={self.k} and id={id}'
          for row in c.execute(queryid):
            if row['P_coe'] is not None:
              res=list(map(int, row['P_coe'].split()))
              gen_int_li=list(map(int, row['gen_coe'].split()))
              del gen_int_li[self_d_sum:]
              gen_matrix=sp.Matrix(gen_int_li)
              self_P_coe_matrix=self.P_coe_matrix()
              res=(gen_matrix.transpose()*self_P_coe_matrix).tolist()[0]
              res=list(map(int, row['P_coe'].split()))
              ref_tex=row['P']  
      except: pass
      del res[HomotopyGroup((self.n-1)//2, (self.n+2*self.k-3)//2).direct_sum():] 
      return res,ref_tex

    def gen_E_coe(self,id):
      ref=[]
      self_d_sum=self.direct_sum()
      for row in c.execute(self.query_id(id)):
        if row['E_coe'] is not None:
          gen_int_li=list(map(int, row['gen_coe'].split()))
          del gen_int_li[self_d_sum:]
          gen_matrix=sp.Matrix(gen_int_li)
          self_E_coe_matrix=self.E_coe_matrix()
          res=(gen_matrix.transpose()*self_E_coe_matrix).tolist()[0]
          ref=row['E']
        else: res=[]
        # hg=HomotopyGroup(self.n+1,self.k) if self.k+2>=self.n else HomotopyGroup(self.k+2,self.k)
        hg=HomotopyGroup(self.n+2,self.k) if self.k+2>=self.n else HomotopyGroup(self.k+2,self.k)
        del res[hg.direct_sum():]
      return res,ref

    def gen_H_coe(self, id):
      res=[]
      ref_tex=''
      self_d_sum=self.direct_sum()
      if self.k+2>=self.n:
        for row in c.execute(self.query_id(id)):
          if row['H_coe'] is not None:
            res=list(map(int, row['H_coe'].split()))
            gen_int_li=list(map(int, row['gen_coe'].split()))
            del gen_int_li[self_d_sum:]
            gen_matrix=sp.Matrix(gen_int_li)
            self_H_coe_matrix=self.H_coe_matrix()
            try: res=(gen_matrix.transpose()*self_H_coe_matrix).tolist()[0]
            except: res=[0]
            ref_tex=row['H']
      else: res=[0]*12
      del res[HomotopyGroup(2*self.n-1, self.k-self.n+1).direct_sum():] 
      return res,ref_tex

###########################################################

  # 汎用的なホモトピー群作成関数
  def create_hogroup(n,k,odd,group_type='hogroup'):
    if odd:
      if group_type=='hogroup':
        nn=[n-2,n-2,n,n-2,n-2,n]
        kk=[k,k,k,k-1,k-1,k-1]
        txt_templates=[' Q_{ {{nn1 + kk1}} }^{ {{nn1}} }' if i%3==0 else ' \pi_{ {{nn1 + kk1}} }^{ {{nn1}} } ' for i in range(6)]
      elif group_type=='hogroup2':
        nn=[n+2,n,n,n+2,n,n]
        kk=[k+1,k,k,k,k-1,k-1]
        txt_templates=[' Q_{ {{nn1 + kk1}} }^{ {{nn1}} }' if i%3==1 else ' \pi_{ {{nn1 + kk1}} }^{ {{nn1}} } ' for i in range(6)]
      else:
        nn=[n-2,3*n-2,3*n-4,n-2,3*n-2,3*n-4]
        kk=[k,-2*n+k+3,-2*n+k+3,k-1,-2*n+k+2,-2*n+k+2]
        txt_templates=[' Q_{ {{nn1 + kk1}} }^{ {{nn1}} }' if i%3==0 else ' \pi_{ {{nn1 + kk1}} }^{ {{nn1}} } ' for i in range(6)]
    else:
      nn=[0,n-1,n,2*n-1,0,0]
      kk=[0,k,k,k-n+1,0,0]
      txt_templates=['0' if i%4==0 else ' \pi_{ {{nn1 + kk1}} }^{ {{nn1}} } ' for i in range(6)]

    hogroup=[]
    for i in range(6 if odd else 5):
      template=Template(txt_templates[i])
      rendered=template.render({'nn1':nn[i],'kk1':kk[i]})
      hogroup.append(rendered)
    return nn,kk,hogroup

  # 汎用的なEHPマップと矢印作成関数
  def create_ehp_map_and_arrows(n,odd,group_type='hogroup'):
    if odd:
      ehp_map=[]
      if group_type=='hogroup':
        ehp_map=['P','E^{2}','H','P','E^{2}']
      elif group_type=='hogroup2':
        ehp_map=['H','P','E^{2}','H','P']
      else:
        ehp_map=['J','\Delta','I','J','\Delta']
      arrow_template=[' \stackrel{ {{map1}} }{\longrightarrow} ' for _ in range(len(ehp_map))]
    else:
      ehp_map=['','E',f'[\iota_{ {n} },\iota_{ {n} }]','','']
      arrow_template=[' \stackrel{ {{map1}} }{\longleftarrow}' if group_type=='hogroup' and i==2 else ' \stackrel{ {{map1}} }{\longrightarrow} ' for i in range(len(ehp_map))]
    arrow_template=[Template(arrow_template[i]) for i in range(len(ehp_map))]
    arrows=[arrow_template[i].render({'map1':ehp_map[i]}) for i in range(len(ehp_map))]
    return ehp_map,arrows

  # テーブル作成
  def create_table(hogroup,arrows):
    table=hogroup[0]
    for i in range(1,len(hogroup)):
      table+=f" & & & {arrows[i-1]} & & & {hogroup[i]}"
    return table

  # 汎用的なデータベースクエリ処理
  def fetch_table_ref(c,nn,kk,group_type='hogroup'):
    """
    nn と kk のリストに基づいてデータベースからデータを取得する。
    fiber3 と sphere テーブルを切り替えながら、table_ref を構築する。

    Args:
        c: データベース接続オブジェクト
        nn: n のリスト
        kk: k のリスト

    Returns:
        table_ref: 各 n, k に対応するデータのリスト
    """
    table_ref=[[] for _ in range(len(nn))]
    if group_type=='hogroup':
      for i in range(len(nn)):
        if i%3==0:  # fiber3 テーブルを使用
          query=f"select * from fiber3 where n={nn[i]} and k={kk[i]}"
          key='P'
        else:  # sphere テーブルを使用
          query=f"select * from sphere where n={nn[i]} and k={kk[i]}"
          key='E' if i%3==1 else 'H'  # sphere テーブルのカラム名を切り替え
        table_ref[i]=[row[key] for row in c.execute(query)]
    elif group_type=='hogroup2':
      for i in range(len(nn)):
        if i%3==1:  # fiber3 テーブルを使用
          query=f"select * from fiber3 where n={nn[i]} and k={kk[i]}"
          key='P'
        else:  # sphere テーブルを使用
          query=f"select * from sphere where n={nn[i]} and k={kk[i]}"
          key='E' if i%3==2 else 'H'  # sphere テーブルのカラム名を切り替え
        table_ref[i]=[row[key] for row in c.execute(query)]
    return table_ref

  # ジェネレーター、イメージ、矢印作成
  def create_table_gen_images_and_arrows(hg,nn,kk,odd,group_type='hogroup'):
    table_gen=[[] for _ in range(6)]
    table_image=[[] for _ in range(6)]
    table_arrow=[[] for _ in range(6)]

    for i in range(6):
      if not odd:
        if not (i==1 or i==3): continue
        for j in range(hg[i].direct_sum()):
          table_gen[i].append(hg[i].rep_linear_tex(hg[i].gen_coe_list(j)))
      elif group_type=='hogroup' or group_type=='hogroup3':
        if i==0 or i==3: 
          query=f"select * from 'fiber3' where n={nn[i]} and k={kk[i]}"
          table_gen[i].append([row['generator'] for row in c.execute(query)])
          table_gen[i]=[row['generator'] for row in c.execute(query)]
        else:
          for j in range(hg[i].direct_sum()):
            table_gen[i].append(hg[i].rep_linear_tex(hg[i].gen_coe_list(j)))
            if i<5:
              table_arrow[i].append('\longrightarrow')
      elif group_type=='hogroup2':
        if i==1 or i==4: 
          query=f"select * from 'fiber3' where n={nn[i]} and k={kk[i]}"
          table_gen[i].append([row['generator'] for row in c.execute(query)])
          table_gen[i]=[row['generator'] for row in c.execute(query)]
        else:
          for j in range(hg[i].direct_sum()):
            table_gen[i].append(hg[i].rep_linear_tex(hg[i].gen_coe_list(j)))
            if i<5:
              table_arrow[i].append('\longrightarrow')

    # even の場合の特殊処理
    if not odd:
      if table_gen[1]!=['0']:
        table_gen[2].extend(map(lambda x: 'E'+x if x and x!='0' else '', table_gen[1]))
      if table_gen[3]!=['0']:
        table_gen[2].extend(map(lambda x: f'[\iota_{ {n} },\iota_{ {n} }]'+x if x and x!='0' else '', table_gen[3]))

    # 'hogroup' のときだけ特別なロジックを適用
    if group_type=='hogroup':
      if nn[1]<=kk[1]+2:
        table_image[1]=[
          hg[2].rep_linear_tex(
            hg[2].gen_coe_to_rep_coe(
              hg[2].mod_gen_coe_list(
                hg[2].rep_coe_to_gen_coe(hg[1].gen_E_coe(j)[0])
              )
            )
          )
          for j in range(hg[1].direct_sum())
        ]
      else:
        table_image[1]=table_gen[2]

      if nn[4]<=kk[4]+2:
        table_image[4]=[
          hg[5].rep_linear_tex(
            hg[5].gen_coe_to_rep_coe(
              hg[5].mod_gen_coe_list(
                hg[5].rep_coe_to_gen_coe(hg[4].gen_E_coe(j)[0])
              )
            )
          )
          for j in range(hg[4].direct_sum())
        ]
      else:
        table_image[4]=table_gen[5]
    elif group_type=='hogroup2':
      if nn[2]<=kk[2]+2:
        table_image[2]=[
          hg[3].rep_linear_tex(
            hg[3].gen_coe_to_rep_coe(
              hg[3].mod_gen_coe_list(
                hg[3].rep_coe_to_gen_coe(hg[2].gen_E_coe(j)[0])
              )
            )
          )
          for j in range(hg[2].direct_sum())
        ]
      else:
        table_image[2]=table_gen[3]

    return table_gen,table_image,table_arrow

  # 群データ作成
  def populate_table_group(c,nn,kk,hg,odd,group_type='hogroup'):
    table_group=[[] for _ in range(6)]

    for i in range(6):
      if not odd and i==2:
        continue
      if group_type=='hogroup' or group_type=='hogroup3':
        if nn[i]<=kk[i]+2:
          query=f"select * from {'fiber3' if odd and i%3==0 else 'sphere'} where n={nn[i]} and k={kk[i]}"
        else:
          offset=2 if kk[i]%2==1 else 3
          query=f"select * from {'fiber3' if odd and i%3==0 else 'sphere'} where n={kk[i]+offset} and k={kk[i]}"
        for row in c.execute(query):
          if row['orders']==0:
            table_group[i].append('0')
          elif row['orders']==float('inf'):
            table_group[i].append('Z')
          else:
            table_group[i].append(f"Z_{int(row['orders'])}")
      else:
        if nn[i]<=kk[i]+2:
          query=f"select * from {'fiber3' if odd and i%3==1 else 'sphere'} where n={nn[i]} and k={kk[i]}"
        else:
          offset=2 if kk[i]%2==1 else 3
          query=f"select * from {'fiber3' if odd and i%3==1 else 'sphere'} where n={kk[i]+offset} and k={kk[i]}"
        for row in c.execute(query):
          if row['orders']==0:
            table_group[i].append('0')
          elif row['orders']==float('inf'):
            table_group[i].append('Z')
          else:
            table_group[i].append(f"Z_{int(row['orders'])}")

    if not odd:
      if nn[1]<=kk[1]+2:
        if table_group[1]!=['0']:
          table_group[2].extend(table_group[1])
      if nn[2]<=kk[2]+2:
        if table_group[3]!=['0']:
          table_group[2].extend(table_group[3])
      if table_group[2]==[]:
        table_group[2].append('0')

    return table_group

  # シーケンス処理
  def process_sequence(n,k,c,group_type='hogroup'):
    odd=n%2==1
    nn,kk,hogroup=create_hogroup(n,k,odd,group_type)
    ehp_map,arrows=create_ehp_map_and_arrows(n,odd,group_type)
    table=create_table(hogroup,arrows)
    table_ref=fetch_table_ref(c,nn,kk,group_type)
    hg=[HomotopyGroup(nn[i],kk[i]) for i in range(6)]
    table_gen,table_image,table_arrow=create_table_gen_images_and_arrows(hg,nn,kk,odd,group_type)
    table_group=populate_table_group(c,nn,kk,hg,odd,group_type)
    return nn,kk,hogroup,arrows,table,table_ref,table_gen,table_image,table_arrow,table_group

  # メイン処理
  nn1,kk1,HoGroup1,Arrow1,table1,table_ref1,table_gen1,table_image1,table_arrow1,table_group1=process_sequence(n,k,c,'hogroup')
  nn2,kk2,HoGroup2,Arrow2,table2,table_ref2,table_gen2,table_image2,table_arrow2,table_group2=process_sequence(n,k,c,'hogroup2')
  nn3,kk3,HoGroup3,Arrow3,table3,table_ref3,table_gen3,table_image3,table_arrow3,table_group3=process_sequence(n,k,c,'hogroup3')

  conn.close()

  m_d_sum=3
  m_d_sum2=3
  m_d_sum3=2

  return render_template('homotopy_group.html', n=n, k=k, m_d_sum=m_d_sum \
    , HoGroup=HoGroup1, Arrow=Arrow1 \
    , table_group=table_group1, table_gen=table_gen1 \
    , table_arrow=table_arrow1, table_image=table_image1, table_ref=table_ref1 \
    , m_d_sum2=m_d_sum2, HoGroup2=HoGroup2, Arrow2=Arrow2 \
    , table_group2=table_group2, table_gen2=table_gen2 \
    , table_arrow2=table_arrow2, table_image2=table_image2, table_ref2=table_ref2 \
    , m_d_sum3=m_d_sum3, HoGroup3=HoGroup3, Arrow3=Arrow3 \
    , table_group3=table_group3, table_gen3=table_gen3 \
    , table_arrow3=table_arrow3, table_image3=table_image3, table_ref3=table_ref3 
    )

if __name__=="__main__":
  app.run(debug=True)

