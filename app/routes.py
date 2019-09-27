import flask
from app import instance
import app.forms
import app.model

print('Chargement du module routes.py')

@instance.route('/unused')
def main():
	# Page d'accueil définie dans main.html
	return(flask.render_template('main.html')) 

@instance.route('/', methods=['GET', 'POST'])
def show_form():
	form = app.forms.QuestionForm()
	if form.validate_on_submit():
		model = app.model.Model(form)
		model.predict()
		return flask.render_template('predict.html', 
									 title='Résultat', 
									 form=form,
									 model=model)
	else:
		print("Erreur de validation")
	return flask.render_template('predict.html', 
								 title='Question à catégoriser',
								 form=form)
