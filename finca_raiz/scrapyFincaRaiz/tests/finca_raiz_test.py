import os
import sys
import copy
import json


stepDir = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(stepDir, 'libraries_test'))
from libraries_test.constants4Test import Constants as testSpecificCons
dirRelativeParents = '.'
sys.path.append(os.path.normpath(os.path.join(stepDir, dirRelativeParents)))
from scrapyFincaRaiz.spiders.fincaRaiz import InmueblesFincaRaizinfoSpider
from scrapy.http import Request, TextResponse


class Test_InmueblesFincaRaizinfoSpider:
    __doc__ = "\n    This class allows to test the 'FINCARAIZ' page spider: https://api.fincaraiz.com.co/document/api/1.0/listing/search\n    "

    # Setup configurations
    testSpecificCons = testSpecificCons()
    testJsonForm = json.loads(testSpecificCons.POSTDATAJSON.format(
      ubicacion = 'cali',
      inmueble = 'apartment',
      transaccion = 'rent',
      pagina = '1' ))
    
    testJsonForm_2 = json.loads(testSpecificCons.POSTDATAJSON.format(
      ubicacion = '',
      inmueble = '',
      transaccion = 'rent',
      pagina = '1' ))

    apartmentChoiceFake = json.loads(testSpecificCons.DICTFAKEPARAMETERS.format(
      name = "Apartamento",
      slug = "apartment"))
    
    apartmentChoiceFake_2 = json.loads(testSpecificCons.DICTFAKEPARAMETERS.format(
      name = "Casa Lote",
      slug = "Casa Lote"))
    property_type = testJsonForm["inmueble"]
    location_path = testJsonForm["ubicacion"]
    offer = testJsonForm["transaccion"]
    api_data = copy.deepcopy(testSpecificCons.DICTFAKEAPIPARAMETERS)
    api_data["filter"]["offer"]["slug"].append(offer)
    api_data["filter"]["property_type"]["slug"].append(property_type)
    api_data["filter"]["location_path"] = location_path
    api_data["fields"]["offset"] = 0
    spider = InmueblesFincaRaizinfoSpider(crawl_args=(json.dumps(testJsonForm)))
    spider_invalid_parameters = InmueblesFincaRaizinfoSpider(crawl_args=(json.dumps(testJsonForm_2)))
    spider_null_parameters = InmueblesFincaRaizinfoSpider(crawl_args=(json.dumps({})))
    def mock_response(self, file_name=None, url=None, request=None):

        """Create a Scrapy fake HTTP response from a JSON file"""
        if not url:
            url = self.testSpecificCons.URL
        if not request:
            request_ = Request(url=url)
        else:
            request_ = Request(url=url, body=request)
        if file_name:
            if not file_name[0] == '/':
                responses_dir = os.path.dirname(os.path.realpath(__file__))
                file_path = os.path.join(responses_dir, "mockJsonResponses", file_name)
            else:
                file_path = file_name
            file_content = open(file_path, 'rb').read()
        else:
            file_content = ''
        response = TextResponse(url=url, request=request_, body=file_content,
                                encoding='utf-8')
        return response


    def test_start_request(self):
        response = TextResponse(str(next(self.spider.start_requests()).url))
        method_request = next(self.spider.start_requests()).method
        response_invalid_parameters = next(
            self.spider_invalid_parameters.start_requests()).cb_kwargs
        null_paramteres_response = next(self.spider_null_parameters.start_requests()).cb_kwargs
        assert all(response_invalid_parameters["correct_params_values"]) == False
        assert all(null_paramteres_response["correct_params_values"]) == False
        assert str(response.status) == '200'
        assert method_request == "POST"
    
    def test_parse(self):
        response_api = self.mock_response("case1.json")
        null_response_api = self.mock_response("case3.json")
        response_spider_clear_fields =  next(self.spider.parse(response_api,
        **{"api_data":self.api_data,"current_page":1,"registros":[],"correct_params_values":[False]}))
        response_error_invalid_page =  next(self.spider.parse(response_api,
        **{"api_data":self.api_data,"current_page":41,"registros":[],"correct_params_values":[True]}))

        api_null_data = copy.deepcopy(self.testSpecificCons.DICTFAKEAPIPARAMETERS)
        api_null_data["filter"]["location_path"] = ".."
        response_spider_null_data =  next(self.spider.parse(null_response_api,
        **{"api_data":api_null_data,"current_page":1,"registros":[],"correct_params_values":[True]}))
        response_spider = next(self.spider.parse(response_api,
        **{"api_data":self.api_data,"current_page":1,"registros":[],"correct_params_values":[True]}))
        response_spider_invalid_page = next(self.spider.parse(response_api,
        **{"api_data":self.api_data,"current_page":0,"registros":[],"correct_params_values":[True]}))

        response_api =json.loads(response_api.text)
        descriptions_api = []
        descriptions_spider=[]
        api_response_records = response_api["hits"]["hits"]
        for inmueble in api_response_records:
            descriptions_api.append( inmueble["_source"]["listing"]["description"] )
        spider_response_records = response_spider["DATA"]["resultados"]
        total_records_spider = len(spider_response_records)
        total_records_api = len(api_response_records)
        for inmueble in spider_response_records:
            descriptions_spider.append(inmueble["descripcionGeneral"])

        assert descriptions_api == descriptions_spider
        assert total_records_api == total_records_spider
        assert response_spider_null_data == self.testSpecificCons.RESULTSNOTFOUND
        assert response_spider_invalid_page == self.testSpecificCons.INVALIDPAGE
        assert response_spider_clear_fields == self.testSpecificCons.INVALIDFIELDVALUE
        assert response_error_invalid_page == self.testSpecificCons.INVALIDPAGE

    def test_get_key(self):
        response_dumy = self.spider.get_key(
            [self.apartmentChoiceFake],self.testSpecificCons.APIOPTIONSAVAILABLES["tipo_inmueble"])
        
        response_error = self.spider.get_key(
            [self.apartmentChoiceFake_2],self.testSpecificCons.APIOPTIONSAVAILABLES["tipo_inmueble"])
        assert response_error == "NA"
        assert response_dumy == "apartamento"
    

    def test_calculate_pagination(self):
        metrics = {"min_value_pagination":0,"max_value_pagination":975}
        min_value = self.spider.calculate_pagination(1)
        max_value = self.spider.calculate_pagination(40)
        error_value = self.spider.calculate_pagination(-1)
        assert min_value == metrics["min_value_pagination"]
        assert max_value == metrics["max_value_pagination"]
        assert error_value == 0
    
    def test_extract_apartment_type(self):
        response_dumy = json.loads( self.mock_response("case1.json").text)
        response_dumy_2 = json.loads( self.mock_response("case2.json").text)
        results = []
        for response  in response_dumy_2["hits"]["hits"]:
            categories = []
            kind_of_property  =self.spider.get_key( 
                response["_source"]["listing"]["property_type"], 
                self.testSpecificCons.APIOPTIONSAVAILABLES["tipo_inmueble"])
            if "categories" in response["_source"]["listing"].keys():
                categories = response["_source"]["listing"]["categories"]
            kind_of_apartment = self.spider.extract_apartment_type(categories,kind_of_property)
            results.append(kind_of_apartment)
        assert(len(response_dumy["hits"]["hits"])) > 0
        assert(results.count("Loft")) >=0
    
    def test_check_key_exists(self):
        response_dumy = json.loads (self.mock_response("case2.json").text)["hits"]["hits"]
        for record in response_dumy:
            response_spider = self.spider.check_key_exists(record["_source"]["listing"], "description")
            without_value = self.spider.check_key_exists(record["_source"], "description")
            error_dict = self.spider.check_key_exists([], "description")
            without_keys = self.spider.check_key_exists(record["_source"]["listing"])
            assert(response_spider) != "Sin especificar"
            assert(error_dict) == False
            assert(without_keys) == False
            assert(without_value) == "Sin especificar"
   
            
        
