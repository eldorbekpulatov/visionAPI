import io, os, sys, collections


def intify(lis):
    """ Returns the int values of a list of string numerals.

        Params:
            lis     :   list of numeral strings     <list>
    """
    n_lis=[]
    for each in lis:
        n_lis.append(int(each))
    return n_lis


def BBparser(uni):
    """ Returns a list of ints from a bounding box unicode seperated by commas.
        
        Params:
            uni     : unicode containing 4 numerals seperated by commas     <uni>
    """
    return intify(uni.split(','))


def getCorners(bounds):
    """ Returns the corner coordinates from a parsed list of Azure bounds.
        T-L  --------------  T-R
         |                    |      
         |                    |
        B-L  --------------  B-R

        ORDERING: T-L, B_R, T_R, B_L

        Params:
            bounds  : 4 numerals             <list/tuple>
    """
    bounds=BBparser(bounds)
    t_l=(int(bounds[0]),int(bounds[1]))
    b_r=(int(bounds[0])+int(bounds[2]), int(bounds[1])+(int(bounds[3])))
    t_r=(int(bounds[0])+int(bounds[2]), int(bounds[1]))
    b_l=(int(bounds[0]), int(bounds[1])+int(bounds[3]))
    return [t_l, t_r, b_l, b_r]


def getCenter(bounds):
    """ Returns the center coordinate given the bounds
        
        Params:
            try: Google
                bounds  : BoundyingPoly         <google.cloud.vision_v1.types.BoundingPoly>               
            except: Microsoft
                bounds  : 4 numerals            <list/tuple>
    """
    try:
        xmid=(bounds.vertices[0].x)+(bounds.vertices[1].x)/2
        ymid=(bounds.vertices[0].y)+(bounds.vertices[2].y)/2
    except:
        bounds=BBparser(bounds)
        xmid=int(bounds[0])+int(bounds[2])/2
        ymid=int(bounds[1])+int(bounds[3])/2

    return (xmid, ymid)


