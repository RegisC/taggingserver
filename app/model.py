import app.forms
import nltk
import numpy as np
import pandas as pd
import pickle
import re
import sklearn.linear_model

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class Model:
	def __init__(self, form):
		print("Nouveau modèle instancié")
		self.load()
		self.text = self.tokenize_text(form.question.data)
		print("Tokenized question :", self.text)
	
	def load(self):
		MODEL1_FILE = "data/supervised_model.sav"
		MODEL2_FILE = "data/unsupervised_model.sav"
		data = pickle.load(open(MODEL1_FILE, 'rb'))
		self.model1_name, self.vect1, self.labels1, self.model1 = data
		print(f"{self.model1_name} chargé.")
		data = pickle.load(open(MODEL2_FILE, 'rb'))
		self.model2_name, self.vect2, self.model2 = data
		print(f"{self.model2_name} chargé.")
		self.initialise()
		
	def predict(self):
		text_words = self.vect1.transform([self.text])
		print(f"Taille de la matrice de vocabulaire : {text_words.shape}")
		out = self.model1.predict(text_words)
		cats = [self.labels1[i] for i in np.where(out[0] == 1)[0]]		
		self.cat1 = " ".join(cats)
		self.cat2 = ""
		print(f"Prédiction par modèle {self.model1_name}: {self.cat1}")
		print(f"Prédiction 2 : {self.cat2}")

	def initialise(self):
		self.stop_words = set(nltk.corpus.stopwords.words("english"))
		new_words = ['using', 'trying', 'running', 'want', 'except', 
					 'guys', 'get', 'gives',
					 'code', 'run', 'might', 'tried', 'whenever', 'current', 
					 'name', 'try', 'must', 'know', 'looks', 'problem', 'problems',
					 'anyone', 'without', 'the', 'error', 'popular', 'really', 
					 'would', 'need', 'example', 'way', 'seem', 'possible', 
					 'thank', 'something', 'however', 'able', 'solution', 'think',
					 'question', 'issue', 'sure', 'expect', 'another']
		self.stop_words = self.stop_words.union(new_words)
		print(f"Nombre total de mots à ignorer : {len(self.stop_words)}")	

	def get_replace_list(self):
		# Avant suppression des chiffres, nous préservons certains termes
		replace_list = [('vt100', 'vthundred'),
						('port 25', 'porttwentyfive'),
						('port 8000', 'porteightthousand'),
						('port 8080', 'porteightyeighty'),
						('2D', 'twodim'),
						('3D', 'threedim'),
						('vt100', 'vthundred'),
						('c#', 'csharp'),
						('in c', 'clanguage'),
						('c++11', 'cppeleven'),
						('c++', 'cpp'),
						('g++', 'gpp'),
						('s3', 'sthree'),
						('x64', 'xsixtyfour'),
						('i386', 'ithreeeightsix')
						]
		return replace_list
		
	def get_regex_list(self):
		regex_list = [(r'\br\b', 'RSoftware'), (r'\s.net\b', 'dotnet')]
		return regex_list

	def replace_words_containing_non_alphas(self, s):
		for w1, w2 in self.get_replace_list():
			s = s.replace(w1, w2)
		for w1, w2 in self.get_regex_list():
			s = re.sub(w1, w2, s)
		return s
		
	def tokenize_text(self, s): 
		# Suppression des balises HTML
		cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
		s = re.sub(cleanr, '', s.lower())    
		# Élimine chiffres et caractères spéciaux des mots importants
		s = self.replace_words_containing_non_alphas(s)
		# Suppression des caractères non alphabétiques
		s = re.sub(r'[^a-zA-Z]', ' ', s)    
		# Suppression des mots dans `stop_words`
		s = [w for w in nltk.tokenize.word_tokenize(s) if w not in self.stop_words]    
		# Lemmatisation
		stemmed = []
		lemmatizer = nltk.stem.WordNetLemmatizer() 
		for item in s:
			w = lemmatizer.lemmatize(item, pos='n')
			stemmed.append(lemmatizer.lemmatize(w, pos='v'))
		return ' '.join(stemmed)  