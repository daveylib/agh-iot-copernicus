const btn1 = document.getElementById('button1');
const btn2 = document.getElementById('button2');
const led1 = document.getElementById('led1');
const led2 = document.getElementById('led2');
const light_sensor = document.getElementById('light-sensor');
const knob = document.getElementById('knob');
const dashboard = document.getElementById('dashboard');
const temperature = document.getElementById('temperature-marker');
const led2_color_chooser = document.getElementById('led2-color-chooser');


// Buttons
btn1.addEventListener('mousedown', e=> {
    eel.button1_down_handler()(state=>{
        if (state)
            update_button1_state(true);
    })

    addEventListener('mouseup', button1_mouseup_handler);
});

function button1_mouseup_handler(e) {
    eel.button1_up_handler()(state=>{
        if (state)
            update_button1_state(false);
    })

    removeEventListener('mouseup', button1_mouseup_handler);
}

btn2.addEventListener('mousedown', e=> {
    eel.button2_down_handler()(state=>{
        if (state)
            update_button2_state(true);
    })

    addEventListener('mouseup', button2_mouseup_handler);
});

function button2_mouseup_handler(e) {
    eel.button2_up_handler()(state=>{
        if (state)
            update_button2_state(false);
    })
    removeEventListener('mouseup', button2_mouseup_handler);
}


// Leds
led1.addEventListener('click', e=> {
    eel.toggle_led1()(state=>{
        update_led1(state);
    })
});

led2.addEventListener('click', e=> {
    led2_color_chooser.style.display = 'flex';
}, true);

led2_color_chooser.addEventListener('click', e=> {
    const color = e.target.getAttribute('name');
    led2_color_chooser.style.display = 'none';
    if (!color) 
        return

    eel.set_led2_color(color)(state=>{
        if (state) {
            if (color == 'Off'){
                led2.style.background = 'gray';
                return;
            }
            led2.style.background = color;
        }
    });
    
    
});


//knob
let knob_value = 0;
let knob_value_rounded = 0;
let starting_diff_angle = 0;
const no_spins = 2;
const knob_center = {x: 0, y: 0}
function getKnobAngle(e){
    if (e.clientX >= knob_center.x && e.clientY < knob_center.y)
        return Math.atan2(Math.abs(e.clientX - knob_center.x), Math.abs(e.clientY - knob_center.y)) * (180 / Math.PI) - starting_diff_angle;
    if (e.clientX > knob_center.x && e.clientY >= knob_center.y)
        return 90 + Math.atan2(Math.abs(e.clientY - knob_center.y), Math.abs(e.clientX - knob_center.x)) * (180 / Math.PI) - starting_diff_angle;
    if (e.clientX <= knob_center.x && e.clientY > knob_center.y)
        return Math.atan2(Math.abs(e.clientX - knob_center.x), Math.abs(e.clientY - knob_center.y)) * (180 / Math.PI) + 180 - starting_diff_angle;
    if (e.clientX < knob_center.x && e.clientY <= knob_center.y)
        return 270 + Math.atan2(Math.abs(e.clientY - knob_center.y), Math.abs(e.clientX - knob_center.x)) * (180 / Math.PI) - starting_diff_angle;
}

knob.addEventListener('mousedown', e=> {
    e.preventDefault();
    const rect = knob.getBoundingClientRect();
    knob_center.x = rect.left + rect.width / 2;
    knob_center.y = rect.top + rect.height / 2;
    let angle = parseFloat(getComputedStyle(knob).getPropertyValue('--knob-angle'));
    if (angle > 360)
        angle -= 360;
    starting_diff_angle = getKnobAngle(e)- parseFloat(angle);

    if (starting_diff_angle > 180)
        starting_diff_angle = (360 - starting_diff_angle) * (-1);
    else if (starting_diff_angle < -180)
        starting_diff_angle = (360 + starting_diff_angle) * (1); 

    knob.classList.remove('knob-animate-rotation');
    document.addEventListener('mousemove', knob_move_handler);
    document.addEventListener('mouseup', e=> {
        document.removeEventListener('mousemove', knob_move_handler);
        starting_diff_angle = 0;
    });
});



