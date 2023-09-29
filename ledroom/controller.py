from serial_com import SerialCommunication
from strip import Strip

class ProgramController:
    def __init__(self,model:SerialCommunication, strip1:Strip):
        self.model = model
        self.strip1 = strip1
        
    def run_program(self):
        self.model.open_serial()

        mode_data = ['Pattern','Color1','Color2','Color3','Color4','Brightness']
        while True:
            mode_data = self.model.get_request() #grabs request 
            mode_data = self.model.translate_request(mode_data) #translates request

            pattern = mode_data[0] #defines each var
            color1 = mode_data[1]
            color2 = mode_data[2]
            color3 = mode_data[3]
            color4 = mode_data[4]
            brightness = mode_data[5] 
    
            self.strip1.brightness = brightness #sets strip brightness to input
            if pattern == 'flow':
                self.strip1.flow_effect(color1,color2)
            elif pattern == 'twinkle':
                self.strip1.twinkle_effect(color1,color2,color3,color4)
            elif pattern == 'fill_color':
                self.strip1.fill_color_effect(color1)
            elif pattern == 'dual_cats':
                self.strip1.dual_catapillars_effect(color1,color2,color3,color4)
            elif pattern == 'rainbow_anim':
                self.strip1.rainbow_animation_effect()
            elif pattern == 'pulse':
                self.strip1.pulse_effect(color1,color2,color3)
            elif pattern == 'sin_wave':
                self.strip1.sin_wave_effect(color1,color2,color3,color4)
            elif pattern == 'ball':
                self.strip1.bouncing_ball_effect(color1)
            elif pattern == 'stars':
                self.strip1.shooting_stars_effect(color1)
            elif pattern =='fire':
                self.strip1.fire_effect(color1)
            elif pattern =='transitions':
                self.strip1.transition_effects()


