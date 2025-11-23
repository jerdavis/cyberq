#include "cyberq_number.h"

namespace esphome {
namespace cyberq {

static const char *TAG = "cyberq.number";

void CyberQNumber::setup() {
  // Setup if needed
}

void CyberQNumber::control(float value) {
  if (this->parent_ == nullptr) {
    return;
  }
  
  if (this->number_type_ == "pit1_setpoint") {
    this->parent_->set_pit1_temp(value);
  } else if (this->number_type_ == "pit2_setpoint") {
    this->parent_->set_pit2_temp(value);
  } else if (this->number_type_ == "food1_setpoint") {
    this->parent_->set_food1_temp(value);
  } else if (this->number_type_ == "food2_setpoint") {
    this->parent_->set_food2_temp(value);
  }
  
  this->publish_state(value);
}

void CyberQNumber::dump_config() {
  LOG_NUMBER("", "CyberQ Number", this);
  ESP_LOGCONFIG(TAG, "  Type: %s", this->number_type_.c_str());
}

}  // namespace cyberq
}  // namespace esphome

