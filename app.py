from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète_ici'

categoriesDepenses = [
    {'id': 1, 'libelleCategorie': 'Autoroute', 'budget': 'déplacement'},
    {'id': 2, 'libelleCategorie': 'Carburant', 'budget': 'déplacement'},
    {'id': 3, 'libelleCategorie': 'Repas', 'budget': 'hébergement'},
    {'id': 4, 'libelleCategorie': 'Hébergement', 'budget': 'hébergement'}
]

depenses = [
    {'id': 1, 'destinataireDepense': 'Service d\'autoroute Vinci', 'montant': '35', 'description': 'Péages Belfort-Lyon', 'date_depense': '2014-04-20', 'categorieDepense_id': 1, 'image': 'img_depense_1.png'},
    {'id': 2, 'destinataireDepense': 'Organisation ACD', 'montant': '410.47', 'description': 'Comité de direction', 'date_depense': '2014-07-03', 'categorieDepense_id': 3, 'image': 'img_depense_2.png'},
    {'id': 3, 'destinataireDepense': 'intendance UTBM', 'montant': '120', 'description': 'forum étudiants', 'date_depense': '2014-08-18', 'categorieDepense_id': 4, 'image': 'img_depense_4.png'},
    {'id': 4, 'destinataireDepense': 'Autoroute Ouest', 'montant': '25.5', 'description': 'Péages Paris-Nantes', 'date_depense': '2014-07-28', 'categorieDepense_id': 1, 'image': 'img_depense_3.png'},
    {'id': 5, 'destinataireDepense': 'TotalEnergies', 'montant': '45', 'description': 'Sans plomb 95 35L', 'date_depense': '2014-04-14', 'categorieDepense_id': 2, 'image': 'img_depense_5.png'},
    {'id': 6, 'destinataireDepense': 'Hilton Hotels & Resorts', 'montant': '842', 'description': 'Hotel Hilton Paris', 'date_depense': '2014-01-06', 'categorieDepense_id': 4, 'image': 'img_depense_6.png'},
    {'id': 7, 'destinataireDepense': 'Service d\'autoroute Vinci', 'montant': '42.00', 'description': 'Péages Belfort-Paris', 'date_depense': '2014-12-07', 'categorieDepense_id': 1, 'image': 'img_depense_1.png'},
    {'id': 8, 'destinataireDepense': 'TotalEnergies', 'montant': '75', 'description': 'Diezel 60L', 'date_depense': '2014-10-31', 'categorieDepense_id': 2, 'image': 'img_depense_3.png'}
]


@app.route('/')
def show_accueil():
    return render_template('layout.html')


@app.route('/categorie-depense/show')
def show_categorie_depense():
    return render_template('categorie_depense/show_categorie_depense.html', categories=categoriesDepenses)

@app.route('/categorie-depense/add', methods=['GET'])
def add_categorie_depense():
    return render_template('categorie_depense/add_categorie_depense.html')

@app.route('/categorie-depense/add', methods=['POST'])
def valid_add_categorie_depense():
    try:
        new_id = max(c['id'] for c in categoriesDepenses) + 1
        nouvelle_categorie = {
            'id': new_id,
            'libelleCategorie': request.form['libelleCategorie'],
            'budget': request.form['budget']
        }
        categoriesDepenses.append(nouvelle_categorie)
        flash('Catégorie ajoutée avec succès!', 'success')
        return redirect(url_for('show_categorie_depense'))
    except Exception as e:
        flash(f'Une erreur s\'est produite : {str(e)}', 'danger')
        return redirect(url_for('add_categorie_depense'))

@app.route('/categorie-depense/delete')
def delete_categorie_depense():
    id = int(request.args.get('id'))
    categorie = next((cat for cat in categoriesDepenses if cat['id'] == id), None)
    if categorie:
        if not any(d['categorieDepense_id'] == id for d in depenses):
            categoriesDepenses.remove(categorie)
            flash('Catégorie supprimée avec succès!', 'success')
        else:
            flash('Impossible de supprimer une catégorie contenant des dépenses.', 'danger')
    return redirect('/categorie-depense/show')

@app.route('/categorie-depense/edit/<int:id>', methods=['GET'])
def edit_categorie_depense(id):
    categorie = next((cat for cat in categoriesDepenses if cat['id'] == id), None)
    if categorie is None:
        flash('Catégorie non trouvée.', 'danger')
        return redirect(url_for('show_categorie_depense'))
    return render_template('categorie_depense/edit_categorie_depense.html', categorie=categorie)

