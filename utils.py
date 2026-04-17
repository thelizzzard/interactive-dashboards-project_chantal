import numpy as np
import nibabel as nib
import pandas as pd


def annot_to_label_gii(annot_path, out_path):
    labels, ctab, names = nib.freesurfer.read_annot(annot_path)

    label_table = nib.gifti.GiftiLabelTable()
    for i, (name, color) in enumerate(zip(names, ctab)):
        gl = nib.gifti.GiftiLabel(
            key=i,
            red=color[0] / 255,
            green=color[1] / 255,
            blue=color[2] / 255,
            alpha=1.0,
        )
        gl.label = name.decode() if isinstance(name, bytes) else name
        label_table.labels.append(gl)

    arr = nib.gifti.GiftiDataArray(
        data=labels.astype(np.int32),
        intent=nib.nifti1.intent_codes["NIFTI_INTENT_LABEL"],
        datatype="NIFTI_TYPE_INT32",
    )
    img = nib.gifti.GiftiImage(darrays=[arr], labeltable=label_table)
    nib.save(img, out_path)


def csv_to_scalar_gii(csv_path, out_path):
    """Convert a CSV file with vertex values to a GIFTI scalar file."""
    df = pd.read_csv(csv_path, index_col=0)

    # Get the values as a 1D array
    data = df.iloc[:, 0].values.astype(np.float32)

    # Create a GIFTI data array with NIFTI_INTENT_ESTIMATE intent for scalar data
    arr = nib.gifti.GiftiDataArray(
        data=data,
        intent=nib.nifti1.intent_codes["NIFTI_INTENT_ESTIMATE"],
        datatype="NIFTI_TYPE_FLOAT32",
    )

    # Create and save the GIFTI image
    img = nib.gifti.GiftiImage(darrays=[arr])
    nib.save(img, out_path)
