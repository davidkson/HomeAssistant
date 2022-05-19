rgb = []
r = 0
g = 0
b = 0
reverse = False
gradient_grade = 0.5

start_led = data.get("start_led")
stop_led = data.get("stop_led")
active_led_count = data.get("active_led_count")
style = data.get("style")
ip_address = data.get("ip_address")

if(stop_led < start_led):
    reverse = True
    temp_stop = stop_led
    stop_led = start_led
    start_led = temp_stop

if(style == 'red_green'):
    r = 255
    g = 0
    gradient_grade = 0.75
elif(style == 'green_red'):
    r = 0
    g = 255
    gradient_grade = 0.25

total_led_count = (stop_led - start_led) + 1
increment_count = round(total_led_count * gradient_grade)
decrement_count = total_led_count - increment_count

increment = round(255/increment_count)
decrement = round(255/decrement_count)

for i in range(0,total_led_count):
    if i < active_led_count:
        rgb.append("[" + str(r)  + "," + str(g) + "," + str(b) + "]")
        if(style == 'red_green'):
            if(g < 255):
                g = min(255,g + increment)
            elif(r > 0):
                r = max(0,r - decrement)
        elif(style == 'green_red'):
            if(r < 255):
                r = min(255, r + increment)
            elif(g > 0):
                g = max(0, g - decrement)
    else:
        rgb.append("[0,0,0]")        

output = ""  
for index, x in enumerate(rgb):
    if reverse:
        output = output + str((stop_led - index-1)) + "," + x + ","
    else:
        output = output +  str((index + start_led-1)) + "," + x + ","
    
output = '{"seg":{"i":[' + output[:-1] + ']}}'

service_data = {"url" : "http://" + ip_address + "/json/state", "payload" : output }
hass.services.call('rest_command','post', service_data, False)
