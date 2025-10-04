class NeedlemanWunsch:
    def __init__(self, match=1, mismatch=-1, gap=-1):
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def align(self, s1: str, s2: str):
        m, n = len(s1), len(s2)

        # Step 1: Create DP score matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        # Traceback matrix to remember the direction (diag, up, left)
        tb = [[None] * (n + 1) for _ in range(m + 1)]

        # Step 2: Initialize first row and column (gap penalties)
        for i in range(1, m + 1):
            dp[i][0] = i * self.gap
            tb[i][0] = "up"  # came from above (gap in s2)
        for j in range(1, n + 1):
            dp[0][j] = j * self.gap
            tb[0][j] = "left"  # came from left (gap in s1)

        # Step 3: Fill in DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # score if diagonal (match/mismatch)
                diag = dp[i - 1][j - 1] + (
                    self.match if s1[i - 1] == s2[j - 1] else self.mismatch
                )
                # score if moving up (gap in s2)
                up = dp[i - 1][j] + self.gap
                # score if moving left (gap in s1)
                left = dp[i][j - 1] + self.gap

                # choose best score
                dp[i][j] = max(diag, up, left)

                # record direction
                if dp[i][j] == diag:
                    tb[i][j] = "diag"
                elif dp[i][j] == up:
                    tb[i][j] = "up"
                else:
                    tb[i][j] = "left"

        # Step 4: Traceback to build alignment
        aligned1, aligned2 = [], []
        i, j = m, n
        matches = mismatches = gaps = 0

        while i > 0 or j > 0:
            if tb[i][j] == "diag":
                # Both characters aligned
                aligned1.append(s1[i - 1])
                aligned2.append(s2[j - 1])
                if s1[i - 1] == s2[j - 1]:
                    matches += 1
                else:
                    mismatches += 1
                i -= 1
                j -= 1
            elif tb[i][j] == "up":
                aligned1.append(s1[i - 1])
                aligned2.append("-")
                gaps += 1
                i -= 1
            else:  # "left"
                aligned1.append("-")
                aligned2.append(s2[j - 1])
                j -= 1

        # Reverse the aligned strings because we traced back
        return (
            "".join(reversed(aligned1)),
            "".join(reversed(aligned2)),
            matches,
            mismatches,
            gaps,
        )


# MAIN EXECUTION BLOCK
if __name__ == "__main__":
    tests = [
        ["CRANE", "RAIN"],
        ["CYCLE", "BICYCLE"],
        ["ASTRONOMY", "GASTRONOMY"],
        ["INTENTION", "EXECUTION"],
        ["AGGTAB", "GXTXAYB"],
        ["GATTACA", "GCATGCU"],
        ["DELICIOUS", "RELIGIOUS"],
    ]

    aligner = NeedlemanWunsch(match=1, mismatch=-3, gap=-1)

    for s1, s2 in tests:
        a1, a2, matches, mismatches, gaps = aligner.align(s1, s2)
        print(f"{s1:10} --> |{a1}| matches: {matches}, mismatches: {mismatches}")
        print(f"{s2:10} --> |{a2}| gaps: {gaps}\n")
