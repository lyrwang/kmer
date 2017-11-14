from feature_scaling import scale_to_range
from feature_selection import recursive_feature_elimination
from models import neural_network_validation, support_vector_machine_validation
from data import get_kmer_us_uk_mixed, get_kmer_us_uk_split
from data import get_genome_region_us_uk_mixed, get_genome_region_us_uk_split
from sklearn.feature_selection import chi2, f_classif
import numpy as np
from run import run
from multiprocessing import Process
from sklearn.svm import SVC

def get_data(model, data, model_args, name):
    print name
    path = '/home/rboothman/Data/svm_parameters/C/'
    c = model_args[1]
    d = run(model=model,
            data=data,
            model_args=model_args)
    with open(path+name+'.txt', 'a') as f:
        f.write('%.15f,%f\n' % (c,d))

def test_selection_method(method):
    c_vals = list(np.logspace(-25,25,51,base=2))
    for c in c_vals:
        args = ('linear', c)
        print "C: ", c
        # p = Process(target=get_data,
        #             args=(neural_network_validation,
        #                   get_genome_region_us_uk_split,
        #                   args,
        #                   'nn_split_genome_region'))
        # p.start()
        # p.join()
        #
        # p = Process(target=get_data,
        #             args=(neural_network_validation,
        #                    get_genome_region_us_uk_mixed,
        #                    args,
        #                    'nn_mixed_genome_region'))
        # p.start()
        # p.join()
        #
        # p = Process(target=get_data,
        #             args=(neural_network_validation,
        #                   get_kmer_us_uk_mixed,
        #                   args,
        #                   'nn_mixed_kmer'))
        # p.start()
        # p.join()
        #
        # p = Process(target=get_data,
        #             args=(neural_network_validation,
        #                   get_kmer_us_uk_split,
        #                   args,
        #                   'nn_split_kmer'))
        # p.start()
        # p.join()

        p = Process(target=get_data,
                    args=(support_vector_machine_validation,
                          get_kmer_us_uk_split,
                          args,
                          'svm_split_kmer'))
        p.start()
        p.join()

        p = Process(target=get_data,
                    args=(support_vector_machine_validation,
                          get_kmer_us_uk_mixed,
                          args,
                          'svm_mixed_kmer'))
        p.start()
        p.join()

        p = Process(target=get_data,
                    args=(support_vector_machine_validation,
                          get_genome_region_us_uk_mixed,
                          args,
                          'svm_mixed_genome_region'))
        p.start()
        p.join()

        p = Process(target=get_data,
                    args=(support_vector_machine_validation,
                          get_genome_region_us_uk_split,
                          args,
                          'svm_split_genome_region'))
        p.start()
        p.join()

if __name__ == "__main__":
    test_selection_method(recursive_feature_elimination)
