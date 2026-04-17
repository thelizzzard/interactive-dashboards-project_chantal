from pathlib import Path
import utils

data_dir = Path("data")

utils.annot_to_label_gii(
    f"{data_dir}/atlases/lh.HCPMMP1.annot", f"{data_dir}/atlases/lh.HCPMMP1.label.gii"
)
utils.annot_to_label_gii(
    f"{data_dir}/atlases/rh.HCPMMP1.annot", f"{data_dir}/atlases/rh.HCPMMP1.label.gii"
)

# Convert CSV files to GIFTI format
utils.csv_to_scalar_gii(
    f"{data_dir}/stats-maps/roi-5_L_V3_acc_05-dims_lh.csv",
    f"{data_dir}/atlases/roi-5_L_V3_acc_05-dims_lh.gii",
)
utils.csv_to_scalar_gii(
    f"{data_dir}/stats-maps/roi-5_L_V3_acc_05-dims_rh.csv",
    f"{data_dir}/atlases/roi-5_L_V3_acc_05-dims_rh.gii",
)
