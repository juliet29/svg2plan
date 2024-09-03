from itertools import cycle, islice

from classes.layout import Layout
from problems.classes.problem import Problem
from problems.classes.actions import Action
from problems.classes.sequence import Sequence
from problems.action_generator import ActionGenerator
from problems.modifier import ModifyBlock
from problems.reporter import Reporter

from svg_helpers.helpers import key_from_value


class SequenceRunner():
    def __init__(self, sequence: Sequence, starting_problem: Problem):
        self.problems = sequence.problems
        self.actions = sequence.actions
        self.layout = sequence.layout

        self.curr_problem = starting_problem
        self.LIMIT = 10
        self.limit_counter = 0

    def run(self):
        active_problems = [p for p in self.problems if p.resolved == False]
        while len(active_problems) > 0:
            self.execute_actions()
            
            if self.limit_counter > self.LIMIT:
                print("exceeded max iterations")
                break


    def execute_actions(self):
        print(f"--executing action #{self.limit_counter}")
        print(f"curr problem = {self.curr_problem}")
        self.limit_counter+=1
        self.decide_action()
        self.take_action()
        self.eval_action()
        print(f"curr problem = {self.curr_problem}")


    def decide_action(self):
        assert self.layout.graph
        self.curr_action = ActionGenerator(self.curr_problem, self.layout).generate_action()


    def take_action(self):
        self.mb = ModifyBlock(self.curr_action, self.layout)
        self.mb.run()
        self.temp_layout = self.mb.modified_layout

    def eval_action(self):
        if self.is_problem_resolved() and self.is_helpful_action():
            self.process_action(SUCCESS=True)
        else:
            self.process_action(SUCCESS=False)


    def is_problem_resolved(self):
        self.re = Reporter(self.temp_layout, self.problems)
        self.re.run()
        [test_prob] = [p for p in self.re.problems if p.index == self.curr_problem.index]
        if test_prob.resolved == True:
            print("problem resolved")
            return True
        else:
            print("problem not resolved")
            return False


    def is_helpful_action(self):
            return False
    
    def process_action(self, SUCCESS:bool):
        self.get_next_problem()
        self.curr_action.succesful = SUCCESS
        self.actions.append(self.curr_action)
        if SUCCESS:
            self.layout = self.temp_layout

    def get_next_problem(self):
        indices = [i.index for i in self.problems if i.resolved == False]
        cycled_indices = cycle(indices)
        iterator = islice(cycled_indices, self.curr_problem.index, None)

        next(iterator)
        ix = next(iterator)
        [self.curr_problem] = [p for p in self.problems if p.index == ix]
        


        

    


    


    
    

