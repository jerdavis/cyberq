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
}).extend(uart.UART_DEVICE_SCHEMA).extend(cv.COMPONENT_SCHEMA)

def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    yield cg.register_component(var, config)
    yield uart.register_uart_device(var, config)


# Platform schemas are defined in sensor.py and number.py
# Export classes for use in platform files
__all__ = ['cyberq_ns', 'CyberQComponent', 'CyberQSensor', 'CyberQNumber', 'CONF_CYBERQ_ID']

