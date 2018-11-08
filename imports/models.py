import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class RefImport(models.Model):
    reference = models.CharField(max_length=50, null=True)


class Import(models.Model):
    pub_date = models.DateTimeField('date published', null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ref = models.ForeignKey(RefImport, on_delete=models.CASCADE, null=True)


class ImportOptimum(models.Model):
    dossier = models.CharField(max_length=50, null=True)
    code_regroupement_syndic = models.CharField(max_length=50, null=True)
    id_pm = models.CharField(max_length=50, null=True)
    type_de_pm = models.CharField(max_length=50, null=True)
    etat_de_pm = models.CharField(max_length=50, null=True)
    date_etat_pm = models.DateTimeField('Date Etat PM', null=True)
    date_construction_pm = models.DateTimeField('Date Constrution PM', null=True)
    id_pa = models.CharField(max_length=50, null=True)
    etat_de_pa = models.CharField(max_length=50, null=True)
    identifiant_processus = models.CharField(max_length=50, null=True)
    date_maj_contour = models.DateTimeField('Date Maj contour', null=True)
    num_voie = models.IntegerField(null=True)
    num_cplt = models.IntegerField(null=True)
    voie = models.CharField(max_length=50, null=True)
    adresse = models.CharField(max_length=50, null=True)
    batiment = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=50, null=True)
    Localite = models.CharField(max_length=50, null=True)
    rivoli = models.CharField(max_length=50, null=True)
    operateur_d_imeuble = models.CharField(max_length=50, null=True)
    etat_negociation = models.CharField(max_length=50, null=True)
    etat_technique = models.CharField(max_length=50, null=True)
    etat_site = models.CharField(max_length=50, null=True)
    site_bloque = models.CharField(max_length=50, null=True)
    type_site = models.CharField(max_length=50, null=True)
    detection_zlin = models.CharField(max_length=50, null=True)
    pre_equipe = models.CharField(max_length=50, null=True)
    nb_logement = models.IntegerField(null=True)
    nb_logement_r = models.IntegerField(null=True)
    nb_logement_p = models.IntegerField(null=True)
    typologie = models.CharField(max_length=50, null=True)
    civilite_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    nom_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    prenom_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    num_tel_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    num_mobile_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    fax_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    email_pdt_conseil_syndical = models.CharField(max_length=50, null=True)
    nra = models.CharField(max_length=50, null=True)
    type_blocage_site = models.CharField(max_length=50, null=True)
    cause_blocage_syndic = models.CharField(max_length=50, null=True)
    etat_pre_etude_site = models.CharField(max_length=50, null=True)
    etat_reseau_t_d = models.CharField(max_length=50, null=True)
    etude_site = models.CharField(max_length=50, null=True)
    etat_etude_site = models.CharField(max_length=50, null=True)
    date_fin_etude_site = models.DateTimeField('date fin étude site', null=True)
    resultat_etude_site = models.CharField(max_length=50, null=True)
    date_theorique_raccordement = models.DateTimeField('Date théorique raccordement', null=True)
    date_raccordement_au_pm_ou_au_pa = models.DateTimeField('Date raccordement au PM ou au PA', null=True)
    identifiant_pb = models.CharField(max_length=50, null=True)
    date_pose_du_pb = models.DateTimeField('Date pose du PB', null=True)
    date_effective_raccordement = models.DateTimeField('Date effective raccordement', null=True)
    presence_dta = models.CharField(max_length=50, null=True)
    nom_contact_syndic = models.CharField(max_length=50, null=True)
    prenom_contact_syndic = models.CharField(max_length=50, null=True)
    num_tel_contact_syndic = models.CharField(max_length=50, null=True)
    date_affectation_negociateur = models.DateTimeField('Date affectation négociateur', null=True)
    negociateur_interne = models.CharField(max_length=50, null=True)
    negociateur_externe = models.CharField(max_length=50, null=True)
    premier_conctact = models.CharField(max_length=50, null=True)
    date_rdv_syndic = models.DateTimeField('Date RDV Syndic', null=True)
    attente = models.CharField(max_length=50, null=True)
    date_ag = models.DateTimeField('Date AG', null=True)
    ag_non_pertinente = models.CharField(max_length=50, null=True)
    envoi_accord_syndic = models.CharField(max_length=50, null=True)
    date_retour_convention = models.DateTimeField('Date Retour Convention', null=True)
    attente_probation = models.CharField(max_length=50, null=True)
    retour_accord_syndic = models.CharField(max_length=50, null=True)
    refus_accord_syndic = models.CharField(max_length=50, null=True)
    date_mesc_arcep_pm = models.DateTimeField('Date MESC ARCEP PM', null=True)
    date_pose_pre = models.DateTimeField('Date Pose PRE', null=True)

    import_fk = models.ForeignKey(Import, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.importOptimum

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=5)


class Pmz(models.Model):
    refPmz = models.CharField(max_length=50, null=True, unique=True)
    import_fk = models.ForeignKey(Import, on_delete=models.CASCADE, null=True)


class Pa(models.Model):
    refPa = models.CharField(max_length=50, null=True, unique=True)
    import_fk = models.ForeignKey(Import, on_delete=models.CASCADE, null=True)
    pmz_fk = models.ForeignKey(Pmz, on_delete=models.CASCADE, null=True)


class Imb(models.Model):
    refImb = models.CharField(max_length=50, null=True, unique=True)
    date_effective_de_raccordement = models.DateField('dare effective de raccordement', null=True)
    import_fk = models.ForeignKey(Import, on_delete=models.CASCADE, null=True)
    pa_fk = models.ForeignKey(Pa, on_delete=models.CASCADE, null=True)
