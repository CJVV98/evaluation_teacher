import nltk # type: ignore
import pandas as pa; # type: ignore
import numpy as np; # type: ignore
import re;
import spacy # type: ignore
import tabula # type: ignore

from sklearn import svm, datasets # type: ignore
from nltk import SnowballStemmer # type: ignore
from unidecode import unidecode # type: ignore
from nltk.tokenize import word_tokenize # type: ignore
from nltk.corpus import stopwords # type: ignore
from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.svm import SVC # type: ignore
from sklearn.multiclass import OneVsRestClassifier # type: ignore
from sklearn.metrics import accuracy_score, classification_report # type: ignore
from nltk.sentiment import SentimentIntensityAnalyzer # type: ignore
from sklearn.svm import LinearSVC # type: ignore
from sklearn.preprocessing import StandardScaler # type: ignore
from sklearn.metrics import confusion_matrix # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore
from joblib import dump, load # type: ignore
from model_manage.models import Model
from datetime import datetime

nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load('es_core_news_sm')

class ModelSupportVectorMachine:
  RUTA='/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/'
  def proc_info(self,word):
    #Eliminar caracteres especiales
    letters_comment = re.sub("[^A-Za-záéíóúñÁÉÍÓÚÑ]", " ", word)
    #Eliminar palabras repetidas más de dos veces
    repeat_words = re.sub("(.)\\1{2,}", "\\1\\1", letters_comment)
    #Si vienen con guion intermedio
    union_words = re.sub("([A-Za-z]+)-([A-Za-z]+)", "\\1\\2", repeat_words);
    #Conversión de mayúsculas a minúsculas
    lower_words=union_words.lower();
    return lower_words

  def proc_tokenize(self,lower_words):
    #Tokenizar el comentario por palabras
    tokens = word_tokenize(lower_words)
    tokens_words=[x for x in tokens if len(x) > 1]
    return tokens_words

  def delete_stop_word(self,tokens_words):
    #Eliminar StopWords
    stop = set(stopwords.words('spanish'))
    # Guardar en la lista las palabras que no son stopwords
    stop.discard("no")
    stop.discard("es")
    stop_tokens = [w for w in tokens_words if w not in stop]
    stop_token_ = [word.strip() for word in stop_tokens]
    return stop_token_


  def lemmatize_words(self,word):
    doc = nlp(word)
    lemmas = [tok.lemma_.lower() for tok in doc]
    return lemmas


  def proc_lemmatize_and_stemming(self,stop_tokens):
    SnowballStemmer('spanish')
    #Se lematiza por palabra
    lemmas = [model.lemmatize_words(word) for word in stop_tokens]
    stems = [' '.join([item[0] for item in lemmas])]
    #Se hace stemming para definir las raices de las palabras
    #stems = [' '.join([spanishstemmer.stem(lemma) for lemma in flattened_list])]
    comment_proc=str(stems)
    comment_proc = re.sub("[^A-Za-záéíóúñÁÉÍÓÚÑ]", " ", comment_proc)
    return comment_proc



  def remove_emojis(self,text):
      # Utiliza una expresión regular para eliminar emojis
      emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticones
                            u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
                            u"\U0001F680-\U0001F6FF"  # transporte y mapas
                            u"\U0001F700-\U0001F77F"  # alquimia, flechas, etc.
                            u"\U0001F780-\U0001F7FF"  # Geométricos Extendidos
                            u"\U0001F800-\U0001F8FF"  # Suplemento de Área de Planos
                            u"\U0001F900-\U0001F9FF"  # Símbolos de Lenguaje de Señas
                            u"\U0001FA00-\U0001FA6F"  # Símbolos Arqueológicos
                            u"\U0001FA70-\U0001FAFF"  # Símbolos CJK de Letras y Puntuación
                            u"\U00002702-\U000027B0"  # Diversos (Check, Cross, etc.)
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)

      # Reemplaza los emojis con una cadena vacía
      return emoji_pattern.sub(r'', text)

  def proc_vectorizer(self,comment):
      vectorizer = model.load_vectorizador()
      new_comment=vectorizer.transform([comment])
      return new_comment

  def proc_text(self,comment):
    words=model.proc_info(comment)
    words_tokenize=model.proc_tokenize(words)
    words_delete_stop_word=model.delete_stop_word(words_tokenize)
    words_lemmatizee=model.proc_lemmatize_and_stemming(words_delete_stop_word)
    return words_lemmatizee

  def train_model_with_parameters(counts_comments,parameter_c,parameter_gamma,parmeter_random, kernel):
    match int(counts_comments):
      case 3000:
        name_file=model.RUTA+'dataset_test.csv'
      case 4000:
        name_file=model.RUTA+'dataset_test.csv'
      case _:  
        name_file=model.RUTA+'dataset_test.csv'

    model.load_file(name_file,int(parameter_c),float(parameter_gamma),int(parmeter_random), kernel) 
      

  def load_file(self,name_file,parameter_c,parameter_gamma,parmeter_random, kernel):
    #dwn_url_pruebas='/content/drive/MyDrive/ProyectoGrado/Maestria/Evaluaciones/dataset_test__44.csv'
    date_start=datetime.now()
    dwn_url_pruebas=name_file
    df_pruebas = pa.read_csv(dwn_url_pruebas, encoding='utf-8',header=None, sep=';')
    df_pruebas.columns=["Comentario","Emocion"]

    df_test = pa.DataFrame(columns=['Comentario', 'Emocion'])
    print(df_test)
    for index, row in df_pruebas.iterrows():
        comment = str(row['Comentario'])
        comment_without_emojis = model.remove_emojis(comment)
        comment_proc = model.proc_text(comment_without_emojis)
        new_row = pa.DataFrame({'Comentario': comment_proc, 'Emocion': row['Emocion']},index=[0])
        df_test = pa.concat([df_test, new_row], ignore_index=True)
    mapeo = {'scared': 0, 'mad': 1, 'sad': 2, 'surprise':3,'joyful':4, 'trust':5,'others':6}
    df_test['Emocion'] = df_test['Emocion'].map(mapeo)
    model.training_model(df_test,dwn_url_pruebas,date_start,parameter_c,parameter_gamma,parmeter_random, kernel)


  def training_model(self,df_test,name_file,date_start,parameter_c,parameter_gamma,parmeter_random, kernel):
      
    # Dividir los datos en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(df_test["Comentario"],df_test["Emocion"], test_size=0.2, random_state=parmeter_random)

    # Escalamiento de datos

    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Inicializar y entrenar el modelo SVM
    svm_model  = SVC(C=parameter_c, cache_size=200, class_weight=None, coef0=0.0,
      decision_function_shape='ovr', degree=6,
      gamma=parameter_gamma, kernel=kernel,
      probability=False, random_state=42, shrinking=True,
      verbose=False)
    y_train_encoded = y_train
    svm_model.fit(X_train_tfidf, y_train_encoded)

    # Realizar predicciones en el conjunto de prueba
    y_pred = svm_model.predict(X_test_tfidf)


    y_test_encoded = y_test
    accuracy = accuracy_score(y_test_encoded, y_pred)
    
    measurment=classification_report(y_test_encoded, y_pred)
    list_measurment=model.convert_str_to_list(measurment)
    #Matriz de confusión
    cm = confusion_matrix(y_test_encoded, y_pred)
    date_end=datetime.now()
    print(date_start,date_end)
    Model.objects.create(file=name_file, count_register=len(df_test),parameter_training=20,precision=float(accuracy),
                                    list_measurement=list_measurment,matrix=cm.tolist(),date_start=date_start,date_end=date_end)


  def convert_str_to_list(self,list_measurment):
    list_measurment_convert=[]
    rows = list_measurment.strip().split('\n')
    for row in rows:
        if(row.strip() != ''):
          row=row.replace("avg","")
          row=row.replace("accuracy","accuracy - - ")
          word_text = row.split()
          fila_convertida = [float(word) if word.replace('.', '', 1).isdigit() else word for word in word_text] 
          list_measurment_convert.append(fila_convertida)
    list_measurment_convert.pop(0)
    return  list_measurment_convert  

  def load_model():
    modelo_cargado = load('/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/evaluacion_docente_svm.joblib')
    return modelo_cargado



  def load_vectorizador():
    model_vec = load('/Users/corinviracacha/Documents/Proyectos/ProyectoEvaluacionDocente/evaluation_teacher/utils/resources/vectorizador.joblib')
    return model_vec



model=ModelSupportVectorMachine()

