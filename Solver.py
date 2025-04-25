class Cell:
    # Initiate a new cell
    def __init__(self, value: int, candidates: list[bool], numCandidates: int):
        # Unsolved cells have a value of 0
        self.value = value
        # Candidates is a list with size 9, with each element representing the candidates 1-9 (index + 1)
        self.candidates = candidates.copy()
        self.numCandidates = numCandidates
    # Remove a candidate from a cell
    def removeCandidate(self, candidate: int):
        if self.candidates[candidate-1] == True:
            self.candidates[candidate-1] = False
            self.numCandidates -= 1
        else:
            raise Exception("ERROR: Tried to remove nonexistent candidate.")
    # Solve a cell
    def solveCell(self):
        if self.numCandidates == 1:
            count = 0
            for candidateBool in self.candidates:
                if candidateBool == True:
                    self.value = count + 1
                    break
                count += 1
            if self.value == 0:
                raise Exception("ERROR: numCandidates is 1, but no candidates found")
        elif self.numCandidates > 1:
            raise Exception("ERROR: Tried to solve a cell with multiple candidates.")
        else:
            raise Exception("ERROR: Cell has less than 1 candidate.")