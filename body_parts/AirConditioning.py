class AirConditioning():

    def __init__(self, refrigerant_type, compressor_type, heat_exchanger_efficiency):
        self.is_activated = False
        self.refrigerant_type = refrigerant_type
        self.compressor_type = compressor_type
        self.heat_exchanger_efficiency = heat_exchanger_efficiency