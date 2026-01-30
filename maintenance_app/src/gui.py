import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from db_connection import init_database, database_exists, fermer_connexion
import data_access
import business_logic


class MaintenanceApp:
    """Application principale de suivi de maintenance."""

    def __init__(self, root):
        self.root = root
        self.root.title("Suivi de Maintenance")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # Couleurs
        self.bg_color = "#f5f5f5"
        self.sidebar_color = "#2c3e50"
        self.button_color = "#34495e"
        self.button_hover = "#4a6278"
        self.accent_color = "#3498db"
        self.text_color = "#2c3e50"

        self.root.configure(bg=self.bg_color)

        # Initialiser la base de donnees
        self._init_database()

        # Creer l'interface
        self._create_widgets()

        # Afficher le message de bienvenue
        self._show_welcome()

    def _init_database(self):
        """Initialise la base de donnees si necessaire."""
        if not database_exists():   
            init_database()

    def _create_widgets(self):
        """Cree tous les widgets de l'interface."""
        # Frame principale
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar (menu)
        self._create_sidebar()

        # Zone de contenu
        self._create_content_area()

    def _create_sidebar(self):
        """Cree la barre laterale avec les boutons de menu."""
        self.sidebar = tk.Frame(self.main_frame, bg=self.sidebar_color, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Titre
        title_frame = tk.Frame(self.sidebar, bg=self.sidebar_color)
        title_frame.pack(fill=tk.X, pady=(20, 30))

        tk.Label(
            title_frame,
            text="Maintenance",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.sidebar_color
        ).pack()

        tk.Label(
            title_frame,
            text="Gestion du parc materiel",
            font=("Segoe UI", 9),
            fg="#bdc3c7",
            bg=self.sidebar_color
        ).pack()

        # Separateur
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill=tk.X, padx=15, pady=10)

        # Section GESTION
        tk.Label(
            self.sidebar,
            text="GESTION",
            font=("Segoe UI", 9, "bold"),
            fg="#bdc3c7",
            bg=self.sidebar_color
        ).pack(anchor="w", padx=15, pady=(5, 0))

        gestion_items = [
            ("+ Ajouter Intervention", self.add_intervention, "#27ae60"),
            ("+ Ajouter Technicien", self.add_technicien, "#27ae60"),
            ("+ Ajouter Equipement", self.add_equipement, "#27ae60"),
        ]

        for text, command, color in gestion_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                font=("Segoe UI", 9, "bold"),
                fg="white",
                bg=color,
                activebackground="#2ecc71",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=6,
                anchor="w",
                cursor="hand2",
                command=command
            )
            btn.pack(fill=tk.X, padx=10, pady=2)

            # Effet hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#2ecc71"))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=c))

        # Separateur
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill=tk.X, padx=15, pady=10)

        # Section ANALYSES
        tk.Label(
            self.sidebar,
            text="ANALYSES",
            font=("Segoe UI", 9, "bold"),
            fg="#bdc3c7",
            bg=self.sidebar_color
        ).pack(anchor="w", padx=15, pady=(5, 0))

        # Boutons de menu
        menu_items = [
            ("Indicateurs globaux", self.show_indicateurs_globaux),
            ("Equipements sollicites", self.show_equipements_sollicites),
            ("Frequence par type", self.show_frequence_par_type),
            ("Cout par equipement", self.show_cout_par_type),
            ("Taux disponibilite", self.show_taux_disponibilite),
            ("Indice fiabilite", self.show_indice_fiabilite),
            ("Tendance des couts", self.show_tendance_couts),
            ("Alertes maintenance", self.show_alertes),
            ("Interventions/mois", self.show_interventions_mois),
            ("Performance techniciens", self.show_performance_techniciens),
            ("Historique equipement", self.show_historique_equipement),
            ("Rapport complet", self.show_rapport_synthese),
        ]

        for text, command in menu_items:
            btn = tk.Button(
                self.sidebar,
                text=text,
                font=("Segoe UI", 10),
                fg="white",
                bg=self.button_color,
                activebackground=self.button_hover,
                activeforeground="white",
                bd=0,
                padx=20,
                pady=8,
                anchor="w",
                cursor="hand2",
                command=command
            )
            btn.pack(fill=tk.X, padx=10, pady=2)

            # Effet hover
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.button_hover))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.button_color))

        # Bouton Quitter en bas
        tk.Frame(self.sidebar, bg=self.sidebar_color).pack(fill=tk.BOTH, expand=True)

        quit_btn = tk.Button(
            self.sidebar,
            text="Quitter",
            font=("Segoe UI", 10),
            fg="white",
            bg="#c0392b",
            activebackground="#e74c3c",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.quit_app
        )
        quit_btn.pack(fill=tk.X, padx=10, pady=(0, 20))

    def _create_content_area(self):
        """Cree la zone de contenu principale."""
        self.content_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Titre de la section
        self.section_title = tk.Label(
            self.content_frame,
            text="Bienvenue",
            font=("Segoe UI", 18, "bold"),
            fg=self.text_color,
            bg=self.bg_color,
            anchor="w"
        )
        self.section_title.pack(fill=tk.X, pady=(0, 10))

        # Separateur
        ttk.Separator(self.content_frame, orient="horizontal").pack(fill=tk.X, pady=(0, 15))

        # Zone de texte avec scrollbar
        text_frame = tk.Frame(self.content_frame, bg=self.bg_color)
        text_frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area = tk.Text(
            text_frame,
            font=("Consolas", 11),
            fg=self.text_color,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=15,
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.text_area.yview)

    def _clear_and_set_title(self, title: str):
        """Efface la zone de texte et met a jour le titre."""
        self.section_title.config(text=title)
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)

    def _append_text(self, text: str):
        """Ajoute du texte a la zone d'affichage."""
        self.text_area.insert(tk.END, text)

    def _finalize_text(self):
        """Finalise l'affichage du texte."""
        self.text_area.config(state=tk.DISABLED)

    def _format_table(self, headers: list, rows: list, col_widths: list = None) -> str:
        """Formate un tableau en texte."""
        if not rows:
            return "  Aucune donnee\n"

        if col_widths is None:
            col_widths = [max(len(str(h)), max(len(str(row[i])) for row in rows))
                          for i, h in enumerate(headers)]

        result = ""
        header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
        result += f"  {header_line}\n"
        result += f"  {'-' * len(header_line)}\n"

        for row in rows:
            line = " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(headers)))
            result += f"  {line}\n"

        return result

    def _show_welcome(self):
        """Affiche le message de bienvenue."""
        self._clear_and_set_title("Bienvenue")
        self._append_text("""
  Application de Suivi de Maintenance
  ====================================

  Bienvenue dans l'application de gestion du parc materiel.

  Utilisez le menu a gauche pour naviguer entre les differentes
  fonctionnalites:

  GESTION (Nouveaux ajouts):
    + Ajouter Intervention : Creer une nouvelle intervention
    + Ajouter Technicien : Enregistrer un nouveau technicien
    + Ajouter Equipement : Ajouter un nouvel equipement au parc

  ANALYSES:
    - Indicateurs globaux : Vue d'ensemble des couts et interventions
    - Equipements sollicites : Les equipements les plus maintenus
    - Frequence par type : Analyse des types d'intervention
    - Cout par equipement : Repartition des couts
    - Taux disponibilite : Disponibilite par type (calcul Python)
    - Indice fiabilite : Score de fiabilite (calcul Python)
    - Tendance des couts : Evolution des depenses (calcul Python)
    - Alertes maintenance : Equipements a surveiller (calcul Python)
    - Interventions/mois : Historique mensuel
    - Performance techniciens : Evaluation des equipes
    - Historique equipement : Detail par equipement
    - Rapport complet : Synthese globale

  Les indicateurs marques "(calcul Python)" sont calcules
  cote application, pas en SQL.
""")
        self._finalize_text()

    def show_indicateurs_globaux(self):
        """Affiche les indicateurs globaux."""
        self._clear_and_set_title("Indicateurs Globaux")

        cout_total = data_access.obtenir_cout_total()
        nb_interventions = data_access.obtenir_nombre_interventions()
        duree_moyenne = data_access.obtenir_duree_moyenne()

        self._append_text(f"""
  Cout total de maintenance     : {cout_total:,.2f} EUR
  Nombre total d'interventions  : {nb_interventions}
  Duree moyenne d'intervention  : {duree_moyenne:.1f} minutes ({duree_moyenne/60:.1f} heures)
""")
        self._finalize_text()

    def show_equipements_sollicites(self):
        """Affiche les equipements les plus sollicites."""
        self._clear_and_set_title("Equipements les Plus Sollicites")

        equipements = data_access.obtenir_equipements_sollicites(10)

        headers = ["Equipement", "Type", "Nb Interv.", "Cout Total", "Duree (min)"]
        rows = [
            (eq['nom'][:25], eq['type'], eq['nombre_interventions'],
             f"{eq['cout_total']:.2f} EUR", eq['duree_totale'])
            for eq in equipements
        ]

        self._append_text("\n")
        self._append_text(self._format_table(headers, rows, [25, 18, 10, 12, 12]))
        self._finalize_text()

    def show_frequence_par_type(self):
        """Affiche la frequence des interventions par type."""
        self._clear_and_set_title("Frequence des Interventions par Type")

        frequences = data_access.obtenir_frequence_par_type()

        headers = ["Type", "Nombre", "Cout Total", "Cout Moyen", "Duree Moy."]
        rows = [
            (f['type_intervention'], f['nombre'], f"{f['cout_total']:.2f} EUR",
             f"{f['cout_moyen']:.2f} EUR", f"{f['duree_moyenne']:.0f} min")
            for f in frequences
        ]

        self._append_text("\n")
        self._append_text(self._format_table(headers, rows, [15, 8, 12, 12, 12]))
        self._finalize_text()

    def show_cout_par_type(self):
        """Affiche le cout par type d'equipement."""
        self._clear_and_set_title("Cout de Maintenance par Type d'Equipement")

        couts = data_access.obtenir_cout_par_type_equipement()

        headers = ["Type Equipement", "Nb Equip.", "Nb Interv.", "Cout Total", "Cout Moy."]
        rows = [
            (c['type'], c['nombre_equipements'], c['nombre_interventions'],
             f"{c['cout_total'] or 0:.2f} EUR", f"{c['cout_moyen_intervention'] or 0:.2f} EUR")
            for c in couts
        ]

        self._append_text("\n")
        self._append_text(self._format_table(headers, rows, [20, 10, 10, 12, 12]))
        self._finalize_text()

    def show_taux_disponibilite(self):
        """Affiche le taux de disponibilite."""
        self._clear_and_set_title("Taux de Disponibilite par Type (Calcul Python)")

        taux = business_logic.calculer_taux_disponibilite()

        self._append_text("\n  [Indicateur calcule cote Python, pas en SQL]\n\n")

        for type_eq, pourcentage in taux.items():
            barre = "=" * int(pourcentage / 5) + "-" * (20 - int(pourcentage / 5))
            self._append_text(f"  {type_eq:22} : [{barre}] {pourcentage:.1f}%\n")

        self._finalize_text()

    def show_indice_fiabilite(self):
        """Affiche l'indice de fiabilite."""
        self._clear_and_set_title("Indice de Fiabilite des Equipements (Calcul Python)")

        fiabilite = business_logic.calculer_indice_fiabilite()

        self._append_text("\n  [Indicateur calcule cote Python: score base sur pannes, couts et age]\n\n")

        headers = ["Equipement", "Type", "Age", "Pannes", "Cout", "Indice"]
        rows = [
            (f['nom'][:22], f['type'][:15], f"{f['age_annees']}a",
             f['nb_pannes'], f"{f['cout_total']:.0f} EUR", f"{f['indice_fiabilite']}/100")
            for f in fiabilite
        ]

        self._append_text(self._format_table(headers, rows, [22, 15, 5, 7, 10, 8]))
        self._finalize_text()

    def show_tendance_couts(self):
        """Affiche la tendance des couts."""
        self._clear_and_set_title("Tendance des Couts 2024 (Calcul Python)")

        tendance = business_logic.calculer_tendance_couts(2024)

        self._append_text("\n  [Indicateur calcule cote Python: analyse semestrielle]\n")
        self._append_text(f"""
  Tendance globale    : {tendance['tendance'].upper()}
  Variation S1 -> S2  : {tendance['variation_pct']:+.1f}%
  Cout 1er semestre   : {tendance.get('cout_s1', 0):,.2f} EUR
  Cout 2nd semestre   : {tendance.get('cout_s2', 0):,.2f} EUR
""")

        self._append_text("\n  Detail par mois:\n")
        noms_mois = ['', 'Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun',
                     'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']

        for mois, cout in tendance['detail_mois'].items():
            barre = "=" * int(cout / 50) if cout > 0 else ""
            self._append_text(f"    {noms_mois[mois]:3} : {barre} {cout:.0f} EUR\n")

        self._finalize_text()

    def show_alertes(self):
        """Affiche les alertes de maintenance."""
        self._clear_and_set_title("Alertes de Maintenance (Calcul Python)")

        alertes = business_logic.generer_alertes()

        self._append_text("\n  [Alertes generees par analyse Python des donnees]\n\n")

        if not alertes:
            self._append_text("  Aucune alerte\n")
        else:
            for niveau in ['CRITIQUE', 'ATTENTION', 'INFO']:
                alertes_niveau = [a for a in alertes if a['niveau'] == niveau]
                if alertes_niveau:
                    symbole = {'CRITIQUE': '[!]', 'ATTENTION': '[*]', 'INFO': '[i]'}[niveau]
                    self._append_text(f"  {symbole} {niveau}:\n")
                    for alerte in alertes_niveau:
                        self._append_text(f"     - {alerte['equipement']}: {alerte['message']}\n")
                    self._append_text("\n")

        self._finalize_text()

    def show_interventions_mois(self):
        """Affiche les interventions par mois."""
        self._clear_and_set_title("Interventions par Mois (2024)")

        interventions = data_access.obtenir_interventions_par_mois(2024)

        noms_mois = {
            '01': 'Janvier', '02': 'Fevrier', '03': 'Mars', '04': 'Avril',
            '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Aout',
            '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Decembre'
        }

        headers = ["Mois", "Nb Interv.", "Cout Total", "Duree Totale"]
        rows = [
            (noms_mois.get(i['mois'], i['mois']), i['nombre_interventions'],
             f"{i['cout_total']:.2f} EUR", f"{i['duree_totale']} min")
            for i in interventions
        ]

        self._append_text("\n")
        self._append_text(self._format_table(headers, rows, [12, 12, 12, 14]))
        self._finalize_text()

    def show_performance_techniciens(self):
        """Affiche la performance des techniciens."""
        self._clear_and_set_title("Performance des Techniciens")

        perf = data_access.obtenir_performance_techniciens()

        headers = ["Technicien", "Specialite", "Nb Interv.", "Temps Total", "Valeur"]
        rows = [
            (p['technicien'], p['specialite'][:12], p['nombre_interventions'],
             f"{p['temps_total'] or 0} min", f"{p['valeur_interventions'] or 0:.0f} EUR")
            for p in perf
        ]

        self._append_text("\n")
        self._append_text(self._format_table(headers, rows, [20, 12, 10, 12, 10]))
        self._finalize_text()

    def show_historique_equipement(self):
        """Affiche l'historique d'un equipement."""
        self._clear_and_set_title("Historique d'un Equipement")

        # Lister les equipements
        equipements = data_access.obtenir_tous_equipements()

        # Creer la liste pour le choix
        choix_list = [f"{eq['id']}. {eq['nom']} ({eq['type']})" for eq in equipements]

        # Boite de dialogue pour choisir
        choix = simpledialog.askstring(
            "Choix de l'equipement",
            "Entrez le numero de l'equipement:\n\n" + "\n".join(choix_list),
            parent=self.root
        )

        if not choix:
            self._append_text("\n  Operation annulee.\n")
            self._finalize_text()
            return

        try:
            eq_id = int(choix)
            equipement = data_access.obtenir_equipement_par_id(eq_id)

            if not equipement:
                self._append_text("\n  Equipement non trouve.\n")
                self._finalize_text()
                return

            self._append_text(f"\n  Historique de: {equipement['nom']}\n")
            self._append_text(f"  Type: {equipement['type']} | Localisation: {equipement['localisation']}\n")
            self._append_text(f"  Statut actuel: {equipement['statut']}\n\n")

            historique = data_access.obtenir_historique_equipement(eq_id)

            if historique:
                headers = ["Date", "Type", "Description", "Duree", "Cout", "Technicien"]
                rows = [
                    (h['date_intervention'], h['type_intervention'][:10],
                     h['description'][:25], f"{h['duree_minutes']}m",
                     f"{h['cout']:.0f} EUR", h['technicien'][:15])
                    for h in historique
                ]
                self._append_text(self._format_table(headers, rows, [12, 10, 25, 6, 8, 15]))
            else:
                self._append_text("  Aucune intervention enregistree.\n")

        except ValueError:
            self._append_text("\n  Entree invalide.\n")

        self._finalize_text()

    def show_rapport_synthese(self):
        """Affiche le rapport de synthese complet."""
        self._clear_and_set_title("Rapport de Synthese Complet")

        rapport = business_logic.generer_rapport_synthese()

        # Indicateurs globaux
        self._append_text("\n  INDICATEURS GLOBAUX\n")
        self._append_text("  " + "-" * 40 + "\n")
        ig = rapport['indicateurs_globaux']
        self._append_text(f"    Cout total        : {ig['cout_total']:,.2f} EUR\n")
        self._append_text(f"    Interventions     : {ig['nombre_interventions']}\n")
        self._append_text(f"    Duree moyenne     : {ig['duree_moyenne_minutes']:.1f} min\n")

        # Taux de disponibilite
        self._append_text("\n  TAUX DE DISPONIBILITE\n")
        self._append_text("  " + "-" * 40 + "\n")
        for type_eq, taux in rapport['taux_disponibilite'].items():
            self._append_text(f"    {type_eq:22} : {taux:.1f}%\n")

        # Tendance
        self._append_text("\n  TENDANCE DES COUTS\n")
        self._append_text("  " + "-" * 40 + "\n")
        tend = rapport['tendance_couts']
        self._append_text(f"    Tendance  : {tend['tendance'].upper()}\n")
        self._append_text(f"    Variation : {tend['variation_pct']:+.1f}%\n")

        # Top equipements
        self._append_text("\n  TOP 5 EQUIPEMENTS SOLLICITES\n")
        self._append_text("  " + "-" * 40 + "\n")
        for i, eq in enumerate(rapport['top_equipements_sollicites'][:5], 1):
            self._append_text(f"    {i}. {eq['nom'][:25]} - {eq['nombre_interventions']} interv. ({eq['cout_total']:.0f} EUR)\n")

        # Alertes
        self._append_text("\n  ALERTES\n")
        self._append_text("  " + "-" * 40 + "\n")
        alertes_critiques = [a for a in rapport['alertes'] if a['niveau'] == 'CRITIQUE']
        if alertes_critiques:
            for a in alertes_critiques[:3]:
                self._append_text(f"    [!] {a['equipement']}: {a['message'][:45]}\n")
        else:
            self._append_text("    Aucune alerte critique\n")

        self._finalize_text()

    def add_technicien(self):
        """Formulaire d'ajout de technicien."""
        self._clear_and_set_title("Ajouter un Technicien")

        # Créer une fenêtre de dialogue personnalisée
        dialog = tk.Toplevel(self.root)
        dialog.title("Nouveau Technicien")
        dialog.geometry("400x350")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f'400x350+{x}+{y}')

        # Titre
        tk.Label(dialog, text="Nouveau Technicien", font=("Segoe UI", 14, "bold"),
                bg=self.bg_color, fg=self.text_color).pack(pady=15)

        # Frame pour les champs
        fields_frame = tk.Frame(dialog, bg=self.bg_color)
        fields_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Champs
        fields = {}
        labels = [
            ("Nom *", "nom"),
            ("Prénom *", "prenom"),
            ("Spécialité *", "specialite"),
            ("Email *", "email"),
            ("Date embauche (YYYY-MM-DD) *", "date_embauche")
        ]

        for i, (label_text, field_name) in enumerate(labels):
            tk.Label(fields_frame, text=label_text, bg=self.bg_color,
                    font=("Segoe UI", 9)).grid(row=i, column=0, sticky="w", pady=5)

            entry = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
            entry.grid(row=i, column=1, pady=5, padx=10)
            fields[field_name] = entry

        # Boutons
        buttons_frame = tk.Frame(dialog, bg=self.bg_color)
        buttons_frame.pack(pady=15)

        def save():
            try:
                # Validation
                for field_name, entry in fields.items():
                    if not entry.get().strip():
                        messagebox.showerror("Erreur", f"Le champ {field_name} est obligatoire", parent=dialog)
                        return

                # Validation email
                email = fields['email'].get().strip()
                if '@' not in email:
                    messagebox.showerror("Erreur", "Email invalide", parent=dialog)
                    return

                # Validation date
                date_embauche = fields['date_embauche'].get().strip()
                if len(date_embauche) != 10 or date_embauche[4] != '-' or date_embauche[7] != '-':
                    messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD)", parent=dialog)
                    return

                # Insertion
                technicien_id = data_access.ajouter_technicien(
                    fields['nom'].get().strip(),
                    fields['prenom'].get().strip(),
                    fields['specialite'].get().strip(),
                    email,
                    date_embauche
                )

                messagebox.showinfo("Succès", f"Technicien ajouté avec l'ID {technicien_id}", parent=dialog)
                dialog.destroy()

                # Rafraîchir l'affichage
                self._append_text(f"\n✓ Technicien ajouté: {fields['prenom'].get()} {fields['nom'].get()}\n")
                self._finalize_text()

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}", parent=dialog)

        tk.Button(buttons_frame, text="Enregistrer", command=save, bg=self.accent_color,
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Annuler", command=dialog.destroy, bg="#95a5a6",
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)

        self._append_text("\nFormulaire ouvert dans une nouvelle fenêtre...\n")
        self._finalize_text()

    def add_equipement(self):
        """Formulaire d'ajout d'équipement."""
        self._clear_and_set_title("Ajouter un Equipement")

        dialog = tk.Toplevel(self.root)
        dialog.title("Nouvel Equipement")
        dialog.geometry("450x450")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (450 // 2)
        dialog.geometry(f'450x450+{x}+{y}')

        tk.Label(dialog, text="Nouvel Equipement", font=("Segoe UI", 14, "bold"),
                bg=self.bg_color, fg=self.text_color).pack(pady=15)

        fields_frame = tk.Frame(dialog, bg=self.bg_color)
        fields_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        fields = {}
        row = 0

        # Nom
        tk.Label(fields_frame, text="Nom *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['nom'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['nom'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Type (liste déroulante)
        tk.Label(fields_frame, text="Type *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['type'] = ttk.Combobox(fields_frame, font=("Segoe UI", 10), width=23,
                                      values=['ordinateur', 'machine', 'equipement_technique'], state='readonly')
        fields['type'].grid(row=row, column=1, pady=5, padx=10)
        fields['type'].current(0)
        row += 1

        # Marque
        tk.Label(fields_frame, text="Marque", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['marque'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['marque'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Modèle
        tk.Label(fields_frame, text="Modele", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['modele'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['modele'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Numéro de série
        tk.Label(fields_frame, text="Numero serie *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['numero_serie'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['numero_serie'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Date acquisition
        tk.Label(fields_frame, text="Date acquisition *\n(YYYY-MM-DD)", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['date_acquisition'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['date_acquisition'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Localisation
        tk.Label(fields_frame, text="Localisation *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['localisation'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=25)
        fields['localisation'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Statut
        tk.Label(fields_frame, text="Statut *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['statut'] = ttk.Combobox(fields_frame, font=("Segoe UI", 10), width=23,
                                       values=['actif', 'en_panne', 'en_maintenance', 'reforme'], state='readonly')
        fields['statut'].grid(row=row, column=1, pady=5, padx=10)
        fields['statut'].current(0)

        buttons_frame = tk.Frame(dialog, bg=self.bg_color)
        buttons_frame.pack(pady=15)

        def save():
            try:
                # Validation champs obligatoires
                required = ['nom', 'numero_serie', 'date_acquisition', 'localisation']
                for field_name in required:
                    if not fields[field_name].get().strip():
                        messagebox.showerror("Erreur", f"Le champ {field_name} est obligatoire", parent=dialog)
                        return

                # Validation date
                date_acq = fields['date_acquisition'].get().strip()
                if len(date_acq) != 10 or date_acq[4] != '-' or date_acq[7] != '-':
                    messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD)", parent=dialog)
                    return

                # Insertion
                equipement_id = data_access.ajouter_equipement(
                    fields['nom'].get().strip(),
                    fields['type'].get(),
                    fields['marque'].get().strip() or None,
                    fields['modele'].get().strip() or None,
                    fields['numero_serie'].get().strip(),
                    date_acq,
                    fields['localisation'].get().strip(),
                    fields['statut'].get()
                )

                messagebox.showinfo("Succès", f"Equipement ajouté avec l'ID {equipement_id}", parent=dialog)
                dialog.destroy()

                self._append_text(f"\n✓ Equipement ajouté: {fields['nom'].get()}\n")
                self._finalize_text()

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}", parent=dialog)

        tk.Button(buttons_frame, text="Enregistrer", command=save, bg=self.accent_color,
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Annuler", command=dialog.destroy, bg="#95a5a6",
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)

        self._append_text("\nFormulaire ouvert dans une nouvelle fenêtre...\n")
        self._finalize_text()

    def add_intervention(self):
        """Formulaire d'ajout d'intervention."""
        self._clear_and_set_title("Ajouter une Intervention")

        dialog = tk.Toplevel(self.root)
        dialog.title("Nouvelle Intervention")
        dialog.geometry("500x500")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()

        # Centrer la fenêtre
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f'500x500+{x}+{y}')

        tk.Label(dialog, text="Nouvelle Intervention", font=("Segoe UI", 14, "bold"),
                bg=self.bg_color, fg=self.text_color).pack(pady=15)

        fields_frame = tk.Frame(dialog, bg=self.bg_color)
        fields_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        fields = {}
        row = 0

        # Récupérer les équipements et techniciens
        equipements = data_access.obtenir_tous_equipements()
        techniciens = data_access.obtenir_tous_techniciens()

        # Equipement (liste déroulante)
        tk.Label(fields_frame, text="Equipement *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        equipement_choices = [f"{eq['id']} - {eq['nom']}" for eq in equipements]
        fields['equipement'] = ttk.Combobox(fields_frame, font=("Segoe UI", 9), width=30,
                                           values=equipement_choices, state='readonly')
        fields['equipement'].grid(row=row, column=1, pady=5, padx=10)
        if equipements:
            fields['equipement'].current(0)
        row += 1

        # Technicien (liste déroulante)
        tk.Label(fields_frame, text="Technicien *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        technicien_choices = [f"{t['id']} - {t['prenom']} {t['nom']}" for t in techniciens]
        fields['technicien'] = ttk.Combobox(fields_frame, font=("Segoe UI", 9), width=30,
                                           values=technicien_choices, state='readonly')
        fields['technicien'].grid(row=row, column=1, pady=5, padx=10)
        if techniciens:
            fields['technicien'].current(0)
        row += 1

        # Date intervention
        tk.Label(fields_frame, text="Date *\n(YYYY-MM-DD)", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['date_intervention'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=32)
        fields['date_intervention'].grid(row=row, column=1, pady=5, padx=10)
        # Pré-remplir avec la date du jour
        from datetime import datetime
        fields['date_intervention'].insert(0, datetime.now().strftime('%Y-%m-%d'))
        row += 1

        # Type intervention
        tk.Label(fields_frame, text="Type *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['type_intervention'] = ttk.Combobox(fields_frame, font=("Segoe UI", 10), width=30,
                                                  values=['preventive', 'corrective', 'installation', 'mise_a_jour'], state='readonly')
        fields['type_intervention'].grid(row=row, column=1, pady=5, padx=10)
        fields['type_intervention'].current(0)
        row += 1

        # Description
        tk.Label(fields_frame, text="Description *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="nw", pady=5)
        fields['description'] = tk.Text(fields_frame, font=("Segoe UI", 10), width=32, height=4)
        fields['description'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Durée
        tk.Label(fields_frame, text="Duree (minutes) *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['duree_minutes'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=32)
        fields['duree_minutes'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Coût
        tk.Label(fields_frame, text="Cout (EUR) *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['cout'] = tk.Entry(fields_frame, font=("Segoe UI", 10), width=32)
        fields['cout'].grid(row=row, column=1, pady=5, padx=10)
        row += 1

        # Statut
        tk.Label(fields_frame, text="Statut *", bg=self.bg_color, font=("Segoe UI", 9)).grid(row=row, column=0, sticky="w", pady=5)
        fields['statut'] = ttk.Combobox(fields_frame, font=("Segoe UI", 10), width=30,
                                       values=['planifiee', 'en_cours', 'terminee', 'annulee'], state='readonly')
        fields['statut'].grid(row=row, column=1, pady=5, padx=10)
        fields['statut'].current(2)  # Par défaut "terminee"

        buttons_frame = tk.Frame(dialog, bg=self.bg_color)
        buttons_frame.pack(pady=15)

        def save():
            try:
                # Validation
                if not fields['equipement'].get() or not fields['technicien'].get():
                    messagebox.showerror("Erreur", "Veuillez sélectionner un équipement et un technicien", parent=dialog)
                    return

                description = fields['description'].get("1.0", tk.END).strip()
                if not description:
                    messagebox.showerror("Erreur", "La description est obligatoire", parent=dialog)
                    return

                duree = fields['duree_minutes'].get().strip()
                cout = fields['cout'].get().strip()

                if not duree or not cout:
                    messagebox.showerror("Erreur", "Durée et coût sont obligatoires", parent=dialog)
                    return

                # Validation numérique
                try:
                    duree_int = int(duree)
                    cout_float = float(cout)
                    if duree_int <= 0 or cout_float < 0:
                        raise ValueError()
                except ValueError:
                    messagebox.showerror("Erreur", "Durée et coût doivent être des nombres valides", parent=dialog)
                    return

                # Extraire les IDs
                equipement_id = int(fields['equipement'].get().split(' - ')[0])
                technicien_id = int(fields['technicien'].get().split(' - ')[0])

                # Insertion
                intervention_id = data_access.ajouter_intervention(
                    equipement_id,
                    technicien_id,
                    fields['date_intervention'].get().strip(),
                    fields['type_intervention'].get(),
                    description,
                    duree_int,
                    cout_float,
                    fields['statut'].get()
                )

                messagebox.showinfo("Succès", f"Intervention ajoutée avec l'ID {intervention_id}", parent=dialog)
                dialog.destroy()

                self._append_text(f"\n✓ Intervention ajoutée (ID: {intervention_id})\n")
                self._append_text(f"  Equipement: {fields['equipement'].get()}\n")
                self._append_text(f"  Type: {fields['type_intervention'].get()}\n")
                self._append_text(f"  Cout: {cout_float} EUR\n")
                self._finalize_text()

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout: {str(e)}", parent=dialog)

        tk.Button(buttons_frame, text="Enregistrer", command=save, bg=self.accent_color,
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Annuler", command=dialog.destroy, bg="#95a5a6",
                 fg="white", font=("Segoe UI", 10), padx=20, pady=5, cursor="hand2").pack(side=tk.LEFT, padx=5)

        self._append_text("\nFormulaire ouvert dans une nouvelle fenêtre...\n")
        self._finalize_text()

    def quit_app(self):
        """Ferme l'application."""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter?"):
            fermer_connexion()
            self.root.destroy()


def main():
    """Point d'entree principal."""
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
