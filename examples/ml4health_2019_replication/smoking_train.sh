pip install transformers
pip install ConfigArgParse

wget https://github.com/prasmussen/gdrive/releases/download/2.1.1/gdrive_2.1.1_linux_386.tar.gz
tar -xf gdrive_2.1.1_linux_386.tar.gz

./gdrive info 1cjtB74Z4LGLDSUsv_uFzEUWq2j5UqQvj

# +
python ./train_n2c2_2006.py
tar -zcvf ./bert_results.tar.gz ./results

./gdrive upload ./bert_results.tar.gz --parent 1cjtB74Z4LGLDSUsv_uFzEUWq2j5UqQvj
