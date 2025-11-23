# CyberQ ESP32 ESPHome Integration

This project provides an ESPHome custom component for communicating with a CyberQ grill controller via serial connection on an ESP32.

## Overview

The original Python script communicated with the CyberQ controller over USB/serial. This ESPHome implementation provides:

- **Sensors** for reading:
  - Pit 1 & Pit 2 temperatures
  - Food 1 & Food 2 temperatures  
  - Fan 1 & Fan 2 speeds

- **Number controls** for setting:
  - Pit 1 & Pit 2 setpoints
  - Food 1 & Food 2 setpoints

## Hardware Setup

1. **ESP32 Board**: Any ESP32 development board
2. **Serial Connection**: Connect the CyberQ controller to the ESP32:
   - CyberQ TX → ESP32 RX (GPIO16 in config, change as needed)
   - CyberQ RX → ESP32 TX (GPIO17 in config, change as needed)
   - Common GND between ESP32 and CyberQ
   - 5V power (if needed, check CyberQ requirements)

## Software Setup

1. **Install ESPHome**: Follow the [ESPHome installation guide](https://esphome.io/guides/getting_started_hassio.html)

2. **Configure WiFi**: Create a `secrets.yaml` file in your ESPHome config directory:
   ```yaml
   wifi_ssid: "YourWiFiSSID"
   wifi_password: "YourWiFiPassword"
   ```

3. **Deploy the Component**: 
   - Copy the `components/cyberq` directory to your ESPHome config directory
   - Copy `cyberq_esp32.yaml` to your ESPHome config directory
   - Adjust GPIO pins in the YAML if needed (default: TX=GPIO17, RX=GPIO16)

4. **Compile and Upload**:
   ```bash
   esphome compile cyberq_esp32.yaml
   esphome upload cyberq_esp32.yaml
   ```

## Configuration

The main configuration file (`cyberq_esp32.yaml`) includes:

- **UART Configuration**: Serial communication settings (9600 baud)
- **CyberQ Component**: Main controller component
- **Sensors**: All temperature and fan speed sensors
- **Number Controls**: Setpoint controls for pit and food temperatures

### Adjusting GPIO Pins

If you need to use different GPIO pins, modify the `uart` section:

```yaml
uart:
  id: uart_bus
  tx_pin: GPIO17  # Change as needed
  rx_pin: GPIO16  # Change as needed
  baud_rate: 9600
```

## Protocol Details

The component implements the CyberQ serial protocol:

- **Query Commands**: Single character commands (A, B, C, D, E, F) to read values
- **Set Commands**: "~" prefix followed by lowercase letter (h, i, l, m) and encoded value
- **Response Format**: 6-byte responses where bytes 2-5 contain the encoded value
- **Value Encoding**: Values are encoded/decoded using a special format matching the original Python implementation

## Integration with Home Assistant

Once deployed, the ESP32 will appear in Home Assistant (if using ESPHome integration). You can:

- View all sensor values in real-time
- Control setpoints using number entities
- Create automations based on temperature readings
- Set up notifications for temperature alerts

## Troubleshooting

1. **No sensor readings**: 
   - Check serial connections (TX/RX may be swapped)
   - Verify baud rate is 9600
   - Check ESP32 logs via ESPHome dashboard

2. **Setpoints not working**:
   - Verify the CyberQ controller accepts serial commands
   - Check that the controller is powered and responsive

3. **Connection issues**:
   - Ensure WiFi credentials are correct
   - Check that ESP32 can reach your network

## Files Structure

```
.
├── cyberq_esp32.yaml          # Main ESPHome configuration
├── components/
│   └── cyberq/
│       ├── __init__.py        # Python registration code
│       ├── cyberq.h            # Main component header
│       ├── cyberq.cpp          # Main component implementation
│       ├── sensor/
│       │   ├── cyberq_sensor.h
│       │   └── cyberq_sensor.cpp
│       └── number/
│           ├── cyberq_number.h
│           └── cyberq_number.cpp
└── README.md                   # This file
```

## License

This code is provided as-is for use with CyberQ controllers.

