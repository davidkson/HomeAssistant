start_led = data.get("start_led")
stop_led = data.get("stop_led")
active_led_count = data.get("active_led_count")
style = data.get("style")
ip_address = data.get("ip_address")

def red_to_green(r, g, b):
    if(g < 255):
        g = min(255, g + increment)
    elif(r > 0):
        r = max(0, r - decrement)
    return (r,g,b)

def green_to_red(r, g, b):
    if(r < 255):
        r = min(255, r + increment)
    elif(g > 0):
        g = max(0, g - decrement)
    return (r,g,b)

def toRgbString(t):
    return "[" + str(t[0]) + ", " + str(t[1]) + ", " + str(t[2]) + "]"

reverse = False
r = 0
g = 0
b = 0
gradientFunc = lambda r,g,b : (r,g,b)
gradient_grade = 0.5

if(stop_led < start_led):
    reverse = True
    temp_stop = stop_led
    stop_led = start_led
    start_led = temp_stop

if(style == 'red_green'):
    r = 255
    g = 0
    gradient_grade = 0.75
    gradientFunc = red_to_green
elif(style == 'green_red'):
    r = 0
    g = 255
    gradient_grade = 0.25
    gradientFunc = green_to_red

total_led_count = (stop_led - start_led) + 1
increment_count = round(total_led_count * gradient_grade)
decrement_count = total_led_count - increment_count

increment = round(255/increment_count)
decrement = round(255/decrement_count)

rgb = []

for current_led in range(0, total_led_count):
    if current_led < active_led_count:        
        rgb.append((r,g,b))
        r,g,b = gradientFunc(r, g, b)        
    else:        
        rgb.append((0,0,0))

payload = ""  
for index, rgb_value in enumerate(rgb):
    if reverse:
        ledIndex = (stop_led - index - 1)                
    else:
        ledIndex = (index + start_led-1)

    payload = payload + str(ledIndex) + "," + toRgbString(rgb_value) + ","
    
payload = '{"seg":{"i":[' + payload[:-1] + ']}}'

service_data = {"url" : "http://" + ip_address + "/json/state", "payload" : payload }
hass.services.call('rest_command','post', service_data, False)
