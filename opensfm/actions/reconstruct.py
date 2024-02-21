from opensfm import io
from opensfm import reconstruction
from opensfm.dataset_base import DataSetBase
import os

def run_dataset(data: DataSetBase, algorithm: reconstruction.ReconstructionAlgorithm) -> None:
    """Compute the SfM reconstruction."""

    tracks_manager = data.load_tracks_manager()

    if algorithm == reconstruction.ReconstructionAlgorithm.INCREMENTAL:
        report, reconstructions = reconstruction.incremental_reconstruction(
            data, tracks_manager
        )
    elif algorithm == reconstruction.ReconstructionAlgorithm.TRIANGULATION:
        report, reconstructions = reconstruction.triangulation_reconstruction(
            data, tracks_manager
        )
    else:
        raise RuntimeError(f"Unsupported algorithm for reconstruction {algorithm}")

    data.save_reconstruction(reconstructions)
    data.save_report(io.json_dumps(report), "reconstruction.json")


    ### 添加置信度
    tracks_manager = data.load_tracks_manager()
    initial_points_count = tracks_manager.num_tracks()
    reconstructed_points_count = 0.0
    for rec in reconstructions:
        if len(rec.points) > 0:
            reconstructed_points_count += len(rec.points)

    # with open(os.path.join(data.data_path, "confidence.txt"), "w") as f:
    #     if not os.path.exists(os.path.join(data.data_path, "current_gps.csv")):
    #         confidence = 0.
    #     else:
    #         confidence = reconstructed_points_count / initial_points_count
    #     f.write(io.json_dumps(confidence))
            
    with open(os.path.join(data.data_path, "confidence.txt"), "w") as f:
        confidence = reconstructed_points_count / initial_points_count
        f.write(io.json_dumps(confidence))

