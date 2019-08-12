from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import boto3, botocore, random
import os, secrets, json, string, glob, operator
from PIL import Image
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return os.getcwd()


@app.route("/<user>/<name>")
def serve(user, name):
    return render_template(f"{user}-{name}.html")
        
@app.route("/api/v1/falcon_create_html", methods=["POST"])
def falcon_create_html():
    data = request.json
    print(data)
    #inputs
    input_arr_length, output_arr_length = "", ""
    input_shape = ("", "", "")
    if "image" in data["input"]:
        input_type = data["input"].split(".")[0]
        input_shape = data["input"].split(".")[1].split("x")
    if "noise" in data["input"]:
        input_type = "noise"
    if "text" in data["input"]:
        input_type = "text"
    if "numbers" in data["input"]:
        input_type = "numbers"
        input_arr_length = data["input_arr_length"]
    
    #outputs
    output_shape = ("", "", "")
    output_num_labels = ""
    if "image" in data["output"]:
        output_type = data["output"].split(".")[0]
        output_shape = data["output"].split(".")[1].split("x")
    if "label" in data["output"]:
        output_type = "label"
        output_num_labels = data["output"][1]
    if "text" in data["output"]:
        output_type = "text"
    if "numbers" in data["output"]:
        output_type = "numbers"
        output_arr_length = output_type.split(".")[1]
        
    config = {
        "api_key": str(data["api_key"]),
        "name": str(data["name"]),
        "model_url": str(data["model_url"]),
        "code_url": str(data["code_url"]),
        "input_type": str(input_type),
        "input_channels": str(input_shape[0]),
        "input_width": str(input_shape[1]),
        "input_height": str(input_shape[2]),
        "input_arr_length": input_arr_length,
        "output_type": str(output_type),
        "output_channels": str(output_shape[0]),
        "output_width": str(output_shape[1]),
        "output_height": str(output_shape[2]),
        "output_arr_length": str(output_arr_length),
        "output_num_labels": str(output_num_labels),
        "page_title": data["page_title"],
        "page_subheading": data["page_subheading"],
        "page_info": data["page_info"],
    }

    text_file = open("templates/" + "jtguibas-" + data["name"] + ".html", "w")
    text_file.write(render_template("newtejpal.html", config=config))
    text_file.close()

    return jsonify(config)

@app.route("/api/v1/falcon_incoming_request/<input_type>/<json_string>", methods=["POST"])
def falcon_incoming_request(input_type, json_string):
    s3 = boto3.client("s3", aws_access_key_id="xd", aws_secret_access_key="xd")
    config = json.loads(json_string)
    print("got here")
    if input_type == "image":
        file = request.files["file"]
        extension = os.path.splitext(file.filename)[1]
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print(filename)
        secure_filename(filename+extension)
        file.save(filename + extension)
        print(filename+extension)
        s3.upload_file(filename + extension, "pytorchfalcon", filename + extension)
        url = s3.generate_presigned_url('get_object',
                                Params={
                                    'Bucket': 'pytorchfalcon',
                                    'Key': filename + extension,
                                },                                  
                                ExpiresIn=31536000)

        config["input_url"] = filename + extension
        print(config["input_url"])

    if config["input_type"] == "noise":
        #do nothing
        print("input type was noise... not doing anything")
    if config["input_type"] == "text":
        data = request.data
        config["input_text"] = data["input_text"]
    if config["input_type"] == "numbers":
        data = request.data
        config["input_arr"] = data["input_arr"]
    
    r = render(config)
    print(r.json)
    return r


def render(config):
    s3 = boto3.client("s3", aws_access_key_id="xd", aws_secret_access_key="xd")
    print(config)
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

    print(config["model_url"])
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


    return "nice one"




if __name__ == '__main__':
    app.run(debug=True)
    
