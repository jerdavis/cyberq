import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, uart
from esphome.const import CONF_ID

DEPENDENCIES = ["cyberq"]

# Import from parent module
from .. import cyberq_ns, CyberQComponent, CONF_CYBERQ_ID

CyberQSensor = cyberq_ns.class_("CyberQSensor", sensor.Sensor, cg.PollingComponent)

def validate_sensor_config(config):
    sensor_types = ["pit1_temperature", "pit2_temperature", "food1_temperature", 
                    "food2_temperature", "fan1_speed", "fan2_speed"]
    if not any(key in config for key in sensor_types):
        raise cv.Invalid("At least one sensor type must be specified")
    return config

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_CYBERQ_ID): cv.use_id(CyberQComponent),
    cv.Optional("pit1_temperature"): sensor.sensor_schema(
        CyberQSensor,
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("pit2_temperature"): sensor.sensor_schema(
        CyberQSensor,
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("food1_temperature"): sensor.sensor_schema(
        CyberQSensor,
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("food2_temperature"): sensor.sensor_schema(
        CyberQSensor,
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("fan1_speed"): sensor.sensor_schema(
        CyberQSensor,
        accuracy_decimals=1,
    ),
    cv.Optional("fan2_speed"): sensor.sensor_schema(
        CyberQSensor,
        accuracy_decimals=1,
    ),
    cv.Optional("update_interval"): cv.update_interval,
}).add_extra(validate_sensor_config)

def to_code(config):
    parent = yield cg.get_variable(config[CONF_CYBERQ_ID])
    
    sensor_type = ""
    sensor_config = None
    
    if "pit1_temperature" in config:
        sensor_type = "pit1_temperature"
        sensor_config = config["pit1_temperature"]
    elif "pit2_temperature" in config:
        sensor_type = "pit2_temperature"
        sensor_config = config["pit2_temperature"]
    elif "food1_temperature" in config:
        sensor_type = "food1_temperature"
        sensor_config = config["food1_temperature"]
    elif "food2_temperature" in config:
        sensor_type = "food2_temperature"
        sensor_config = config["food2_temperature"]
    elif "fan1_speed" in config:
        sensor_type = "fan1_speed"
        sensor_config = config["fan1_speed"]
    elif "fan2_speed" in config:
        sensor_type = "fan2_speed"
        sensor_config = config["fan2_speed"]
    
    if sensor_config:
        sens = yield sensor.new_sensor(sensor_config)
        cg.add(sens.set_cyberq_parent(parent))
        cg.add(sens.set_sensor_type(sensor_type))
        
        if "update_interval" in config:
            yield cg.register_component(sens, {"update_interval": config["update_interval"]})