function knob_move_handler(e) {
    const dist = Math.sqrt((e.clientX - knob_center.x) ** 2 + (e.clientY - knob_center.y) ** 2);
    if (dist < knob.clientWidth / 4) {
        return;
    }

    let prev_angle = parseFloat(getComputedStyle(knob).getPropertyValue('--knob-angle'));

    if (prev_angle > 360)
        prev_angle -= 360;
    let diff = getKnobAngle(e) - prev_angle;

    if (diff > 180)
        diff = (360 - diff) * (-1);
    else if (diff < -180)
        diff = (360 + diff) * (1);
    if ((knob_value == 0 && diff > 30) ||(knob_value == 63 && diff < -30))
        return;

    knob_value += diff * 63 / (360 * no_spins) ;
    if (knob_value > 63){
        knob_value = 63;
        knob.style.setProperty('--knob-angle',  (360*no_spins) + "deg");
        return
    }
    if (knob_value < 0){
        knob_value = 0;
        knob.style.setProperty('--knob-angle',  0 + "deg");
        return
    }

    const angle =  knob_value / 63 * 360 * no_spins
    knob.style.setProperty('--knob-angle',  angle + "deg");
    if (knob_value_rounded != Math.round(knob_value)){
        knob_value_rounded = Math.round(knob_value);
        eel.knob_handler(Math.round(knob_value));
    }
    
    
}




//EXPOSE FUNCTIONS
//buttons
eel.expose(update_button1_state);
function update_button1_state(state) {
    if (state) {
        btn1.classList.add('blue-bg');
    } else {
        btn1.classList.remove('blue-bg');
    }
}

eel.expose(update_button2_state);
function update_button2_state(state) {
    if (state) {
        btn2.classList.add('blue-bg');
    } else {
        btn2.classList.remove('blue-bg');
    }
}



//leds
eel.expose(update_led1);
function update_led1(state) {
    if (state) {
        led1.style.backgroundColor = 'yellow';
    } else {
        led1.style.backgroundColor = 'gray';
    }
}

eel.expose(update_led2);
function update_led2(colorArray) {
    if (colorArray[0] == 0 && colorArray[1] == 0 && colorArray[2] == 0) {
        led2.style.backgroundColor = 'gray';
        return;
    }
    const color = {
        0: 'red',
        1: 'green',
        2: 'blue'
    }

    led2.style.backgroundColor = color[colorArray.indexOf(3)];
}


//dashboard
eel.expose(update_dashboard);
function update_dashboard(angle) {
    const dashboard_offset = 90;
    if (angle < 0) 
        angle = 0
    else if (angle > 180)
        angle = 180
    angle -= dashboard_offset;
    dashboard.style.setProperty('--dashboard-angle', angle + "deg");
}

//knob
eel.expose(update_knob);
function update_knob(value) {
    knob_value = value;
    knob_value_rounded = value;
    const angle =  value / 63 * 360 * no_spins
    document.removeEventListener('mousemove', knob_move_handler);
    starting_diff_angle = 0;
    knob.classList.add('knob-animate-rotation');
    knob.style.setProperty('--knob-angle', angle + "deg");

}

//temperature
eel.expose(update_temperature);
function update_temperature(temp) {
    const min_temp = 10;
    const max_temp = 41;
    temperature.parentElement.setAttribute('name', "Temperature Sensor: " + temp + "°C");

    temp = (temp - min_temp) / (max_temp - min_temp) * 100;
    
    if (temp < 0)
        temp = 0;
    else if (temp > 100)
        temp = 100;
    temp = temp * 0.9 + 5;
    temperature.style.setProperty('--marker-position', temp + "%");
}

eel.expose(update_light_sensor);
function update_light_sensor(value){
    const min_value = 0;
    const max_value = 63;

    value = Math.floor((value - min_value) / (max_value - min_value) * 100);
    
    if (value < 0)
        value = 0;
    else if (value > 100)
        value = 100;

    light_sensor.style.backgroundColor = `hsl(60, 0%, ${value}%)`;
}