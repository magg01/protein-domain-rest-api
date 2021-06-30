import json
from django.test import TestCase
from django.test.testcases import TransactionTestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.db.utils import IntegrityError

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *

class PfamTest(APITestCase):

    pfam1 = None
    pfam2 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.pfam1 = PfamFactory.create(domain_id = "CoiledCoil", domain_description = "coil prediction")
        self.pfam2 = PfamFactory.create(domain_id = "PF00014", domain_description = "Kunitz/Bovinepancreatictrypsininhibitordomain")
        self.good_url = reverse('pfam_api', kwargs={"domain_id": "PF00014"})
        self.bad_url = reverse('pfam_api', kwargs={"domain_id": "XXXXXX"})
        self.good_url_get_response = self.client.get(self.good_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)
        
    def test_PfamDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_PfamDetailDomainIdRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['domain_id'], "PF00014")

    def test_PfamDetailDomainDescriptionRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['domain_description'], "Kunitz/Bovinepancreatictrypsininhibitordomain")

    def test_PfamDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_PfamPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_PfamPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_PfamPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_PfamDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)

class ProteinTest(APITestCase):

    protein1 = None
    good_url = ''
    bad_url = ''
    good_url_get_response = None
    good_url_get_response_json = None

    def setUp(self):
        self.protein1 = ProteinFactory.create()
        self.good_url = reverse('GET_protein_api', kwargs={"protein_id": self.protein1.protein_id})
        self.bad_url = reverse('GET_protein_api', kwargs={"protein_id": "XXXXXX"})
        self.good_url_get_response = self.client.get(self.good_url)
        self.bad_url_response = self.client.get(self.bad_url)
        self.good_url_get_response_json = json.loads(self.good_url_get_response.content)

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)
        
    def test_ProteinDetailReturnSuccess(self):
        self.assertEqual(self.good_url_get_response.status_code, 200)

    def test_ProteinDetailProteinIdRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['protein_id'], self.protein1.protein_id)

    def test_ProteinDetailSequenceRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['sequence'], self.protein1.sequence)

    def test_ProteinDetailTaxonomyRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['taxonomy']['taxa_id'], self.protein1.taxonomy.taxa_id)
    
    def test_ProteinDetailLengthRecievedCorrect(self):
        self.assertEqual(self.good_url_get_response_json['length'], self.protein1.length)

    def test_ProteinDetailNumberOfPfamsRecievedCorrect(self):
        self.assertEqual(len(self.good_url_get_response_json['domains']), len(self.protein1.domains.values()))

    def test_ProteinDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, 404)

    def test_ProteinPostMethodNotAllowed(self):
        response = self.client.post(self.good_url)
        self.assertEqual(response.status_code, 405)

    def test_ProteinPutMethodNotAllowed(self):
        response = self.client.put(self.good_url)
        self.assertEqual(response.status_code, 405)
        
    def test_ProteinPatchMethodNotAllowed(self):
        response = self.client.patch(self.good_url)
        self.assertEqual(response.status_code, 405)
    
    def test_ProteinDeleteMethodNotAllowed(self):
        response = self.client.delete(self.good_url)
        self.assertEqual(response.status_code, 405)


class PfamTransactionTest(TransactionTestCase):

    pfam = None
    
    def setUp(self):
        self.pfam = PfamFactory.create()
    
    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_PfamUniqueConstraintOnDomainId(self):
        with self.assertRaises(IntegrityError):
            PfamFactory.create(domain_id=self.pfam.domain_id)

    def test_PfamNotUniqueDomainDescriptionIsAllowed(self):
        try:
            PfamFactory.create(domain_description=self.pfam.domain_description)
        except IntegrityError:
            self.fail("an integrity error was generated on this operation, which wasn't expected")

class PfamSerializerTest(APITestCase):
    pfam1 = None
    pfamSerializer = None
    data = None

    def setUp(self):
        self.pfam1 = PfamFactory.create()
        self.pfamSerializer = PfamSerializer(instance=self.pfam1)
        self.data = self.pfamSerializer.data

    def tearDown(self):
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_pfamSerializer(self):
        self.assertEqual(set(self.data.keys()), set(['domain_id', 'domain_description']))

    def test_pfamSerializerDomainIdHasCorrectData(self):
        self.assertEqual(self.data['domain_id'], self.pfam.domain_id)

    def test_pfamSerializerDomainIdHasCorrectData(self):
        self.assertEqual(self.data['domain_description'], self.pfam1.domain_description)
        
class ProteinSerializerTest(APITestCase):
    protein1 = None
    proteinSerializer = None
    data = None

    def setUp(self):
        self.protein1 = ProteinFactory.create()
        self.proteinSerializer = ProteinSerializer(instance=self.protein1)
        self.data = self.proteinSerializer.data

    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Organism.objects.all().delete()
        OrganismFactory.reset_sequence(0)

    def test_proteinSerializer(self):
        self.assertEqual(set(self.data.keys()), set(['id','taxonomy', 'protein_id', 'sequence', 'length', 'pfams']))

    def test_proteinSerializerTaxonomyHasCorrectData(self):
        self.assertEqual(self.data['taxonomy'], self.protein1.taxonomy.taxa_id)

    def test_proteinSerializerProteinIdHasCorrectData(self):
        self.assertEqual(self.data['protein_id'], self.protein1.protein_id)

    def test_proteinSerializerSequenceHasCorrectData(self):
        self.assertEqual(self.data['sequence'], self.protein1.sequence)

    def test_proteinSerializerLengthHasCorrectData(self):
        self.assertEqual(self.data['length'], self.protein1.length)

class ProteinDomainSerializerTest(APITestCase):
    proteinDomain1 = None
    proteinDomainSerializer = None
    data = None

    def setUp(self):
        self.proteinDomain1 = ProteinDomainFactory.create()
        self.proteinDomainSerializer = ProteinDomainSerializer(instance=self.proteinDomain1)
        self.data = self.proteinDomainSerializer.data

    def tearDown(self):
        ProteinDomain.objects.all().delete()
        ProteinDomainFactory.reset_sequence(0)
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        Pfam.objects.all().delete()
        PfamFactory.reset_sequence(0)

    def test_proteinDomainSerializer(self):
        self.assertEqual(set(self.data.keys()), set(['pfam_id','start', 'stop', 'description']))

    def test_proteinDomainSerializerPfamIdHasCorrectData(self):
        self.assertEqual(self.data['pfam_id']['domain_id'], self.proteinDomain1.pfam_id.domain_id)

    def test_proteinDomainSerializerStartHasCorrectData(self):
        self.assertEqual(self.data['start'], self.proteinDomain1.start)

    def test_proteinDomainSerializerStopHasCorrectData(self):
        self.assertEqual(self.data['stop'], self.proteinDomain1.stop)
    
    def test_proteinDomainSerializerDescriptionHasCorrectData(self):
        self.assertEqual(self.data['description'], self.proteinDomain1.description)

