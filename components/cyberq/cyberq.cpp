#include "cyberq.h"
#include <cmath>

namespace esphome {
namespace cyberq {

void CyberQComponent::setup() {
  ESP_LOGCONFIG(TAG, "Setting up CyberQ...");
  this->last_query_time_ = millis();
}

void CyberQComponent::loop() {
  // Component loop - can be used for periodic tasks if needed
}

void CyberQComponent::dump_config() {
  ESP_LOGCONFIG(TAG, "CyberQ Controller:");
  ESP_LOGCONFIG(TAG, "  Baud Rate: 9600");
}

float CyberQComponent::query_value(char command) {
  // Prevent concurrent queries
  if (this->query_in_progress_) {
    return NAN;
  }
  
  this->query_in_progress_ = true;
  std::string cmd(1, command);
  this->send_command(cmd);
  delay(100);  // Delay for response
  std::string response = this->read_response(6);
  this->query_in_progress_ = false;
  
  if (response.length() >= 6) {
    return this->process_response(response);
  }
  return NAN;
}

float CyberQComponent::process_response(const std::string &raw_value) {
  if (raw_value.length() < 6) {
    return NAN;
  }
  
  // Process bytes 2-5 (indices 2, 3, 4, 5)
  uint32_t value = 0;
  for (int i = 0; i < 4; i++) {
    uint8_t byte_val = static_cast<uint8_t>(raw_value[2 + i]);
    uint8_t nibble = byte_val & 0x0F;  // Lower 4 bits
    value += static_cast<uint32_t>(nibble) * static_cast<uint32_t>(pow(16, 3 - i));
  }
  
  return (value + 1.0f) / 2.0f;
}

std::string CyberQComponent::get_usb_value(uint16_t value) {
  std::string result;
  result += static_cast<char>(((value & 0xF) / 1) + 48);
  result += static_cast<char>(((value & 0xF0) / 16) + 48);
  result += static_cast<char>(((value & 0xF00) / 256) + 48);
  result += static_cast<char>(((value & 0xF000) / 4096) + 48);
  result += "^";
  return result;
}

void CyberQComponent::send_command(const std::string &command) {
  this->write_array(reinterpret_cast<const uint8_t *>(command.c_str()), command.length());
  this->flush();
}

std::string CyberQComponent::read_response(size_t length) {
  std::string response;
  response.reserve(length);
  
  unsigned long start_time = millis();
  while (response.length() < length && (millis() - start_time) < 1000) {
    if (this->available()) {
      uint8_t byte;
      if (this->read_byte(&byte)) {
        response += static_cast<char>(byte);
      }
    }
    delay(10);
  }
  
  return response;
}

float CyberQComponent::query_pit1_temp() {
  return this->query_value('A');
}

float CyberQComponent::query_pit2_temp() {
  return this->query_value('B');
}

float CyberQComponent::query_food1_temp() {
  return this->query_value('E');
}

float CyberQComponent::query_food2_temp() {
  return this->query_value('F');
}

float CyberQComponent::query_fan1_speed() {
  return this->query_value('C');
}

float CyberQComponent::query_fan2_speed() {
  return this->query_value('D');
}

void CyberQComponent::set_pit1_temp(float temp) {
  uint16_t temp_value = static_cast<uint16_t>(temp * 2);
  std::string request = "~h" + this->get_usb_value(temp_value);
  this->send_command(request);
}

void CyberQComponent::set_pit2_temp(float temp) {
  uint16_t temp_value = static_cast<uint16_t>(temp * 2);
  std::string request = "~i" + this->get_usb_value(temp_value);
  this->send_command(request);
}

void CyberQComponent::set_food1_temp(float temp) {
  uint16_t temp_value = static_cast<uint16_t>(temp * 2);
  std::string request = "~l" + this->get_usb_value(temp_value);
  this->send_command(request);
}

void CyberQComponent::set_food2_temp(float temp) {
  uint16_t temp_value = static_cast<uint16_t>(temp * 2);
  std::string request = "~m" + this->get_usb_value(temp_value);
  this->send_command(request);
}

}  // namespace cyberq
}  // namespace esphome

