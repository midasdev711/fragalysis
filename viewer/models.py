from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """A django model to define a given project_id. Not currently used.
    Could be used to define certain attributes."""
    # The title of the project_id -> userdefined
    title = models.CharField(max_length=200,unique=True)
    # The date it was made
    init_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        permissions = (
            ('view_project', 'View project'),
        )

class Target(models.Model):
    """A Django model to define a given protein target"""
    # The title of the project_id -> userdefined
    title = models.CharField(unique=True, max_length=200)
    # The date it was made
    init_date = models.DateTimeField(auto_now_add=True)
    # A field to link projects and targets together
    project_id = models.ManyToManyField(Project)
    # Indicates the uniprot_id id for the target. Is a unique key
    uniprot_id = models.CharField(max_length=100, null=True)

    class Meta:
        permissions = (
            ('view_target', 'View target'),
        )

class Protein(models.Model):
    """A Django model to hold the information for a given protein, unique set of coords"""
    # code for this protein
    code = models.CharField(max_length=50,unique=True, db_index=True)
    target_id = models.ForeignKey(Target)
    apo_holo = models.NullBooleanField()
    pdb_info = models.FileField(upload_to='pdbs/', null=True, max_length=10000000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    init_date = models.DateTimeField(auto_now_add=True)
    cif_info = models.FileField(upload_to='cifs/', null=True, max_length=10000000)
    mtz_info = models.FileField(upload_to='mtzs/', null=True, max_length=10000000)
    map_info = models.FileField(upload_to='maps/', null=True, max_length=10000000)
    aligned = models.NullBooleanField()
    aligned_to = models.ForeignKey('self', null=True)
    has_eds = models.NullBooleanField()

    class Meta:
        permissions = (
            ('view_protein', 'View protein'),
        )


class Compound(models.Model):
    """A Django model to hold the information for a given compound -> a unique 2D molecule"""
    # Character attributes
    inchi = models.CharField(max_length=5000, unique=True, db_index=True)
    smiles = models.CharField(max_length=500, db_index=True)
    # Float attributes
    mol_log_p = models.FloatField()
    mol_wt = models.FloatField()
    tpsa = models.FloatField()
    # Integer attributes
    heavy_atom_count = models.IntegerField()
    heavy_atom_mol_wt = models.FloatField()
    nhoh_count = models.IntegerField()
    no_count = models.IntegerField()
    num_h_acceptors = models.IntegerField()
    num_h_donors = models.IntegerField()
    num_het_atoms = models.IntegerField()
    num_rot_bonds = models.IntegerField()
    num_val_electrons = models.IntegerField()
    ring_count = models.IntegerField()

    class Meta:
        permissions = (
            ('view_compound', 'View compound'),
        )


class Molecule(models.Model):
    """A Django model to hold the information for a molecule -> a 3D set of
    co-ordinates"""
    # Character attributes
    smiles = models.CharField(max_length=500, db_index=True,null=True)
    lig_id = models.CharField(max_length=5,null=True)
    chain_id = models.CharField(max_length=1,null=True)
    # Textfield
    sdf_info = models.TextField(null=True)
    # Float attributes
    rscc = models.FloatField(null=True)
    occupancy = models.FloatField(null=True)
    x_com = models.FloatField(null=True)
    y_com = models.FloatField(null=True)
    z_com = models.FloatField(null=True)
    rmsd = models.FloatField(null=True)
    # Foreign key relations
    prot_id = models.ForeignKey(Protein)
    cmpd_id = models.ForeignKey(Compound)

    # Unique constraints
    class Meta:
        unique_together = ('prot_id', 'cmpd_id', )
        permissions = (
                ('view_molecule', 'View molecule'),
            )

class ActivityPoint(models.Model):
    """A Django model to hold the activity information for a given compound"""
    # This should encompass the activity type too
    source = models.CharField(max_length=50, null=True, db_index=True)
    # Foreign key to Target object
    target_id = models.ForeignKey(Target)
    # Foreign key to compound object
    cmpd_id = models.ForeignKey(Compound)
    # Measured -log(10) activity
    activity = models.FloatField(db_index=True)
    # The units (uM or whatever). Should be more option
    units = models.CharField(max_length=50)
    # The confidence score
    confidence = models.IntegerField(null=True, db_index=True)
    # The ID of the compound for internal use
    internal_id = models.CharField(max_length=150, null=True)
    # The operator > < or = (= is default)
    operator = models.CharField(max_length=5, default="NA")

    class Meta:
        unique_together = ('target_id', 'activity', 'cmpd_id', 'units', )
        permissions = (
            ('view_activitypoint', 'View activitypoint'),
        )

class ViewScene(models.Model):
    """
    A Django Model for a given view.
    """
    # The uuid that will enable this to be shared
    uuid = models.UUIDField(unique=True)
    # The title - optional
    title = models.CharField(max_length=200,default="NA")
    # The JSON describing the data
    scene = models.TextField()

    permissions = (
        ('view_scene', 'View scene'),
    )


class ProtChoice(models.Model):
    """
    A Django model to store a selection from a user
    """
    user_id = models.ForeignKey(User)
    prot_id = models.ForeignKey(Protein)
    # Score between 0 and 9; Convention for n memberd list -> num_in_list/(num_choices-1)
    # E.g.
    score = models.IntegerField()
    class Meta:
        unique_together = ('user_id', 'prot_id',)

class MolChoice(models.Model):
    """
    A Django model to store a selection from a user
    """
    user_id = models.ForeignKey(User)
    mol_id = models.ForeignKey(Molecule)
    text = models.TextField(default="DENSITY")
    # Score between 0 and 9; Convention for n memberd list -> num_in_list/(num_choices-1)
    # E.g.
    score = models.IntegerField(null=True)
    class Meta:
        unique_together = ('user_id', 'mol_id', 'text')


class CmpdChoice(models.Model):
    """
    A Django model to store a selection from a user
    """
    user_id = models.ForeignKey(User)
    cmpd_id = models.ForeignKey(Compound)
    # Score between 0 and 9; Convention for n memberd list -> num_in_list/(num_choices-1)
    # E.g.
    score = models.IntegerField()
    class Meta:
        unique_together = ('user_id', 'cmpd_id',)