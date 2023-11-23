# ComfyUI-Prompt-Translator-diy
ComfyUI 通过语言模型自动翻译 Prompt 为中文提示词插件。

增加了自定义的字典 .(translations.csv),使翻译后的结果更能贴合stablediffusion模型的语句习惯!

它基于模型 [https://huggingface.co/facebook/mbart-large-50-many-to-one-mmt]


 该翻译插件不需要联网翻译，只需要下载翻译模型就可以正常工作。  

## 安装插件
```
cd ComfyUI/custom_nodes
git clone https://github.com/gaodianzhuo/ComfyUI-Prompt-Translator-diy.git
```

## 语言模型下载
```
pip install -U huggingface_hub hf_transfer
huggingface-cli download --resume-download facebook/mbart-large-50-many-to-one-mmt
```

## 使用效果
![使用效果](ui.png)

## 参考项目
https://github.com/MofaAI/ComfyUI-Prompt-Translator
https://github.com/studyzy/sd-prompt-translator