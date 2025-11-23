import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number, uart
from esphome.const import CONF_ID

DEPENDENCIES = ["cyberq"]

# Import from parent module
from .. import cyberq_ns, CyberQComponent, CONF_CYBERQ_ID

CyberQNumber = cyberq_ns.class_("CyberQNumber", number.Number, cg.Component)

def validate_number_config(config):
    number_types = ["pit1_setpoint", "pit2_setpoint", "food1_setpoint", "food2_setpoint"]
    if not any(key in config for key in number_types):
        raise cv.Invalid("At least one number type must be specified")
    return config

# number.number_schema() returns a schema, but we need to ensure it includes all number options
# Extend the base schema to explicitly include min_value, max_value, and step
_base_schema = number.number_schema(CyberQNumber).extend({
    cv.Optional("min_value"): cv.float_,
    cv.Optional("max_value"): cv.float_,
    cv.Optional("step"): cv.positive_float,
})

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_CYBERQ_ID): cv.use_id(CyberQComponent),
    cv.Optional("pit1_setpoint"): _base_schema,
    cv.Optional("pit2_setpoint"): _base_schema,
    cv.Optional("food1_setpoint"): _base_schema,
    cv.Optional("food2_setpoint"): _base_schema,
}).add_extra(validate_number_config)

def to_code(config):
    parent = yield cg.get_variable(config[CONF_CYBERQ_ID])
    
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
        # Extract min_value, max_value, and step from config (required by number.new_number)
        min_value = number_config.get("min_value", 0.0)
        max_value = number_config.get("max_value", 500.0)
        step = number_config.get("step", 1.0)
        
        num = yield number.new_number(
            number_config,
            min_value=min_value,
            max_value=max_value,
            step=step,
        )
        cg.add(num.set_cyberq_parent(parent))
        cg.add(num.set_number_type(number_type))

