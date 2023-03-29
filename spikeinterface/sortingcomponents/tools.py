import numpy as np


def make_multi_method_doc(methods, ident='    '):
    doc = ""
    
    doc += "method: " + ', '.join(f"'{method.name}'" for method in methods) + '\n'
    doc += ident + "    Method to use.\n"

    for method  in methods:
        doc += "\n"
        doc += ident + f"arguments for method='{method.name}'"
        for line in method.params_doc.splitlines():
            doc += ident + line + '\n'

    return doc


def get_prototype_spike(recording, peaks, job_kwargs, nb_peaks=1000, ms_before=0.5, ms_after=0.5):
    from spikeinterface.sortingcomponents.peak_pipeline import run_peak_pipeline, ExtractSparseWaveforms
    sparse_waveforms = ExtractSparseWaveforms(recording, ms_before=ms_before, ms_after=ms_after, 
                                                      return_output=True, local_radius_um=5)
    nbefore = sparse_waveforms.nbefore
    idx = np.sort(np.random.choice(len(peaks), nb_peaks, replace=False))
    
    waveforms = run_peak_pipeline(recording, peaks[idx], [sparse_waveforms], job_kwargs=job_kwargs)
    prototype =  np.median(waveforms[:, :, 0]/(waveforms[:, nbefore, 0][:, np.newaxis]), axis=0)
    return prototype
