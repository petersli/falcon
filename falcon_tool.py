import sys, requests, json, boto3, random, string, os, progressbar

def upload_progress(chunk):
    up_progress.update(up_progress.currval + chunk)

# > falcon -d config.json

action = sys.argv[1]
config = sys.argv[2]

with open(config, 'r') as f:
    config = json.load(f)



s3 = boto3.client("s3", aws_access_key_id="AKIAJGMBJ3NQ3G4D6X5A", aws_secret_access_key="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")

unique_url = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

name = config["name"]

print("[Falcon 🚀] Successful Connection To Falcon Service")
print(f'[Falcon 🚀]\n NAME: {name}\n MODEL_URL: {config["model_url"]}\n CODE_URL: {config["code_url"]}\n INPUT: {config["input"]}\n OUTPUT: {config["output"]}')
print("[Falcon 🚀] Uploading Model...")
statinfo = os.stat(config['model_url'])
up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
up_progress.start()
s3.upload_file(config['model_url'], "pytorchfalcon", name + "_" + unique_url + '.pt', Callback=upload_progress)
config['model_url'] = name + "_" + unique_url + '.pt'
up_progress.finish()

print("[Falcon 🚀] Uploading Code...")
statinfo = os.stat(config['code_url'])
up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
up_progress.start()
s3.upload_file(config['code_url'], "pytorchfalcon", name + "_" + unique_url + '.py', Callback=upload_progress)
config['code_url'] = name + "_" + unique_url + '.py'
up_progress.finish()

print(f"Your deployment is available at getfalcon.ml/jtguibas/{name}. Enjoy!!!")


print(config["model_url"], config["code_url"])


if (action == '-d'):
    r = requests.post('http://localhost:5000/api/v1/falcon_create_html', json=config)
