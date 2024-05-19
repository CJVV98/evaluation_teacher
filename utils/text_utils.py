

import nltk
#nltk.download('punkt')  # Necesario solo la primera vez para descargar los modelos necesarios
from nltk.tokenize import sent_tokenize


def split_paragraph(text):
    sentences = sent_tokenize(text)
    return sentences

def split_connectors(text):
    connectors = ["sin embargo","pero","no obstante","además","en cambio","por otro lado","ya que","por ende","puesto que",
                  "por consiguiente", "por ultimo",".","sinembargo","igualmente","de la misma forma"]
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
      split_sentence=split_connectors(text)
      for sentence in split_sentence:
        if(sentence.strip() != "" and sentence.strip().count(" ") == 1):
          comment_valid=sentence.strip()
        if(sentence.strip() != "" and sentence.strip().count(" ") > 1):             
          comments.append(comment_valid+sentence.strip())
          comment_valid=""

    return comments
