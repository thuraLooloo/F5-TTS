import os
import csv
import numpy as np
from datasets import load_dataset
from scipy.io.wavfile import write
from tqdm import tqdm

# Load dataset in streaming mode
ds = load_dataset("Porameht/processed-voice-th-169k", streaming=True)

# Compute total duration for each split
# for split in ["train", "dev", "test"]:
#     total_seconds = sum(
#         len(sample["audio"]["array"]) / sample["audio"]["sampling_rate"]
#         for sample in ds[split]
#     )
#     total_hours = total_seconds / 3600
#     print(f"{split}: {total_hours:.2f} hours")

# Output directories
output_dir = "data/porameht_voice_th169k"
wavs_dir = os.path.join(output_dir, "wavs")
os.makedirs(wavs_dir, exist_ok=True)

# Batch size for processing
BATCH_SIZE = 1000

def process_split(split_name, start_index):
    print(f"Processing split: {split_name}")

    # Metadata file for this split
    metadata_path = os.path.join(output_dir, f"{split_name}_metadata.csv")

    dataset_iter = iter(ds[split_name])
    index = start_index
    total_processed = 0

    with open(metadata_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter="|")
        writer.writerow(["audio_file", "text"])

        while True:
            batch = list(next(dataset_iter, None) for _ in range(BATCH_SIZE))
            batch = [b for b in batch if b is not None]
            if not batch:
                break

            for i, sample in enumerate(batch):
                if "audio" not in sample or "sentence" not in sample:
                    continue  # Skip invalid data

                audio_data = sample["audio"].get("array")
                sampling_rate = sample["audio"].get("sampling_rate")
                text = sample.get("sentence", "").strip()

                if audio_data is None or sampling_rate is None or not text:
                    continue  # Skip empty audio or text

                filename = f"audio_{index + i:06d}.wav"
                file_path = os.path.join(wavs_dir, filename)

                # Save audio file
                write(file_path, sampling_rate, np.array(audio_data))

                # Write to this split's metadata
                writer.writerow([f"wavs/{filename}", text])

            index += len(batch)
            total_processed += len(batch)

            # Print progress
            print(f"Processed {total_processed} samples in {split_name}")

    return index  # Return new index to continue from

# Start index for naming audio files
current_index = 1
for split in ["train", "dev", "test"]:
    current_index = process_split(split, current_index)

print("All splits processed successfully!")