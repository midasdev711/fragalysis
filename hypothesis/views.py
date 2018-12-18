from rest_framework import viewsets

from hypothesis.models import (
    Vector,
    Vector3D,
    Interaction,
    InteractionPoint,
    ProteinResidue,
    TargetResidue,
)
from hypothesis.serializers import (
    VectorSerializer,
    Vector3DSerializer,
    InteractionSerializer,
    InteractionPointSerializer,
    ProteinResidueSerialzier,
    TargetResidueSerialzier,
)


class VectorView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = Vector.objects.filter()
    serializer_class = VectorSerializer
    filter_fields = ("cmpd_id", "smiles", "type")


class Vector3DView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = Vector3D.objects.filter()
    serializer_class = Vector3DSerializer
    filter_fields = ("mol_id", "vector_id", "number")


class InteractionView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = Interaction.objects.filter()
    serializer_class = InteractionSerializer
    filter_fields = (
        "interaction_point",
        "interaction_version",
        "interaction_type",
        "interaction_point__prot_res_id__targ_res_id__target_id",
        "interaction_point__mol_id",
        "interaction_point__prot_res_id__prot_id",
        "distance",
        "score",
        "prot_smarts",
        "mol_smarts",
    )


class InteractionPointView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = InteractionPoint.objects.filter()
    serializer_class = InteractionPointSerializer
    filter_fields = ("prot_res_id", "mol_id", "protein_atom_name", "molecule_atom_name")


class ProteinResidueView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = ProteinResidue.objects.filter()
    serializer_class = ProteinResidueSerialzier
    filter_fields = ("prot_id", "targ_res_id")


class TargetResidueView(viewsets.ReadOnlyModelViewSet):
    paginate_by = None
    queryset = TargetResidue.objects.filter()
    serializer_class = TargetResidueSerialzier
    filter_fields = ("target_id", "res_name", "res_num", "chain_id")
