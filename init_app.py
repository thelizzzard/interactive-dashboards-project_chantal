import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import nilearn
    from nilearn import datasets
    from ipyniivue import NiiVue
    from pathlib import Path
    import nibabel as nib
    from scipy.spatial import KDTree
    import numpy as np

    return KDTree, NiiVue, Path, datasets, mo, nib


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Interactive Dashboard
    """)
    return


@app.cell
def _(datasets):
    fsaverage = datasets.fetch_surf_fsaverage(mesh="fsaverage")
    return (fsaverage,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Plot Glasser Atlas
    """)
    return


@app.cell
def _(mo):
    hemi = mo.ui.radio(
        options=["Left", "Right"],
        value = "Left",
        label="Hemisphere"
    )
    hemi
    return (hemi,)


@app.cell
def _(mo):
    get_label, set_label = mo.state("Hover over brain...")
    return get_label, set_label


@app.cell
def _(KDTree, fsaverage, nib):
    lh_coords, _ = nib.load(fsaverage["infl_left"]).agg_data()
    rh_coords, _ = nib.load(fsaverage["infl_right"]).agg_data()

    lh_tree = KDTree(lh_coords)
    rh_tree = KDTree(rh_coords)


    lh_labels, _, lh_names = nib.freesurfer.read_annot("data/atlases/lh.HCPMMP1.annot")
    rh_labels, _, rh_names = nib.freesurfer.read_annot("data/atlases/rh.HCPMMP1.annot")

    hemisphere = {
        "Left":  {
            "tree":   lh_tree,
            "labels": lh_labels,
            "names":  ["Background"] + [n.decode() if isinstance(n, bytes) else n for n in lh_names[1:]],
        },
        "Right": {
            "tree":   rh_tree,
            "labels": rh_labels,
            "names":  ["Background"] + [n.decode() if isinstance(n, bytes) else n for n in rh_names[1:]],
        },
    }
    return (hemisphere,)


@app.cell
def _(NiiVue, Path, fsaverage, hemi, hemisphere, set_label):
    meshes = []
    if hemi.value in ("Left"):
        meshes.append({
            "path": Path(fsaverage["infl_left"]),
            "layers": [{"path": Path("data/atlases/lh.HCPMMP1.label.gii")}]
        })
    if hemi.value in ("Right"):
        meshes.append({
            "path": Path(fsaverage["infl_right"]),
            "layers": [{"path": Path("data/atlases/rh.HCPMMP1.label.gii")}]
        })

    nv = NiiVue()
    nv.load_meshes(meshes)



    @nv.on_location_change
    def show_location(location):
        coords_str = location["string"]
        try:
            x, y, z = [float(v) for v in coords_str.split("×")]
            h = hemisphere[hemi.value]
            dist, idx = h["tree"].query([x, y, z])
            region = h["names"][h["labels"][idx]]
            set_label(f"{hemi.value} | {region} | vertex: {idx} | {coords_str}")
        except Exception as e:
            set_label(f"Error: {e}")
    
    nv
    return


@app.cell
def _(get_label, mo):

    mo.md(get_label())

    return


if __name__ == "__main__":
    app.run()
