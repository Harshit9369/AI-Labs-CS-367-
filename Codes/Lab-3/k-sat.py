import random

def generate_k_sat(k, m, n):
    if k > n:
        raise ValueError("k cannot be greater than n, since each clause must contain distinct variables.")

    clauses = []
    for _ in range(m):
        variables = random.sample(range(1, n + 1), k)
        clause = []
        for var in variables:
            if random.choice([True, False]):
                clause.append(-var)
            else:
                clause.append(var)
        clauses.append(clause)

    return clauses

def main():
    print("Random k-SAT Problem Generator")
    k = int(input("Enter the number of literals per clause (k): "))
    m = int(input("Enter the number of clauses (m): "))
    n = int(input("Enter the number of variables (n): "))

    try:
        k_sat_problem = generate_k_sat(k, m, n)
        print("\nGenerated k-SAT problem:")
        for clause in k_sat_problem:
            print(clause)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()