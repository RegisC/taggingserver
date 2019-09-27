import datetime
import flask_wtf
import wtforms as wtf
from wtforms.fields import StringField
from wtforms.widgets import TextArea

class QuestionForm(flask_wtf.FlaskForm):	
    question = StringField('Texte de la question', widget=TextArea())
    submit = wtf.SubmitField("Prédire les catégories de la question")
