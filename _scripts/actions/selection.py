from typing import List
from fixes.reporter import Reporter
from actions.interfaces import ResultsLog
from actions.operations import (
    study_many_problems,
)
from visuals.plots import make_subplot_for_all_probs
from visuals.plotter import plot_general


def sort_results_by_score(results: List[ResultsLog]):
    return sorted(results, key=lambda x: x.score)


def get_next_best_result(
    current_result: ResultsLog, sorted_results: List[ResultsLog]
) -> ResultsLog:
    ix = sorted_results.index(current_result) + 1
    try:
        return sorted_results[ix]
    except IndexError:
        raise Exception("No more results!")


def are_domains_equal(doms_a, doms_b):
    try:
        assert len(doms_a) == len(doms_b)
        for key in doms_a:
            try:
                assert doms_a[key] == doms_b[key]
            except:
                return False
    except AssertionError:
        print("Unequal len")
        return False
    return True


def is_domain_in_history(curr_dom, hist: list):
    for h in hist:
        if are_domains_equal(h, curr_dom):
            return True


class Cook:
    def __init__(self, init_report: Reporter) -> None:
        self.res_hist = []
        self.bl_hist = []
        self.history = [init_report.layout.domains]
        self.results = study_many_problems(init_report.layout, init_report.problems)

        self.count = 0
        print(f"initializing.. {self.count}")
        self.handle()

    def run_again(self):
        self.results = study_many_problems(self.bl.layout, self.bl.problems)
        if self.results:
            self.handle()
        else:
            print("No more results!")

    def handle(self):
        self.count += 1
        print(f"running again -> {self.count}")

        self.sorted_res = sort_results_by_score(self.results)
        self.bl = self.sorted_res[0]

        while is_domain_in_history(self.bl.layout.domains, self.history):
            self.bl = get_next_best_result(self.bl, self.sorted_res)
            print(f"skipping bc prev domains are in history")

        print(f"next best layout {self.bl.short_message()}")
        # print(f"problem being studied: -> {self.bl.problem_being_addressed}")

        self.res_hist.append(self.sorted_res)
        self.history.append(self.bl.layout.domains)
        self.bl_hist.append(self.bl)

    def plot(self, ix):
        plot_general(self.history[ix], f"iteration {ix}")

    def plot_all(self):
        make_subplot_for_all_probs(self.history[0], self.bl_hist)

    def show_results_at_ix(self, ix):
        [i.short_message() for i in self.res_hist[ix]]


# report = run_new_layout()
# c = Cook(report)
# c.run_again()
# make_subplot_for_all_probs(c.history[0], c.bl_hist)
