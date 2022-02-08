Example:

service: script.labb_led
data:
  ip_address: 192.168.1.121
  brightness: 255  
  start_led: 1
  stop_led: 60
  led_count: "{{ ((60 * states('sensor.volkswagen_id_id_4_rxg75z_state_of_charge')|int/100))| int }}"