def distSQ(c1, c2):
    """ Returns distance squared.
    
        Params: 
            c1  :   first coordinate    (x,y)        <tuple>
            c1  :   second coordinate   (x,y)        <tuple>
    """
    return (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2


def isSameLine(firstBB, secondBB):
    try: #Google
        if (str(type(firstBB)) == 'unicode') or (str(type(secondBB))== 'unicode'):
            raise ValueError

        if firstBB.vertices[0].y>=secondBB.vertices[0].y:
            if firstBB.vertices[0].y>secondBB.vertices[2].y:
                return False
            else:
                return True
        elif firstBB.vertices[2].y<=secondBB.vertices[2].y:
            if firstBB.vertices[2].y<secondBB.vertices[0].y:
                return False
            else:
                return True

    except: #Microsoft
        firstBB=getCorners(firstBB)
        secondBB=getCorners(secondBB)

        if firstBB[0][1]>=secondBB[0][1]:
            if firstBB[0][1]>secondBB[2][1]:
                return False
            else:
                return True
        elif firstBB[2][1]<=secondBB[2][1]:
            if firstBB[2][1]<secondBB[0][1]:
                return False
            else:
                return True


def getPhraseBounds(setOfBounds):
    x_list=[]
    y_list=[]
    boundType=str(type(setOfBounds[0]))

    if (boundType == 'unicode' or boundType == 'str'):
        for eachBound in setOfBounds:
            corners=getCorners(eachBound)
            for coord in corners:
                x_list.append(coord[0])
                y_list.append(coord[1])
    else:
        for eachBound in setOfBounds:
            # print(eachBound)
            for eachVert in eachBound.vertices:
                x_list.append(eachVert.x)
                y_list.append(eachVert.y)

    x_max=max(x_list)
    x_min=min(x_list)
    y_max=max(y_list)
    y_min=min(y_list)

    t_l=(x_min, y_min)
    t_r=(x_max, y_min)
    b_l=(x_min, y_max)
    b_r=(x_max, y_max)
    
    return [t_l, t_r, b_l, b_r]


def azureFindings(azure_resp):
    """ Returns a dict with found word entries from each word_sets.
        Form:
        {
            word_0  : [ found entries ... ],
            ...............................,
            word_%n : [ found entries ... ],                         
        }

        where:  
            n                   :   number of words in doc      <int>
            entry               :   {   'text'          :   word_txt,
                                        'boundingBox'   :   word.bounding_box   }
            word.bounding_box   :   bounds          <uni>
            word_txt            :   original txt    <string>

        Params:
            document    :   a data structure directly from the Microsoft Vision API
    """
    
    findings_set={}
    
    for region in azure_resp['regions']:
    
        for line in region['lines']:

            for word in line['words']:

                if not (word['text'].lower() in findings_set):
                    findings_set[word['text'].lower()]=[word]
                else:
                    findings_set[word['text'].lower()].append(word) 
    return findings_set


def googleFindings(document):
    """ Returns a dict with found word entries and a list of all acuurrances.
        Form:
            {
            word_0  : [ found entries ... ],
            ...............................,
            word_%n : [ found entries ... ],                         
            }

        where:  
            n                   :   number of words in doc      <int>
            entry               :   {   'text'          :   word_txt,
                                        'boundingBox'   :   word.bounding_box   }
            word.bounding_box   :   bounds  <google.cloud.vision_v1.types.BoundingPoly>
            word_txt            :   original txt    <string>
                    
        Param:  
            document    : a data structure directly from the Google Cloud Vision API
    """

    findings_set={}

    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_txt=''
                    for symbol in word.symbols:
                        word_txt+=symbol.text
                    entry= {
                        'text'          :   word_txt,
                        'boundingBox'   :   word.bounding_box
                    }
                    if not (word_txt.lower() in findings_set):
                        findings_set[word_txt.lower()]=[entry]
                    else:
                        findings_set[word_txt.lower()].append(entry)
    return findings_set


def getPhraseUno(findings, words):
    """Returns a list of found combos <tuple> of the words.
    
    Param:
        findings    :   a dict containing sets of all words
    """
    combos=[]

    if not (words[0] in findings):
        return combos
    firstWords=findings[words[0]]

    for firstWord in firstWords:
        phrase = firstWord['text']
        combos.append(phrase)
    return combos


def getPhraseDuo(findings, words, radius):
    """Returns a list of found combos <tuple> of the words from each set.
    
    Param:
        findings    :   a dict containing sets of all words 
        radius      :   an int/pixel distance that descrbes closeness
        words       :   list of words in a phrase
    """
    combos=[]

    if not ((words[0] in findings) and (words[1] in findings)):
        return combos

    firstWords=findings[words[0]]
    secondWords=findings[words[1]]
    
    
    for firstWord in firstWords:
        firstWordCenter = getCenter(firstWord['boundingBox'])
        
        for secondWord in secondWords:
            secondtWordCenter = getCenter(secondWord['boundingBox'])
            
            # conditions:
            withinRadius = (distSQ(firstWordCenter, secondtWordCenter) <= radius**2)
            sameLine = isSameLine(firstWord['boundingBox'], secondWord['boundingBox'])
            
            if  withinRadius and sameLine:
                phrase = str(firstWord['text'])+ ' ' + str(secondWord['text'])
                combos.append( phrase )
    
    return combos


def getPhraseTrio(findings, words, radius):
    """Returns a list of found combos <tuple> of the words from each set.
    
    Param:
        findings    :   a dict object containing sets of all words 
        radius      :   an int/pixel distance that descrbes closeness 
        words       :   list of words in a phrase
    """
    combos=[]

    if not ((words[0] in findings) and (words[1] in findings) and (words[2] in findings)):
        return combos
    
    firstWords=findings[words[0]]
    secondWords=findings[words[1]]
    thirdWords=findings[words[2]]
    
    for firstWord in firstWords:
        firstWordCenter = getCenter(firstWord['boundingBox'])
        
        for secondWord in secondWords:
            secondWordCenter = getCenter(secondWord['boundingBox'])
            
            # conditions:
            withinRadiusOneTwo = (distSQ(firstWordCenter, secondWordCenter) <= radius**2)
            sameLineOneTwo = isSameLine(firstWord['boundingBox'], secondWord['boundingBox'])
            
            if  withinRadiusOneTwo and sameLineOneTwo:
                for thirdWord in thirdWords:
                    thirdWordCenter = getCenter(thirdWord['boundingBox'])

                    # conditions:
                    withinRadiusTwoThree = (distSQ(secondWordCenter, thirdWordCenter) <= radius**2)
                    sameLineTwoThree = isSameLine(secondWord['boundingBox'], thirdWord['boundingBox'])

                    if withinRadiusTwoThree and sameLineTwoThree:
                        phrase =    str(firstWord['text']) + ' ' + \
                                    str(secondWord['text'])+ ' ' + \
                                    str(thirdWord['text']) 
                        combos.append(phrase)
    return combos


def findPhrase(phrase, findings, Rtolorance):
    """ Returns a list of found phrase hits.

    Params:
        phrase      :   a string of phrase              <string>
        findings    :   a dictionary of found words     <dict>
        Rtolorance  :   a radius tolorance              <int>
    """
    words = phrase.strip().split(' ')
    if len(words) == 1:
        return getPhraseUno(findings, words)

    elif len(words) == 2:
        return getPhraseDuo(findings, words, Rtolorance)

    elif len(words) == 3:
        return getPhraseTrio(findings, words, Rtolorance)

    else:
        return "Can't look for more than 3 word Phrases"


def findPhrases(document, listPhrases, Rtolorance):
    """ Returns a list of found phrase hits.

    Params:
        document     :   an API Response     <GOOGLE/Microsoft>
        listPhrases  :   a list of phrases   <list>
        Rtolorance   :   a radius tolorance  <int>
    """
    if isinstance(document, collections.Iterable):
        findings=azureFindings(document)
    else:
        findings=googleFindings(document)

    result=[]

    for phrase in listPhrases:
        hits=findPhrase(phrase, findings, Rtolorance)
        result.append(hits)
    return result


def getWordCount(document):
    if isinstance(document, collections.Iterable):
        findings=azureFindings(document)
    else:
        findings=googleFindings(document)
        
    wordCount=len(findings)
    return wordCount


def getComboCount(allCombos):
    n=0
    for each in allCombos:
        for word in each:
            n+=1
    return n