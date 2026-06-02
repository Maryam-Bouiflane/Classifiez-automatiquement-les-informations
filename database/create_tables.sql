-- ======================
-- TABLE 1 : DATASET EMPLOYES
-- ======================

CREATE TABLE IF NOT EXISTS employees(
    id_employee INT PRIMARY KEY,

    age INT CHECK (age >= 18 AND age < 80),
    genre VARCHAR(1),
    statut_marital VARCHAR(20),
    departement VARCHAR(40),
    poste VARCHAR(40),
    nombre_experiences_precedentes INT,
    annee_experience_totale INT,
    annees_dans_l_entreprise INT,
    annees_dans_le_poste_actuel INT,
    satisfaction_employee_environnement INT CHECK (satisfaction_employee_environnement BETWEEN 0 AND 5),
    note_evaluation_precedente INT CHECK (note_evaluation_precedente BETWEEN 0 AND 5),
    satisfaction_employee_nature_travail INT CHECK (satisfaction_employee_nature_travail BETWEEN 0 AND 5),
    satisfaction_employee_equipe INT CHECK (satisfaction_employee_equipe BETWEEN 0 AND 5),
    satisfaction_employee_equilibre_pro_perso INT CHECK (satisfaction_employee_equilibre_pro_perso BETWEEN 0 AND 5),
    note_evaluation_actuelle INT CHECK (note_evaluation_actuelle BETWEEN 0 AND 5),
    heure_supplementaires VARCHAR(3),
    augementation_salaire_precedente FLOAT CHECK (augementation_salaire_precedente >= 0 AND augementation_salaire_precedente <= 100),
    nombre_participation_pee INT CHECK (nombre_participation_pee BETWEEN 0 AND 70),
    nb_formations_suivies INT CHECK (nb_formations_suivies >= 0),
    distance_domicile_travail INT,
    niveau_education INT CHECK (niveau_education BETWEEN 1 AND 5),
    domaine_etude VARCHAR(40),
    frequence_deplacement VARCHAR(40),
    annees_depuis_la_derniere_promotion INT,
    annes_sous_responsable_actuel INT
);

-- ======================
-- TABLE 2 : LOGS PREDICTIONS (IMPORTANT TRAÇABILITÉ)
-- ======================

CREATE TABLE IF NOT EXISTS predictions_log (
    id SERIAL PRIMARY KEY,
    employee_id INT NULL,
    input_data JSONB,
    output_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);