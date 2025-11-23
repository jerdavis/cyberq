import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number, uart

# Define classes (same as in parent module)
cyberq_ns = cg.esphome_ns.namespace("cyberq")
CyberQComponent = cyberq_ns.class_("CyberQComponent", cg.Component, uart.UARTDevice)
CyberQNumber = cyberq_ns.class_("CyberQNumber", number.Number, cg.Component)
CONF_CYBERQ_ID = "cyberq_id"

def validate_number_config(config):
    # Ensure at least one number type is specified
    number_types = ["pit1_setpoint", "pit2_setpoint", "food1_setpoint", "food2_setpoint"]
    if not any(key in config for key in number_types):
        raise cv.Invalid("At least one number type must be specified")
    return config

NUMBER_PLATFORM_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_CYBERQ_ID): cv.use_id(CyberQComponent),
    cv.Optional("pit1_setpoint"): number.number_schema(
        CyberQNumber,
        unit_of_measurement="°F",
    ),
    cv.Optional("pit2_setpoint"): number.number_schema(
        CyberQNumber,
        unit_of_measurement="°F",
    ),
    cv.Optional("food1_setpoint"): number.number_schema(
        CyberQNumber,
        unit_of_measurement="°F",
    ),
    cv.Optional("food2_setpoint"): number.number_schema(
        CyberQNumber,
        unit_of_measurement="°F",
    ),
}).add_extra(validate_number_config)

def number_to_code(config):
    parent = yield cg.get_variable(config[CONF_CYBERQ_ID])
    
    # Determine number type and get the appropriate config
    number_type = ""
    number_config = None
    
    if "pit1_setpoint" in config:
        number_type = "pit1_setpoint"
        number_config = config["pit1_setpoint"]
    elif "pit2_setpoint" in config:
        number_type = "pit2_setpoint"
        number_config = config["pit2_setpoint"]
    elif "food1_setpoint" in config:
        number_type = "food1_setpoint"
        number_config = config["food1_setpoint"]
    elif "food2_setpoint" in config:
        number_type = "food2_setpoint"
        number_config = config["food2_setpoint"]
    
    if number_config:
        num = yield number.new_number(number_config)
        cg.add(num.set_cyberq_parent(parent))
        cg.add(num.set_number_type(number_type))

