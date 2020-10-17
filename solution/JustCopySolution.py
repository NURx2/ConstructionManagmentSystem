from solution.Solution import Solution

class JustCopySolution(Solution):
    def solve(self, tasks): # we need to copy tasks (to make previous tasks immutable)
        result = []
        for task in tasks:
            result.append(task.copy())
        return result

    def name(self):
        return "JustCopySolution"
