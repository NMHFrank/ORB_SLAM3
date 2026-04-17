import pandas as pd
import argparse
import os

def convert_euroc_to_tum(input_csv, output_file):
    # Load euroc ground truth
    df = pd.read_csv(input_csv)
    df.columns = df.columns.str.strip()

    # Convert timestamp ns -> seconds
    df["#timestamp"] = df["#timestamp"].astype(float)

    # Build TUM format
    tum = pd.DataFrame()
    tum["timestamp"] = df["#timestamp"]
    tum["tx"] = df["p_RS_R_x [m]"]
    tum["ty"] = df["p_RS_R_y [m]"]
    tum["tz"] = df["p_RS_R_z [m]"]

    # Reorder quaternion (w,x,y,z -> x,y,z,w)
    tum["qx"] = df["q_RS_x []"]
    tum["qy"] = df["q_RS_y []"]
    tum["qz"] = df["q_RS_z []"]
    tum["qw"] = df["q_RS_w []"]

    # Save
    tum.to_csv(output_file, sep=" ", header=False, index=False)

    print(f"Saved TUM ground truth to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert EuRoC ground truth CSV to TUM format")
    
    parser.add_argument("input_csv", help="Path to EuRoC data.csv")
    parser.add_argument("-o", "--output", help="Output TUM file (default: groundtruth_tum.txt)")

    args = parser.parse_args()

    output_file = args.output
    if output_file is None:
        output_file = os.path.join(os.path.dirname(args.input_csv), "groundtruth_tum.txt")

    convert_euroc_to_tum(args.input_csv, output_file)