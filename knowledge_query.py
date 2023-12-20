import os 
from utils import create_db,split_text,load_emb_model
from langchain import FAISS
import tqdm
from config import PROMPT_KB_CHAT,emb_model_path

class KnowledgeBaseService(object):
    def __init__(self,txt_path,kb_path,model,**kwargs):
        self.txt_path=txt_path
        self.kb_path=kb_path
        self.emb_model=load_emb_model(emb_model_path)
        self.model=model
        
    def get_file_names(self):
        datanames = os.listdir(self.txt_path)
        return  datanames

    def read_data(self,datanames):
        dataset={}
        for i in datanames :
            with open(self.txt_path+i) as f:
                data=f.read()
                dataset[i]=data
                f.close()
        return dataset        
    def create_kb(self):
        if os.path.exists(self.kb_path):
            print("知识库已存在！")
        else:
            datanames=self.get_file_names()
            dataset=self.read_data(datanames)
            
            #创建local知识库
            for i in tqdm.tqdm(datanames):
                doc=split_text(dataset[i],i)
                create_db(doc,self.emb_model,i,self.kb_path)
                
            #创建global知识库 
            docs=[]
            for i in tqdm.tqdm(datanames):
                doc=split_text(dataset[i],i)
                docs+=doc
            create_db(docs,self.emb_model,"all",self.kb_path)
            print("知识库创建成功！")
            
    def search_info(self,query):

        glob=FAISS.load_local(self.kb_path,index_name="all",embeddings=self.emb_model)
        d=glob.similarity_search(query,k=1)
        index=d[0].metadata['name']
        if "公司" in query:
            query1="公司"+query.split("公司")[1]
        else:
            query1=query
        print("问题是："+query1)
        local1=FAISS.load_local(self.kb_path,index_name=index,embeddings=self.emb_model)
        d2=local1.similarity_search(query1,k=8)
        info = "\n".join([doc.page_content for doc in d2])
        #prompt=prompt.format(info=info,query=query)
        #answer=get_llm_answer(prompt,remote_api=False)
        return info
    
    def get_answer(self,info,query):
        q=PROMPT_KB_CHAT.format(info=info,input=query)
        response=self.model.chat.completions.create(
            model="Tongyi-Finance-14B-Chat", 
            messages=[{"role": "user", "content": q}], 
            temperature=0,)
        return  response.choices[0].message.content
    