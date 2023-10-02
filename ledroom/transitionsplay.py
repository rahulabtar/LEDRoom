from strip import Strip
import board


stripex = Strip(board.D21,300,0.05)
stripex.trans_flag == True
stripex.flow_effect()
