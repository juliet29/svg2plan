from copy import deepcopy

from classes.layout import Layout
from problems.classes.problem import Problem, ProblemType
from problems.classes.problems_base import ProblemsBase

from problem_types.overlap.identifier import OverlapIdentifier
from problem_types.hole.identifier import HoleIdentifier
from problem_types.side_hole.identifier import SideHoleIdentifier



class Reporter():
    def __init__(
        self,
        layout: Layout,
        existing_problems: list[Problem] = [],
    ) -> None:
        self.layout = deepcopy(layout)
        self.problems: list[Problem] = deepcopy(existing_problems)

        self.index = len(self.problems)
        self.candidates: list[Problem] = []
        self.temporary: list[Problem] = []

    def run(self):
        self.reset_exisiting_problems()
        self.find_problems()
        self.compare_with_existing()
        self.check_existing_for_resolution()
        self.merge_new_and_existing_problems()
        self.summarize()

    def reset_exisiting_problems(self):
        for p in self.problems:
            p.matched = False

    def find_problems(self):
        for identifier in [OverlapIdentifier, HoleIdentifier, SideHoleIdentifier]:
            self.identifier = identifier(self.layout)
            self.identifier.report_problems()
            self.candidates.extend(self.identifier.problems)

    def compare_with_existing(self):
        for candidate in self.candidates:
            self.candidate_problem = candidate
            # print(f"Checking {self.candidate_problem}")
            for p in self.problems:
                if candidate == p:
                    # print(f"{self.candidate_problem} was matched")
                    p.matched = True
                    return
            # print(f"I was not matched {self.candidate_problem}")
            self.add_problem_and_update_index()


    def add_problem_and_update_index(self):
        self.index += 1
        self.candidate_problem.index = self.index
        self.temporary.append(self.candidate_problem)

    def check_existing_for_resolution(self):
        for p in self.problems:
            if p.matched == False:
                p.resolved = True

    def merge_new_and_existing_problems(self):
        self.problems.extend(self.temporary)




    def summarize(self):
        overlap = 0
        hole = 0
        side_hole = 0
        for p in self.problems:
            # print(f"summarizing for {p}")
            if p.resolved == False:
                match p.problem_type:
                    case ProblemType.OVERLAP:
                        overlap+=1
                    case ProblemType.HOLE:
                        hole+=1
                    case ProblemType.SIDE_HOLE:
                        side_hole+=1
                    
        print(f"Overlaps: {overlap}. Holes: {hole}. Sideholes: {side_hole}")
        
