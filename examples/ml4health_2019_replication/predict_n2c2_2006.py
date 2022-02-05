import sys, os, logging, torch
from tqdm import tqdm
import pandas as pd

#appends current directory to sys path allowing data imports.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from data import load_n2c2_2006
from sklearn.metrics import f1_score, precision_score, recall_score
from bert_document_classification.models import SmokerPhenotypingBert


# +
log = logging.getLogger()

def get_name(arr):

    #PAST SMOKER, CURRENT SMOKER, NON-SMOKER, UNKNOWN
    
    if arr[0]==1:
        return "PAST SMOKER"
    elif arr[1]==1:
        return "CURRENT SMOKER"
    elif arr[2]==1:
        return "NON-SMOKER"
    else:
        return "UNKNOWN"


# -

if __name__ == "__main__":

    test = list(load_n2c2_2006(partition='test'))

    print(len(test))

    smoking_bert_phenotyper = SmokerPhenotypingBert(model_name="/workspace/results/run_2022_01_25_20_01_56_dgxa-000/checkpoint_1000", device='cuda') #CPU prediction (change to 'cuda' if possible)
    labels = smoking_bert_phenotyper.labels

    test_documents, test_labels = [],[]
    for _, text, status in test:
        test_documents.append(text)
        label = [0]*len(labels)
        for idx, name in enumerate(labels):
            if name == status:
                label[idx] = 1
        test_labels.append(label)

    correct_labels = torch.FloatTensor(test_labels).transpose(0,1)

    predictions = smoking_bert_phenotyper.predict(test_documents)
    assert correct_labels.shape == predictions.shape

    precisions = []
    recalls = []
    fmeasures = []
    
    df = pd.DataFrame(columns=["Text","Correct","Predicted"])
    for i in tqdm(range(predictions.shape[1])):
        
        c = get_name(test_labels[i])
        
        if predictions[0][i]==1:
            p = "PAST SMOKER"
        elif predictions[1][i]==1:
            p = "CURRENT SMOKER"
        elif predictions[2][i]==1:
            p = "NON-SMOKER"
        else:
            p="UNKNOWN"
            
        t = test_documents[i]
        df.loc[len(df.index)] =  [t, c, p]
    df.to_csv("test.csv")
    
    print("pred",predictions.shape)
    print(predictions)
    
    for label_idx in tqdm(range(predictions.shape[0])):
        correct = correct_labels[label_idx].view(-1).numpy()
        predicted = predictions[label_idx].view(-1).numpy()
        present_f1_score = f1_score(correct, predicted, average='binary', pos_label=1)
        present_precision_score = precision_score(correct, predicted, average='binary', pos_label=1)
        present_recall_score = recall_score(correct, predicted, average='binary', pos_label=1)

        precisions.append(present_precision_score)
        recalls.append(present_recall_score)
        fmeasures.append(present_f1_score)
        
        

    print('Metric\t' + '\t'.join([labels[label_idx] for label_idx in range(predictions.shape[0])]))
    print('Precision\t' + '\t'.join([str(precisions[label_idx]) for label_idx in range(predictions.shape[0])]))
    print('Recall\t' + '\t'.join([str(recalls[label_idx]) for label_idx in range(predictions.shape[0])]))
    print('F1\t' + '\t'.join([str(fmeasures[label_idx]) for label_idx in range(predictions.shape[0])]))
    print('Micro F1\t' + str(f1_score(correct_labels.reshape(-1).numpy(), predictions.reshape(-1).numpy(), average='micro')) )
    print('Macro F1\t' + str(f1_score(correct_labels.reshape(-1).numpy(), predictions.reshape(-1).numpy(), average='macro')) )
