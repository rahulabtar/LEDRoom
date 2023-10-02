from serial_com import SerialCommunication
from strip import Strip
import threading 
class ProgramController:
    def __init__(self,model:SerialCommunication, strip1:Strip):
        self.model = model
        self.strip1 = strip1
        
    def run_program(self):
        mode_data = ['Pattern','Color1','Color2','Color3','Color4','Brightness']
        self.strip1.flag = 'clear_strip'
        effect_thread = threading.Thread(target=self.strip1.clear_strip)
        self.strip1.pixels.show()
        effect_thread.start()
        print("Program Initialized and Started!")
        while True:
            mode_data = self.model.get_request() #grabs request 
            print("Controller: Request got!:" , mode_data)
            mode_data = self.model.translate_request(mode_data)
            print("Controller: Request translated!", mode_data)

            if mode_data[0] == 'Brightness':
                self.strip1.pixels.brightness = mode_data[1] #sets strip brightness to input
                print('Controller: Brightness Changed to:', self.strip1.pixels.brightness)
                self.strip1.pixels.show()
            elif mode_data[0] == 'Pattern':
                if mode_data[1] == 'Rainbow':
                    self.strip1.trans_flag = False
                    self.strip1.flag = 'Rainbow_Animation'
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.rainbow_animation_effect)
                    effect_thread.start()
                elif mode_data[1] == 'Flow_Effect':
                    self.strip1.trans_flag = False
                    self.strip1.flag = 'Flow'
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.flow_effect,args=(mode_data[2],mode_data[3]))
                    effect_thread.start()
                elif mode_data[1] == "Dual_Catapillars":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "Dual_Cats"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.dual_catapillars_effect,args=(mode_data[2],mode_data[3],mode_data[4],mode_data[5]))
                    effect_thread.start()
                elif mode_data[1] == "Twinkle_Effect":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "Twinkle"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.twinkle_effect,args=(mode_data[2],mode_data[3],mode_data[4],mode_data[5]))
                    effect_thread.start()
                elif mode_data[1] == "Shooting_Stars":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "shooting_stars"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.shooting_stars_effect,args=(mode_data[2],))
                    effect_thread.start()
                elif mode_data[1] == "Bouncing_Ball":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "bouncing_ball"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.bouncing_ball_effect,args=(mode_data[2],))
                    effect_thread.start()
                elif mode_data[1] == "Shimmer":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "shimmer"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.shimmer_effect,args=(mode_data[2],mode_data[3],mode_data[4],))
                    effect_thread.start()
                elif mode_data[1] == "Sin_Wave":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "sin_wave"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.sin_wave_effect,args=(mode_data[2],mode_data[3],mode_data[4],mode_data[5]))
                    effect_thread.start()
                elif mode_data[1] == "Fire":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "fire"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.fire_effect)
                    effect_thread.start()
                elif mode_data[1] == "Pulse":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "pulse"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.pulse_effect,args=(mode_data[2],mode_data[3],mode_data[4]))
                    effect_thread.start()
                elif mode_data[1] == "Fill_Color_Effect":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "fill_color"
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.fill_color_effect,args=(mode_data[2],))
                    self.strip1.fill_color_effect(mode_data[2])
                    effect_thread.start()
                elif mode_data[1] == "Clear_Strip":
                    self.strip1.trans_flag = False
                    self.strip1.flag = "clear_strip"
                    effect_thread.join()
                    self.strip1.clear_strip()
                    self.strip1.pixels.show()
                    effect_thread = threading.Thread(target=self.strip1.clear_strip())
                    effect_thread.start()
                elif mode_data[1] == "Transition_Effect":
                    self.strip1.trans_flag = True
                    self.strip1.flag = 'Trans'
                    effect_thread.join()
                    effect_thread = threading.Thread(target=self.strip1.transition_effects)
                    effect_thread.start()
            else:
                print('OH fuck')


