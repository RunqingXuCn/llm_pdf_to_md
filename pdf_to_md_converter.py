from dotenv import load_dotenv
from pdfdeal import Doc2X
from pdfdeal.file_tools import get_files, unzips, auto_split_mds, mds_replace_imgs
from pdfdeal.FileTools.Img.Ali_OSS import Ali_OSS
import os

load_dotenv()

Client = Doc2X()
current_dir = os.getcwd()
input_path = os.path.join(current_dir, "Files")
output_path = os.path.join(current_dir, "Output")

def print_result(success, failed, flag):
    print(success, failed, flag)
    if not flag:
        print(f"Success with result:\n{success}")
    else:
        exit(f"Failed with error:\n{failed}")
    return


# PDF to MD
out_type = "md_dollar"
file_list, rename_list = get_files(path=input_path, mode="pdf", out=out_type)
success, failed, flag = Client.pdf2file(
    pdf_file=file_list,
    output_path=output_path,
    output_names=rename_list,
    output_format=out_type,
)
print("Start convert all PDFs to MDs")
print_result(success, failed, flag)

# unzip all MD
zips = []
for file in success:
    if file.endswith(".zip"):
        zips.append(file)
success, failed, flag = unzips(zip_paths=zips)
print("Start unzip all MDs")
print_result(success, failed, flag)

# add rag split flag to all MDs
success, failed, flag = auto_split_mds(mdpath=output_path, out_type="replace")
print("Start add rag split flag to all MDs")
print_result(success, failed, flag)

# replace image url to online url
ossupload = Ali_OSS(
    OSS_ACCESS_KEY_ID=os.environ.get("OSS_ACCESS_KEY_ID"),
    OSS_ACCESS_KEY_SECRET=os.environ.get("OSS_ACCESS_KEY_SECRET"),
    Endpoint=os.environ.get("Endpoint"),
    Bucket=os.environ.get("Bucket"),
)

success, failed, flag = mds_replace_imgs(
    path=output_path,
    replace=ossupload,
    threads=5,
)
print("Start replace image url to online url")
print_result(success, failed, flag)