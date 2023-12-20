from utils import get_llm ,read_data,save_data,format_data,get_raw_company,get_company,question_cls
from langchain.utilities import SQLDatabase
from sql_query import DataBaseService
from config import PROMPT_QUERY_CLS ,model_path,txt_path,kb_path,pdf_path
from knowledge_query import KnowledgeBaseService
import tqdm


def main():
    raw_company =get_raw_company(pdf_path)
    company=get_company(raw_company)
    question_cls(company)
    
    questions = read_data('./question_cls.jsonl')
    model=get_llm()
    db=SQLDatabase.from_uri("sqlite:////tcdata/bs_challenge_financial_14b_dataset/dataset/博金杯比赛数据.db")   
    dbservice=DataBaseService(db=db,model=model)
    kbservice=KnowledgeBaseService(txt_path=txt_path,kb_path=kb_path,model=model)
    kbservice.create_kb()
    try:
            for q in tqdm.tqdm(questions):   
                query=q['question']
                if q.get("type")==0 :           
                    info=kbservice.search_info(query=query)
                    answer=kbservice.get_answer(info=info,query=query)
                    q['answer']=answer
                else :
                    tables=dbservice.select_tables(query)
                    sql=dbservice.generate_sql(tables=tables,query=query)
                    result=dbservice.exec_sql(sql=sql)
                    if len(result)>200:
                        result=result[:200]
                    answer=dbservice.get_answer(result=result,query=query)
                    q["type"]=1
                    q['answer']=answer
            save_data("./result.jsonl",data=questions)
            format_data("./result.jsonl","./submit_result.jsonl")
    except Exception as e:
        print(e)
        save_data("./result.jsonl",data=questions)
        format_data("./result.jsonl","./submit_result.jsonl")
if __name__=="__main__":
    main()
    