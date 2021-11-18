# Personalized_WSD_Dataset
Code used to generate a dataset for personalized WSD.



#Place this file in the directory that you want to store the dataset

#Download entire blog corpus from https://lingcog.blogspot.com/p/datasets.html

#Extract blog corpus to "blogs" directory
unzip blogs.zip

#Python packages required
#nltk

nltk.download('punkt') #This will download the sentence splitter

#Generate dataset
python generateDataset.py 

#Code above will generate the following:

#dataset.txt - One instance per line in the format Sample ID||author||lemma||post ID||Sense||WordNet Synset||text with target tagged with "<b></b>"

Post IDs are not unique, but indicate the post number for a specific author 

#Training/  - A directory that contains files that contain posts from the authors that were not used for annotated instances. One post per line.



