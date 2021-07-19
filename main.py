import threading
from genetics import GET


def main(mode, number_cores):
    param_settings = []  # DL PS variable
    folder_making = -1
    profile_matching = 0, "Typical Profile Matching"
    epidemic_duration = 1, "Typical Epidemic Duration"
    epidemic_duration_w_sirs = 2, "Epidemic Duration w SIRS"
    print(epidemic_duration_w_sirs)

    # reading parameters
    f = open("params.txt", "r")
    param_settings = [line.split(' ') for line in f.readlines()]
    param_numbers = len(param_settings)
    f.close()
    if mode < 0:
        folder_mode()
    else:
        index = 1
        while index <= param_numbers:
            # setup
            workers = []
            for i in range(index - 1, index + number_cores):
                if i < param_numbers:
                    pass
                    # workers.add(new GET(mode, profileNum, PS.get(i), removedLength, outPath));


def folder_mode():
    pass


import os

if __name__ == '__main__':
    try:
        os.mkdir('results')
    except:
        pass

for i in range(1, 3):
    try:
        os.mkdir('results_length/profile' + str(i))
        # os.mkdir('results/profile' + str(i))
    except:
        pass
    a = GET(i, [0.492493, 0.0061366, 0.0119631, 0.0516803, 0.00828679, 0.00524339, 0.284642, 0.012744, 0.126811],
            'out')
    x = threading.Thread(target=a.run())
    x.start()
