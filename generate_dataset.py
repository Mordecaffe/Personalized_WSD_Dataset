import json
import sys
import os

blogs_dir = 'blogs/'

def readInAuthorFiles(curr_author):
    author_blogs = {}
    #print(curr_author)
    author_posts = {}
    curr_file = open(blogs_dir+curr_author+'.xml', encoding="UTF-8", errors="ignore")
    curr_line = curr_file.readline().strip()
    within_post = False
    curr_post = ''
    num_posts= 0
    while(len(curr_line) > 0):

        curr_line = curr_line.strip()

        if(within_post and curr_line != '</post>'):
            curr_post = curr_post + ' ' + curr_line 

        if(curr_line == '<post>'):
            within_post = True
            curr_post = ''
        if(curr_line == '</post>'):
            within_post = False
            
            author_posts[str(num_posts)] = {}
            author_blogs[str(num_posts)] = curr_post.strip()

            num_sents = 0

            num_posts += 1
        curr_line = curr_file.readline()
    return author_blogs

allAuthorsPosts = {}
authorPostsUsed = {}
loadedConversions = json.load(open('conversions.json'))
outFile = open('dataset.txt', 'w')
for currID in loadedConversions:
    currSample = loadedConversions[currID]
    curr_author = currSample['author']
    if(curr_author not in allAuthorsPosts):
        allAuthorsPosts[curr_author] = readInAuthorFiles(curr_author)
        authorPostsUsed[curr_author] = []
    postID = currSample['post_ID']
    authorPostsUsed[curr_author].append(postID)
    author_text = allAuthorsPosts[curr_author][postID]
    start = currSample['start index'] 
    end = currSample['end_index']
    transitions = currSample['transitions']

    #Replace urls
    arr = author_text.split()
    for word in arr:
        word= word.strip('.')
        word= word.strip(',')
        preBr = ''
        postBr = ''
        if(".com" in word or '.org' in word):
            word = word.strip("'s")
            if(word[0] == '('):
                preBr = '('
            if(word[-1] == ')'):
                postBr = ')'
            author_text = author_text.replace(word, preBr+'urlLink'+postBr)
            

    
    for curr_transitions in transitions:
        author_text = author_text.replace(curr_transitions[0], curr_transitions[1])

    startTag = currSample['startTag']
    endTag = currSample['endTag']
    temp = author_text[start:end]

    temp_2 = temp[:startTag] + '<b>' + temp[startTag:]
    targetText = temp_2[:endTag] + '</b>' + temp_2[endTag:]
    targetText = targetText.strip()

    outFile.write(currSample['author'] + '||' + currSample['lemma'] + '||' +postID + '||' + targetText + '\n')

outFile.close()

##Save all posts that did not contain an annotated instance
training_dir = "Training/" 
if not os.path.exists(training_dir):
    os.mkdir(training_dir)

for authorID in authorPostsUsed:
    currFile = open(training_dir+authorID+'.txt', 'wb')
    for postID in allAuthorsPosts[authorID]:
        if(postID not in authorPostsUsed):
            currPostB = allAuthorsPosts[authorID][postID].encode(sys.stdout.encoding, errors='ignore')

            currFile.write(currPostB + '\n'.encode(sys.stdout.encoding, errors='ignore'))
    currFile.close()


