import torch, os, requests

os.environ['NO_PROXY'] = '127.0.0.1'

def deploy(model, code, name, input, output):
    
    torch.save(model, f"{api_key}.pt")
    model_url = upload_file(f"{api_key}.pt")
    code_url = upload_file("resetdb.py")
    os.system(f"rm {api_key}.pt")

    r = requests.post("http://127.0.0.1:5000/api/v1/falcon_submit", json={
        "model_url": model_url,
        "code_url": code_url,
        "id": name,
        "api_key": "aeab0c7c51",
        "input": input,
        "output": output
    })

    print(r.content)

def upload_file(filename):
    upload_cmd = "aws s3 cp " + filename + " s3://pytorch-falcon/" + filename
    presign_cmd = "aws s3 presign s3://pytorch-falcon/" + filename + " --expires-in 518400"

    res = os.popen(upload_cmd).read()
    print(res)

    res = os.popen(presign_cmd).read()

    return res.split("\n")[0]