@app.route('/categorie-depense/edit', methods=['POST'])
def valid_edit_categorie_depense():
    try:
        id = int(request.form['id'])
        categorie = next((cat for cat in categoriesDepenses if cat['id'] == id), None)
        if categorie:
            categorie['libelleCategorie'] = request.form['libelleCategorie']
            categorie['budget'] = request.form['budget']
            flash('Catégorie mise à jour avec succès!', 'success')
        else:
            flash('Catégorie non trouvée.', 'danger')
        return redirect(url_for('show_categorie_depense'))
    except Exception as e:
        flash(f'Une erreur s\'est produite : {str(e)}', 'danger')
        return redirect(url_for('show_categorie_depense'))


@app.route('/depense/show')
def show_depense():
    return render_template('depense/show_depense.html', depenses=depenses, categories=categoriesDepenses)
@app.route('/depense/add', methods=['GET'])
def add_depense():
    return render_template('depense/add_depense.html', categories=categoriesDepenses)

from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

@app.route('/depense/add', methods=['POST'])
def valid_add_depense():
    try:
        if request.method == 'POST':
            new_id = max(d['id'] for d in depenses) + 1
            nouvelle_depense = {
                'id': new_id,
                'destinataireDepense': request.form['destinataireDepense'],
                'montant': float(request.form['montant']),
                'description': request.form['description'],
                'date_depense': request.form['date_depense'],
                'categorieDepense_id': int(request.form['categorieDepense_id']),
                'image': request.form.get('image', '')
            }
            depenses.append(nouvelle_depense)
            flash('Dépense ajoutée avec succès!', 'success')
            return redirect(url_for('show_depense'))
    except KeyError as e:
        flash(f'Erreur: Champ manquant - {str(e)}', 'danger')
    except ValueError as e:
        flash(f'Erreur: Valeur invalide - {str(e)}', 'danger')
    except Exception as e:
        flash(f'Une erreur inattendue s\'est produite: {str(e)}', 'danger')

    return redirect(url_for('add_depense'))

@app.route('/depense/delete')
def delete_depense():
    id = int(request.args.get('id'))
    depense = next((dep for dep in depenses if dep['id'] == id), None)
    if depense:
        depenses.remove(depense)
        flash('Dépense supprimée avec succès!', 'success')
    return redirect('/depense/show')

@app.route('/depense/edit', methods=['GET'])
def edit_depense():
    id = int(request.args.get('id'))
    depense = next((dep for dep in depenses if dep['id'] == id), None)
    if depense is None:
        flash('Dépense non trouvée.', 'danger')
        return redirect('/depense/show')
    return render_template('depense/edit_depense.html', depense=depense, categories=categoriesDepenses)

@app.route('/depense/edit', methods=['POST'])
def valid_edit_depense():
    id = int(request.form['id'])
    depense = next((dep for dep in depenses if dep['id'] == id), None)
    if depense:
        depense['destinataireDepense'] = request.form['destinataireDepense']
        depense['montant'] = request.form['montant']
        depense['description'] = request.form['description']
        depense['date_depense'] = request.form['date_depense']
        depense['categorieDepense_id'] = int(request.form['categorieDepense_id'])
        depense['image'] = request.form.get('image', '')
        flash('Dépense mise à jour avec succès!', 'success')
    return redirect('/depense/show')


@app.route('/depense/filtre', methods=['GET'])
def filtre_depense():
    categorie_id = request.args.get('categorie', type=int)
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    montant_min = request.args.get('montant_min', type=float)
    montant_max = request.args.get('montant_max', type=float)

    depenses_filtrees = depenses.copy()

    if categorie_id:
        depenses_filtrees = [d for d in depenses_filtrees if d['categorieDepense_id'] == categorie_id]

    if date_debut:
        depenses_filtrees = [d for d in depenses_filtrees if d['date_depense'] >= date_debut]

    if date_fin:
        depenses_filtrees = [d for d in depenses_filtrees if d['date_depense'] <= date_fin]

    if montant_min is not None:
        depenses_filtrees = [d for d in depenses_filtrees if float(d['montant']) >= montant_min]

    if montant_max is not None:
        depenses_filtrees = [d for d in depenses_filtrees if float(d['montant']) <= montant_max]

    return render_template('depense/front_depense_filtre_show.html', depenses=depenses_filtrees, categories=categoriesDepenses)

if __name__ == '__main__':
    app.run(debug=True)