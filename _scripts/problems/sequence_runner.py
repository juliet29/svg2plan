from itertools import cycle, islice

from svg_helpers.layout import Layout
from problems.classes.problem import Problem
from problems.classes.actions import Action
from problems.classes.sequence import Sequence
from problems.action_generator import ActionGenerator
from problems.modifier import BlockModifier
from problems.reporter import Reporter
from problems.fix_logger import fix_logger

from svg_helpers.helpers import key_from_value


class SequenceRunner:
    def __init__(self, sequence: Sequence, starting_problem: Problem):
        self.problems = sequence.problems
        self.actions = sequence.actions
        self.layout = sequence.layout

        self.curr_problem = starting_problem
        self.LIMIT = 10
        self.limit_counter = 0
        self.are_problems_solved = False

    def run(self):
        active_problems = [p for p in self.problems if p.resolved == False]
        while len(active_problems) > 0:
            self.execute_actions()
            if self.are_problems_solved:
                fix_logger.info("no more problems!")
                break

            if self.limit_counter > self.LIMIT:
                fix_logger.warning("exceeded max iterations")
                break

    def execute_actions(self):
        if self.are_problems_solved:
            fix_logger.info("no more problems!")
            return
        fix_logger.debug(f"--iteration #{self.limit_counter+1}")
        fix_logger.debug(f"curr problem = {self.curr_problem}")
        self.limit_counter += 1
        self.decide_action()
        self.take_action()
        self.eval_action()
        if self.are_problems_solved:
            fix_logger.info("no more problems!")
            return
        fix_logger.debug(f"next problem = {self.curr_problem}")

    def decide_action(self):
        assert self.layout.graph
        self.ag = ActionGenerator(
            self.curr_problem, self.layout
        )
        self.ag.handle_case()
        self.curr_action = self.ag.action
        fix_logger.debug(self.curr_action)

    def take_action(self):
        assert self.curr_action
        self.mb = BlockModifier(self.curr_action, self.layout)
        self.mb.run()
        self.temp_layout = self.mb.modified_layout

    def eval_action(self):
        if self.is_problem_resolved():
            self.process_action(is_successful_action=True)
        else:
            self.process_action(is_successful_action=False)

    def is_problem_resolved(self):
        self.re = Reporter(self.temp_layout, self.problems)
        self.re.run()
        [test_prob] = [
            p for p in self.re.problems if p.index == self.curr_problem.index
        ]
        if test_prob.resolved == True:
            fix_logger.debug("problem resolved")
            return True
        else:
            fix_logger.warning("problem not resolved")
            return False


    def process_action(self, is_successful_action: bool):
        assert self.curr_action
        if is_successful_action:
            self.layout = self.temp_layout
            self.problems = self.re.problems
        self.get_next_problem()
        self.curr_action.succesful = is_successful_action
        self.actions.append(self.curr_action)

    def get_next_problem(self):
        indices = [i.index for i in self.problems if i.resolved == False]
        fix_logger.debug(f"indices: {indices}")

        if len(indices) == 0:
            self.are_problems_solved = True
            return

        if len(indices) == 1:
            fix_logger.debug(f"there is just one index and it is {indices}")
            [self.curr_problem] = [p for p in self.problems if p.index == indices[0]]
            return

        cycled_indices = cycle(indices)
        iterator = islice(cycled_indices, self.curr_problem.index, None)

        next(iterator)
        ix = next(iterator)
        [self.curr_problem] = [p for p in self.problems if p.index == ix]


# TODO make it easier to get problems by index
