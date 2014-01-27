#################### procedure vs. retrieval ###################


import ccm      
log=ccm.log(html=True)   

from ccm.lib.actr import *  

class Arithmetic(ccm.Model):
    operator=ccm.Model(operator='plus',visible='no')
    numbers=ccm.Model(number_left='two',number_right='three',visible='no')


class MotorModule(ccm.Model):
    def reveal_operator(self):
        yield .1
        print "operator visible"
        self.parent.parent.operator.visible='yes'
        
    def reveal_numbers(self):
        yield .1
        print "numbers visible"
        self.parent.parent.numbers.visible='yes'
        
        
class Participant(ACTR):    
    focus=Buffer()
    imaginal=Buffer()
    motor=MotorModule()

    def init():
        focus.set('wait')
        imaginal.set('number_left:no number_right:no operator:no') 

    def respond_operator(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='operator:?operator visible:yes', numbers='visible:no'):
        print "I see the operator"
        focus.set('numbers')
        imaginal.modify(operator=operator)

        
#     def respond_number(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='visible:no', numbers='number_left:?nL number_right:?nR visible:yes'):
#         print "I see the numbers"
#         imaginal.modify(number_left=nL)
#         imaginal.modify(number_right=nR)
#         #focus.set('sandwich cheese')
#         
#         
#     def respond_both(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='visible:yes',numbers='visible:yes'):
#         print "I see both"
#         imaginal.set('number_left:yes number_right:yes operator:yes')
#         #focus.set('sandwich cheese')
                             
#     def addition(imaginal='number_left:no number_right:no operator:!no', numbers='number_left:?nL number_right:?nR visible:yes'):
# 		print "I see the arithmetic problem"
# 		imaginal.modify(number_left=nL)
# 		imaginal.modify(number_right=nR)
# 		focus.set('stop')
	
	#def retrieve(focus="retrieve', 


class Referee(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('start')

    def fixation(focus='start'):
        print "pause"
        focus.set('prime')
        
    def sign_prime(focus='prime'):
        print "reveal the operator"
        motor.reveal_operator()
        focus.set('wait')

#     def no_prime(focus='prime'):
#         print "reveal the problem"
#         motor.reveal_operator()
#         motor.reveal_numbers()
#         focus.set('stop')
# 
#     def numbers_prime(focus='prime'):
#         print "reveal the numbers"
#         motor.reveal_numbers()
#         focus.set('stop')

	def numbers_late(focus='numbers'):
		print "complete the problem with numbers"
		motor.reveal_numbers()

tom=Participant()
siri=Referee()
env=Arithmetic()
env.agent=tom
env.agent=siri

ccm.log_everything(env)

env.run()
ccm.finished()
