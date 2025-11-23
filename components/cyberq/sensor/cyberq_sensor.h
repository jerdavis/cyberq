#pragma once

#include "esphome.h"
#include "esphome/components/sensor/sensor.h"
#include "../cyberq.h"

namespace esphome {
namespace cyberq {

class CyberQSensor : public sensor::Sensor, public PollingComponent {
 public:
  void set_cyberq_parent(CyberQComponent *parent) { this->parent_ = parent; }
  void set_sensor_type(const std::string &type) { this->sensor_type_ = type; }
  
  void setup() override;
  void update() override;
  void dump_config() override;

 protected:
  CyberQComponent *parent_;
  std::string sensor_type_;
};

}  // namespace cyberq
}  // namespace esphome

