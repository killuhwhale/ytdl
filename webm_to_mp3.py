import os
import subprocess

def convert_webm_to_mp3(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        print(f"Input directory '{input_dir}' not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    webm_files = [f for f in os.listdir(input_dir) if f.endswith(".webm")]

    if not webm_files:
        print(f"No .webm files found in '{input_dir}'.")
        return

    for file_name in webm_files:
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.mp3")

        try:
            # Using ffmpeg to convert .webm to .mp3
            command = [
                "ffmpeg", "-i", input_file, "-vn", "-ab", "192k", "-ar", "44100",
                "-y", output_file
            ]
            subprocess.run(command, check=True)
            print(f"Converted: {file_name} -> {output_file}")

        except subprocess.CalledProcessError as e:
            print(f"Failed to convert {file_name}: {e}")

if __name__ == "__main__":
    # input_dir = input("Enter the path to the directory containing .webm files: ").strip()
    # output_dir = input("Enter the path to save the converted .mp3 files: ").strip()

    input_dir = "/home/killuh/Music/yt_dl/Mac Miller - KIDS"
    output_dir = "/home/killuh/Music/yt_dl/Mac Miller - KIDS"

    convert_webm_to_mp3(input_dir, output_dir)
