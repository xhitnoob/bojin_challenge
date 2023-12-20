from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import FAISS
from langchain.schema import Document
from langchain.document_loaders import PyPDFium2Loader,PyMuPDFLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings
import jsonlines
from openai import  OpenAI
from config import emb_model_path,kb_path
from config import PROMPT_COMPANY_NAME
import tqdm
import os 

def read_data(path):
    content = []
    with jsonlines.open(path, "r") as json_file:
        for obj in json_file.iter(type=dict, skip_invalid=True):
            content.append(obj)
    return content

def save_data(path,data):
    with jsonlines.open(path, "w") as json_file:
        for d in data:
            json_file.write(d)
         
def format_data(input_path,output_path):
    data=read_data(input_path)
    data2=[]
    for  d in data:
        d2={"id":d["id"],"question":d["question"],"answer":d["answer"]}
        data2.append(d2)
    save_data(path=output_path,data=data2)      
     
def load_emb_model(model):
    emb= HuggingFaceBgeEmbeddings(model_name=model,model_kwargs={"device":"cpu"})
    return emb


def get_llm():
        model = OpenAI(base_url='http://127.0.0.1:8000/v1', api_key='none')
        return model
    
    
def split_text(content,file_name):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=256,
        #chunk_size=128,
        chunk_overlap=48,
        #chunk_overlap=24,
        separators=['\n\n','\n','。'],
        )
    docs=splitter.split_text(content)
    return [Document(page_content=doc,metadata={"name":file_name}) for doc in docs]
    

def create_db(text,emb_model,file_name,kb_path):
    vs=FAISS.from_documents(text,emb_model)
    vs.save_local(kb_path,index_name=file_name)   
    return vs

#提取招股说明书起始和结尾的文段
def get_raw_company(pdf_path):
    datanames = os.listdir(pdf_path)
    raw_company=[]
    for d in tqdm.tqdm(datanames):
        path="/tcdata/bs_challenge_financial_14b_dataset/pdf/{file_name}"
        path=path.format(file_name=d)
        loader=PyMuPDFLoader(path)
        data=loader.load_and_split()
        if len(data[0].page_content)<10:
            raw_company.append([data[1].page_content,data[-2].page_content,data[-1].page_content])
        else:
            raw_company.append([data[0].page_content,data[-2].page_content,data[-1].page_content])
    return raw_company 

#获取公司名
def get_company(raw_company):
    company=[]
    model=get_llm()
    for r in tqdm.tqdm(raw_company):
        r="/n".join([d for d in r])    
        q=PROMPT_COMPANY_NAME.format(info=r)
        response=model.chat.completions.create(
                model="Tongyi-Finance-14B-Chat", 
                messages=[{"role": "user", "content": q}], 
                temperature=0,)
        c=response.choices[0].message.content
        c=c.replace("青島銀行","青岛银行")
        c=c.replace("。","")
        c=c.replace("，","")
        c=c.replace(" ","")
        company.append(c)
    company.append("华瑞股份")
    company.append("国科微电子")
    company.append("勤上")
    company.append("真兰仪表")
    company.append("旷达汽车")
    return company

#对问题进行分类
def question_cls(company):
    data=read_data("/tcdata/question_v2.json")
    count=0
    for d in tqdm.tqdm(data):
        q=d["question"]
        for c in company:
            if len(c)>=4:                
                c=c[:4]
            if c in q:
                d["type"]=0
                count+=1
    save_data(data=data,path="./question_cls.jsonl")

    