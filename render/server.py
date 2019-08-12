from flask import Flask, request, render_template, jsonify
import os, secrets, json, glob, random, string
import boto3, botocore, collections
import operator
from PIL import Image


app = Flask(__name__)

@app.route("/")
def hello():
    s3 = boto3.client("s3", aws_access_key_id="AKIAJGMBJ3NQ3G4D6X5A", aws_secret_access_key="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")

    unet_config = {
        "input_url": "input_unet.png",
        "model_url": "unet.pt",
        "code_url": "falcon_run_unet.py",
        "input_type": "image",
        "input_channels": "3",
        "input_width": "256",
        "input_height": "256",
        "output_type": "image",
        "output_channels": "1",
        "output_width": "256",
        "output_height": "256",
        "output_num_labels": ""
    }

    resnet18_config = {
        "input_url": "input_resnet18.png",
        "model_url": "resnet18.pt",
        "code_url": "falcon_run_resnet18.py",
        "input_type": "image",
        "input_channels": "3",
        "input_width": "224",
        "input_height": "224",
        "output_type": "label",
        "output_channels": "",
        "output_width": "",
        "output_height": "",
        "output_num_labels": "1000"
    }


    gan_config = {
        "input_url": "",
        "model_url": "generative.pt",
        "code_url": "falcon_run_gan.py",
        "input_type": "noise",
        "input_channels": "",
        "input_width": "",
        "input_height": "",
        "output_type": "image",
        "output_channels": "3",
        "output_width": "776",
        "output_height": "260",
        "output_num_labels": ""
    }

    summary_config = {
        "input_url": "",
        "model_url": "text_sentiment.pt",
        "code_url": "falcon_run_nlp.py",
        "input_type": "text",
        "input_text": "MEMPHIS, Tenn. – Four days ago, Jon Rahm was \
    enduring the season’s worst weather conditions on Sunday at The \
    Open on his way to a closing 75 at Royal Portrush, which \
    considering the wind and the rain was a respectable showing. \
    Thursday’s first round at the WGC-FedEx St. Jude Invitational \
    was another story. With temperatures in the mid-80s and hardly any \
    wind, the Spaniard was 13 strokes better in a flawless round. \
    Thanks to his best putting performance on the PGA Tour, Rahm \
    finished with an 8-under 62 for a three-stroke lead, which \
    was even more impressive considering he’d never played the \
    front nine at TPC Southwind.",
        "input_channels": "",
        "input_width": "",
        "input_height": "",
        "output_type": "text",
        "output_channels": "",
        "output_width": "",
        "output_height": "",
        "output_num_labels": "",
        "extra_url": "dictionary.pt"
    }

    lr_config = {
        "input_url": "",
        "model_url": "linear_regression.pt",
        "code_url": "falcon_run_regression.py",
        "input_type": "numbers",
        "input_channels": "",
        "input_width": "",
        "input_height": "",
        "input_arr": {"x": 4.0},
        "output_type": "numbers",
        "output_channels": "",
        "output_width": "",
        "output_height": "",
        "output_num_labels": ""
    }
    

    config = lr_config

    if config["input_type"] == "image":
        s3.download_file("pytorchfalcon", config["input_url"], config["input_url"])
        img_size = (int(config["input_width"]), int(config["input_height"]))
        imgs = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg") + glob.glob("*.gif")+ glob.glob("*.tiff")
        for img_path in imgs:
            img = Image.open(img_path)
            img.thumbnail(img_size, Image.ANTIALIAS)
            os.system(f'mv {img_path} input.png')
        

    if config["input_type"] == "text":
        input_text = config["input_text"]
        text_file = open("input.txt", "w")
        text_file.write(input_text)
        text_file.close()
        s3.download_file("pytorchfalcon", config["extra_url"], config["extra_url"])


    if config["input_type"] == "noise":
        print("noise appreciated")

    if config["input_type"] == "numbers":
        data = config["input_arr"]
        with open('input.json', 'w') as fp:
            json.dump(data, fp)


    s3.download_file("pytorchfalcon", config["model_url"], "model.pt")
    s3.download_file("pytorchfalcon", config["code_url"], "falcon_run.py")
    terminal_output = os.popen("python3.7 falcon_run.py").read()

    if config["output_type"] == "image":
        unique_url = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        os.system(f"mv result.png {unique_url + '.png'}")
        s3.upload_file(f"{unique_url + '.png'}", "pytorchfalcon", f"{unique_url + '.png'}")
        url = s3.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'pytorchfalcon',
                                    'Key': f"{unique_url + '.png'}",
                                },                                  
                                ExpiresIn=31536000)
        return jsonify({"url": url})

    if config["output_type"] == "label":
        with open('result.json', 'r') as f:
            result = json.load(f)
    
        result = sorted(result.items(), key=operator.itemgetter(1))
        result.reverse()
        result = result[:5]
        return jsonify(result)
    
    if config["output_type"] == "text":
        with open('output.txt', 'r') as file:
            data = file.read().replace('\n', '')
        return jsonifty({"result": data})
    
    if config["output_type"] == "numbers":
        with open('output.json', 'r') as f:
            result = json.load(f)
        return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
    
