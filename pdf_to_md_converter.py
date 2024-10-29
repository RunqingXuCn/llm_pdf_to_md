from dotenv import load_dotenv
from pdfdeal import Doc2X
from pdfdeal.file_tools import get_files, unzips, auto_split_mds, md_replace_imgs, gen_folder_list
import os, oss2, logging

load_dotenv()

Client = Doc2X()
current_dir = os.getcwd()
input_path = os.path.join(current_dir, "Files")
output_path = os.path.join(current_dir, "Output")

def print_result(success, failed, flag):
    if not flag:
        print(f"Success with result:\n{success}")
    else:
        exit(f"Failed with error:\n{failed}")
    return

class OSS:
    def __init__(self, OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, Endpoint, Bucket):
        """Initialize the OSS client.

        Args:
            OSS_ACCESS_KEY_ID (str): The access key ID for Aliyun OSS.
            OSS_ACCESS_KEY_SECRET (str): The access key secret for Aliyun OSS.
            Endpoint (str): The endpoint for Aliyun OSS.
            Bucket (str): The name of the bucket to upload to.
        """
        self.auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(self.auth, Endpoint, Bucket)

    def upload_file(self, local_file_path, remote_file_path):
        """Upload a file to Aliyun OSS.

        Args:
            local_file_path (str): The path of the local file to upload.
            remote_file_path (str): The path of the remote file to upload to.

        Returns:
            tuple: A tuple containing the URL of the uploaded file and a boolean indicating whether the upload was successful.
        """
        try:
            headers = {'Cache-Control': 'max-age=315360000'}
            self.bucket.put_object_from_file(remote_file_path, local_file_path, headers=headers)
            # * Default think the bucket is public read
            return (
                f"https://{self.bucket.bucket_name}.{self.bucket.endpoint.split('://')[1]}/{remote_file_path}",
                True,
            )
        except Exception as e:
            logging.error(f"Error to upload the file: {local_file_path}, {e}")
            return e, False


def Ali_OSS(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, Endpoint, Bucket) -> callable:
    """Initialize the OSS client and return a callable function to upload files.

    Args:
        OSS_ACCESS_KEY_ID (str): The access key ID for Aliyun OSS.
        OSS_ACCESS_KEY_SECRET (str): The access key secret for Aliyun OSS.
        Endpoint (str): The endpoint for Aliyun OSS.
        Bucket (str): The name of the bucket to upload to.

    Returns:
        callable: The upload_file method of the OSS client.
    """
    ali_oss = OSS(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, Endpoint, Bucket)
    return ali_oss.upload_file

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

for file_path in gen_folder_list(output_path, "md", True):
    flag = md_replace_imgs(
        mdfile=file_path,
        replace=ossupload,
        threads=5,
    )
# success, failed, flag = mds_replace_imgs(
#     path=output_path,
#     replace=ossupload,
#     threads=5,
# )
    print("Start replace image url to online url")
    print(flag)