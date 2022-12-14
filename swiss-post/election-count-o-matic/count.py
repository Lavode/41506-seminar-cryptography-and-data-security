import sys
import yaml

class Question():
    def __init__(self, title, options):
        self._title = title
        self._options = options
        self._primes = set([option._prime for option in options])

    def __repr__(self):
        out = [f"Question: {self._title}"]
        for option in self._options:
            out.append(f"- {repr(option)}")

        return "\n".join(out)

    def increment(self, prime):
        if prime not in self._primes:
            raise ValueError("Not a valid prime for this question: {}".format(prime))

        for option in self._options:
            if option._prime == prime:
                option._count += 1

class Option():
    def __init__(self, title, prime):
        self._title = title
        self._prime = int(prime)
        self._count = 0

    def __repr__(self):
        return f"{self._title} ({self._prime}): {self._count}"

def main():
    mapping_file = sys.argv[1]
    results_file = sys.argv[2]

    questions = load_questions(mapping_file)
    results = load_results(results_file)

    for prime in results:
        vote_counted = False 
        for q in questions:
            if prime in q._primes:
                q.increment(prime)
                vote_counted = True
                break

        if not vote_counted:
            print(f"ERROR: No clue what to do with prime: {prime}")

    for question in questions:
        print("===========================")
        print(question._title)
        print("")

        outcome = [(o._title, o._count) for o in question._options]
        for (title, count) in sorted(outcome, key=lambda x: x[1], reverse=True):
            print(f"- {title}: {count}")
        
    print("===========================")
        
def load_results(path):
    results = []
    with open(path, 'rb') as f:
        for l in f.readlines():
            primes = l.strip().split(b';')
            results.extend([int(p) for p in primes])

    return results

def load_questions(path):
    with open(path, 'rb') as f:
        data = yaml.load(f, Loader=yaml.loader.SafeLoader)

    questions = []

    for question in data:
        options = [
                Option("Abstain", question['blank_prime'])
        ]

        for option in question['options']:
            options.append(
                    Option(option['title'], option['prime'])
            )

        questions.append(
                Question(question['title'], options)
        )

    return questions


if __name__ == '__main__':
    main()
