#pragma once

#include "esphome.h"
#include "esphome/components/number/number.h"

namespace esphome {
namespace cyberq {

// Forward declaration
class CyberQComponent;

class CyberQNumber : public number::Number, public Component {

 public:
  void set_cyberq_parent(CyberQComponent *parent) { this->parent_ = parent; }
  void set_number_type(const std::string &type) { this->number_type_ = type; }
  
  void setup() override;
  void control(float value) override;
  void dump_config() override;

 protected:
  CyberQComponent *parent_;
  std::string number_type_;
};

}  // namespace cyberq
}  // namespace esphome

