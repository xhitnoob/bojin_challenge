
from config import PROMPT_TABLE_SELECT,PROMPT_SQL_GENERATE_BASE,PROMPT_DB_CHAT
from langchain.utilities import SQLDatabase
from config import PROMPT_SQL_GENERATE_GG,PROMPT_SQL_GENERATE_AG_GP,PROMPT_SQL_GENERATE_AG_HY,PROMPT_SQL_GENERATE_JJ,PROMPT_SQL_GENERATE_JJ_GP,PROMPT_SQL_GENERATE_JJ_ZQ,PROMPT_SQL_GENERATE_JJ_KZZ,PROMPT_SQL_GENERATE_JJ_HQ,PROMPT_SQL_GENERATE_JJ_CY,PROMPT_SQL_GENERATE_JJ_HY,PROMPT_SQL_GENERATE_HY,PROMPT_SQL_GENERATE_JJ_GM,PROMPT_SQL_GENERATE_JJ_GP_2
class DataBaseService(object):
    def __init__(self,db,model):
        self.db=db
        self.model=model
        
    #选择数据表    
    
    def reg(self,sql):
        sql = sql.replace('"昨收盘(元)"', "昨收盘")
        sql = sql.replace('"今开盘(元)"', "今开盘")
        sql = sql.replace('"最高价(元)"', "最高价")
        sql = sql.replace('"最低价(元)"', "最低价")
        sql = sql.replace('"收盘价(元)"', "收盘价")
        sql = sql.replace('"成交量(股)"', "成交量")
        sql = sql.replace('"所属国家(地区)"', "所属国家")
  
        sql = sql.replace("昨收盘(元)","昨收盘")
        sql = sql.replace("今开盘(元)", "今开盘")
        sql = sql.replace("最高价(元)", "最高价")
        sql = sql.replace("最低价(元)", "最低价")
        sql = sql.replace("收盘价(元)", "收盘价")
        sql = sql.replace("成交量(股)", "成交量")
        sql = sql.replace("所属国家(地区)", "所属国家")
        
        sql = sql.replace("昨收盘",'"昨收盘(元)"')
        sql = sql.replace("今开盘", '"今开盘(元)"')
        sql = sql.replace("最高价", '"最高价(元)"')
        sql = sql.replace("最低价", '"最低价(元)"')
        sql = sql.replace("收盘价", '"收盘价(元)"')
        sql = sql.replace("成交量", '"成交量(股)"')
        sql = sql.replace("所属国家", '"所属国家(地区)"')

        sql = sql.replace("基金管理人", "管理人")

        # sql = sql.replace("昨收盘(元)","'昨收盘(元)'")
        # sql = sql.replace("今开盘(元)", "'今开盘(元)'")
        # sql = sql.replace("最高价(元)", "'最高价(元)'")
        # sql = sql.replace("最低价(元)", "'最低价(元)'")
        # sql = sql.replace("收盘价(元)", "'收盘价(元)'")
        # sql = sql.replace("成交量(股)", "'成交量(股)'")
        # sql = sql.replace("成交金额(元)", "'成交金额(元)'")
        # sql = sql.replace("所属国家(地区)", "'所属国家(地区)'")
        
        return sql
    
    def select_tables(self,query):
        table_names=self.db.get_table_names()
        tab=""
        for i in table_names:
                tab=tab+i+","
        q=PROMPT_TABLE_SELECT.format(table_info=self.db.table_info,input=query,table_names=tab)
        
        response=self.model.chat.completions.create(
            model="Tongyi-Finance-14B-Chat", 
            messages=[{"role": "user", "content": q}], 
            temperature=0,)
        
        tables=[]
        for t in table_names:
            if t in  response.choices[0].message.content:
                tables.append(t)
                
        return tables
    
    #生成SQL
    def generate_sql(self,query,tables):
        table_info=self.db.get_table_info(tables)
        #基于规则选择PROMPT模板
        if "港股" in query:
             PROMPT=PROMPT_SQL_GENERATE_GG
        elif "代码和股票名称" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_GP_2
        elif "基金" not in query and "行业" not in query:
             PROMPT=PROMPT_SQL_GENERATE_AG_GP
        elif "基金" not in query and "行业" in query and "股票" not in query:
             PROMPT=PROMPT_SQL_GENERATE_HY
        elif "基金" not in query and "行业" in query and "股票" in query and  "季报" not in query:
             PROMPT=PROMPT_SQL_GENERATE_AG_HY
        elif "基金" not in query and "行业" in query and "季报"  in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_HY
        elif "基金" in query and "可转债" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_KZZ
        elif "基金" in query and "投资者" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_CY
        elif "基金" in query and "申购" in query :
             PROMPT=PROMPT_SQL_GENERATE_JJ_GM
        elif "基金" in query and "赎回" in query :
             PROMPT=PROMPT_SQL_GENERATE_JJ_GM
        elif "基金" in query and "单位净值" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_HQ
        elif "基金" in query and "管理费率" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ
        elif "基金" in query and "债券" in query and "股票" not in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ_ZQ
        elif "基金" in query and "股票" in query or "重仓股" in query :
             PROMPT=PROMPT_SQL_GENERATE_JJ_GP
        elif "重股" in query :
             PROMPT=PROMPT_SQL_GENERATE_JJ_GP
        elif "基金" in query:
             PROMPT=PROMPT_SQL_GENERATE_JJ
        else:
             PROMPT=PROMPT_SQL_GENERATE_BASE
        
        q=PROMPT.format(table_info=table_info,input=query)
        response=self.model.chat.completions.create(
            model="Tongyi-Finance-14B-Chat", 
            messages=[{"role": "user", "content": q}], 
            temperature=0,)
        sql=response.choices[0].message.content
        print(sql)
        return  self.reg(sql)

    #TODO 修改SQL
    # def modify_sql(db,sql,e,prompt):
    #     prompt=prompt.format(table_info=db.table_info,sql=sql,e=e)
    #     print(prompt)
    #     return get_llm_answer(prompt)


        
    def exec_sql(self,sql):

        sql=sql
        #print(sql.content)
        try:  
            sql=sql.replace("，",",")
            result=self.db.run(sql)
        except Exception as e:
            result=""
        #answer=db.run(sql.content)
        #final_answer=get_final(answer,query)
        #return final_answer
        return result
    
    def get_answer(self,result,query):
       
        q=PROMPT_DB_CHAT.format(result=result,input=query)
        response=self.model.chat.completions.create(
            model="Tongyi-Finance-14B-Chat", 
            messages=[{"role": "user", "content": q}], 
            temperature=0,)
        return  response.choices[0].message.content
