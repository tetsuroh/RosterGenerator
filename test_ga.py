from rg import GA


def main():
    ga = GA()
    ga.evolve_verbose()
    print(ga.log)
    print(ga.entities[0].gene)
    print(ga.answer)

if __name__ == '__main__':
    main()
