from datetime import datetime
import data_access


# ========== CALCULS SIMPLES ==========
def calculer_taux_disponibilite():
    equipements = data_access.obtenir_tous_equipements()

    # Compter par type
    stats_types = {}  # {type: {'total': 0, 'actifs': 0}}

    for eq in equipements:
        type_eq = eq['type']

        # Initialiser si pas encore vu
        if type_eq not in stats_types:
            stats_types[type_eq] = {'total': 0, 'actifs': 0}

        # Compter
        stats_types[type_eq]['total'] += 1
        if eq['statut'] == 'actif':
            stats_types[type_eq]['actifs'] += 1

    # Calculer le pourcentage
    resultats = {}
    for type_eq, stats in stats_types.items():
        if stats['total'] > 0:
            pourcentage = (stats['actifs'] / stats['total']) * 100
            resultats[type_eq] = round(pourcentage, 2)

    return resultats


def calculer_indice_fiabilite():
    equipements = data_access.obtenir_tous_equipements()
    interventions = data_access.obtenir_interventions_completes()

    # Regrouper les interventions par équipement
    interventions_par_equipement = {}
    for inter in interventions:
        eq_id = inter['equipement_id']
        if eq_id not in interventions_par_equipement:
            interventions_par_equipement[eq_id] = []
        interventions_par_equipement[eq_id].append(inter)

    resultats = []
    date_maintenant = datetime.now()

    for eq in equipements:
        eq_id = eq['id']
        inters = interventions_par_equipement.get(eq_id, [])

        # Compter les pannes (interventions correctives)
        nb_pannes = 0
        cout_total = 0
        for inter in inters:
            if inter['type_intervention'] == 'corrective':
                nb_pannes += 1
            cout_total += inter['cout']

        # Calculer l'âge en années
        date_acq = datetime.strptime(eq['date_acquisition'], '%Y-%m-%d')
        age_jours = (date_maintenant - date_acq).days
        age_annees = age_jours / 365

        # Calculer l'indice (score sur 100)
        score = 100

        # Enlever des points pour chaque panne
        score -= nb_pannes * 15

        # Enlever des points si coût élevé
        if cout_total > 500:
            score -= 10
        if cout_total > 1000:
            score -= 10

        # Bonus si équipement récent
        if age_annees < 2:
            score += 10
        # Malus si équipement ancien
        elif age_annees > 5:
            score -= 10

        # Garder entre 0 et 100
        if score < 0:
            score = 0
        if score > 100:
            score = 100

        resultats.append({
            'nom': eq['nom'],
            'type': eq['type'],
            'age_annees': round(age_annees, 1),
            'nb_pannes': nb_pannes,
            'cout_total': round(cout_total, 2),
            'indice_fiabilite': int(score)
        })

    # Trier du plus fiable au moins fiable
    resultats.sort(key=lambda x: x['indice_fiabilite'], reverse=True)

    return resultats


def calculer_tendance_couts(annee=2024):
    interventions = data_access.obtenir_interventions_completes()

    # Regrouper par mois
    couts_par_mois = {}  # {1: 150.0, 2: 200.0, ...}

    for inter in interventions:
        date_inter = datetime.strptime(inter['date_intervention'], '%Y-%m-%d')

        if date_inter.year == annee:
            mois = date_inter.month

            if mois not in couts_par_mois:
                couts_par_mois[mois] = 0

            couts_par_mois[mois] += inter['cout']

    # Calculer les totaux par semestre
    cout_s1 = 0  # Mois 1 à 6
    cout_s2 = 0  # Mois 7 à 12

    for mois in range(1, 7):
        cout_s1 += couts_par_mois.get(mois, 0)

    for mois in range(7, 13):
        cout_s2 += couts_par_mois.get(mois, 0)

    # Calculer la variation en %
    if cout_s1 > 0:
        variation = ((cout_s2 - cout_s1) / cout_s1) * 100
    else:
        variation = 0

    # Déterminer la tendance
    if variation > 10:
        tendance = 'hausse'
    elif variation < -10:
        tendance = 'baisse'
    else:
        tendance = 'stable'

    return {
        'tendance': tendance,
        'variation_pct': round(variation, 2),
        'cout_s1': round(cout_s1, 2),
        'cout_s2': round(cout_s2, 2),
        'detail_mois': {k: round(v, 2) for k, v in sorted(couts_par_mois.items())}
    }


def generer_alertes():
    equipements = data_access.obtenir_tous_equipements()
    interventions = data_access.obtenir_interventions_completes()

    # Regrouper les interventions par équipement
    interventions_par_equipement = {}
    for inter in interventions:
        eq_id = inter['equipement_id']
        if eq_id not in interventions_par_equipement:
            interventions_par_equipement[eq_id] = []
        interventions_par_equipement[eq_id].append(inter)

    alertes = []
    date_maintenant = datetime.now()

    for eq in equipements:
        eq_id = eq['id']
        inters = interventions_par_equipement.get(eq_id, [])

        if not inters:
            # Pas d'intervention enregistrée
            alertes.append({
                'equipement': eq['nom'],
                'niveau': 'INFO',
                'message': "Aucune intervention enregistrée"
            })
            continue

        # Compter les pannes
        nb_pannes = sum(1 for i in inters if i['type_intervention'] == 'corrective')

        if nb_pannes >= 2:
            alertes.append({
                'equipement': eq['nom'],
                'niveau': 'CRITIQUE',
                'message': f"{nb_pannes} pannes enregistrées - envisager remplacement"
            })

        # Vérifier le coût total
        cout_total = sum(i['cout'] for i in inters)
        if cout_total > 1000:
            alertes.append({
                'equipement': eq['nom'],
                'niveau': 'ATTENTION',
                'message': f"Coût élevé: {cout_total:.0f}€"
            })

        # Dernière intervention
        dates = [datetime.strptime(i['date_intervention'], '%Y-%m-%d') for i in inters]
        derniere = max(dates)
        jours_depuis = (date_maintenant - derniere).days

        if jours_depuis > 180:
            alertes.append({
                'equipement': eq['nom'],
                'niveau': 'ATTENTION',
                'message': f"Pas de maintenance depuis {jours_depuis} jours"
            })

    # Trier par niveau (CRITIQUE d'abord)
    ordre = {'CRITIQUE': 0, 'ATTENTION': 1, 'INFO': 2}
    alertes.sort(key=lambda x: ordre.get(x['niveau'], 3))

    return alertes


def generer_rapport_synthese():
    return {
        'indicateurs_globaux': {
            'cout_total': data_access.obtenir_cout_total(),
            'nombre_interventions': data_access.obtenir_nombre_interventions(),
            'duree_moyenne_minutes': data_access.obtenir_duree_moyenne(),
        },
        'taux_disponibilite': calculer_taux_disponibilite(),
        'tendance_couts': calculer_tendance_couts(),
        'top_equipements_sollicites': data_access.obtenir_equipements_sollicites(5),
        'frequence_par_type': data_access.obtenir_frequence_par_type(),
        'alertes': generer_alertes()
    }
