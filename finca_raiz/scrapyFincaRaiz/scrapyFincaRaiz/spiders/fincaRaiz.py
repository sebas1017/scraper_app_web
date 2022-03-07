# -*- coding: utf-8 -*-
import scrapy
import logging
import sys
import json
import os
import copy


sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from libraries.constants import Constants as specificCons
 
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../..'))
#from generalLibraries.constants import Constants as generalCons

class InmueblesFincaRaizinfoSpider(scrapy.Spider):
    """
    The following information corresponds to the property records available on the FINCARAIZ page, 
    which is a portal that groups different types of properties for Sale and Lease

    Returns the data of the available properties according to the 3 initial parameters that are sent.

    To consult the data of all the properties available through POST, the service must be started
    from scrapyrt like so: scrapyrt -p 9081.

    Then, the data that is sent by POST must have the following structure:

    transaction field can have 2 values(in spanish):
        En arriendo   =  To rent
        En venta      = To sell

         {
        "crawl_args":"{\"ubicacion\":\"cali\", \"inmueble\":\"Apartamento\", \"transaccion\":\"En arriendo\", \"pagina\":\"1\" }",
        "spider_name":"inmueblesFincaRaiz",
        "start_requests": "True"
        }
     example of the first 2 records
     "items": [
        {
            "DATA": {
                "resultados": [
                    {
                        "descripcionGeneral": "ALQUILO EN CALI,  HERMOSOS APARTAMENTO EN LUGAR PRIVILEGIADO.  Facil acceso,  tres alcobas,  dos baños,  sala,  comedor,  cocina,  zona de ropas,  balcon,  parqueadero propio en plataforma.  Cerca a centros comerciales,  supermercados,  centros de salud.  Acceso a transporte pulico facil .",
                        "habitaciones": "3",
                        "areaConstruida": "71.0m2",
                        "antiguedad": "9 a 15 años",
                        "tipoApartamento": "NA",
                        "estado": "Sin especificar-NONE",
                        "administracion": "{'incluida': 'NO', 'precio': '228000.0'}",
                        "banos": "2",
                        "areaPrivada": "0.0m2",
                        "precioM2": "17605.6338028169",
                        "parqueaderos": "1",
                        "estrato": "Estrato 4",
                        "piso": "4°"
                    },
                    {
                        "descripcionGeneral": "Alquilo apartamento en barrio Calicanto - Valle del Lili. Segundo y tercer piso. Consta de 3 habitaciones,  3 closets,  3 baños,  sala-comedor,  1 balcón,  1 sala de estar,  zona de oficios amplia,  pisos en cerámica,  totalmente fresco y ventilado. Cerca a centros comerciales,  clínicas y estaciones del MIO. Cra 95A # 45-39. Agenda tu cita. .",
                        "habitaciones": "3",
                        "areaConstruida": "160.0m2",
                        "antiguedad": "menor a 1 año",
                        "tipoApartamento": "NA",
                        "estado": "Sin especificar-NONE",
                        "administracion": "{'incluida': 'NO', 'precio': '0.0'}",
                        "banos": "3",
                        "areaPrivada": "160.0m2",
                        "precioM2": "7187.5",
                        "parqueaderos": "Sin especificar",
                        "estrato": "Estrato 4",
                        "piso": "Sin especificar"
                    }
            ]
             }
        }
    ]


      The json returned by the spider has the following structure when ubicacion is not found:
      input json post
      {
        "crawl_args":"{\"ubicacion\":\"*\", \"inmueble\":\"Apartamento\", \"transaccion\":\"En arriendo\",\"pagina\":\"1\" }",
        "spider_name":"inmueblesFincaRaiz",
        "start_requests": "True"
        }

      result not found
      "items": [
        {
            "DATA": {
                "resultados": [
                    {
                        "mensaje": "No se encontraron coincidencias..."
                    }
                ]
            }
        }
    ]
    """
    specificCons = specificCons()
    #generalCons = generalCons()
    name = "inmueblesFincaRaiz" 
    url = 'https://api.fincaraiz.com.co/document/api/1.0/listing/search'
    crawl_args = None
    __allowed = ("crawl_args")
    custom_settings = {
        "ROBOTSTXT":True,
        "FEED_EXPORT_ENCODING":'utf-8'
    }
    options =specificCons.JSONOPTIONS
    
    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.ERROR)
        super(InmueblesFincaRaizinfoSpider, self).__init__(*args, **kwargs)
        for k, v in kwargs.items():
            if( k in self.__class__.__allowed):
                setattr(self, k, v)
        self.crawl_args = kwargs


    def extract_apartment_type(self, record_categories, type_of_propertie):
        apartment_type = "NA"
        if len(record_categories)>0:
            for data in record_categories:
                if data["parent"]["slug"] == type_of_propertie:
                    apartment_type = data["name"]
                    break
        return apartment_type

    def check_key_exists(self,element, *keys):
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(element, dict):
            return False
        if len(keys) == 0:
            return False

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return "Sin especificar"
        return _element

    def get_key(self, list_property_types, my_dict):
        data_final = "NA"
        for data in list_property_types:
            val = data["slug"]
            for key, value in my_dict.items():
                if val == value:
                    return key
        return data_final

    def calculate_pagination(self,page):
        to  = 0
        if (page > 0 and page <=40 ) :
            page_finca  = page
            current_page= page_finca - 1
            per_page =self.specificCons.RECORDSPERPAGE
            to  = per_page * current_page
        return to


    def start_requests(self):
        """
        here the parameters are constructed in JSON format.
        It allows to consult the direct API of the FINCARAIZ source. 
        returns the response in JSON format
        """  
        keys = self.crawl_args.keys()
        if "crawl_args" in keys:
            params = json.loads( self.crawl_args["crawl_args"])
        else:
            params = self.crawl_args
        if len(params.keys()) ==0:
            params = {"ubicacion":"", "transaccion":"", "pagina":"", "inmueble":""}
        for key , value in params.items():
                if len(value.strip()) > 0:
                    try:
                        if key == "inmueble":
                            params[key] = self.options["tipo_inmueble"][value.strip().lower()]
                        if key == "transaccion":
                            params[key] = self.options["tipo_transaccion"][value.strip().lower()]
                    except KeyError:
                        pass
                else:
                    params[key] = 'NA'

        correct_params_values =  [True if value.strip() != "NA" else False for key , value in params.items()]
        property_type  = params["inmueble"]
        location_path = params["ubicacion"]
        offer = params["transaccion"]
        initial_page = int(params["pagina"]) if params["pagina"].strip() != "NA" else 0
        offset = self.calculate_pagination(initial_page)
        api_data = copy.deepcopy(self.specificCons.JSONPOSTAPI)
        api_data["filter"]["offer"]["slug"].append(offer)
        api_data["filter"]["property_type"]["slug"].append(property_type)
        api_data["filter"]["location_path"] = location_path
        api_data["fields"]["offset"] = offset
    
        yield scrapy.Request(url=self.url,
         method="POST",body=json.dumps(api_data), headers={'Content-Type':'application/json'} , callback=self.parse,
             meta = {"solve_captcha": False},cb_kwargs={"api_data":api_data,"current_page":initial_page,"registros":[],"correct_params_values":correct_params_values})
        

    def parse(self, response, **kwargs):
        """
        It allows you to consume the API where you can find all the information 
        about the properties available on the FINCARAIZ page in a specific location, 
        with a filter determined by type of transaction (for rent or sale) 
        and by a specific type of property.

        Parameters:
            response: start_requets 

        Departure:
            Json with all the property information of the FINCARAIZ page, the json
            has the following structure:

                {"DATA": {"resultados":[final_output]}
        """
        final_page = self.specificCons.FINALPAGELIMIT
        no_data_message= self.specificCons.NULLRESULTSMESSAGE
        page_validation_message = self.specificCons.PAGEVALIDATIONMESSAGE
        clear_fields_message = self.specificCons.NULLVALUESMESSAGE
        verify_params_values =  kwargs["correct_params_values"]
        list_ids = kwargs["registros"]
        current_page = kwargs["current_page"]
        data_response = json.loads(response.text)
        propiedades = data_response["hits"]["hits"] if data_response["hits"]["hits"] else []
        if int(current_page) <= final_page and all(verify_params_values): 
            if ( len(propiedades)> 0 and (current_page!= "" and int(current_page) >0 ) ):
                ids = []
                for propiedad in  propiedades:
                    if "categories" in propiedad["_source"]["listing"].keys():
                        categories = propiedad["_source"]["listing"]["categories"]
                    else:
                        categories= []
                    data =  propiedad["_source"]["listing"]
                    property = self.specificCons.JSONFINCARAIZ.format(
                        descripcion_general = self.check_key_exists(data,"description"),
                        habitaciones =self.check_key_exists(data,"rooms","name"),
                        area_construida=self.check_key_exists(data,"area") + "m2",
                        antiguedad=self.check_key_exists(data,"age","name"),
                        tipo_apartamento=self.extract_apartment_type(categories,
                            self.get_key( propiedad["_source"]["listing"]["property_type"], self.options["tipo_inmueble"])
                            ),
                        estado =self.check_key_exists(data,"condition","name") +  "-" + self.check_key_exists(data,"condition","slug"),
                        administracion={
                                "incluida":"SI" if propiedad["_source"]["listing"]["administration"]["is_included"] else "NO",
                                "precio":self.check_key_exists(data, "administration","price")
                                },
                        banos=self.check_key_exists(data,"baths","name") ,
                        area_privada=self.check_key_exists( data , "living_area") + "m2",
                        precio_m2=self.check_key_exists(data,"price_m2"),
                        parqueaderos=self.check_key_exists(data,"garages","name"),
                        estrato=self.check_key_exists(data,"stratum","name"),
                        piso=self.check_key_exists(data,"floor","name")
                    )
                    property = json.loads(property)
                    ids.append(property)
                list_ids.extend(ids)
                data = list_ids if len(list_ids) > 0 else [no_data_message]
                final_output = { "DATA":{"resultados":data}}
                yield final_output
            else:
                if (current_page == "" or int(current_page) == 0 ):
                    data = [page_validation_message]
                else:  
                    data = list_ids if len(list_ids) > 0 else [no_data_message]
                final_output = { "DATA":{"resultados":data}}
                yield final_output
        else:
                final_data = []
                if all(verify_params_values) is False:
                    final_data.append (clear_fields_message)
                elif int(current_page) > final_page:
                    final_data.append(page_validation_message)
                final_output = { "DATA":{"resultados":final_data}}
                yield final_output