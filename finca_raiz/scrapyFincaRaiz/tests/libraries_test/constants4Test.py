

class Constants:
    __doc__ = '\n    Class that allows to manage the constant variables of the program,\n    is carried out as a class and using the hint @properties to ensure\n    that the value is not modified during the time of execution.\n    '

    def __init__(self):
        self._Constants__POSTDATAJSON = '''
                                        {{
                "ubicacion":"{ubicacion}",
                "inmueble":"{inmueble}",
                "transaccion":"{transaccion}" ,
                "pagina":"{pagina}"
                                        }}
                                        '''
        self._Constants__RESULTSNOTFOUND = {'DATA': {'resultados': [{'mensaje': 'No se encontraron coincidencias...'}]}}

        self._Constants__INVALIDPAGE =  {'DATA': {'resultados': [{"mensaje":"El campo pagina no puede estar vacio , y debe ser mayor que 0 y menor o igual a 40"}]}}
        
        self._Constants__APIOPTIONSAVAILABLES = { "tipo_inmueble":{
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
        

        self._Constants__URL = "https://api.fincaraiz.com.co/document/api/1.0/listing/search"


        self._Constants__DICTFAKEPARAMETERS = '''
                                        {{
                        "name": "{name}", 
                        "slug": "{slug}"
                                        }}'''


        self._Constants__INVALIDFIELDVALUE = {'DATA': {'resultados': [{'mensaje': 'Uno de los campos que esta ingresando se encuentra Vacio favor verificar'}]}}
       
       
        self._Constants__DICTFAKEAPIPARAMETERS = {
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
        
    
    @property
    def POSTDATAJSON(self):
        """
        Allows to create a base json that contains the basic information
        taken from service body request.
        """
        return self._Constants__POSTDATAJSON
    
    
    @property
    def INVALIDFIELDVALUE(self):
        """
        allows to return the error message when any of the 
        parameters sent by the client are empty
        """
        return self._Constants__INVALIDFIELDVALUE
    
    @property
    def INVALIDPAGE(self):
        """
        allows to return the test case of the message that the API must return 
        when the entered page is not in the inclusive range from 1 to 40
        """
        return self._Constants__INVALIDPAGE

    @property
    def APIOPTIONSAVAILABLES(self):
        """
        allows to return the dictionary of equivalent 
        parameters that the API needs to be consumed
        """
        return self._Constants__APIOPTIONSAVAILABLES
    

    @property
    def RESULTSNOTFOUND(self):
        """
        allows to return the message indicating that no 
        results were found
        """
        return self._Constants__RESULTSNOTFOUND


    @property
    def DICTFAKEPARAMETERS(self):
        """
        Allows to create a base json that contains the basic information
        taken from service body request.
        """
        return self._Constants__DICTFAKEPARAMETERS
 

    @property
    def DICTFAKEAPIPARAMETERS(self):
        """
        allows to return a fake dictionary that needs a spider 
        function to validate that it extracts the correct parameters
        """
        return self._Constants__DICTFAKEAPIPARAMETERS


    @property
    def URL(self):
        """
        returns the url of the API that will be consumed
        """
        return self._Constants__URL

