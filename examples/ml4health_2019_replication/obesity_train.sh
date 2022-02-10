pip install transformers
pip install ConfigArgParse

wget https://github.com/prasmussen/gdrive/releases/download/2.1.1/gdrive_2.1.1_linux_386.tar.gz
tar -xf gdrive_2.1.1_linux_386.tar.gz
./gdrive info 1LOAGy_LusCZngqShMHnHH19TwbkJlG7K

python ./train_n2c2_2008.py
tar -zcvf bioClinicalBert_results.tar.gz results

./gdrive upload bioClinicalBert_results.tar.gz --parent 1LOAGy_LusCZngqShMHnHH19TwbkJlG7K
