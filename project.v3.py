#################### procedure vs. retrieval ###################


import ccm      
log=ccm.log(html=False)   

from ccm.lib.actr import *  

# define the environment
class Arithmetic(ccm.Model):
    operator=ccm.Model(operator='none',visible='no')
    numbers=ccm.Model(number_left='none',number_right='none',visible='no')
    new_trial=ccm.Model(switch='yes')

import random
class MotorModule(ccm.Model):
    def reveal_operator(self):
        yield .1
        print "operator visible"
        operator=random.choice(['plus','multiply'])
        self.parent.parent.operator.operator=operator
        self.parent.parent.operator.visible='yes'
        
#     def reset_operator(self):
#         yield 0
#         self.parent.parent.operator.visible='no'
        
    def reveal_numbers(self):
    	yield .1
    	print "numbers visible"
    	nL=random.choice(['zero','one','two','three','four','five','six','seven','eight','nine'])
    	nR=random.choice(['zero','one','two','three','four','five','six','seven','eight','nine'])
    	self.parent.parent.numbers.number_left=nL
    	self.parent.parent.numbers.number_right=nR
    	self.parent.parent.numbers.visible='yes'

#     def reset_numbers(self):
#     	yield 0
#     	self.parent.parent.numbers.visible='no'

    def trial_switch(self):    # flag in-trial or between-trial
    	yield 0
#     	print "trial switched"
    	self.parent.parent.new_trial.switch='no'
    	
    def reset_trial(self):
    	yield 0
    	print "trial reset"
    	self.parent.parent.new_trial.switch='yes'
    	self.parent.parent.numbers.number_left='none'
    	self.parent.parent.numbers.number_right='none'
    	self.parent.parent.numbers.visible='no'
    	self.parent.parent.operator.operator='none'
    	self.parent.parent.operator.visible='no'
        
        
class Participant(ACTR):    
    focus=Buffer()
    imaginal=Buffer()
    motor=MotorModule()

    def init():
        imaginal.set('number_left:no number_right:no operator:no')
        focus.set('wait')

    def respond_operator(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='operator:?operator visible:yes', numbers='visible:no'):
        print "I see the operator. It is a", operator
        focus.set('numbers')
        imaginal.modify(operator=operator)
        
    def addition(focus='numbers', imaginal='number_left:no number_right:no operator:!no', numbers='number_left:?nL number_right:?nR visible:yes', operator='operator:plus visible:yes'):
        print "I see the arithmetic problem. It is", nL, "plus", nR
        imaginal.modify(number_left=nL)
        imaginal.modify(number_right=nR)
        focus.set('wait')
        imaginal.set('number_left:no number_right:no operator:no')
        motor.reset_trial()
        
    def multiplication(focus='numbers', imaginal='number_left:no number_right:no operator:!no', numbers='number_left:?nL number_right:?nR visible:yes', operator='operator:multiply visible:yes'):
        print "I see the arithmetic problem. It is", nL, "multiply", nR
        imaginal.modify(number_left=nL)
        imaginal.modify(number_right=nR)
        focus.set('wait')
        imaginal.set('number_left:no number_right:no operator:no')
        motor.reset_trial()
        
    def respond_number(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='visible:no', numbers='number_left:?nL number_right:?nR visible:yes'):
        print "I see the numbers"
        imaginal.modify(number_left=nL)
        imaginal.modify(number_right=nR)
        focus.set('operator')
        
    def addition(focus='operator', imaginal='number_left:?nL number_right:?nR operator:no', numbers='visible:yes', operator='operator:?operator visible:yes'):
    	print "I see the arithmetic problem. It is", nL, operator, nR
    	imaginal.modify(operator=operator)
        focus.set('wait')
        imaginal.set('number_left:no number_right:no operator:no')
    	motor.reset_trial()
        
        
    def respond_both(focus='wait', imaginal='number_left:no number_right:no operator:no', operator='operator:?operator visible:yes',numbers='number_left:?nL number_right:?nR visible:yes'):
        print "I see the arithmetic problem all at once. It is", nL, operator, nR
        imaginal.modify(number_left=nL)
        imaginal.modify(number_right=nR)
        imaginal.modify(operator=operator)
        focus.set('wait')
        imaginal.set('number_left:no number_right:no operator:no')
        motor.reset_trial()                             

	
# 	def retrieve(focus='retrieve'):
# 		print "answer is"
# 		focus.set('stop')


class Referee(ACTR):    
    focus=Buffer()
    motor=MotorModule()

    def init():
        focus.set('new_trial')

    def fixation(focus='new_trial', new_trial='switch:yes'):
        print "pause"
        focus.set('prime')
        motor.trial_switch()
        
    def sign_prime(focus='prime'):    #use counter to record how many problems have been presented
        print "reveal the operator"
        motor.reveal_operator()
        focus.set('numbers_late')
        
    def numbers_late(focus='numbers_late', numbers='visible:no', operator='visible:yes'):
        print "complete the problem with numbers"
        motor.reveal_numbers()
        focus.set('new_trial')
		
    def no_prime(focus='prime'):    #use counter
        print "reveal the problem"
        motor.reveal_operator()
        motor.reveal_numbers()
        focus.set('new_trial')

    def numbers_prime(focus='prime'):    #use counter
        print "reveal the numbers"
        motor.reveal_numbers()
        focus.set('operator_late')
        
    def operator_late(focus='operator_late', numbers='visible:yes', operator='visible:no'):
    	print "complete the problem with the operator"
    	motor.reveal_operator()
    	focus.set('new_trial')

	

Ppt=Participant()
Experimenter=Referee()
env=Arithmetic()
env.agent1=Ppt
env.agent2=Experimenter

#ccm.log_everything(env)

env.run(4)
ccm.finished()
