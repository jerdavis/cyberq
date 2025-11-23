#include "cyberq_sensor.h"
#include "../cyberq.h"

namespace esphome {
namespace cyberq {

static const char *TAG_SENSOR = "cyberq.sensor";

void CyberQSensor::setup() {
  // Setup if needed
}

void CyberQSensor::update() {
  if (this->parent_ == nullptr) {
    this->publish_state(NAN);
    return;
  }
  
  float value = NAN;
  
  if (this->sensor_type_ == "pit1_temperature") {
    value = this->parent_->query_pit1_temp();
  } else if (this->sensor_type_ == "pit2_temperature") {
    value = this->parent_->query_pit2_temp();
  } else if (this->sensor_type_ == "food1_temperature") {
    value = this->parent_->query_food1_temp();
  } else if (this->sensor_type_ == "food2_temperature") {
    value = this->parent_->query_food2_temp();
  } else if (this->sensor_type_ == "fan1_speed") {
    value = this->parent_->query_fan1_speed();
  } else if (this->sensor_type_ == "fan2_speed") {
    value = this->parent_->query_fan2_speed();
  }
  
  this->publish_state(value);
}

void CyberQSensor::dump_config() {
  LOG_SENSOR("", "CyberQ Sensor", this);
  ESP_LOGCONFIG(TAG_SENSOR, "  Type: %s", this->sensor_type_.c_str());
}

}  // namespace cyberq
}  // namespace esphome

