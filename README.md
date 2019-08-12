This is supporting code for our submission to PyTorch's Summer Hackathon at Facebook in Menlo Park, California. 
Made By:
- [Peter Li](petersli.com)
- [John Guibas](github.com/jtguibas)
- [Tejpal Virdi](github.com/tejpalv)

# PyTorch Falcon

Deploy a browser demo of your PyTorch model in seconds. 
**You focus on the research, we'll handle the rest.** 
Frontend? Backend? We got it.

### Deploy in Seconds

Falcon uses a small config to get info about your model, I/O,  runtime specifications,  and anything you'd like displayed with your demo.

` $ falcon -d config.json `
```
[Falcon] Uploading Model...  
100% |########################|  
[Falcon] Uploading Code...  
100% |########################|  
[Falcon] Your deployment is available at: 
getfalcon.ml/jtguibas/unet
```

### PyTorch Falcon Features
- One-line deployment of a browser demo
- Automatic modern UI generation on the web (based on your model's specifications)
- All the flexibility of a normal .py file -- customize how your model runs on the web (preprocessing, augmentation, etc.)
- Purely python: no HTML, CSS, JS, or backend development needed

### Getting Started
Falcon takes in a config file of the following form:
```
// config.json
{
"api_key": "aQnZfx",
"name": "unet",
"model_path": "unet.pt",
"code_path": "falcon_run_unet.py",
"input": "image.3x256x256",
"output": "image.1x256x256
}
```

`"model_path"`:
Your serialized PyTorch model. Consider using`torch.save()`.

`"code_path"`:
Your python script that runs the model. See **Falcon Script Standards for Outputs.**

`"input"`: input type and dimensions

`"output"`: output type and dimensions

### Falcon Script Standards for Outputs

For models that output images, use `torchvision.utils.save_image()` and save as `result.png`

For models that output text, write to `output.txt`

For models that output numeric data or tensors, write to `output.json`

### Inspiration and Potential Impact

- Researchers in universities are incentivized to publish, and the public usage of their work isn’t considered very often. This gap between research and practice is slowing the growth of AI tremendously 
- We believe the solution starts with #DemoCulture. Just as how we expect most papers to have a Github, we should also expect every paper to have an online demo
-- Demos allow other researchers to validate the results of a paper 
-- Demos make research more accessible and easy to understand by the general public (ex. Nvidia, OpenAI) 
-- Demos extend the impact of the original paper by allowing more people to use the application 
- Ex: Diagnosis networks that are actually useful in medicine but are rarely actually implemented 
- Currently, demos are difficult to make; hosting your own backend is inefficient and time-consuming

### What We Learned
- Gained experience with different tools, frameworks, and libraries (Jinja, AWS, PyTorch, etc.) 
- Making a multi-module system (cloud storage, server, database, user) and learning how to connect it cleanly 
- Learned a lot of common practices in PyTorch and general software development

### What's Next for PyTorch Falcon
- Scaling to handle more users, bigger models, and more input/output types 
- Easy customization of the webpage for the user (perhaps a collection of frontend templates) 
- Increased protection to prevent spamming on our server 
- More features for the user of the demos, such as easily editing the model and providing feedback for the researcher. 
- Creating a collection of demos (ex. a machine learning playground)

### Accomplishments That We’re Proud Of 
- It works! 
- This is the most complex system we’ve built, and we’re surprised we got all the different parts to work together properly in 24 hours 
- We have no software engineering experience and most of the tools we worked with we hadn’t used before 
- We’ve had problems developing demos for projects in the past, and now we can actually use our own product to make those demos

### Challenges we ran into 
- Since our product is meant to serve a large variety of projects, there were times when we had to rethink our approach to incorporate as many cases as possible 
- We had never used Jinja or AWS Lamda before; some of the models were too big for Lambda to support 
- We had to divide up the different components of the system when working on it, and sometimes the way we implemented one module was not compatible with another

### Essay

Last summer, we built a MRI brain tumor segmentation network that achieved leading accuracies with limited training data. We were extremely excited to share our results with the world and see our work in action, but we were disappointed to learn how few resources there are for sharing your ML models with the world. 

We tried to build a demo page, but hosting our own backend and creating a web application was inefficient and time consuming

These days, researchers are incentivized simply to publish projects in journals and conferences, then move on to the next idea. There is a growing gap between the progress happening in research labs and the work being harnessed in practice. This bottleneck is slowing the growth of AI tremendously.

We understand, though. Researchers are busy, and developing and hosting a demo does not seem to have a tangible benefit. In addition, many practitioners these days aren’t always fluent enough in HTML, CSS, and JavaScript to create a demo easily. 

We think there is great potential in spreading the popularity of demos. First off, they allow other researchers to validate the results of a paper. It’s super inefficient to have to download a huge model and weights just to run one image through it to test it. 

Secondly, demos make research more accessible and easy to understand by the general public; we see this with companies like Nvidia and OpenAI whose demos garner a lot of attention. By showing more people your idea, you extend the impact of the original paper. It sparks new ideas in the public and can make your paper far more impactful to society. 

A machine learning model that never leaves its written form in arXiv is a lot of wasted potential. So just as how researchers have started to expect most papers to have their own Github, we think every paper should also be expected to have its own online demo. |
