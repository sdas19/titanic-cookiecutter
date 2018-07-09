#imports
import requests
from requests import session
import os
from dotenv import load_dotenv, find_dotenv
import logging

#make a dictionary for payload for post
payload ={
    'action' : 'login',
    'username' : os.environ.get("KAGGLE_TITANIC_USERNAME"),
    'password' : os.environ.get("KAGGLE_TITANIC_PASSWORD")
}

#create function which will write to .csv file after downloading the data from url
def extract_data(url,path):
    with session() as c:
        c.post("https://www.kaggle.com/account/login",data=payload)
        #open file to write
        with open(path, 'w') as handle:
            response = c.get(url,stream = True)
            for block in response.iter_content(1024):
                handle.write(block)
            
def main(project_dir):
    
    #setup logger
    logger = logging.getLogger(__name__)
    logger.info('getting raw data')
    
    #define urls    
    #url for the train file
    train_url = "https://storage.googleapis.com/kaggle-competitions-data/kaggle/3136/train.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1531387679&Signature=mwuqW%2BkO%2BveR8UiPmFn2MxE3zYGtwYHIWPWdH%2Fj7HevVxia1TSZH2DH1uJVE%2BLKr%2FTumpRVs5l9GxBSH51FT%2FGBUMm3FsIW6KWx%2FfdOq1ufeVe%2B7rgvAKJp2Iicx5UOqzPYxEhq3W9vbGHCLg30mtlMaoao16mcl3YxTdbgiI1wc8%2B9JhQbb%2BC2pdl8fLZcMorflOGnW9Y4y%2BMBdPLzVwjjwbLZx4wmLmFZodEJ0XJ5A%2Bd9v717K52JeURC8s0WJBa01e1GRvcKHXBY6yLcolrY6axYnuLDyUmGYl4F2WBJCoCC7pF1YHfnJcoYgLY3zOGlyJqAVJD1CYrz7PTFtQQ%3D%3D"
    #url for the test file
    test_url = "https://storage.googleapis.com/kaggle-competitions-data/kaggle/3136/test.csv?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1531388547&Signature=G1rVf9BMR9Uh4%2B4ahQ1B8WwiVp8J7BUIGLzxpDZ3M4KyzOoZmHfUHsWkfQ4viLJ2Zl5r86FXFiLTdGIq1wXW7OI8rT1Dnf54%2BDI6lWZzGcnmjry9DEBual%2FQkS6yr5ROLafHcTWI3vYO8slNFncIYpd0iMBFj0Y3cOD7sQnim6Jw69Mmwe%2FsbbbRzqabs7I3NkMPreZ6bVhEN5504jDytv892KGg7LKObEQ%2FJrtcLeWcAP%2BmiatnNvbfnr49LDM%2Fj1rP%2BQ5oUecSh4qzoVYEsHTvFSbVRKwoiKI6gO4kDZNNb1splEzowYm%2BHa2BDLfX4tty84uwCRWNIQKAgi0uFQ%3D%3D"

    #raw data path
    raw_data_path=os.path.join(project_dir,'data','raw')
    #train_data_path
    train_data_path=os.path.join(raw_data_path,'train.csv')
    #test_data_path
    test_data_path=os.path.join(raw_data_path,'test.csv')

    #extract data
    extract_data(train_url,train_data_path)
    extract_data(test_url,test_data_path)
    logger.info('downloaded raw training and test data')
    
if(__name__=='__main__'):
    
    #getting root directory
    project_dir = os.path.join(os.path.dirname(__file__),os.pardir,os.pardir)
    
    log_fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level= logging.INFO, format = log_fmt)
    
    #find dotenv automatically by walking up directories until it is found
    dotenv_path= find_dotenv()
    #load up the entries as environment variable
    load_dotenv(dotenv_path)
    
    #call the main
    main(project_dir)