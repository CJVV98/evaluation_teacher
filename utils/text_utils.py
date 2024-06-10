

import nltk
#nltk.download('punkt')  # Necesario solo la primera vez para descargar los modelos necesarios
from nltk.tokenize import sent_tokenize


def split_paragraph(text):
    sentences = sent_tokenize(text)
    return sentences

def split_connectors(text):
    connectors = ["sin embargo","pero","no obstante","mientras tanto",".","sinembargo","igualmente","a pesar de",
                  "en cambio","a diferencia de","a pesar de","a pesar de que","contrariamente","no obstante","al contrario"]
    text=text.lower()

    for e in connectors:
        text=text.replace(e, "\n")  
    sentences = text.split("\n")
    return sentences

def separate_paragraph(paragraph):
    comments = []
    comment_valid=""
    sentences = split_paragraph(paragraph)
    for text in sentences:
      if(text.strip() != "" and len(text.strip()) > 12):
        split_sentence=split_connectors(text)
      else:
        split_sentence=[text]
      comment_valid=""
      for sentence in split_sentence:
        if(comment_valid.strip() == "" or (comment_valid.strip().count(".")== 0 and len(comment_valid.strip()) < 15)):   
          comment_valid=comment_valid+" "+sentence.strip()
        if(comment_valid.strip() != ""  and len(comment_valid.strip()) >= 15):
          comment_valid = comment_valid.replace(".", "").replace(",", "").replace(";", "")  
          comment_valid=comment_valid.strip()        
          comments.append(comment_valid)
          comment_valid=""
    return comments
