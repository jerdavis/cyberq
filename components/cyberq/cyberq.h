#pragma once

#include "esphome.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace cyberq {

static const char *TAG = "cyberq";

class CyberQComponent : public Component, public uart::UARTDevice {
 public:
  void setup() override;
  void loop() override;
  void dump_config() override;

  // Query methods
  float query_pit1_temp();
  float query_pit2_temp();
  float query_food1_temp();
  float query_food2_temp();
  float query_fan1_speed();
  float query_fan2_speed();
  
  // Set methods
  void set_pit1_temp(float temp);
  void set_pit2_temp(float temp);
  void set_food1_temp(float temp);
  void set_food2_temp(float temp);

 protected:
  float query_value(char command);
  float process_response(const std::string &raw_value);
  std::string get_usb_value(uint16_t value);
  void send_command(const std::string &command);
  std::string read_response(size_t length = 6);
  
  unsigned long last_query_time_ = 0;
  static const unsigned long QUERY_INTERVAL_MS = 500;
  bool query_in_progress_ = false;
};

}  // namespace cyberq
}  // namespace esphome

