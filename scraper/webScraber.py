import requests
from bs4 import BeautifulSoup
import csv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import unicodedata as ud
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
# Download required NLTK datasets
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


class webScraber:
        link=''
        elements=[]
        filename=''
        def __init__(self, link,elements,filename):
             self.link=link
             self.elements=elements
             self.filename=filename
             
        def scrape_data(self, link, elements):
                _data = requests.get(link)
                content = _data.text
                soup = BeautifulSoup(content, 'html.parser')
                data=[]
                for _tag in elements:
                    name_of_tag=soup.find(_tag)
                    tag_content=name_of_tag.text.strip() if name_of_tag else ""
                    data.append(tag_content)
                print("complete scraping content")
                return data
            
               
     
        def scrape_metadata(self,link):
            metadata = []
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract meta tags with name attribute set to "description"
            meta_description_tags = soup.find_all('meta', attrs={'name': 'description'})
            
            # Extract other meta tags
            meta_other_tags = soup.find_all('meta', attrs={'name': lambda x: x != 'description'})
            
            # Append meta description tags to metadata list
            for tag in meta_description_tags:
                tag_attrs = tag.attrs
                metadata.append(tag_attrs)
                
            # Append other meta tags to metadata list
            for tag in meta_other_tags:
                tag_attrs = tag.attrs
                metadata.append(tag_attrs)
                    
            print("Completed scraping metadata")
            return metadata
            
        def cleanMetadata(self,data):
            _string = ''
            for _data in data:
                if 'content' in _data:
                    _string += _data['content']
            return _string
       
        def save_to_csv(self, data):
            with open(self.filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames=self.elements+['meta data']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in data:
                    writer.writerow(item)
            print("complete saving")
      
        def init(self):
            
            _data=[]
            for index, _link in enumerate(self.link):
                    dictionary={}
                    meta_data= self.scrape_metadata(_link)
                    scrape_data_= self.scrape_data(_link, self.elements)
                    data = [self.cleanMetadata(meta_data)]
                    for index, row in enumerate( scrape_data_):
                        dictionary[self.elements[index]]=row
            
                    dictionary["meta data"]=data
                    _data.append(dictionary)
                    
                
           
            self.save_to_csv(_data)
            

class CleanData:
        
        
        def to_unicode(text):
            return ud.normalize('NFKD', text).encode('ascii','ignore').decode('utf-8','ignore')
        
        # function to remove punctuations
        def remove_punctuation(text):
            text = text.lower()
            lst = [c for c in text if c not in string.punctuation]
            return ''.join(lst)

        # function to remove stopwords
        def remove_stopwords(text):
            stop_words = stopwords.words('english')
            stop_words.extend(['contact','us'])
            lst = [word for word in text.split() if word not in stop_words]
            return ' '.join(lst)
        
        # we also need to remove numbers from the text
        def remove_number(text):
            return ''.join([i for i in text if not i.isdigit()])
        
        
        # function for stemming
        def stemming(text):
            stemmer = SnowballStemmer('english')
            l = [stemmer.stem(word) for word in text.split()]
            return " ".join(l)

