#!/usr/bin/python

__author__ = "Ultracom"
__license__ = "Users authorized by Bancolombia"
__credits__ = "Ultracom-Bancolombia"
__version__ = "1.0"
__maintainer__ = "Ultracom-Bancolombia"


class Constants:
    """
    Class that allows to manage the constant variables of the program, 
    is carried out as a class and using the hint @properties to ensure
    that the value is not modified during the time of execution.
    """


    def __init__(self):


        self.__JSONFINCARAIZ = '''{{
                        "descripcionGeneral":"{descripcion_general}",
                        "habitaciones":"{habitaciones}",
                        "areaConstruida":"{area_construida}",
                        "antiguedad":"{antiguedad}",
                        "tipoApartamento":"{tipo_apartamento}",
                        "estado":"{estado}",
                        "administracion":"{administracion}",
                        "banos":"{banos}",
                        "areaPrivada":"{area_privada}",
                        "precioM2":"{precio_m2}",
                        "parqueaderos":"{parqueaderos}",
                        "estrato":"{estrato}",
                        "piso":"{piso}"

                    }}'''


        self.__JSONOPTIONS = { "tipo_inmueble":{
                "apartamento" :"apartment",
                "casa":"house",
                "lote":"lot",
                "oficina":"office",
                "bodega":"warehouse",
                "apartaestudios":"studio"
        },
        "tipo_transaccion":{
            "en venta":"sell",
            "en arriendo":"rent"
        }
        }


        self.__RECORDSPERPAGE = 25


        self.__FINALPAGELIMIT = 40


        self.__JSONPOSTAPI = {
        "filter": {
            "offer": {
            "slug": [
               
            ]
            },
            "property_type": {
            "slug": [
               
            ]
            },
            "location_path": ""
        },
        "fields": {
            "exclude": [],
            "facets": [
            "rooms.slug",
            "baths.slug",
            "locations.countries.slug",
            "locations.states.slug",
            "locations.cities.slug",
            "locations.neighbourhoods.slug",
            "locations.groups.slug",
            "locations.groups.subgroups.slug",
            "offer.slug",
            "property_type.slug",
            "categories.slug",
            "stratum.slug",
            "age.slug",
            "media.floor_plans.with_content",
            "media.photos.with_content",
            "media.videos.with_content",
            "products.slug",
            "is_new"
            ],
            "include": [
            "categories.name",
            "categories.parent.slug",
            "floor.name",
            "garages.name",
            "price_m2",
            "living_area",
            "administration.is_included",
            "administration.price",
            "condition.name",
            "condition.slug",
            "age.name",
            "description",
            "area",
            "baths.id",
            "baths.name",
            "baths.slug",
            "client.client_type",
            "client.company_name",
            "client.first_name",
            "client.fr_client_id",
            "client.last_name",
            "garages.name",
            "is_new",
            "min_area",
            "min_price",
            "offer.name",
            "price",
            "products.configuration.tag_id",
            "products.configuration.tag_name",
            "products.label",
            "products.name",
            "products.slug",
            "property_id",
            "property_type.name",
            "property_type.slug",
            "fr_property_id",
            "fr_parent_property_id",
            "rooms.id",
            "rooms.name",
            "rooms.slug",
            "stratum.name",
            "title"
            ],
            "limit": 25,
            "offset": "",
            "ordering": [],
            "platform": 40,
            "with_algorithm": False
        }
        }
        self.__NULLVALUESMESSAGE = {"mensaje":"Uno de los campos que esta ingresando se encuentra Vacio favor verificar"}


        self.__NULLRESULTSMESSAGE = {"mensaje":"No se encontraron coincidencias..."}


        self.__PAGEVALIDATIONMESSAGE =  {"mensaje":"El campo pagina no puede estar vacio , y debe ser mayor que 0 y menor o igual a 40"}


    @property
    def JSONFINCARAIZ(self):
        """
        It allows to create a final json that contains the professional 
        registration information.
        """
        return self.__JSONFINCARAIZ
    

    @property
    def JSONOPTIONS(self):
        """
        It allows to create a dictionary that contains 
        the equivalences of the client parameters with the parameters 
        that will be sent to the API
        """
        return self.__JSONOPTIONS


    @property
    def JSONPOSTAPI(self):
        """
        It allows to create a dictionary that contains the parameters necessary by 
        default to consume the API and also has variable parameters that are configured at runtime.
        """
        return self.__JSONPOSTAPI


    @property
    def RECORDSPERPAGE(self):
        """
        this constant represents the number 
        of records each page will have
        """
        return self.__RECORDSPERPAGE


    @property
    def FINALPAGELIMIT(self):
        """
        this constant represents the limit 
        of pages that can be extracted
        """
        return self.__FINALPAGELIMIT


    @property
    def NULLRESULTSMESSAGE(self):
        """
        allows to return the dictionary that contains 
        the message in case there are no results
        """
        return self.__NULLRESULTSMESSAGE


    @property
    def PAGEVALIDATIONMESSAGE(self):
        """
        allows to return the message that indicates an error in the 
        validation of the page when it is not in the range of 1 to 40 inclusive
        """
        return self.__PAGEVALIDATIONMESSAGE


    @property
    def NULLVALUESMESSAGE(self):
        """
        allows to return the error message when any of the parameters 
        sent by the client are empty
        """
        return self.__NULLVALUESMESSAGE