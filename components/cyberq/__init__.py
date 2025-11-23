import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart, sensor, number
from esphome.const import CONF_ID

DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor", "number"]

cyberq_ns = cg.esphome_ns.namespace("cyberq")
CyberQComponent = cyberq_ns.class_("CyberQComponent", cg.Component, uart.UARTDevice)
CyberQSensor = cyberq_ns.class_("CyberQSensor", sensor.Sensor, cg.PollingComponent)
CyberQNumber = cyberq_ns.class_("CyberQNumber", number.Number, cg.Component)

CONF_CYBERQ_ID = "cyberq_id"
CONF_CYBERQ = "cyberq"

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(CyberQComponent),
}).extend(uart.UART_DEVICE_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)


# Sensor platform
SENSOR_PLATFORM_SCHEMA = sensor.SENSOR_PLATFORM_SCHEMA.extend({
    cv.GenerateID(CONF_CYBERQ_ID): cv.use_id(CyberQComponent),
    cv.Optional("pit1_temperature"): sensor.sensor_schema(
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("pit2_temperature"): sensor.sensor_schema(
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("food1_temperature"): sensor.sensor_schema(
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("food2_temperature"): sensor.sensor_schema(
        unit_of_measurement="°F",
        accuracy_decimals=1,
    ),
    cv.Optional("fan1_speed"): sensor.sensor_schema(
        accuracy_decimals=1,
    ),
    cv.Optional("fan2_speed"): sensor.sensor_schema(
        accuracy_decimals=1,
    ),
}).add_extra(cv.requires_one_of("pit1_temperature", "pit2_temperature", "food1_temperature", "food2_temperature", "fan1_speed", "fan2_speed"))

def sensor_to_code(config):
    parent = yield cg.get_variable(config[CONF_CYBERQ_ID])
    
    # Determine sensor type and get the appropriate config
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


# Number platform
NUMBER_PLATFORM_SCHEMA = number.NUMBER_PLATFORM_SCHEMA.extend({
    cv.GenerateID(CONF_CYBERQ_ID): cv.use_id(CyberQComponent),
    cv.Optional("pit1_setpoint"): number.number_schema(
        unit_of_measurement="°F",
    ),
    cv.Optional("pit2_setpoint"): number.number_schema(
        unit_of_measurement="°F",
    ),
    cv.Optional("food1_setpoint"): number.number_schema(
        unit_of_measurement="°F",
    ),
    cv.Optional("food2_setpoint"): number.number_schema(
        unit_of_measurement="°F",
    ),
}).add_extra(cv.requires_one_of("pit1_setpoint", "pit2_setpoint", "food1_setpoint", "food2_setpoint"))

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

